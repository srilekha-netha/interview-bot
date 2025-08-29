# 🤖 Interview Bot

An AI-powered **Interview Assistant** built with **Streamlit**, designed to:
- Parse resumes and extract key information
- Generate personalized interview questions
- Conduct **video interview sessions** with AI-powered audio question prompts
- Provide an **HR FAQ chatbot** for quick answers

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


