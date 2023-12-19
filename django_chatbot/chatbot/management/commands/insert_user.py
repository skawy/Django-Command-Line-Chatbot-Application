from django.core.management.base import BaseCommand
from chatbot.models import Users

class Command(BaseCommand):
    help = 'Try To add row to mydb'

    def add_arguments(self, parser):
        # Define command-line arguments here (optional)
        parser.add_argument('phone', nargs='+', type=int, help='')
        parser.add_argument('name', nargs='+', type=str, help='')
        parser.add_argument('email', nargs='+', type=str, help='')
        parser.add_argument('physical_address', nargs='+', type=str, help='')

    def handle(self, *args, **kwargs):
        row = Users.objects.create(
            phone = kwargs['phone'][0],
            name = kwargs['name'][0],
            email = kwargs['email'][0],
            physical_address = kwargs['physical_address'][0],

        )

        self.stdout.write(self.style.SUCCESS(f'Row added with ID: {row.id}'))

        