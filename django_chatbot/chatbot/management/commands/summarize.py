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
    help = "Try To give a summary of the customer's problem"

    def add_to_logs(self,message,response,log_time , user_id,chat_id):
        row = Logs.objects.create(
            message = message,
            response = response,
            log_time = log_time,
            user_id = user_id,
            chat_id = chat_id
        )
        return row.id
        
    def add_chat(self,summary,user_id,active):
        row = Chats.objects.create(
            summary = summary,
            user_id = user_id,
            active = active
        )
        return row.id
        
    def add_user(self,phone,name,email,physical):
        row = Users.objects.create(
            phone = phone,
            name = name,
            email = email,
            physical_address = physical
        )
        return row.id

    
    def handle(self, *args, **kwargs):
        # Logic to execute when the command is called
        client = OpenAI()

        goodbyes = ["bye" , "goodbye" , "quit" ,"exit"]
        chat_log = [ 
            {
            'role': 'system',
            'content' : 'You will be provided with the customer complain, your task is to listen and try to solve his problem'
            }
        ]
        user_instance = Users.objects.get(id = 7)
        user_instance.name = "SkawY"
        user_instance.save()

        print("\nHello, Customer How can i help you`\n")
        while True:
            user_message = input("You: ")
            # End Of The Conversation And Get The Summary
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
                    max_tokens = 200,
                    top_p=1
                )
                self.stdout.write(
                self.style.SUCCESS(f'AI: {response.choices[0].message.content}')
                )
                break

            else:
                chat_log.append({"role": "user","content":user_message})

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log,
                    temperature = 0.7,
                    max_tokens = 64,
                    top_p=1
                )

                bot_response = response.choices[0].message.content

               

                self.stdout.write(
                    self.style.SUCCESS(f'AI: {bot_response}')
                    )
                
                customer_information_completed = False
                chat_log.append({"role":"assistant","content":bot_response})


        # print(chat_log)
        self.stdout.write(self.style.SUCCESS('The chat finished successfully'))
        # Access command-line arguments if defined
        # argument_value = kwargs['argument_name']
        # self.stdout.write(self.style.SUCCESS(f'Argument received: {argument_value}'))

        

        