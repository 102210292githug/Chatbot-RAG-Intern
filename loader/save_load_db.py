import os
from config.config import OPENAI_API_KEY, QDRANT_SERVER, QDRANT_API_KEY, _k, collection_name, embeddings
from qdrant_client import models

from loader.load_document import load_document
from loader.process_foler import process_pdf_folder

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
from langchain_openai import OpenAIEmbeddings

# save db
from langchain_qdrant import QdrantVectorStore, Qdrant


def save_vector_db(docs):
    # Initialize QdrantVectorStore with embeddings and store the documents
    QdrantVectorStore.from_documents(
        docs,
        embeddings,  # embeddings are handled when creating the vector store
        url=QDRANT_SERVER,
        prefer_grpc=True,
        collection_name=collection_name,
    )
    print("Đã lưu vector store")


# load db
def load_vector_db():
    try:
        # Initialize the Qdrant client with embeddings for the collection
        client = Qdrant.from_existing_collection(
            embedding=embeddings,  # embeddings are set up in the Qdrant client
            collection_name=collection_name,
            url=QDRANT_SERVER,
            api_key=QDRANT_API_KEY,
        )
        print("Load db thành công")
        return client
    except Exception as e:
        print(f"Lỗi load db: {e}")
        return None


# search tương tự
def similarity_search_qdrant_data(db, query, k=10):
    # Perform similarity search without passing embeddings explicitly
    docs = db.similarity_search(query=query, k=k)
    return docs


def get_full_page_content(db, source: str, page: int):
    """Lấy toàn bộ nội dung từ 1 trang cụ thể của tài liệu chỉ định"""

    # Thêm filter theo source để tránh trùng lặp giữa các tài liệu
    filter_conditions = [
        models.FieldCondition(
            key="metadata.page",
            match=models.MatchValue(value=page),
        ),
        models.FieldCondition(
            key="metadata.source",
            match=models.MatchValue(value=source),
        )
    ]

    # Thêm limit hợp lý và score threshold
    docs = db.similarity_search(
        query="",
        filter=models.Filter(must=filter_conditions),
    )
    return docs


def get_context_db(db, query, k=10):
    docs = similarity_search_qdrant_data(db, query, k)

    # Tạo dict lưu trữ các trang duy nhất với metadata đầy đủ
    # unique_pages = {}
    # for doc in docs:
    #     meta = doc.metadata
    #     source = meta.get('source').strip()
    #     page = int(meta.get('page', 0))
    #     # print(page)
    #
    #     unique_key = f"{source}_{page}"
    #     if unique_key not in unique_pages:
    #         unique_pages[unique_key] = {
    #             'source': source,
    #             'page': page
    #         }
    # all_docs = []  # Chỗ này đổi tên biến để tránh trùng lặp với docs
    # for key, data in unique_pages.items():
    #     page_docs = get_full_page_content(db, data['source'], data['page'])
    #     if isinstance(page_docs, list):  # Nếu là list, thêm tất cả vào all_docs
    #         all_docs.extend(page_docs)
    #     else:  # Nếu không phải list, chỉ thêm 1 tài liệu vào all_docs
    #         all_docs.append(page_docs)
    #
    # # Sắp xếp và loại bỏ trùng lặp theo chunk_id
    # unique_id = set()
    # sorted_docs = sorted(all_docs, key=lambda x: x.metadata.get('page', 0))
    # unique_docs = []
    # for doc in sorted_docs:
    #     chunk_id = doc.metadata.get('chunk_id')  # Lấy chunk_id từ metadata
    #     if chunk_id not in unique_id:
    #         unique_id.add(chunk_id)
    #         unique_docs.append(doc)
    # print(len(sorted_docs))
    # print(len(unique_docs))
    context_items = []
    # for doc in unique_docs:
    for doc in docs:
        data = doc.metadata
        content = doc.page_content
        context_items.append(
            f"📖 {data['source'].upper()} - TRANG {data['page']}\n"
            f"🔍 Nội dung:\n{content}\n"
        )
        # print(doc.metadata['chunk_id'])
    print("\n\n".join(context_items))
    return "\n\n".join(context_items)

# Kiểm tra với câu truy vấn
# get_context_db(load_vector_db(), "Chuyên là gì ? ")


# Example usage:
# save_vector_db(load_document("../data/upload/So tay Van hoa Doanh nghiep - Stavian Group.pdf"))

# client = load_vector_db()
# query = "Tôn giáo trong truyết học"
# docs = similarity_search_qdrant_data(client, query)
# for doc in docs:
#     print(doc.page_content, "\n", doc.metadata.get('package'))
