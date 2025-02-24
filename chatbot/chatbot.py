import os
from config.config import OPENAI_API_KEY
from loader.save_load_db import similarity_search_qdrant_data, similarity_search_qdrant_data_with_filters, \
    load_vector_db
from prompt.prompt import prompt_test

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


def create_openai_client(api_key: str) -> ChatOpenAI:
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=api_key,  # Nếu muốn truyền trực tiếp API key
    )
    return llm


def generate_chat_completion(llm: ChatOpenAI, prompt_text: str):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_text}
            ]
        }
    ]
    print(messages)
    ai_msg = llm.invoke(messages)
    return ai_msg.content


def create_prompt(question, context, history=""):
    return prompt_test.format(question=question, context=context, history=history)


def create_query_with_context(db, query, history=""):
    docs = similarity_search_qdrant_data_with_filters(db, query, "upload")
    context = '\n'.join(
        [f"{doc.page_content} (Page: {doc.metadata.get('page', 'N/A')})" for doc in docs]
    )
    print(context)
    return create_prompt(question=query, context=context, history=history)



def load_conversation_history(file_path="conversation_history.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def save_conversation_history(history, file_path="conversation_history.txt"):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(history)


if __name__ == "__main__":
    db = load_vector_db()
    llm = create_openai_client(OPENAI_API_KEY)
    print("LLM client:", llm)

    # Load lịch sử trò chuyện nếu có
    history_file = "conversation_history.txt"
    conversation_history = load_conversation_history(history_file)

    while True:
        query = input("Nhập câu hỏi của bạn (hoặc 'quit' để thoát): ")
        if query.lower() == 'quit':
            print("Thoát chương trình.")
            break

        prompt = create_query_with_context(db, query, conversation_history)
        print(prompt)
        message = generate_chat_completion(llm, prompt)
        print(f"Bot: {message}")

        # Cập nhật lịch sử: ghi lại câu hỏi của người dùng và phản hồi của bot.
        conversation_history += f"User: {query}\nBot: {message}\n\n"
        save_conversation_history(conversation_history, history_file)
