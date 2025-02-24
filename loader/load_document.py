import json
import re
import uuid  # Thêm thư viện uuid
import PyPDF2
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
# for semantic chunking
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

from config.config import pdf_path


def load_documents(file_path: str):
    loader = PyPDFLoader(file_path)
    pdf_docs = loader.load()
    return pdf_docs


def clean_text(text):
    # 1. Loại bỏ khoảng trắng thừa giữa các ký tự xuống dòng.
    text = re.sub(r'\n\s+\n', '\n\n', text)
    # 2. Làm sạch từng dòng riêng biệt mà vẫn giữ nguyên các dòng rỗng
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if line.strip():
            line = re.sub(r'\s+', ' ', line).strip()
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    return text.strip()


def prepare_docs(pdf_docs):
    docs = []
    for pdf in pdf_docs:
        content = pdf.page_content
        metadata = {
            "type": "text",
            "page": pdf.metadata.get('page', -2),
            "title": pdf.metadata.get('title', None)
        }
        docs.append(Document(page_content=content, metadata=metadata))
    # Làm sạch nội dung của mỗi document với hàm clean_text
    contents = [clean_text(doc.page_content) for doc in docs]
    metadatas = [doc.metadata for doc in docs]
    print("Content và metadata đã được trích xuất và làm sạch từ các tài liệu")
    return contents, metadatas


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


def load_document(pdf_path: str):
    # Loader: lấy tài liệu từ file PDF
    docs = load_documents(pdf_path)
    # Prepare: trích xuất nội dung và metadata
    contents, metadatas = prepare_docs(docs)
    # Chunking: tách nội dung thành các đoạn nhỏ
    list_docs = get_text_chunks(contents, metadatas)
    # Clear data và thêm trường 'package' vào metadata cho mỗi document
    for doc in list_docs:
        doc.page_content = clean_text(doc.page_content)
    return list_docs


if __name__ == "__main__":
    # Đảm bảo rằng biến pdf_path được import từ config và package là tên gói bạn muốn thêm vào metadata
    pdf_path = "../data/upload/So tay Van hoa Doanh nghiep - Stavian Group.pdf"
    list_docs = load_document(pdf_path)
    for doc in list_docs:
        print(doc, "\n=================\n")

# import json
# import re
# import PyPDF2
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# # for semantic chunking
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_openai.embeddings import OpenAIEmbeddings
#
# from config.config import pdf_path
#
#
# def load_documents(file_path: str):
#     loader = PyPDFLoader(file_path)
#     pdf_docs = loader.load()
#     return pdf_docs
#
#
# def clean_text(text):
#     # 1. Loại bỏ khoảng trắng thừa giữa các ký tự xuống dòng.
#     text = re.sub(r'\n\s+\n', '\n\n', text)
#     # 2. Làm sạch từng dòng riêng biệt mà vẫn giữ nguyên các dòng rỗng
#     lines = text.split('\n')
#     cleaned_lines = []
#     for line in lines:
#         if line.strip():
#             line = re.sub(r'\s+', ' ', line).strip()
#         cleaned_lines.append(line)
#     text = '\n'.join(cleaned_lines)
#     # 3. Loại bỏ ký tự đặc biệt
#     # text = re.sub(r'[^\w\s\%\.\,\:\;\!\?\-]', '', text, flags=re.UNICODE)
#     # Loại bỏ dấu gạch dưới (_), vì \w giữ lại dấu này
#     # text = text.replace('_', '')
#     return text.strip()
#
#
# def prepare_docs(pdf_docs):
#     docs = []
#     for pdf in pdf_docs:
#         content = pdf.page_content
#         metadata = {
#             "type": "text",
#             "page": pdf.metadata.get('page', None),
#             "title": pdf.metadata.get('title', None)
#         }
#         docs.append(Document(page_content=content, metadata=metadata))
#     # Làm sạch nội dung của mỗi document với hàm clean_text
#     contents = [clean_text(doc.page_content) for doc in docs]
#     metadatas = [doc.metadata for doc in docs]
#     print("Content và metadata đã được trích xuất và làm sạch từ các tài liệu")
#     return contents, metadatas
#
#
# def get_text_chunks(contents, metadatas):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=0  # , separators=
#     )
#     list_docs = text_splitter.create_documents(contents, metadatas=metadatas)
#     print(f"Documents are split into {len(list_docs)} passages")
#     return list_docs
#
#
# # text_splitter = SemanticChunker(OpenAIEmbeddings(),
# #                                 breakpoint_threshold_type='percentile')
#
# def load_document(pdf_path: str):
#     # Loader: lấy tài liệu từ file PDF
#     docs = load_documents(pdf_path)
#     # Prepare: trích xuất nội dung và metadata
#     contents, metadatas = prepare_docs(docs)
#     # Chunking: tách nội dung thành các đoạn nhỏ
#     list_docs = get_text_chunks(contents, metadatas)
#     # Clear data và thêm trường 'package' vào metadata cho mỗi document
#     for doc in list_docs:
#         doc.page_content = clean_text(doc.page_content)
#         # doc.metadata["package"] = package
#     return list_docs
#
#
# if __name__ == "__main__":
#     # Đảm bảo rằng biến pdf_path được import từ config và package là tên gói bạn muốn thêm vào metadata
#     # package_name = "upload"  # Thay đổi tên gói theo yêu cầu
#     pdf_path = "../data/upload/triethoc.pdf"
#     list_docs = load_document(pdf_path)
#     for doc in list_docs:
#         print(doc, "\n=================\n")
