# Legal-Lens
# 🧠 LegalLens – Simplify Legal Documents Using Local LLM (Mistral via Ollama)

LegalLens is a Flask-based web app that allows users to upload legal documents in various formats (PDF, DOCX, TXT, Images, etc.), simplifies them using a local language model via [Ollama](https://ollama.com/), and supports follow-up question answering – all with multilingual support.

---

## 🚀 Features

- 🧾 Upload PDFs, DOCX, TXT, scanned images.
- 🧠 Simplifies legal jargon into plain language using **Mistral** LLM (via Ollama).
- 🌍 Multilingual support (English + regional languages).
- ❓ Ask questions based on the simplified legal content.
- 🛡️ Runs **completely offline** – no external API needed!

---

## 🛠 Setup Instructions

### 1. Install Dependencies

Install Python libraries:
```bash
pip install -r requirements.txt
```
2. Install and Set Up Ollama
Download and install Ollama from https://ollama.com/download
Then pull the Mistral model:

```bash
ollama pull mistral
```
3. Start the Ollama Service
In a new terminal:

```bash
ollama run mistral
```
This will launch the model and expose the API at http://localhost:11434.

🧪 Run the Flask App
```bash
python app.py
```
App will run at: http://localhost:5000

**Supported File Formats**

.pdf – Extracts text or uses OCR if scanned.

.docx, .doc

.txt

.png, .jpg, .jpeg, .tiff, .bmp – OCR-based text extraction.

**Technologies Used**

Python, Flask

Ollama + Mistral (local LLM)

PyMuPDF, pytesseract, python-docx

Session-based Q&A handling

**Future Enhancements**
Add support for citation tracking

Summarization confidence scoring

UI improvements for multilingual outputs
