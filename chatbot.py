import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.file

#Load your API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

#Configure Gemini
genai.configure(api_key=api_key)

#initialize the model
model = genai.GenerativeModel("models/gemini-2.5-pro")

def chat():
    print("Welcome to the Gemini Chatbot! Type 'exit' to quit.")
    chat_session = model.start_chat()
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye! Have a great day! Hope to help you again!!")
            break
        try:
            response = chat_session.send_message(user_input)
            print("Gemini: ", response.text)
        except Exception as e:
            print("Error: ", e)

if __name__ == "__main__":
    chat()