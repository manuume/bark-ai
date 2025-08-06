# 🐾 BARK AI - The Veterinary Diagnostic Co-Pilot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

An advanced RAG-based conversational AI assistant designed to support veterinary professionals by providing evidence-based insights for canine diagnostics from a curated knowledge base.

---
<img width="2816" height="1536" alt="Image" src="https://github.com/user-attachments/assets/66e8db43-b1fc-4e64-9616-7b3bc54b3148" />


## 🚀 Live Demo

You can access and interact with the live application here:

**[[bark_ai webapp]]([https://bark-ai.streamlit.app/])**

---

## ✨ Key Features

* **Conversational Memory:** Engages in natural, context-aware dialogue, allowing for follow-up questions.
* **Rich Knowledge Base:** Built from professional veterinary literature (Merck Manual, etc.) covering clinical pathology, infectious diseases, endocrinology, toxicology, and more.
* **Advanced RAG Pipeline:** Utilizes a state-of-the-art retrieval and generation pipeline with LangChain, FAISS, and a powerful LLM to provide accurate, context-aware answers.
* **Structured Analysis:** Delivers responses in a professional, multi-section format, including Clinical Considerations, Differentials, Knowledge Gaps, and Red Flags.
* **Safety First:** Engineered with strict guardrails to act as a supportive co-pilot, not a replacement for professional veterinary judgment.

---

## 🛠️ Technology Stack

* **Backend:** Python
* **Frontend:** Streamlit
* **AI Framework:** LangChain
* **Vector Database:** FAISS (Facebook AI Similarity Search)
* **Embedding Model:** `all-MiniLM-L6-v2` (from Hugging Face)
* **LLM Provider:** Groq (using Llama 3)
* **Deployment:** Streamlit Community Cloud

---

## 📂 Project Structure

The project is organized into a clean, modular structure:

```
BARKAI/
├── data/
│   ├── raw_data/         # Source .txt documents
│   └── vector_store/     # Generated FAISS index
├── src/
│   ├── app.py            # The Streamlit frontend application
│   ├── config.py         # Central configuration
│   ├── data_processor.py # Script to build the vector store
│   └── rag_engine.py     # The core RAG backend logic
├── .env.example          # Example secrets file
├── .gitignore
└── requirements.txt
```

---

## ⚙️ Setup and Local Installation

To run this project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/BARK-AI.git
   cd BARK-AI
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API Keys:**
   * Create a file named `.env` in the root directory.
   * Add your Groq API key to it: `GROQ_API_KEY="gsk_..."`

5. **Build the knowledge base:**
   * Run the data processor script once to create the vector store from the files in `data/raw_data/`.
   ```bash
   python src/data_processor.py
   ```

6. **Launch the application:**
   ```bash
   streamlit run src/app.py
   ```

---

## 🔮 Future Improvements

* Expand the knowledge base with more specialized case studies.
* Implement a user feedback mechanism (thumbs up/down) to evaluate responses.
* Integrate a multi-modal model to analyze images of blood smears or other diagnostics.

---

## 📝 License

This project is licensed under the MIT License.


---

**⚠️ Disclaimer:** BARK AI is designed as a supportive tool for veterinary professionals and should not replace professional veterinary judgment or consultation with qualified veterinarians.
