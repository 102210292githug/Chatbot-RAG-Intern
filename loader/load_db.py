import os

from langchain_openai import OpenAIEmbeddings

from config.config import OPENAI_API_KEY, QDRANT_SERVER, QDRANT_API_KEY, collection_name
from qdrant_client import models

from langchain_qdrant import Qdrant

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# text-embedding-ada-002: Tạo ra các vector embedding với 1536 chiều.
# text-embedding-3-large: Tạo ra các vector với 3072 chiều.


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


def get_full_page_content(db, title: str, page: int):
    """Lấy toàn bộ nội dung từ 1 trang cụ thể của tài liệu chỉ định"""

    # Thêm filter theo title để tránh trùng lặp giữa các tài liệu
    filter_conditions = [
        models.FieldCondition(
            key="metadata.page",
            match=models.MatchValue(value=page),
        ),
        models.FieldCondition(
            key="metadata.source",
            match=models.MatchValue(value=title),
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
    unique_pages = {}
    for doc in docs:
        meta = doc.metadata
        title = meta.get('source').strip()
        page = int(meta.get('page', -2))
        unique_key = f"{title}_{page}"
        if unique_key not in unique_pages:
            unique_pages[unique_key] = {
                'source': title,
                'page': page
            }

    all_docs = []  # Chỗ này đổi tên biến để tránh trùng lặp với docs
    for key, data in unique_pages.items():
        # Nếu get_full_page_content trả về một danh sách, bạn cần xử lý từng phần tử trong đó
        page_docs = get_full_page_content(db, data['source'], data['page'])
        if isinstance(page_docs, list):  # Nếu là list, thêm tất cả vào all_docs
            all_docs.extend(page_docs)
        else:  # Nếu không phải list, chỉ thêm 1 tài liệu vào all_docs
            all_docs.append(page_docs)

    # Sắp xếp và loại bỏ trùng lặp theo chunk_id
    unique_id = set()
    sorted_docs = sorted(all_docs, key=lambda x: x.metadata.get('page', 0))
    unique_docs = []
    for doc in sorted_docs:
        chunk_id = doc.metadata.get('chunk_id')  # Lấy chunk_id từ metadata
        if chunk_id not in unique_id:
            unique_id.add(chunk_id)
            unique_docs.append(doc)
    # print(len(sorted_docs))
    # print(len(unique_docs))
    context_items = []
    for doc in unique_docs:
        data = doc.metadata
        content = doc.page_content
        context_items.append(
            f"📖 {data['source'].upper()} - TRANG {data['page'] + 1}\n"
            f"🔍 Nội dung:\n{content}\n"
            "―--------------------------------------"
        )
        print(doc.metadata['chunk_id'])
    print("\n\n".join(context_items))
    return "\n\n".join(context_items)

# Kiểm tra với câu truy vấn
get_context_db(load_vector_db(), "Chuyên là gì ? ")


# Example usage:
# save_vector_db(load_document("../data/upload/So tay Van hoa Doanh nghiep - Stavian Group.pdf"))

# client = load_vector_db()
# query = "Tôn giáo trong truyết học"
# docs = similarity_search_qdrant_data(client, query)
# for doc in docs:
#     print(doc.page_content, "\n", doc.metadata.get('package'))
