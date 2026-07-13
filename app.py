import streamlit as st
from retriever import get_top_chunks
from llm_client import answer_query

st.set_page_config(
    page_title="Local RAG AI Assistant", 
    page_icon=":books:",
    layout="centered"
    )

st.title("Local RAG AI Assistant")
st.caption("Ask questions about your local documents and get answers!")

# Chat history management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


#chat history
if prompt := st.chat_input("Type your question..."):
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Reply from the assistant
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chunks = get_top_chunks(prompt, top_k=3)
            answer = answer_query(prompt, chunks)
            
            st.markdown(answer)
            
            # Show sources in an expander
            with st.expander("📄 Sources"):
                for score, source, content in chunks:
                    st.markdown(f"**{source}** — Similarity: `{score:.2f}`")
                    st.caption(content[:200] + "...")

    st.session_state.messages.append({"role": "assistant", "content": answer})