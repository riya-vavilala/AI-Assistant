from fastapi import FastAPI
from pydantic import BaseModel

from backend.rag import ask_question


app = FastAPI(
    title="College AI Assistant",
    description="RAG-based AI assistant for college documents",
    version="1.0"
)


class Question(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "College AI Assistant API is running"
    }


@app.post("/ask")
def ask(data: Question):

    answer = ask_question(data.question)

    return {
        "question": data.question,
        "answer": answer
    }