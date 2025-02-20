import os
import streamlit as st
from financial_rag.backend.document_processor import DocumentProcessor
from financial_rag.backend.chatbot import Chatbot
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get the value of EXPERT_PROMPT_FOLDER from .env (with a fallback default)
    EXPERT_PROMPT_FOLDER = os.getenv("EXPERT_PROMPT_PATH", "financial_rag/Expert_Prompt222")

    print("EXPERT_PROMPT_FOLDER: ", EXPERT_PROMPT_FOLDER)
    
    st.title("💬 RAG-Powered DeepSeek R1 Chatbot with Financial Expert")
    
    # Initialize components
    processor = DocumentProcessor()

    # Sidebar: Select expert model

    with st.sidebar:
        st.subheader("🔍 Choose Expert Agent")

        # Get the list of Prompt files (remove .txt extension)
        prompt_files = [f[:-4] for f in os.listdir(EXPERT_PROMPT_FOLDER) if f.endswith(".txt")]

        # Allow user to select a Prompt (without displaying .txt)
        selected_prompt_name = st.selectbox("Choose Agent Type", prompt_files)

        # **Restore the full file name**
        selected_prompt = f"{selected_prompt_name}.txt"

        # Read the content of the Prompt file
        def load_expert_prompt(filename):
            file_path = os.path.join(EXPERT_PROMPT_FOLDER, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    return file.read().strip()
            except FileNotFoundError:
                return "Could not load the selected prompt."

        # Load the selected Prompt
        expert_prompt = load_expert_prompt(selected_prompt)

        # Display Prompt preview in the sidebar
        # st.text_area("Prompt Preview", expert_prompt, height=150)

    # **Initialize the Chatbot and pass the expert Prompt**
    chatbot = Chatbot(expert_prompt=expert_prompt)

    # Initialize session history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar file upload
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload PDF for knowledge base update", type=["pdf"])

    # Process the uploaded PDF
    if uploaded_file:
        with st.spinner("Processing PDF..."):
            report, num_chunks = processor.process_pdf(uploaded_file)
            st.write(report)
    else:
        num_chunks = 0

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"], unsafe_allow_html=True)

    # User input
    user_input = st.chat_input("Enter your question...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # **Optimization**: Prevent UI blocking
        with st.spinner("Thinking..."):
            chatbot.stream_response(user_input, num_chunks)

if __name__ == "__main__":
    main()