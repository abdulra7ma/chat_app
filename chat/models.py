from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import ThreadManager

USER = get_user_model()


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]


class Chat(TrackingModel):
    THREAD_TYPE = (("personal", "Personal"), ("group", "Group"))

    name = models.CharField(max_length=50, null=True, blank=True)
    users = models.ManyToManyField("account.Account")
    chat_type = models.CharField(max_length=15, choices=THREAD_TYPE, default="group")

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.chat_type == "personal" and self.users.count() == 2:
            return f"{self.users.first()} and {self.users.last()}"
        return f"{self.name}"


class Message(TrackingModel):
    thread = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)
    message_content = models.TextField(max_length=500)  # what length you want
    is_readed = models.BooleanField(_("Readed"), default=False)

    def __str__(self):
        return self.message_content
