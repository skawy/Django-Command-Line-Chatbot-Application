import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()
chat_log = []

while True:
    user_message = input()
    if user_message == "quit":
        break
    else:
        chat_log.append({"role": "user","content":user_message})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )
        assistant_response = response.choices[0].message.content
        print(f'ChatGPT: {assistant_response}')
        chat_log.append({"role":"assistant","content":assistant_response})


print(chat_log)