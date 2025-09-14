import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def test_openai():
    if not openai.api_key:
        return "No API key found."

    try:
        response = openai.chat_completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Can you help me?"}
            ],
            temperature=0.7,
            max_tokens=200
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(test_openai())
