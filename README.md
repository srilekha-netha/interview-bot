# 🤖 Interview Bot

An **AI-powered Interview Assistant** built using **Streamlit** that automates and enhances the interview process by combining **resume parsing**, **personalized question generation**, **AI-driven interview sessions**, and an **HR FAQ chatbot**.

This project demonstrates the practical application of **Generative AI**, **NLP**, and **multimodal interaction** (text, audio, and video) in real-world hiring workflows.

---

## Features

### 📄 Resume Upload
- Upload **PDF/DOCX resumes**
- Extracts text using `docx2txt` / `pdfminer`
- Automatically generates personalized interview questions

### 🎥 AI Interview
- AI reads out interview questions using **Text-to-Speech (gTTS)**
- Candidate answers via **live video recording**
- **Timer countdown** for each question
- Automatic navigation between questions
- End interview with a summary

### 💬 FAQ Bot
- HR FAQ chatbot trained from `data/hr_faq.txt`
- Answers common HR-related questions instantly

---

## 🖥️ Application Workflow
<img width="355" height="331" alt="image" src="https://github.com/user-attachments/assets/43becd9a-9b3e-403c-ac16-c266e2266412" />

---

## Tech Stack

- **Python**
- **Streamlit** – Web application framework
- **NLP Libraries** – Resume text extraction
- **gTTS (Google Text-to-Speech)** – Audio-based interview questions
- **Video Recording (Browser-based)** – Candidate responses
- **LLM / GenAI** – Question generation and reasoning

---

## 📁 Project Structure
  <img width="636" height="433" alt="image" src="https://github.com/user-attachments/assets/be416a26-fe7e-4264-9e2d-1b058d334157" />

---

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Interview-Bot.git
   cd Interview-Bot

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    
3. **Run the application**
```bash
streamlit run app.py

