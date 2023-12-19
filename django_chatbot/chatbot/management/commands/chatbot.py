from django.core.management.base import BaseCommand
from chatbot.models import Users,Chats,Logs

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
        if re.match(pattern, phone_num.strip()):
            return True
        else:
            return False
    
    def validate_email(self,email):
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if re.match(pattern, email.strip()):
            return True
        else:
            return False

    def add_user(self,phone,name,email,physical):
        row = Users.objects.create(
            phone = phone,
            name = name,
            email = email,
            physical_address = physical,
        )
        return row.id


    def handle(self, *args, **kwargs):
        # Logic to execute when the command is called
        client = OpenAI()
        phone = None
        name = None
        email = None
        physical_address = hex(uuid.getnode())

        customer_information_completed = False
        chat_log = [ 
            {'role': 'system', 'content' : 'you are given the customers information and they are 1) phone_number 2) name 3) email and wont continue unless you get all of them and print them'}
            ]
        print("\nHello, Can you give me your information: phone_number , name , email\n")
        while True:
            user_message = input("You: ")
            if user_message == "quit":
                # Create Summary and push it to chat db
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

                if ("Phone Number:" and "Email:" and "Name:" in bot_response):
                    # print("all data exists")
                    phone = bot_response.partition("Phone Number:")[2].split('\n')[0]
                    email = bot_response.partition("Email:")[2].split('\n')[0]
                    name = bot_response.partition("Name:")[2].split('\n')[0]
                    customer_information_completed = True

                    if not self.validate_phone_number(phone):
                        print("")
                        customer_information_completed = False
                        print(f"phone is Invalid: {phone}")

                    if not self.validate_email(email):
                        customer_information_completed = False
                        print(f"Mail is Invalid {email}")

                    if customer_information_completed:
                        # print(
                        # f'phone is {phone}, name is {name}, email is {email} , physic {physical_address}'
                        # )
                        user_id = self.add_user(phone,name,email,physical_address)
                        print(f'User Id = {user_id}')



                self.stdout.write(
                    self.style.SUCCESS(f'ChatGPT: {bot_response}')
                    )
                
                customer_information_completed = False
                chat_log.append({"role":"assistant","content":bot_response})


        # print(chat_log)
        self.stdout.write(self.style.SUCCESS('The chat finished successfully'))
        # Access command-line arguments if defined
        # argument_value = kwargs['argument_name']
        # self.stdout.write(self.style.SUCCESS(f'Argument received: {argument_value}'))

        

        