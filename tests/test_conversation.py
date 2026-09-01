from app.rag.service import answer_question


conversation_id, answer = answer_question(
    query="How many vacation days do employees get?"
)

print("===== FIRST QUESTION =====")
print(f"Conversation ID: {conversation_id}")
print(f"Answer: {answer}")


conversation_id, answer = answer_question(
    query="Can employees work remotely?",
    conversation_id=conversation_id,
)

print("\n===== SECOND QUESTION =====")
print(f"Conversation ID: {conversation_id}")
print(f"Answer: {answer}")