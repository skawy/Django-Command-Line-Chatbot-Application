from django.core.management.base import BaseCommand
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import uuid

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class Command(BaseCommand):
    help = 'Starting The Chatbot'
    # def add_arguments(self, parser):
    #     # Define command-line arguments here (optional)
    #     # parser.add_argument('argument_name', nargs='+', type=str, help='Help text')
    def validate_phone_number(self,phone_num):
        pattern = re.compile(r'^\+201[0125]\d{8}$')
        if re.match(pattern, phone_num):
            return True
        else:
            return False
    
    def validate_email(self,email):
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if re.match(pattern, email):
            return True
        else:
            return False

    # def add_user(self,phone,name,email,physical):

    def handle(self, *args, **kwargs):
        # Logic to execute when the command is called
        client = OpenAI()
        chat_log = [ {'role': 'system', 'content' : 'you are given the customers information and they are 1) phone 2) name 3) email'}]
        print("Hello, Can you give me your information: phone , name , email\n")
        while True:
            user_message = input("You: ")
            if user_message == "quit":

                break
            else:
                chat_log.append({"role": "user","content":user_message})

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log,
                    temperature = 0.5,
                    max_tokens = 1024
                )

                bot_response = response.choices[0].message.content
                # print(bot_response.split('\n'))
                print(bot_response.partition("Phone:")[2].split('\n')[0])
                print(bot_response.partition("Name:")[2].split('\n')[0])
                print(bot_response.partition("Email:")[2].split('\n')[0])
                print (hex(uuid.getnode()))

                self.stdout.write(
                    self.style.SUCCESS(f'ChatGPT: {bot_response}')
                    )
                chat_log.append({"role":"assistant","content":bot_response})


        # print(chat_log)
        self.stdout.write(self.style.SUCCESS('The chat finished successfully'))
        # Access command-line arguments if defined
        # argument_value = kwargs['argument_name']
        # self.stdout.write(self.style.SUCCESS(f'Argument received: {argument_value}'))

        

        