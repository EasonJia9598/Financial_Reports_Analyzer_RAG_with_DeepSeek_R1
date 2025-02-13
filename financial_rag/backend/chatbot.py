import streamlit as st
from financial_rag.backend.vector_db import VectorDatabase
from financial_rag.models.models import LLMModel, EmbeddingModel

class Chatbot:
    def __init__(self, expert_prompt=""):
        self.expert_prompt = expert_prompt
        self.vector_db = VectorDatabase()
        self.llm = LLMModel()
        self.embed_model = EmbeddingModel()

    def get_relevant_context(self, question, num_result=10):
        """ 从向量数据库获取相关上下文 """
        query_embedding = self.embed_model.encode([question]).tolist()
        results = self.vector_db.query_documents(query_embedding, num_result)

        if not results:
            return "No relevant documents found."

        return "\n\n".join(f"[{idx+1}] {doc[:200]}..." for idx, doc in enumerate(results) if isinstance(doc, str))

    def stream_response(self, user_input, num_chunks):
        """ 实时流式响应 """
        # 获取上下文
        if num_chunks > 0:
            context_text = self.get_relevant_context(user_input, num_chunks)
        else:
            context_text = "No relevant document found."

        prompt = f"""
        You are an intelligent assistant. I am providing you with multiple chunks of text extracted from a file. 
        Treat these chunks as a single, complete document rather than separate indexed sections.

        When the user asks a question, follow these guidelines:
            • If the question is unrelated to the provided document, completely ignore its content and answer the user question directly.
            • If the question is related, analyze the document as a whole and think carefully before answering.

        Here is the document information:
        {context_text}
        
        Think the guidelines carefully. You do not need to follow the guidelines if the question is unrelated to the document.
        Or if you have better understanding of the question, you can ignore the guideline information and answer directly based on the documentation.

        {self.expert_prompt}

        The user Question is: {user_input}
        """

        print("##############################################################################################################################")

        print(prompt)

        print("##############################################################################################################################")


        
        with st.chat_message("assistant"):
            response_container = st.empty()
            generated_text = ""
            inside_think = False  # 追踪 <think> 代码块

            for token in self.llm.model.stream(prompt):
                if "<think>" in token:
                    inside_think = True
                    token = token.replace("<think>", '> <span style="color:gray;">')

                if "</think>" in token:
                    inside_think = False
                    token = token.replace("</think>", '</span>')

                if inside_think and "\n" in token:
                    token = token.replace("\n", "\n> ")

                generated_text += token

                # **优化**：每 50ms 刷新 UI，而不是等整个消息结束
                response_container.markdown(generated_text, unsafe_allow_html=True)

            st.session_state.chat_history.append({"role": "assistant", "content": generated_text})


