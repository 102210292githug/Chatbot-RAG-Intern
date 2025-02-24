# Chatbot-RAG PDF Reader

## TỔNG QUAN

Project này là một ứng dụng chatbot sử dụng công nghệ RAG (Retrieval-Augmented Generation) để đọc và xử lý các file PDF do người dùng tải lên. Ứng dụng giúp trích xuất thông tin từ các file PDF và trả lời các câu hỏi liên quan đến nội dung của file một cách tự động và thông minh.

## CHỨC NĂNG

- **Đọc file PDF:** Tự động nhận diện và trích xuất nội dung từ các file PDF.
- **Trả lời câu hỏi:** Sử dụng công nghệ RAG để tìm kiếm và trả lời các câu hỏi dựa trên nội dung file PDF.
- **Tương tác tự nhiên:** Giao diện thân thiện giúp người dùng dễ dàng tương tác và nhận thông tin.
- **Đưa ra 3 câu hỏi gợi ý liên quan đến câu trả lời cuối cùng**

## HƯỚNG DẪN CÀI ĐẶT

1. **Cài đặt thư viện:**  
   Chạy lệnh sau trong terminal để cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
2. **Cấu hình API:**
  - Mở file config.py và thêm khóa API của bạn:
    ```pycon
    OPEN_API_KEY = ''
    ```
  - Thêm server Qdrant và API:
    ```pycon
    QDRANT_SERVER = ""
    QDRANT_API_KEY = ""
    ```
## CÁCH SỬ DỤNG
Chạy ứng dụng bằng lệnh sau:
```bash
streamlit run ui.py
```
## CÔNG NGHỆ SỬ DỤNG
- Python: Ngôn ngữ lập trình chính của project.
- Streamlit: Framework dùng để xây dựng giao diện web cho ứng dụng.
- Các thư viện xử lý PDF: Dùng để trích xuất nội dung từ file PDF.
- Retrieval-Augmented Generation (RAG): Công nghệ tích hợp tìm kiếm và tạo nội dung tự động dựa trên dữ liệu đã có.
- Database: Qdrant
## CONTACT
Nếu bạn có bất kỳ thắc mắc hoặc góp ý nào, hãy liên hệ qua ```lehuynhduc.th321@gmail.com``` để được hỗ trợ.
