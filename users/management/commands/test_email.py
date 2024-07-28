# users/management/commands/test_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        send_mail(
            'Test Email',
            'This is a test email sent from Django.',
            'shu15131214@gmail.com',
            ['shu_1315@hotmail.com'],  # Replace with the recipient email address
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Test email sent successfully'))
