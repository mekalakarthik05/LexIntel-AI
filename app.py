import os
import sys
import time
import subprocess
import requests
import streamlit as st
from datetime import datetime


API_URL = "http://127.0.0.1:8001"


@st.cache_resource
def start_backend():
    """Start the existing FastAPI backend once for the Streamlit app."""

    try:
        secrets = dict(st.secrets)
    except Exception:
        secrets = {}

    for key in [
        "GROQ_API_KEY",
        "PINECONE_API_KEY",
        "PINECONE_INDEX_NAME",
        "PINECONE_CLOUD",
        "PINECONE_REGION",
    ]:
        if key in secrets:
            os.environ[key] = str(secrets[key])

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "src.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8001",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for _ in range(30):
        try:
            response = requests.get(f"{API_URL}/", timeout=1)
            if response.status_code < 500:
                return process
        except requests.RequestException:
            pass
        time.sleep(1)

    return process


def get_or_create_session_id():
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    return st.session_state.session_id


def set_session_id(session_id):
    st.session_state.session_id = session_id


def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_message(role, content):
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "time": datetime.now().strftime("%H:%M"),
        }
    )


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            st.caption(message["time"])


def reset_conversation():
    if st.session_state.session_id:
        try:
            response = requests.post(
                f"{API_URL}/session/reset/{st.session_state.session_id}"
            )

            if response.status_code == 200:
                st.session_state.messages = []
                st.success("Conversation reset successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(
                    f"Failed to reset conversation: "
                    f"{response.json().get('detail', 'Unknown error')}"
                )
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.session_state.messages = []
        st.rerun()


def get_document_sources():
    if st.session_state.session_id:
        try:
            response = requests.get(
                f"{API_URL}/sources/{st.session_state.session_id}"
            )

            if response.status_code == 200:
                return response.json().get("document_references", [])

            st.error(
                f"Failed to get sources: "
                f"{response.json().get('detail', 'Unknown error')}"
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")

    return []


def main():
    st.set_page_config(
        page_title="Legal Document Assistant",
        page_icon="⚖️",
        layout="wide",
    )

    start_backend()

    initialize_chat_history()
    session_id = get_or_create_session_id()

    st.title("⚖️ Legal Document Assistant")
    st.markdown(
        "Ask questions about your legal documents and get accurate answers "
        "based on the document content."
    )

    with st.sidebar:
        st.header("Session Information")

        if session_id:
            st.success(f"Active Session: {session_id[:8]}...")
        else:
            st.info("No active session. Start chatting to create one.")

        if st.button("Reset Conversation"):
            reset_conversation()

        st.divider()

        st.header("Document Upload")

        uploaded_file = st.file_uploader(
            "Choose a PDF or TXT file",
            type=["pdf", "txt"],
        )

        if uploaded_file is not None:
            st.caption(f"Selected file: {uploaded_file.name}")

            if st.button("Upload / Process Document"):
                try:
                    with st.spinner("Processing document..."):
                        response = requests.post(
                            f"{API_URL}/upload",
                            files={
                                "file": (
                                    uploaded_file.name,
                                    uploaded_file.getvalue(),
                                    uploaded_file.type
                                    or "application/octet-stream",
                                )
                            },
                            timeout=300,
                        )

                    if response.status_code == 200:
                        payload = response.json()

                        st.success(
                            payload.get(
                                "message",
                                "Document processed successfully.",
                            )
                        )

                        st.write(f"Filename: {payload.get('filename')}")
                        st.write(f"Status: {payload.get('status')}")
                        st.write(f"Chunks processed: {payload.get('chunks')}")
                        st.write(f"Indexed: {payload.get('indexed')}")
                    else:
                        detail = response.json().get(
                            "detail",
                            "Upload failed.",
                        )
                        st.error(detail)

                except Exception as exc:
                    st.error(f"Error: {str(exc)}")

        st.divider()

        st.header("Document References")

        doc_refs = get_document_sources()

        if doc_refs:
            for ref in doc_refs:
                st.markdown(f"- {ref}")
        else:
            st.info("No document sections referenced yet.")

        st.divider()
        st.caption("© 2025 Legal Document Assistant")

    col1, col2 = st.columns([4, 1])

    with col1:
        display_chat_history()

        if prompt := st.chat_input("Ask about your legal documents..."):
            add_message("user", prompt)

            try:
                with st.spinner("Thinking..."):
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={
                            "text": prompt,
                            "session_id": session_id,
                        },
                        timeout=300,
                    )

                if response.status_code == 200:
                    response_data = response.json()

                    if not session_id:
                        set_session_id(response_data["session_id"])

                    add_message(
                        "assistant",
                        response_data["response"],
                    )
                else:
                    error_message = (
                        f"Error: "
                        f"{response.json().get('detail', 'Unknown error')}"
                    )
                    add_message("assistant", error_message)
                    st.error(error_message)

            except Exception as e:
                error_message = f"Error: {str(e)}"
                add_message("assistant", error_message)
                st.error(error_message)

            st.rerun()

    with col2:
        st.subheader("Legal Terms")

        legal_terms = [
            "Plaintiff",
            "Defendant",
            "Liability",
            "Jurisdiction",
            "Deposition",
        ]

        for term in legal_terms:
            with st.expander(term):
                st.write(
                    f"This is where a definition for {term} would appear."
                )


if __name__ == "__main__":
    main()