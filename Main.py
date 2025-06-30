import streamlit as st
from ninebit_ciq import NineBitCIQClient
import time

# CIQ client setup
client = NineBitCIQClient(
    base_url="http://localhost:8090",
    api_key="17c2e97e-d3c7-4018-bb48-e47d0cebea2f"
)

st.set_page_config(page_title="CIQ Chatbot", page_icon="🤖")
st.title("🤖 CIQ Chatbot")
# st.markdown("Ask questions about your uploaded documents.")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# Welcome message
if not st.session_state.history:
    st.chat_message("ai").markdown("👋 Hi! I’m CIQ Assistant. Ask anything about your uploaded documents.")

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.session_state.last_result = None
    st.rerun()

# Show chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f"🧑‍💻 {msg['text']}")
        else:
            st.markdown(f"🤖 {msg['text']}")

# Input box at bottom
user_input = st.chat_input("Ask a question...")

# Safe workflow polling function
def safe_wait_for_completion(wf_id, max_retries=30, delay=2):
    for attempt in range(max_retries):
        try:
            status = client.get_workflow_status(wf_id)
            content = status.get("content", {})
            wf_status = content.get("status", "")

            if wf_status == "success":
                return status
            elif wf_status in ["error", "failed"]:
                raise Exception(f"Workflow failed: {status}")

            time.sleep(delay)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay)
    raise Exception("Timeout: workflow did not complete")

# Handle user input
if user_input:
    st.session_state.history.append({"role": "user", "text": user_input})

    try:
        with st.spinner("Thinking..."):
            wf_id = client.trigger_workflow({
                "workflow": "rag-query",
                "rag_query": user_input,
                "workspace": "ciq-rag-ws",
                "euclidean_threshold": 0.9,
                "top_k": 6
            })

            result = safe_wait_for_completion(wf_id)
            final_answer = result.get("result", "⚠️ No answer found.")

            st.session_state.last_result = result  # Save for debug button
    except Exception as e:
        final_answer = f"❌ Error: {e}"
        st.session_state.last_result = None

    st.session_state.history.append({"role": "ai", "text": final_answer})
    st.rerun()