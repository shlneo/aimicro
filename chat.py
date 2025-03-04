import os
import google.generativeai as genai
import keyboard
import threading
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="Отвечай на вопросы"
)

chat_session = model.start_chat(history=[])
exit_flag = False

def exit_program():
    global exit_flag
    exit_flag = True
    print("\nВыход из программы.")
    os._exit(0)  

keyboard.add_hotkey("esc", exit_program)

print("Бот: Привет! Как я могу помочь?")
print("Нажмите ESC для выхода.\n")

while not exit_flag:
    try:
        user_input = input("Вы: ").strip()
        if not user_input or exit_flag:  # Если пользователь ничего не ввел или нажал ESC
            continue

        response = chat_session.send_message(user_input)
        model_response = response.text

        print(f'Бот: {model_response}')
        print()

        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})

    except EOFError:
        break

