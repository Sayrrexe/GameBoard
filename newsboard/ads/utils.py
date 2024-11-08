import logging

from random import randint
from django.utils import timezone
from datetime import timedelta
from .models import ConfirmationCode
from django.core.mail import send_mail

def create_confirmation_code(user):
    # Генерация нового кода подтверждения
    ConfirmationCode.objects.filter(user=user).delete()
    code = str(randint(100000, 999999))
    deactivation_time = timezone.now() + timedelta(minutes=15)
    confirmation = ConfirmationCode.objects.create(user=user, code=code, deactivation_time=deactivation_time)
    
    # отправка сообщения с кодом
    try:
        send_mail(
                subject='Ваш код',
                message=f'Ваш код подтверждения: {code}. Он истекает через 15 минут!',
                from_email=None,  
                recipient_list=[user.email],
            )
        return True
    except Exception as e: 
        logging.error(f"Ошибка отправки письма для пользователя {user.id}: {e}")
        return False
    