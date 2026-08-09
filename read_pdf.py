from pypdf import PdfReader

reader = PdfReader("Docs/ledger.pdf")

# print(f"Number of pages: {len(reader.pages)}")

full_text = ""

for page in reader.pages:
    full_text += page.extract_text()


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


chunks = chunk_text(full_text)
# print(f"Number of chunks: {len(chunks)}")
# print("--- First chunk ---")
# print(chunks[0])
# print("--- Second chunk ---")
# print(chunks[1])


import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.create_collection(name="ledger")

ids = [f"chunk_{i}" for i in range(len(chunks))]

collection.add(
    documents=chunks,
    ids=ids
)



results = collection.query(
    query_texts=["How much money was added using UPI?"],
    n_results=3
)

print("--- Top matching chunks ---")
for doc in results["documents"][0]:
    print(doc)
    print("---")