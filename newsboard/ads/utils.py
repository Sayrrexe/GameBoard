import random
from django.utils import timezone
from datetime import timedelta
from .models import ConfirmationCode
from django.core.mail import send_mail
from django.conf import settings

def create_confirmation_code(user):
    # Генерация нового кода подтверждения
    ConfirmationCode.objects.filter(user=user).delete()
    code = str(random.randint(100000, 999999))
    deactivation_time = timezone.now() + timedelta(minutes=15)
    confirmation = ConfirmationCode.objects.create(user=user, code=code, deactivation_time=deactivation_time)
    subject = "Ваш код подтверждения"
    message = f"Ваш код подтверждения: {code}. Он истекает через 15 минут."
    recipient_list = [user.email]
    print('Созданн код для пользователя: ',{user}, ' - ', code)
    #send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    return confirmation