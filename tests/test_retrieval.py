from app.rag.retriever import retrieve_chunks


query = "Can employees work remotely?"

chunks = retrieve_chunks(query, limit=3)

print("===== RETRIEVAL RESULT =====")
print(f"Number of chunks retrieved: {len(chunks)}")

for index, chunk in enumerate(chunks):
    print(f"\n--- Result {index + 1} ---")
    print(chunk.content)