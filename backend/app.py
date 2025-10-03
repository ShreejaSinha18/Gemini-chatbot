from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-pro")
app = Flask(__name__)
CORS(app)

engine = create_engine('sqlite:///chatbot.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    message = Column(Text)
    reply = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

def get_gemini_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")
    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400

    reply = get_gemini_response(message)

    session = Session()
    chat = Chat(user_id=user_id, message=message, reply=reply)
    session.add(chat)
    session.commit()
    session.close()

    return jsonify({"reply": reply})

@app.route('/history/<user_id>', methods=['GET'])
def history(user_id):
    session = Session()
    chats = session.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.timestamp).all()
    session.close()
    history = [{"message": c.message, "reply": c.reply, "timestamp": c.timestamp.isoformat()} for c in chats]
    return jsonify({"history": history})

if __name__ == "__main__":
    app.run(debug=True)