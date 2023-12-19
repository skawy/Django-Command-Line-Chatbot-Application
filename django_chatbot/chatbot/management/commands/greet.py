from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Says Hello'

    def add_arguments(self, parser):
        # Define command-line arguments here (optional)
        parser.add_argument('argument_name', nargs='+', type=str, help='Help text')

    def handle(self, *args, **kwargs):
        # Logic to execute when the command is called
        self.stdout.write(self.style.SUCCESS('Command executed successfully!'))
        # Access command-line arguments if defined
        argument_value = kwargs['argument_name']
        self.stdout.write(self.style.SUCCESS(f'Argument received: {argument_value}'))
