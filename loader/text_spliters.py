import json
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def get_text_chunks(contents, metadatas):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0
    )
    list_docs = text_splitter.create_documents(contents, metadatas=metadatas)
    print(f"Documents are split into {len(list_docs)} passages")
    # Thêm UUID vào metadata của mỗi chunk
    for doc in list_docs:
        doc.metadata["chunk_id"] = str(uuid.uuid4())  # Tạo UUID và lưu vào metadata
    return list_docs


if __name__ == "__main__":
    # Đường dẫn file JSON đầu vào và đầu ra
    input_json_path = "../data/output/data_clean.json"
    output_json_path = "../data/output/chunks_data.json"

    # Đọc dữ liệu từ tệp JSON đầu vào
    with open(input_json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Giả sử 'contents' và 'metadatas' là các danh sách chứa nội dung và siêu dữ liệu tương ứng
    contents = [item['page_content'] for item in data]
    metadatas = [item['metadata'] for item in data]

    # Gọi hàm để chia nhỏ văn bản
    chunked_docs = get_text_chunks(contents, metadatas)

    # Chuyển đổi kết quả thành danh sách các dict để lưu dưới dạng JSON
    output_data = []
    for doc in chunked_docs:
        output_data.append({
            'page_content': doc.page_content,
            'metadata': doc.metadata
        })

    # Lưu kết quả vào tệp JSON đầu ra
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)
