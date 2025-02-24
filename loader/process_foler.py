import os
import glob

from loader.load_document import load_document


def process_pdf_folder(folder_name: str):
    """
    Xử lý thư mục chứa file PDF nằm trong ./data/<folder_name>:
      - Lấy tất cả các file PDF trong thư mục.
      - Với mỗi file PDF, gọi hàm load_document để nhận về list_docs, truyền package là folder_name.
      - Trả về danh sách các tài liệu được load từ các file PDF.

    Parameters:
        folder_name (str): Tên thư mục con nằm trong ./data.

    Returns:
        all_docs (list): Danh sách tất cả các tài liệu được load từ các file PDF.
    """
    # Xác định đường dẫn thư mục
    folder_path = "../data/" + folder_name

    # Lấy tất cả các file PDF trong thư mục
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

    all_docs = []

    for pdf_file in pdf_files:
        # Load tài liệu từ file PDF, truyền package là folder_name
        docs = load_document(pdf_file, package=folder_name)
        all_docs.extend(docs)

    print(f"Đã xử lý {len(pdf_files)} file PDF.")
    return all_docs



# if __name__ == "__main__":
#     folder_name = "upload"  # Thay "upload" bằng tên thư mục cụ thể trong ./data
#     all_docs = process_pdf_folder(folder_name)
#     for doc in all_docs:
#         print(doc, "\n=================\n")
