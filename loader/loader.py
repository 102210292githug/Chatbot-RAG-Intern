from unstructured.partition.pdf import partition_pdf
from transformers import logging
import unstructured_pytesseract
import json
from collections import defaultdict

logging.set_verbosity_error()
unstructured_pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def load_documents(file_path: str):
    # Tắt chunking và xử lý theo trang
    raw_elements = partition_pdf(
        filename=file_path,
        extract_image_block_types=["Image"],
        infer_table_structure=False,
        form_extraction_skip_tables=False,
        languages=["vie"],
        strategy="hi_res",  # Dùng độ phân giải cao để xác định trang chính xác
        hi_res_model_name="yolox",
        include_page_breaks=True,  # Thêm phần tử ngắt trang
    )
    return raw_elements


def elements_to_dict(elements):
    pages = defaultdict(list)
    current_page = 1

    for element in elements:
        # Nhận diện phần tử ngắt trang
        if element.category == "PageBreak":
            current_page += 1
            continue

        # Nhóm các phần tử theo trang
        pages[current_page].append(element)

    # Tạo dict cho từng trang
    elements_dict = []
    for page_num, elements_in_page in pages.items():
        page_text = "\n".join([elem.text for elem in elements_in_page if elem.text])

        metadata = {
            "page": page_num,
            "source": elements_in_page[0].metadata.filename if elements_in_page else "",
            "category": "Page"
        }

        elements_dict.append({
            "page_content": page_text,
            "metadata": metadata
        })

    return elements_dict


# Sử dụng
# pdf_path = "../data/upload/So tay Van hoa Doanh nghiep - Stavian Group.pdf"
# json_path = "../data/output/elements_data.json"
#
# list_elements = load_documents(pdf_path)
# elements_dict = elements_to_dict(list_elements)
#
# # Lưu JSON
# with open(json_path, "w", encoding="utf-8") as json_file:
#     json.dump(elements_dict, json_file, ensure_ascii=False, indent=4)
#
# print(f"Đã lưu {len(elements_dict)} trang vào {json_path}")