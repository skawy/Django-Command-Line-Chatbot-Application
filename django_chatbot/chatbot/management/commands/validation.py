from django.core.management.base import BaseCommand
import re

class Command(BaseCommand):
    help = 'Validating phone and email'

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

    def add_arguments(self, parser):
        # Define command-line arguments here (optional)
        parser.add_argument('phone_number', nargs='+', type=str, help='')
        parser.add_argument('email', nargs='+', type=str, help='')

    def handle(self, *args, **kwargs):

        phone_number = kwargs['phone_number'][0]
        
        if self.validate_phone_number(phone_number):
            self.stdout.write(self.style.SUCCESS(f'This Phone Number Is valid'))

        email = kwargs['email'][0]
        
        if self.validate_email(email):
            self.stdout.write(self.style.SUCCESS(f'This Email Is valid'))



        