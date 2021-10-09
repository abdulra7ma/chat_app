from django.contrib.auth import get_user_model
from chat.models import Message
import random


UserModel = get_user_model()


def create_user():
    number = random.randint(77, 77777)
    user_name = "user" + str(number)
    email = user_name + "@gmail.com"
    password = "djangouser" + str(number)
    UserModel.objects.create_user(email=email, username=user_name, password=password)


def test():
    message = Message.objects.all()

    if message:
        message.last().delete()
