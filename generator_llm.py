import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_answer(question):
    response = client.chat.completions.create(
        model=os.getenv("MODEL1"),
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Answer the question concisely in less than 50 words"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature= 0.2
    )
    return response.choices[0].message.content