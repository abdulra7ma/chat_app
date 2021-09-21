from django.http import HttpResponseRedirect
from django.urls import reverse

from account.models import Friends


def friends(request):
    if request.user.is_anonymous:
        return {"friends": ""}
    return {"friends": Friends.objects.filter(user=request.user)[0].friends.all()}
