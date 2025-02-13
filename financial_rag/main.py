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
    
    # 初始化组件
    processor = DocumentProcessor()

    # 侧边栏：选择专家模型
    with st.sidebar:
        st.subheader("🔍 Choose Expert Agent")
        
        # 获取 Prompt 文件列表（去掉 .txt 扩展名）
        prompt_files = [f[:-4] for f in os.listdir(EXPERT_PROMPT_FOLDER) if f.endswith(".txt")]

        # 让用户选择 Prompt（不显示 .txt）
        selected_prompt_name = st.selectbox("Choose Agent Type", prompt_files)

        # **还原完整的文件名**
        selected_prompt = f"{selected_prompt_name}.txt"


        # 读取 Prompt 文件内容
        def load_expert_prompt(filename):
            file_path = os.path.join(EXPERT_PROMPT_FOLDER, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    return file.read().strip()
            except FileNotFoundError:
                return "Count not load the selected prompt."

        # 加载选定的 Prompt
        expert_prompt = load_expert_prompt(selected_prompt)

        # 在侧边栏显示 Prompt 预览
        # st.text_area("Prompt 预览", expert_prompt, height=150)

    # **初始化 Chatbot 并传递专家 Prompt**
    chatbot = Chatbot(expert_prompt=expert_prompt)

    # 初始化 session 历史记录
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 侧边栏文件上传
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload PDF for knowledge base update", type=["pdf"])

    # 处理上传的 PDF
    if uploaded_file:
        with st.spinner("Processing PDF..."):
            report, num_chunks = processor.process_pdf(uploaded_file)
            st.write(report)
    else:
        num_chunks = 0

    # 显示聊天记录
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"], unsafe_allow_html=True)

    # 用户输入
    user_input = st.chat_input("Enter your question...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # **优化**：避免 UI 阻塞
        with st.spinner("Thinking..."):
            chatbot.stream_response(user_input, num_chunks)

if __name__ == "__main__":
    main()