import json
import os

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from config.config import OPENAI_API_KEY, QDRANT_SERVER, collection_name

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# text-embedding-ada-002: Tạo ra các vector embedding với 1536 chiều.
# text-embedding-3-large: Tạo ra các vector với 3072 chiều.



def save_vector_db(docs:list[Document]):
    # Initialize QdrantVectorStore with embeddings and store the documents
    QdrantVectorStore.from_documents(
        docs,
        embeddings,
        url=QDRANT_SERVER,
        prefer_grpc=True,
        collection_name=collection_name,
    )
    print("Đã lưu vector store")

if __name__ == "__main__":

    # Đường dẫn tới tệp JSON chứa các chunks đã lưu
    input_json_path = "../data/output/chunks_data.json"
    print("OKEEE")
    # Đọc dữ liệu từ tệp JSON
    docs = []
    with open(input_json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for item in data:
            # item sẽ là 1 dictionary kiểu: {"page_content": "...", "metadata": {...}}
            page_content = item["page_content"]
            # hoặc item.get("page_content", "") nếu muốn an toàn
            metadata = item["metadata"]
            # hoặc item.get("metadata", {})
            docs.append(Document(page_content=page_content, metadata=metadata))
    print(docs)
    # Lưu các documents đã đọc vào Qdrant
    save_vector_db(docs)







