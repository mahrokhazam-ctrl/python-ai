import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Function to interact with OpenAI using the `requests` library
def generate_openai_response(PROMPT, user_query):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": user_query}
    ]
    data = {
        "model": "gpt-4o",
        "messages": messages,
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    