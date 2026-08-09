import streamlit as st
import chromadb
import ollama
from pypdf import PdfReader
import tempfile
import hashlib

st.title("DocScanSpeak")
st.write("Upload a PDF and ask questions about it.")

uploaded_file = st.file_uploader("Choose a PDF", type="pdf")


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


if uploaded_file:
    # Unique collection name per file, so different uploads don't mix
    file_bytes = uploaded_file.getvalue()
    file_hash = hashlib.md5(file_bytes).hexdigest()[:10]
    collection_name = f"doc_{file_hash}"

    client = chromadb.PersistentClient(path="./chroma_db")

    # Only ingest if this exact file hasn't been processed before
    existing_collections = [c.name for c in client.list_collections()]

    if collection_name not in existing_collections:
        with st.spinner("Reading and indexing document..."):
            # Streamlit gives us an in-memory file; pypdf needs a real path,
            # so we write it to a temporary file first
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            reader = PdfReader(tmp_path)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()

            chunks = chunk_text(full_text)
            ids = [f"chunk_{i}" for i in range(len(chunks))]

            collection = client.create_collection(name=collection_name)
            collection.add(documents=chunks, ids=ids)
        st.success(f"Indexed {len(chunks)} chunks from {uploaded_file.name}")
    else:
        collection = client.get_collection(name=collection_name)
        st.info(f"Using previously indexed version of {uploaded_file.name}")

    question = st.text_input("Ask a question about this document:")

    if question:
        results = collection.query(query_texts=[question], n_results=3)
        retrieved_chunks = results["documents"][0]
        context = "\n\n".join(retrieved_chunks)

        prompt = f"""Answer the question using only the context below.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}"""

        with st.spinner("Thinking..."):
            response = ollama.chat(
                model="llama3.2",
                messages=[{"role": "user", "content": prompt}],
            )

        st.write(response["message"]["content"])

        with st.expander("Show sources"):
            for i, chunk in enumerate(retrieved_chunks):
                st.write(f"**Source {i+1}:**")
                st.write(chunk)
                st.write("---")