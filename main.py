import os
import streamlit as st
from config.config import OPENAI_API_KEY
from loader.save_load_db import load_vector_db, similarity_search_qdrant_data, get_context_db
from prompt.prompt import prompt_1, prompt_2

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from langchain_openai import ChatOpenAI, OpenAIEmbeddings


# Initialize OpenAI client
def create_openai_client(api_key: str) -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=api_key,
    )


db = load_vector_db()
llm = create_openai_client(OPENAI_API_KEY)


# Generate chat completion
def generate_chat_completion(llm: ChatOpenAI, prompt_text: str):
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]
    ai_msg = llm.invoke(messages)
    return ai_msg.content


# Generate prompt for answering the user's query with context
def create_prompt_1(question, context, history=""):
    return prompt_1.format(question=question, context=context, history=history)


# Generate prompt for related questions based on the bot's response
def create_prompt_2(context, history=""):
    return prompt_2.format(context=context, history=history)


# Get context for the user's query from the database
# def get_context(db, query):
#     docs = similarity_search_qdrant_data(db, query)
#     context = "\n".join([
#         f"{doc.page_content} (Title : {doc.metadata.get('title')}) -  (Page: {int(doc.metadata.get('page', '-2')) + 1})"
#         for doc in docs])
#     return context



def response(user_query, history_msg: str):
    context = get_context_db(db, user_query)
    prompt = create_prompt_1(user_query, context, history_msg)
    answer = generate_chat_completion(llm, prompt)
    history_msg += f"Bot: {answer}"
    related_prompt = create_prompt_2(context, history_msg)
    related_questions = generate_chat_completion(llm, related_prompt)
    suggestions = related_questions.split("\n")
    return answer, suggestions

# import os
# import streamlit as st
# from config.config import OPENAI_API_KEY
# from loader.save_load_db import load_vector_db, similarity_search_qdrant_data
# from prompt.prompt import prompt_1, prompt_2
#
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
#
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
#
# # Initialize OpenAI client
# def create_openai_client(api_key: str) -> ChatOpenAI:
#     return ChatOpenAI(
#         model="gpt-4o",
#         temperature=0,
#         max_tokens=None,
#         timeout=None,
#         max_retries=2,
#         api_key=api_key,
#     )
#
# # Generate chat completion
# def generate_chat_completion(llm: ChatOpenAI, prompt_text: str):
#     messages = [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]
#     ai_msg = llm.invoke(messages)
#     return ai_msg.content
#
# # Generate prompt for answering the user's query with context
# def create_prompt_1(question, context, history=""):
#     return prompt_1.format(question=question, context=context, history=history)
#
# # Generate prompt for related questions based on the bot's response
# def create_prompt_2(context, history=""):
#     return prompt_2.format(context=context, history=history)
#
# # Get context for the user's query from the database
# def get_context(db, query, history=""):
#     docs = similarity_search_qdrant_data(db, query)
#     context = "\n".join([f"{doc.page_content} (Title : {doc.metadata.get('title')}) -  (Page: {int(doc.metadata.get('page', '-2')) + 1})" for doc in docs])
#     return context
#
# # Function to process user input and handle related question suggestions
# def handle_query_and_suggestions():
#     # Nếu chưa có session state, khởi tạo
#     if "user_input" not in st.session_state:
#         st.session_state["user_input"] = ""
#
#     # Hộp nhập câu hỏi từ người dùng (có thể đã được cập nhật từ gợi ý)
#     user_query = st.text_input("Nhập câu hỏi của bạn:", value=st.session_state["user_input"], key="user_input")
#
#     if st.button("Gửi"):  # Người dùng phải nhấn gửi
#         if user_query:
#             # Hiển thị câu hỏi hiện tại
#             st.text_area("Câu hỏi đang xử lý", user_query, height=68, key="current_question_display", disabled=True)
#
#             # Cập nhật lịch sử hội thoại
#             st.session_state["conversation_history"] += f"User: {user_query}\n"
#
#             # Xử lý câu hỏi
#             context = get_context(db, user_query)
#             prompt = create_prompt_1(user_query, context, st.session_state["conversation_history"])
#             response = generate_chat_completion(llm, prompt)
#             st.write("**Bot:**", response)
#
#             # Cập nhật lịch sử hội thoại với câu trả lời
#             st.session_state["conversation_history"] += f"Bot: {response}\n"
#
#             # Sinh gợi ý câu hỏi liên quan
#             related_prompt = create_prompt_2(context, st.session_state["conversation_history"])
#             related_questions = generate_chat_completion(llm, related_prompt)
#
#             # Hiển thị các câu hỏi liên quan dưới dạng nút
#             st.write("**Gợi ý câu hỏi tiếp theo:**")
#             questions = related_questions.split("\n")
#
#             for question in questions[:3]:  # 3 câu hỏi gợi ý
#                 st.text(question.strip())
#
#         else:
#             st.warning("Vui lòng nhập câu hỏi của bạn!")
#
# # Initialize session state if not already initialized
# if "db" not in st.session_state:
#     st.session_state["db"] = load_vector_db()
#
# if "llm" not in st.session_state:
#     st.session_state["llm"] = create_openai_client(OPENAI_API_KEY)
#
# if "conversation_history" not in st.session_state:
#     st.session_state["conversation_history"] = ""
#
# db = st.session_state["db"]
# llm = st.session_state["llm"]
#
# # Layout configuration - single full-page layout
# st.set_page_config(page_title="Chatbot", layout="wide")
#
# st.header("💬 Chat với Bot")
# st.markdown("Nhập câu hỏi của bạn để trò chuyện với Bot.")
#
# # Hiển thị lịch sử hội thoại
# st.markdown("### Lịch sử hội thoại:")
# st.text_area("Lịch sử", st.session_state["conversation_history"], height=300, key="history_display", disabled=True)
#
# # Xử lý câu hỏi và gợi ý
# handle_query_and_suggestions()
