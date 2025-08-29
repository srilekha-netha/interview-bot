import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def generate_questions(resume_text: str):
    prompt = f"""
    Based on the following resume, generate 5 HR-style interview questions.
    Return them as a simple numbered list (1., 2., 3., ...).

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    # Split by line, remove empty strings and leading numbers
    questions = []
    for line in content.split("\n"):
        q = line.strip(" .-0123456789")
        if q:
            questions.append(q)

    return questions
