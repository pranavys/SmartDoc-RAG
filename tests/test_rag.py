from app.rag.service import answer_question


query = "How many days of annual leave do employees receive?"

history = """
User: Tell me about the employee handbook.
Assistant: It contains company policies about leave, remote work and working hours.
""".strip()


answer = answer_question(
    query=query,
)

print("===== RAG ANSWER =====")
print(answer)