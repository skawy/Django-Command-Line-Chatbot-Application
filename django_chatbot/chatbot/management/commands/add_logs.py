from django.core.management.base import BaseCommand
from chatbot.models import Users,Chats,Logs
from datetime import datetime

def add_to_logs(self,message,response,time,user,chat):
    row = Logs.objects.create(
        message = message,
        response = response,
        time = time,
        user_id = user,
        chat_id = chat
    )
    return row

class Command(BaseCommand):
    help = "Try To give a summary of the customer's problem"


    def handle(self, *args, **kwargs):

        date_value = datetime.now()
        current_chat = Chats.objects.get(id = 2)
        current_user = Users.objects.get(id = 11)

        log_row = Logs.objects.create(
                message = "are you kidding  ",
                response = "i did it its just date to datetime",
                user_id = current_user,
                chat_id = current_chat
        )
        # print(type(date_value))
        # print(date_value)
        print(f"date_value ===========================================is: {date_value}")


        # logs = self.add_to_logs("ahmed","mohamed",time)
        # Logic to execute when the command is called
        self.stdout.write(self.style.SUCCESS('The chat finished successfully'))
        # Access command-line arguments if defined
        # argument_value = kwargs['argument_name']
        # self.stdout.write(self.style.SUCCESS(f'Argument received: {argument_value}'))

        

        