import google.generativeai as genai
import openai
import sys
import os
import json

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

API_KEY_FILES = {
    "gpt": "apikey_gpt.json",
    "gemini": "apikey_gemini.json"
}
CHAT_HISTORY_FILES = {
    "gpt": "listchat_gpt.json",
    "gemini": "listchat_gemini.json"
}

def save_api_key(api_key, model):
    with open(API_KEY_FILES[model], 'w') as f:
        json.dump({"api_key": api_key}, f)

def load_api_key(model):
    file_path = API_KEY_FILES[model]
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("api_key")
    return None

def delete_api_key(model):
    file_path = API_KEY_FILES[model]
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Đã xoá API key cho {model.capitalize()}.")
    else:
        print(f"Không tìm thấy API key cho {model.capitalize()}.")

def delete_all_api_keys():
    for model in API_KEY_FILES:
        delete_api_key(model)

def save_chat_history(history, model):
    with open(CHAT_HISTORY_FILES[model], 'w') as f:
        json.dump(history, f)

def load_chat_history(model):
    file_path = CHAT_HISTORY_FILES[model]
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

print("Chương trình chat chạy bằng Python được viết bởi VinZ")
print("GitHub: vinzcyun")
print("Phiên bản: Chat Pro 1.5")

while True:
    action = input("Chọn hành động: 1 để chọn model, 2 để xoá API key: ").strip()
    if action == "1":
        selected_model = None
        while selected_model not in ["1", "2"]:
            selected_model = input("Nhấn 1 để chọn GPT, nhấn 2 để chọn Gemini: ").strip()
            if selected_model == "1":
                selected_model = "gpt"
            elif selected_model == "2":
                selected_model = "gemini"
            else:
                print("Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.")

        api_key = load_api_key(selected_model)
        if not api_key:
            api_key = input(f"Nhập API key cho {selected_model.capitalize()}: ")
            save_api_key(api_key, selected_model)

        history = load_chat_history(selected_model)

        if selected_model == 'gemini':
            genai.configure(api_key=api_key)
            print("Đang kết nối đến API của Gemini...")
            try:
                model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
                convo = model.start_chat(history=history)
                print("Đã kết nối đến Gemini")
            except Exception as e:
                print(f"Lỗi khi kết nối đến API của Gemini: {e}")
                exit()
        elif selected_model == 'gpt':
            openai.api_key = api_key
            print("Đang kết nối đến API của GPT...")
            try:
                convo = {"history": history}
                print("Đã kết nối đến GPT")
            except Exception as e:
                print(f"Lỗi khi kết nối đến API của GPT: {e}")
                exit()
        else:
            print("Model không hợp lệ! Thoát chương trình.")
            exit()

        print("Ghi chú: Bạn có thể nhập exit hoặc quit để thoát trò chuyện")
        print("================================================")

        while True:
            user_input = input("Nhập câu hỏi: ")

            if user_input.lower() in ["quit", "exit"]:
                break

            print(f"{selected_model.capitalize()} đang trả lời... chờ xíu nhé!")
            try:
                if selected_model == 'gemini':
                    response = convo.send_message(user_input)
                    print("Gemini đã trả lời:", response.text)
                    history.append({"user": user_input, "gemini": response.text})
                elif selected_model == 'gpt':
                    response = openai.Completion.create(
                        engine="davinci",
                        prompt=user_input,
                        max_tokens=150
                    )
                    answer = response.choices[0].text.strip()
                    print("GPT đã trả lời:", answer)
                    history.append({"user": user_input, "gpt": answer})
                save_chat_history(history, selected_model)
            except Exception as e:
                print(f"Lỗi khi gửi tin nhắn: {e}")

            print("____________________")

        print("Đoạn trò chuyện kết thúc!")
        break
    elif action == "2":
        delete_action = input("Nhấn 1 để xoá API key GPT, nhấn 2 để xoá API key Gemini, nhấn 3 để xoá tất cả: ").strip()
        if delete_action == "1":
            delete_api_key("gpt")
        elif delete_action == "2":
            delete_api_key("gemini")
        elif delete_action == "3":
            delete_all_api_keys()
        else:
            print("Lựa chọn không hợp lệ.")
    else:
        print("Lựa chọn không hợp lệ.")