from app.rag.retriever import retrieve_and_rerank


query = "How many vacation days do employees get?"

results = retrieve_and_rerank(
    query=query,
    retrieval_limit=5,
    rerank_limit=3,
)

print("===== RERANKED RESULTS =====")

for index, (chunk, score) in enumerate(results):
    print(f"\n--- Result {index + 1} ---")
    print(f"Score: {score:.4f}")
    print(chunk.content)