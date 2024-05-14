import google.generativeai as genai
import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

print("Gemini chạy bằng Python được viết bởi VinZ")
print("GitHub: vinzcyun")
print("Phiên bản: Gemini Pro 1.5")

api_key = input("Nhập API Gemini Trong Google Cloud Studio: ")
genai.configure(api_key=api_key)

print("Đang kết nối đến API của Gemini...")

try:
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    print("Đã kết nối")
except Exception as e:
    print(f"Lỗi khi kết nối đến API của Gemini: {e}")
    exit()

convo = model.start_chat(history=[])
print("Ghi chú: Bạn có thể nhập exit hoặc quit để thoát trò chuyện")
print("================================================")

while True:
    user_input = input("Nhập câu hỏi: ")

    if user_input.lower() == "quit" or user_input.lower() == "exit":
        break

    print("Gemini đang trả lời... chờ xíu nhé!")
    try:
        convo.send_message(user_input)
        print("Gemini đã trả lời:", convo.last.text)
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn: {e}")

    print("____________________")

print("Đoạn trò chuyện kết thúc!")