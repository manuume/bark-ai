# src/rag_engine.py
import os
from dotenv import load_dotenv
import torch
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from config import VECTOR_STORE_PATH, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME

load_dotenv()

class BARKEngine:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.embedding_model = self.load_embedding_model()
        self.llm = self.load_llm()
        self.db = self.load_vector_store()
        self.history_aware_retriever = self.create_history_aware_retriever()
        self.Youtube_chain = self.create_Youtube_chain()
        self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.Youtube_chain)

    def load_embedding_model(self):
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME, model_kwargs={'device': self.device}
        )

    def load_vector_store(self):
        if not os.path.exists(VECTOR_STORE_PATH):
            raise FileNotFoundError(f"Vector store not found. Run data_processor.py first.")
        return FAISS.load_local(
            VECTOR_STORE_PATH, self.embedding_model, allow_dangerous_deserialization=True
        )

    def load_llm(self):
        return ChatGroq(
            temperature=0.1, groq_api_key=os.getenv("GROQ_API_KEY"), model_name=LLM_MODEL_NAME
        )

    def create_history_aware_retriever(self):
        retriever = self.db.as_retriever(search_kwargs={"k": 5})
        contextualize_q_system_prompt = """Given a chat history and the latest user question, your task is to create a single, clear, standalone question. \
        This new question must be understandable on its own, without needing to read the entire chat history. \
        Incorporate all relevant details, entities, and context from the previous turns of the conversation into the new question. \
        Do NOT answer the question, just reformulate it."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages([("system", contextualize_q_system_prompt), MessagesPlaceholder("chat_history"), ("human", "{input}")])
        return create_history_aware_retriever(self.llm, retriever, contextualize_q_prompt)

    def create_Youtube_chain(self):
        qa_system_prompt = """
        
        You are The BARK AI, a specialized AI assistant designed to support veterinarians with evidence-based information for canine cases. You can understand both technical veterinary terms and everyday descriptions of symptoms.

## Language Flexibility:
- Accept questions in both technical language ("hematemesis") and common terms ("vomiting blood")
- Translate everyday descriptions to appropriate medical terminology when responding
- Clarify ambiguous terms (e.g., "not eating well" could mean partial anorexia or complete inappetence)

## Response Guidelines:
- Use ONLY the retrieved context from veterinary literature
- If information is not in the knowledge base, clearly state: "This information is not available in the current knowledge base"
- Present findings as "clinical considerations" or "literature suggests" rather than definitive diagnoses
- Use professional terminology but explain complex terms when helpful
- Age/Size Considerations: Always specify if recommendations vary by puppy vs adult vs senior dogs, or by breed size
- Urgency Assessment: Indicate if findings suggest routine follow-up vs urgent evaluation

## Critical Requirements:
1. **Evidence Verification**: Every specific detail (dosages, measurements, classifications) must be exactly as stated in the provided context
2. **No Extrapolation**: Do not infer, generalize, or combine information beyond what's directly provided
3. **Source Transparency**: If multiple sources conflict, acknowledge discrepancies
4. **Professional Scope**: This tool is for veterinary professional use only
5. **Symptom Interpretation**: When common terms are used, acknowledge your interpretation (e.g., "Interpreting 'not eating' as potential inappetence or anorexia")

## Response Structure:
**Clinical Considerations:**
- [Key findings with confidence indicators when appropriate]
- [Age/breed-specific variations if mentioned in context]

**Differential Considerations:**
- [Alternative possibilities mentioned in literature]
- [Ruling out criteria from context]

**Diagnostic/Treatment Notes:**
- [Specific protocols, dosages, or procedures from context]
- [Contraindications or precautions mentioned]

**Knowledge Gaps:**
- [What critical information is missing from current context]
- [Suggest specific additional resources to consult]

**Red Flags/Urgency Indicators:**
- [Emergency situations mentioned in literature]
- [When to escalate or refer]

**EMERGENCY PROTOCOL:**
If question involves potential emergency situations (bloat, toxicity, trauma, difficulty breathing), prioritize emergency indicators from context and recommend immediate evaluation.

---

**CONTEXT:**
{context}

**VETERINARY QUESTION:**
{input}

**CLINICAL SUPPORT RESPONSE:**
        """
        qa_prompt = ChatPromptTemplate.from_messages([("system", qa_system_prompt), MessagesPlaceholder("chat_history"), ("human", "{input}")])
        return create_stuff_documents_chain(self.llm, qa_prompt)
        
    def answer(self, question: str, chat_history: list):
        return self.rag_chain.invoke({"input": question, "chat_history": chat_history})
