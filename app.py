from flask import Flask, request, render_template, session
import requests
import os
import re
from pdf_to_text import extract_text  # Import text extraction function
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random secret key for session management
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Set your Gemini API Key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def decode_legal_text(legal_text):
    """Simplify legal text using Mistral via Ollama."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": f"""
You are a legal assistant. Simplify the following legal text into plain, easy-to-understand language, while keeping its original meaning.

If it's in a non-English language, give the output in both English and the original language.

Also, extract any key details (names, dates, monetary values, places) and show them at the top.

Legal Text:
{legal_text}
""",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        simplified_output = response.json().get("response", "").strip()
        detected_language = "Multilingual (Original + English)" if "ENGLISH:" in simplified_output else "English"
        return simplified_output, detected_language
    except Exception as e:
        return f"Error: {str(e)}", "Unknown"
    
def ask_ollama(question, context):
    """Ask follow-up questions based on simplified legal text using Mistral."""
    url = "http://localhost:11434/api/generate"
    prompt = f"""
You are a legal assistant. Based on the following simplified legal text and previous Q&A, answer the user's question briefly and clearly.

Simplified Legal Text:
{context}

Previous Q&A:
{session.get('chat_history', '')}

Question:
{question}
"""

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    session.setdefault("chat_history", [])
    session.setdefault("simplified_text", None)
    session.setdefault("detected_language", "Unknown")

    if request.method == "POST":
        uploaded_file = request.files.get("file")
        legal_text = request.form.get("legal_text", "").strip()

        extracted_text = ""
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded_file.save(file_path)
            extracted_text = extract_text(file_path) or "Error extracting text."

        if legal_text or extracted_text:
            input_text = extracted_text if extracted_text else legal_text
            simplified_text, detected_language = decode_legal_text(input_text)
            session["simplified_text"] = simplified_text
            session["detected_language"] = detected_language
            session["chat_history"] = []  # Reset Q&A history when new text is submitted
            session.modified = True

    return render_template(
        "index.html",
        simplified_text=session.get("simplified_text", ""),
        detected_language=session.get("detected_language", "Unknown"),
        chat_history=session.get("chat_history", []),
    )

@app.route("/ask", methods=["POST"])
def ask():
    session.setdefault("chat_history", [])
    question = request.form.get("question", "").strip()
    simplified_text = session.get("simplified_text", "")

    if question and simplified_text:
        answer = ask_ollama(question, simplified_text) # Pass legal text as context
        session["chat_history"].insert(0, {"question": question, "answer": answer})  # Insert at top
        session.modified = True

    return render_template(
        "index.html",
        simplified_text=session.get("simplified_text", ""),
        detected_language=session.get("detected_language", "Unknown"),
        chat_history=session.get("chat_history", []),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

