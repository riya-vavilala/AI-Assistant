from backend.rag import ask_question


question = input("Ask a question: ")

answer = ask_question(question)

print("\nAI Assistant:")
print(answer)