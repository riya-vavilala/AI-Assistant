from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

CHROMA_DIR = "chroma_db"


# -----------------------------
# 1. Load embedding model
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# 2. Load ChromaDB
# -----------------------------

vector_store = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)


# -----------------------------
# 3. Load Groq LLM
# -----------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# -----------------------------
# 4. Ask question
# -----------------------------

def ask_question(question):

    results = vector_store.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        result.page_content
        for result in results
    )

    prompt = f"""
You are a College AI Assistant.

Answer the user's question using ONLY
the information provided in the context.

If the answer cannot be found in the
provided context, say:

"I don't know based on the provided documents."

Do not invent information.

Context: 
{context}

Question:
{question}


Answer:
"""
    response = llm.invoke(prompt)

    return response.content
