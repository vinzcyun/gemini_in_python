import google.generativeai as genai

print("Gemini chạy bằng Python được viết bởi VinZ")
print("GitHub: vinzcyun")
print("Phiên bản Gemini Pro 1.5")
api_key = input("Nhập API Gemini Trong Google Cloud Studio: ")
genai.configure(api_key=api_key)

print("Đang kết nối đến API của Gemini...")
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

print("Đã kết nối")
convo = model.start_chat(history=[])
print("Ghi chú: Bạn có thể nhập exit hoặc quit để thoát trò chuyện")
print("=================================")
while True:
    user_input = input("Nhập câu hỏi (chỉ bằng tiếng Anh): ")
    convo.send_message(user_input)
    print("Gemini đã trả lời:",convo.last.text)

    if user_input.lower() == "quit" or user_input.lower() == "exit":
        break

print("Đoạn trò chuyện kết thúc!")
