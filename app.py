import streamlit as st
import chromadb
import ollama

st.title("DocScanSpeak")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="ledger")

question = st.text_input("Ask about your ledger:")

if question:
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