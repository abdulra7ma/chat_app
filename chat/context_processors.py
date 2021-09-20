from account.models import Friends


def friends(request):
    return {"friends":  Friends.objects.filter(user=request.user)[0].friends.all()}