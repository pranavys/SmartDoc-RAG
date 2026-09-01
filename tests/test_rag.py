from app.rag.service import answer_question


query = "What is the company's maternity leave policy?"

history = """
User: Tell me about the employee handbook.
Assistant: It contains company policies about leave, remote work and working hours.
""".strip()


answer = answer_question(
    query=query,
    history=history,
)

print("===== RAG ANSWER =====")
print(answer)