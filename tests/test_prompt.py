from app.rag.prompts import build_prompt


query = "How many vacation days do employees get?"

context = """
Employees receive 30 days of annual leave every year.
Employees should request annual leave through the HR portal.
""".strip()

history = """
User: What does the employee handbook contain?
Assistant: It contains company policies including leave and remote work.
""".strip()


prompt = build_prompt(
    query=query,
    context=context,
    history=history,
)

print("===== FINAL PROMPT =====")
print(prompt)