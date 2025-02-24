import streamlit as st




# Khởi tạo trạng thái phiên cho tin nhắn và lịch sử nhập liệu
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []


# from main import response
# def api_chatbot(query):
#     history_msg = ""
#     for message in st.session_state.messages:
#         role = "User" if message["role"] == "user" else "Bot"
#         history_msg += f"{role}: {message['content']}\n"
#     return response(query, history_msg)



from prompt.dspy_prompt import get_rseponse_with_dspy
def api_chatbot_dspy(query):
    history_msg = ""
    for message in st.session_state.messages:
        role = "User" if message["role"] == "user" else "Bot"
        history_msg += f"{role}: {message['content']}\n"
    return get_rseponse_with_dspy(query, history_msg)


def main():
    st.set_page_config(
        page_title="Chatbot",
        page_icon="🤖",
        layout="centered",
    )

    # Hiển thị các tin nhắn trước đó từ lịch sử trò chuyện
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    # Nhận đầu vào của người dùng
    user_input = st.chat_input("What is your question?")

    if user_input:
        # Hiển thị tin nhắn của người dùng
        with st.chat_message("user"):
            st.markdown(user_input)

        # Thêm tin nhắn của người dùng vào trạng thái phiên
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Lấy phản hồi và gợi ý từ bot
        answer, suggestions = api_chatbot_dspy(user_input)  # api_chatbot_dspy(user_input)

        # Hiển thị phản hồi của bot
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Thêm phản hồi của bot vào trạng thái phiên
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Cập nhật gợi ý trong trạng thái phiên (để hiển thị dưới dạng nút)
        st.session_state.suggestions = suggestions

        # Xóa trường nhập liệu của người dùng sau khi gửi tin nhắn
        st.session_state.user_input = ""

    # Tạo các vị trí trống cho các nút gợi ý
    suggestion_placeholders = [st.empty() for _ in range(3)]

    # Hiển thị các nút gợi ý mới nếu có
    if st.session_state.suggestions:
        for i, suggestion in enumerate(st.session_state.suggestions):
            with suggestion_placeholders[i]:
                if st.button(suggestion, key=f"button_{suggestion}"):
                    # Xử lý khi người dùng nhấn vào một gợi ý
                    with st.chat_message("user"):
                        st.markdown(suggestion)

                    # Thêm gợi ý như một tin nhắn của người dùng vào trạng thái phiên
                    st.session_state.messages.append({"role": "user", "content": suggestion})

                    # Lấy phản hồi và gợi ý mới từ bot
                    answer, suggestions = api_chatbot_dspy(suggestion)  # api_chatbot_dspy(suggestion)

                    # Hiển thị phản hồi của bot
                    with st.chat_message("assistant"):
                        st.markdown(answer)

                    # Thêm phản hồi của bot vào trạng thái phiên
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    # Cập nhật gợi ý mới trong trạng thái phiên
                    st.session_state.suggestions = suggestions

                    # Xóa trường nhập liệu của người dùng sau khi gửi tin nhắn
                    st.session_state.user_input = ""

                    # Reload
                    st.rerun()  # Sử dụng st.experimental_rerun() để làm mới ứng dụng


if __name__ == "__main__":
    main()
