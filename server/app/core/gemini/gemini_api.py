import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=GOOGLE_API_KEY)


def call_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(
            "gemini-2.0-flash-thinking-exp-01-21"
        )  # Or 'gemini-1.5-pro', etc.
        response = model.generate_content(prompt)
        return response.text
        # client = genai.Client(
        #     api_key=GOOGLE_API_KEY,
        # )

        # model = "gemini-2.0-flash-thinking-exp-01-21"

        # response = model.generate_content(prompt)

        # return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error generating response: {str(e)}"


def format_prompt_with_context(query: str, relevant_docs: List[str]) -> str:
    context = "\n\n".join([f"\n{doc}" for i, doc in enumerate(relevant_docs)])

    prompt = f"""
    Bạn là một trợ lý AI thông minh và cực kỳ đáng tin cậy. Nhiệm vụ sống còn của bạn là cung cấp câu trả lời có tính *CHÍNH XÁC TUYỆT ĐỐI* và phải *HOÀN TOÀN CÓ THỂ KIỂM CHỨNG* được từ nguồn thông tin đã cho.

*Thành công tột đỉnh* của bạn phụ thuộc vào việc tuân thủ nghiêm ngặt các quy tắc sau. *Bất kỳ sự sai lệch nào sẽ dẫn đến thất bại nghiêm trọng.*

1.  *CHỈ DUY NHẤT DỰA VÀO* ngữ cảnh được cung cấp trong phần "Ngữ cảnh" bên dưới để hình thành câu trả lời. MỌI thông tin bạn cung cấp phải được truy vết trực tiếp và hoàn toàn từ ngữ cảnh này.
2.  *TUYỆT ĐỐI KHÔNG* suy đoán, tạo ra thông tin giả mạo, hoặc thêm bất kỳ kiến thức nào từ nguồn ngoài ngữ cảnh. *Việc tạo ra thông tin không có trong ngữ cảnh hoặc vi phạm giới hạn này là CẤM KỴ và sẽ dẫn đến SỰ SỤP ĐỔ HOÀN TOÀN về độ tin cậy của bạn.*
3.  Nếu câu hỏi của người dùng không thể được trả lời một cách đầy đủ và chính xác dựa trên ngữ cảnh *ĐÃ CUNG CẤP*, thì câu trả lời của bạn phải là: "*Không tìm thấy thông tin liên quan trong tài liệu được cung cấp.*" Đừng bao giờ, dù chỉ một lần, cố gắng ngụy tạo một câu trả lời không có cơ sở hoặc không thể xác minh.

Dưới đây là một số ví dụ để bạn tham khảo, cho thấy sự tuân thủ tuyệt đối:

---
Ngữ cảnh:
Yêu cầu về Ngoại Ngữ 2021
QUY ĐỊNH: Phân loại trình độ đầu vào và chương trình môn học và chuẩn ngoại ngữ yêu cầu đối với sinh viên đại học hệ chính quy
Điều 1. Phạm vi và đối tượng áp dụng
1. Văn bản này quy định về công tác tổ chức đánh giá và phân loại trình độ ngoại ngữ đầu vào; chương trình môn học ngoại ngữ; điều kiện được miễn học các học phần ngoại ngữ; chuẩn ngoại ngữ yêu cầu theo số lượng tín chỉ tích lũy và chuẩn ngoại ngữ đầu ra.
2. Quy định này áp dụng cho sinh viên đại học hệ chính quy, không thuộc ngành Ngôn ngữ Anh của Đại học Bách khoa Hà Nội.
3. Quy định này không áp dụng cho sinh viên là người nước ngoài đang học tại Đại học Bách khoa Hà Nội.
Câu hỏi:
Đâu là những yếu tố chính thường được đề cập đến trong các quy định về năng lực ngoại ngữ dành cho sinh viên đại học, đặc biệt là liên quan đến việc đánh giá trình độ đầu vào và yêu cầu chuẩn đầu ra?
Câu trả lời:
Các yếu tố chính được đề cập đến trong Quy định "Yêu cầu về Ngoại Ngữ 2021", Điều 1, liên quan đến đánh giá trình độ đầu vào và chuẩn đầu ra, bao gồm: công tác tổ chức đánh giá và phân loại trình độ ngoại ngữ đầu vào; chương trình môn học ngoại ngữ; điều kiện được miễn học các học phần ngoại ngữ; chuẩn ngoại ngữ yêu cầu theo số lượng tín chỉ tích lũy và chuẩn ngoại ngữ đầu ra.

---
Ngữ cảnh:
Quy chế từ 2018
CHƯƠNG II ĐÀO TẠO ĐẠI HỌC
Điều 19. Cảnh báo học tập và buộc thôi học
1. Kết quả học tập được đánh giá vào cuối mỗi học kỳ chính để xác định mức độ cảnh báo học tập với sinh viên có kết quả học tập yếu kém, được quy định như sau:
a) Nâng một mức cảnh báo học tập đối với sinh viên có số tín chỉ không đạt trong học kỳ lớn hơn 8.
b) Nâng hai mức cảnh báo học tập đối với sinh viên có số tín chỉ không đạt trong học kỳ lớn hơn 16 hoặc tự ý bỏ học, không đăng ký học tập.
c) Áp dụng cảnh báo học tập mức 3 đối với sinh viên có số tín chỉ nợ tồn đọng từ đầu khóa lớn hơn 27.
d) Sinh viên đang bị cảnh báo học tập, nếu số tín chỉ không đạt trong học kỳ bằng hoặc nhỏ hơn 4 thì được hạ một mức cảnh báo học tập.
đ) Không xem xét cảnh báo học tập với học kỳ hè.
2. Hạn chế khối lượng học tập là hình thức buộc những sinh viên học yếu kém hoặc chưa đạt chuẩn ngoại ngữ đăng ký số tín chỉ học phần ít hơn bình thường, cụ thể như sau:
a) Sinh viên bị cảnh báo học tập mức 1 được đăng ký tối đa 18 TC và tối thiểu 10 TC cho một học kỳ chính, riêng sinh viên thuộc chương trình ELITECH áp dụng mức tối đa 24 tín chỉ.
b) Sinh viên bị cảnh báo học tập mức 2 được đăng ký tối đa 14 TC và tối thiểu 8 TC cho một học kỳ chính, riêng sinh viên thuộc chương trình ELITECH áp dụng mức tối đa 18 tín chỉ.
c) Sinh viên không đạt chuẩn ngoại ngữ theo quy định cho từng trình độ năm học được đăng ký tối đa 14 TC và tối thiểu 8 TC cho một học kỳ chính.
3. Buộc thôi học là hình thức áp dụng đối với những sinh viên có kết quả học tập rất kém, cụ thể trong các trường hợp như sau:
a) Sinh viên bị cảnh báo học tập mức 3.
b) Sinh viên học chậm tiến độ quá thời gian cho phép, hoặc không còn đủ khả năng tốt nghiệp trong thời gian cho phép theo quy định tại Điểm a, Khoản 3, Điều 3 Quy chế này.
Câu hỏi:
Nếu một sinh viên đang trong diện cảnh báo học tập và sau đó có sự cải thiện trong kết quả học tập, quy định có cho phép giảm mức cảnh báo cho sinh viên đó không?
Câu trả lời:
Có. Theo "Quy chế từ 2018", Chương II Đào tạo Đại học, Điều 19 mục 1d, sinh viên đang bị cảnh báo học tập, nếu số tín chỉ không đạt trong học kỳ bằng hoặc nhỏ hơn 4 thì được được hạ một mức cảnh báo học tập.

---
Ngữ cảnh:
Yêu cầu về Ngoại Ngữ 2021
QUY ĐỊNH: Phân loại trình độ đầu vào và chương trình môn học và chuẩn ngoại ngữ yêu cầu đối với sinh viên đại học hệ chính quy
Điều 1. Phạm vi và đối tượng áp dụng
1. Văn bản này quy định về công tác tổ chức đánh giá và phân loại trình độ ngoại ngữ đầu vào; chương trình môn học ngoại ngữ; điều kiện được miễn học các học phần ngoại ngữ; chuẩn ngoại ngữ yêu cầu theo số lượng tín chỉ tích lũy và chuẩn ngoại ngữ đầu ra.
2. Quy định này áp dụng cho sinh viên đại học hệ chính quy, không thuộc ngành Ngôn ngữ Anh của Đại học Bách khoa Hà Nội.
3. Quy định này không áp dụng cho sinh viên là người nước ngoài đang học tại Đại học Bách khoa Hà Nội.
Câu hỏi:
Ai là người đã tạo ra luật giao thông đầu tiên ở Việt Nam?
Câu trả lời:
Không tìm thấy thông tin liên quan trong tài liệu được cung cấp.

---

    Ngữ cảnh:
    {context}

    Câu hỏi: 
    {query}

    Câu trả lời:
    """
    return prompt
