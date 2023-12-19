from django.test import TestCase
from chatbot.models import Users,Chats,Logs
# Create your tests here.
class UsersTestCase(TestCase):

    def setUp(self):
       Users.objects.create(name = "test" ,phone = "+201111111111" , email = "test@gmail.com" , physical_address = "test")

    def test_user_created(self):
        user = Users.objects.filter(email='test@gmail.com')
        self.assertTrue(user.exists())

class ChatTestCase(TestCase):

    def setUp(self):
        user = Users.objects.create(name = "test" ,phone = "+201111111111" , email = "test@gmail.com" , physical_address = "test")
        Chats.objects.create(summary = "Summary Test", active = False, user_id = user)

    def test_user_created(self):
        chat = Chats.objects.filter(summary="Summary Test")
        self.assertTrue(chat.exists())


class LogsTestCase(TestCase):

    def setUp(self):
        user = Users.objects.create(name = "test" ,phone = "+201111111111" , email = "test@gmail.com" , physical_address = "test")
        chat = Chats.objects.create(summary = "Summary Test", active = False, user_id = user)
        Logs.objects.create(message = "Message From User", response = "Response From Bot", user_id = user , chat_id = chat)

    def test_user_created(self):
        log = Logs.objects.filter(message="Message From User")
        self.assertTrue(log.exists())

