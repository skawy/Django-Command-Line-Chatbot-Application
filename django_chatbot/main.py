import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# assistant = client.beta.assistants.create(
#     name="Math Tutor",
#     instructions="You are a personal math tutor. Write and run code to answer math questions.",
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-3.5-turbo-1106"
# )
# thread = client.beta.threads.create()
# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
# )
# run = client.beta.threads.runs.create(
#   thread_id=thread.id,
#   assistant_id=assistant.id,
#   instructions="Please address the user as Jane Doe. The user has a premium account."
# )
# run = client.beta.threads.runs.retrieve(
#   thread_id=thread.id,
#   run_id=run.id
# )
# messages = client.beta.threads.messages.list(
#   thread_id=thread.id
# )

# print(messages)
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
        print(f'AI: {assistant_response}')
        chat_log.append({"role":"assistant","content":assistant_response})


print(chat_log)