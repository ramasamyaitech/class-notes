import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/api"


st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖"
)


st.title("🤖 Enterprise RAG Chatbot")


st.header("Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


if uploaded_file:

    if st.button("Ingest Document"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            f"{API_URL}/ingest",
            files=files
        )

        if response.status_code == 200:

            st.success(
                "Document ingested successfully!"
            )

        else:

            st.error(response.text)


st.header("Ask Question")

question = st.text_input(
    "Enter your question"
)


if st.button("Ask"):

    if not question:

        st.warning("Please enter a question.")

    else:

        response = requests.post(
            f"{API_URL}/chat",
            json={
                "question": question
            }
        )

        if response.status_code == 200:

            result = response.json()

            st.subheader("Answer")

            st.write(
                result["answer"]
            )

            st.subheader("Sources")

            for source in result["sources"]:

                st.write(source)

        else:

            st.error(response.text)