from django.core.management.base import BaseCommand
from chatbot.models import Users,Chats,Logs
import os ,re , uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
goodbyes = ["bye" , "goodbye" , "quit" ,"exit"]


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

    def add_user_to_db(self,phone,name,email,physical):
        row = Users.objects.create(
            phone = phone,
            name = name,
            email = email,
            physical_address = physical,
        )
        return row


    def customer_information_validation(self,response):
        phone = None
        name = None
        email = None
        physical_address = None
        user = None
        customer_information_valid = False

        if ("Phone Number:" and "Email:" and "Name:" and "Physical Address:"in response):
            phone = response.partition("Phone Number:")[2].split('\n')[0]
            email = response.partition("Email:")[2].split('\n')[0]
            name = response.partition("Name:")[2].split('\n')[0]
            physical_address = response.partition("Physical Address:")[2].split('\n')[0]
            customer_information_valid = True
            

            if not self.validate_phone_number(phone):
                print("")
                customer_information_valid = False
                print(f"phone is Invalid: {phone}")

            if not self.validate_email(email):
                customer_information_valid = False
                print(f"Mail is Invalid {email}")

            if customer_information_valid:
                user = self.add_user_to_db(phone,name,email,physical_address)
                # print(f'User Id = {user.id}')
        
        return user 

    def add_to_logs(self,message,response,user,chat):
        log = Logs.objects.create(
                message = message,
                response = response,
                user_id = user,
                chat_id = chat
        )
        return log
    
    def handle(self, *args, **kwargs):
        # First Get The Customer Information To Start The Chat
        client = OpenAI()

        chat_log = [ 
            {
                'role': 'system', 
                'content' : 'you are given the customers information and they are 1) phone_number 2) name 3) email 4)physical_address and wont continue unless you get all of them and print them'
            }
        ]

        print("\nHello, Can you give me your information: Phone Number , Name , Email and Physical address")
        while True:
            print("\n")
            user_message = input("You: ")
            print("\n")
            chat_log.append({"role": "user","content":user_message})
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_log,
                temperature = 0.5,
                max_tokens = 1024
            )
            bot_response = response.choices[0].message.content

            user = self.customer_information_validation(bot_response)
            self.stdout.write(self.style.SUCCESS(f'AI: {bot_response}')  )
            chat_log.append({"role":"assistant","content":bot_response})

            if user is not None:
                break

        # ===============================================================#
        # Second Start The Complaint Chat Bot And Summarize It In The End
        chat_log = [ 
            {
            'role': 'system',
            'content' : 'You will be provided with the customer complaint, your task is to listen and try to solve his problem'
            }
        ]
        chat_instance =  Chats()
        chat_instance.user_id = user
        chat_instance.active = True
        chat_instance.save()
        chat_id = chat_instance.id
        

        while True:
            print("\n")
            user_message = input("You: ")
            print("\n")
            # If User Says Bye it will be the End Of The Conversation And Get The Summary
            if any(word in user_message.lower() for word in goodbyes):

                chat_log.append( 
                    {'role': 'system',
                    'content' : 'Till now you provided with the customer`s problem, your task is to Provide a brief summary of this customer`s problem'
                    }
                )
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log,
                    temperature = 0.7,
                    max_tokens = 512,
                    top_p=1
                )
                summary = response.choices[0].message.content
                self.stdout.write(self.style.SUCCESS(f'This Complaint Summary: {summary}') )
                self.stdout.write(self.style.SUCCESS(f"This Chat ID = {chat_id}") )

                current_chat = Chats.objects.get(id = chat_id)
                current_chat.summary = summary
                current_chat.save()
                break
            # Else You are resuming chatting with the bot
            else:
                chat_log.append({"role": "user","content":user_message})

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log,
                    temperature = 0.7,
                    max_tokens = 256,
                    top_p=1
                )

                bot_response = response.choices[0].message.content

                self.stdout.write(
                    self.style.SUCCESS(f'AI: {bot_response}')
                    )
                log = self.add_to_logs(user_message , bot_response ,user,chat_instance)
                chat_log.append({"role":"assistant","content":bot_response})


        # print(f"The Full Final Log is {chat_log}")
        self.stdout.write(self.style.SUCCESS('The Conversation Has Ended Successfully'))
        

        