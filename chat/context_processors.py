from django.urls import reverse

from account.models import Friends


def friends(request):
    if request.user.is_anonymous:
        return {"friends": None}

    freinds_list = Friends.objects.filter(user=request.user)

    if freinds_list:
        return {"friends": freinds_list[0].friends.all()}
    else:
        return {"friends": freinds_list}
