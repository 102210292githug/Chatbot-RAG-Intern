import re
from unstructured.cleaners.core import (
    group_broken_paragraphs,
    clean,
)
from collections import defaultdict
import json

# Danh sách các ký tự không mong muốn
unwanted_chars = [
    "ü", "ÿ", "þ", "®", "±", "©", "µ", "÷", "v ", "Ø", "€", "ƒ", "†", "‡", "ˆ", "Š", "Œ", "Ä", "•", "˜", "™", "š", "›",
    "œ", "ž", "Ÿ", "¡", "¢", "£", "¤", "¥", "¦", "§", "¨", "ª", "«", "¬", "°", "²", "³", "µ", "¶", "»", "¿", "Ä", "ü ",
    "ÿ ", "þ ", "® ", "± ", "© ", "µ ", "÷ ", "v ", "Ø ", "€ ", "ƒ ", "† ", "‡ ", "ˆ ", "Š ", "Œ ", "Ä ", "• ", "˜ ",
    "™ ", "š ", "› ", "œ ", "ž ", "Ÿ ", "¡ ", "¢ ", "£ ", "¤ ", "¥ ", "¦ ", "§ ", "¨ ", "ª ", "« ", "¬ ", "° ", "² ",
    "³ ", "µ ", "¶ ", "» ", "¿ ", "Ä ", "‹"
]


# Hàm làm sạch văn bản với các bullet points
def clean_text(text, bullets):
    chars_pattern = "|".join(re.escape(char) for char in bullets)
    bullet_pattern = re.compile(
        r"((?:" + chars_pattern + r").+?)(?=(?:" + chars_pattern + r")|\Z)", re.DOTALL
    )
    matches = bullet_pattern.findall(text)
    cleaned_parts = []
    for match in matches:
        cleaned_part = " ".join(match.split())
        cleaned_parts.append(cleaned_part)
    other_parts = bullet_pattern.split(text)
    other_parts = [
        part
        for part in other_parts
        if part.strip() and not re.match(chars_pattern, part.strip())
    ]
    cleaned_text = "\n\n".join(other_parts + cleaned_parts)
    return cleaned_text


# Hàm loại bỏ các ký tự đặc biệt
def remove_specific_chars(text, chars):
    pattern = re.compile("|".join(re.escape(char) for char in chars))
    cleaned_text = pattern.sub("-", text)
    return cleaned_text


# Hàm loại bỏ dấu chấm và khoảng trắng thừa
def remove_char_dots(text):
    text = re.sub(r"\n\s*\n", "\n\n", text)
    text = re.sub(r" {3,}", " ", text)
    text = re.sub(r"\.\.\.", ".", text)
    return text




# Hàm làm sạch dữ liệu với Unstructured
def clean_data_unstructured(texts):
    _text = []
    for text in texts:
        text = remove_specific_chars(text, unwanted_chars)
        text = group_broken_paragraphs(text)
        text = remove_char_dots(text)
        _text.append(text)
    return _text





# Hàm chính để xử lý dữ liệu
def process_data(data):
    cleaned_data = []
    for item in data:
        page_content = item["page_content"]
        metadata = item["metadata"]

        # Làm sạch nội dung trang
        page_content = clean_data_unstructured([page_content])[0]

        # Làm sạch metadata
        metadata = {k: v for k, v in metadata.items() if v is not None}

        cleaned_data.append({
            "page_content": page_content,
            "metadata": metadata
        })

    return cleaned_data


# Đọc dữ liệu từ file JSON
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Lưu dữ liệu đã làm sạch vào file JSON
def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Ví dụ sử dụng
if __name__ == "__main__":
    # Đường dẫn file JSON đầu vào và đầu ra
    input_json_path = "../data/output/elements_data.json"
    output_json_path = "../data/output/data_clean.json"

    # Đọc dữ liệu
    data = load_json(input_json_path)

    # Xử lý dữ liệu
    cleaned_data = process_data(data)
    # Lưu dữ liệu đã làm sạch
    save_json(cleaned_data, output_json_path)

    print(f"Dữ liệu đã được làm sạch và lưu vào {output_json_path}")

    # ... (phần code trước giữ nguyên)

    # Load lại file JSON và in kiểm tra
    print("\nKIỂM TRA DỮ LIỆU ĐÃ LƯU:")

    with open(output_json_path, "r", encoding="utf-8") as json_file:
        loaded_data = json.load(json_file)

        # In 3 document đầu tiên làm ví dụ
        for i, doc in enumerate(loaded_data, 1):
            print(f"\nDocument {i}:")
            print(f"Page content: {doc['page_content']}...")  # In 100 ký tự đầu
            print("Metadata:")
            for key, value in doc['metadata'].items():
                print(f"- {key}: {value}")
            print("-" * 50)