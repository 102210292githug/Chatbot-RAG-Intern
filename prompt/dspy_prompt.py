from typing import List

import dspy

from config.config import OPENAI_API_KEY
from loader.save_load_db import similarity_search_qdrant_data, load_vector_db, get_context_db

# Cấu hình OpenAI
lm = dspy.LM('openai/gpt-4o-mini',
             api_key=OPENAI_API_KEY,
             temperature=0)
dspy.configure(lm=lm)


# Xác định class câu hỏi
class Question(dspy.Signature):
    """Bạn là hệ thống trích xuất thông tin từ tài liệu. CHỈ sử dụng thông tin trong context được cung cấp.

    Nguyên tắc trả lời:
    1. Trích dẫn nguyên văn từ tài liệu khi có thể
    2. Nếu không có nguyên văn, diễn đạt sát nghĩa nhất
    3. Luôn kèm trích dẫn nguồn chính xác cho từng phần của câu trả lời đưa ra
    4. Tuyệt đối không thêm thông tin không có trong context"""

    context: str = dspy.InputField(
        prefix="[TÀI LIỆU NGUỒN]\n",
        # format=lambda x: "\n".join([f"● {item}" for item in x.split("\n")])
    )
    question: str = dspy.InputField(prefix="[CÂU HỎI] ")
    history: str = dspy.InputField(prefix="[LỊCH SỬ CHAT] ", default="")
    answer: str = dspy.OutputField(
        desc="""TRẢ LỜI PHẢI:
        - Bắt đầu bằng "Theo tài liệu..." nếu có nguyên văn
        - Trích dẫn chính xác (Tên tài liệu - Trang)
        - Định dạng: 
          1. Phần trả lời trực tiếp
          2. Trích dẫn nguồn
          3. Ngữ cảnh liên quan (nếu cần)"""
    )


# Tạo module chatbot
class create_questions(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.ChainOfThought(Question)

    def forward(self, context: str, question: str, history: str) -> str:
        """Trả lời câu hỏi dựa trên ngữ cảnh và lịch sử hội thoạ

        """
        response = self.predictor(
            context=context,
            question=question,
            history=history
        )
        return response.answer


class FollowUpSignature(dspy.Signature):
    """Tạo 3 câu hỏi liên quan đến câu hỏi và câu trả lời gần đây nhất dựa trên lịch sử chat và context
        Câu hỏi phải liên quan, không trùng lặp"""
    context: str = dspy.InputField(prefix="[Tài liệu] ")
    history: str = dspy.InputField(prefix="[Lịch sử hội thoại] ")
    questions: str = dspy.OutputField(
        desc="Danh sách 3 câu hỏi liên quan logic, có tính kế thừa, mỗi câu hỏi một dòng",
        format=lambda x: "\n".join([f"{i + 1}. {q}" for i, q in enumerate(x)])
    )


class EnhancedChatBot(dspy.Module):
    def __init__(self):
        super().__init__()
        self.follow_up_predictor = dspy.ChainOfThought(FollowUpSignature)

    def forward(self, context: str, history: str) -> list:
        # Tạo câu hỏi follow-up
        prediction = self.follow_up_predictor(
            context=context,
            history=history
        )

        # Xử lý kết quả
        raw_questions = prediction.questions.split("\n")
        suggestions = [q.split(". ", 1)[1] for q in raw_questions if ". " in q]

        return suggestions[:3]  # Đảm bảo chỉ trả về 3 câu hỏi


chatbot = create_questions()
enhanced_bot = EnhancedChatBot()
db = load_vector_db()


def get_rseponse_with_dspy(user_question: str, history: str):
    # Câu hỏi mới của người dùng
    pdf_context = get_context_db(db, user_question)
    # Gọi chatbot để trả lời
    print(pdf_context)
    response = chatbot.forward(context=pdf_context, question=user_question, history=history)
    # thêm vào lịch sử
    history += f"User: {user_question} \n Bot: {response}"
    # Tạo câu hỏi follow-up
    suggestions = enhanced_bot.forward(
        context=pdf_context,
        history=history
    )
    return response, suggestions

# print(get_rseponse_with_dspy("Giám đốc cần làm gì?", ""))

# # Sử dụng
# enhanced_bot = EnhancedChatBot()
#
# # Tạo câu hỏi follow-up
# suggestions = enhanced_bot.forward(
#     context=pdf_context,
#     history=history
# )
#
# print("\n=== GỢI Ý CÂU HỎI TIẾP THEO ===")
# for i, question in enumerate(suggestions, 1):
#     print(f"{i}. {question}")

# def get_context(db, query):
#     docs = similarity_search_qdrant_data(db, query, k=5)
#
#     context_items = []
#     for doc in docs:
#         meta = doc.metadata
#         source = f"{meta.get('title', 'Không rõ')}"
#         if 'page' in meta:
#             source += f" - Trang {int(meta['page']) + 1}"
#
#         context_items.append(
#             f"📄 NỘI DUNG: {doc.page_content}\n"
#             f"🏷️ NGUỒN: {source}\n"
#             "―――――――――――――――――――"
#         )
#
#     return "\n".join(context_items)

# # Khởi tạo module chatbot
# chatbot = create_questions()
# history = ""
# db = load_vector_db()
#
# # Câu hỏi mới của người dùng
# user_question = "Giám đốc phải làm gì?"
# pdf_context = get_context(db, user_question)
#
# # Gọi chatbot để trả lời
# response = chatbot.forward(context=pdf_context, question=user_question, history=history)
#
# # In kết quả
# print(response)
#
# # thêm vào lịch sử
# history += f"User: {user_question} \n Bot: {response}"
