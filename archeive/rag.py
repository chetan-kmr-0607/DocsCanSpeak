import chromadb
import ollama

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="ledger")

question = input("Ask about your ledger: ")

results = collection.query(
    query_texts=[question],
    n_results=3
)

retrieved_chunks = results["documents"][0]
context = "\n\n".join(retrieved_chunks)

prompt = f"""Answer the question using only the context below.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}"""

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": prompt}],
)

print("\nAnswer:", response["message"]["content"])