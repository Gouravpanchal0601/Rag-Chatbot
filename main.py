import os
import uuid
import streamlit as st
from image_processing import process_pdf

st.set_page_config(page_title="Rag ChatBot")
st.title("Rag ChatBot")

def generate_thread_id():
    return str(uuid.uuid4())

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

if st.session_state["thread_id"] not in st.session_state["chat_threads"]:
    st.session_state["chat_threads"].append(st.session_state["thread_id"])

if "messages_by_thread" not in st.session_state:
    st.session_state["messages_by_thread"] = {}

if "qa_chains" not in st.session_state:
    st.session_state["qa_chains"] = {}

if "uploaded_filename_by_thread" not in st.session_state:
    st.session_state["uploaded_filename_by_thread"] = {}

if st.session_state["thread_id"] not in st.session_state["messages_by_thread"]:
    st.session_state["messages_by_thread"][st.session_state["thread_id"]] = []

with st.sidebar:
    st.title("Hijacked")

    if st.button("New Chat"):
        new_id = generate_thread_id()
        st.session_state["thread_id"] = new_id
        if new_id not in st.session_state["chat_threads"]:
            st.session_state["chat_threads"].append(new_id)
        st.session_state["messages_by_thread"][new_id] = []
        st.session_state["qa_chains"].pop(new_id, None)
        st.session_state["uploaded_filename_by_thread"].pop(new_id, None)

    st.header("My Conversations")
    for t_id in st.session_state["chat_threads"][::-1]:
        fname = st.session_state["uploaded_filename_by_thread"].get(t_id)
        label = f"{t_id[:8]}{'...' if len(t_id)>8 else ''} — {fname if fname else 'No PDF'}"
        if st.button(label, key=f"btn_{t_id}"):
            st.session_state["thread_id"] = t_id
            if t_id not in st.session_state["messages_by_thread"]:
                st.session_state["messages_by_thread"][t_id] = []

thread_id = st.session_state["thread_id"]
uploader_key = f"uploader_{thread_id}"
uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf", key=uploader_key)

if uploaded_pdf is not None:
    prev_filename = st.session_state["uploaded_filename_by_thread"].get(thread_id)
    if prev_filename != uploaded_pdf.name or thread_id not in st.session_state["qa_chains"]:
        with st.spinner("Processing PDF..."):
            temp_path = f"temp_uploaded_{thread_id}.pdf"
            with open(temp_path, "wb") as f:
                f.write(uploaded_pdf.read())
            st.session_state["qa_chains"][thread_id] = process_pdf(temp_path)
            st.session_state["uploaded_filename_by_thread"][thread_id] = uploaded_pdf.name
        st.success("✅ PDF processed! Ask a question below.")
else:
    if thread_id not in st.session_state["qa_chains"]:
        st.info("⬆️ Please upload a PDF to begin chatting for this thread.")

messages = st.session_state["messages_by_thread"].get(thread_id, [])
for role, text in messages:
    st.chat_message(role).markdown(text)

qa_chain = st.session_state["qa_chains"].get(thread_id)

qa_chains = st.session_state['qa_chains'].get(thread_id)
if qa_chain is None:
    st.warning("Upload and process a PDF for this conversation to ask questions.")
else:
    if prompt := st.chat_input("Ask something about the PDF..."):
        st.chat_message("user").markdown(prompt)
        st.session_state["messages_by_thread"][thread_id].append(("user", prompt))

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = qa_chain({"question": prompt})
                    answer = response.get("answer") if isinstance(response, dict) else response
                    if answer is None:
                        answer = "Sorry — no answer returned by the QA chain."
                except Exception as e:
                    answer = f"Error during QA chain execution: {e}"

                st.markdown(answer)
                st.session_state["messages_by_thread"][thread_id].append(("assistant", answer))
