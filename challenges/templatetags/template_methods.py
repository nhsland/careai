from django import template
from challenges.models import Challenge
from users.models import User
from users.models import Developer

register = template.Library()

@register.simple_tag()
def user_is_in_challenge(challengeid, userid):

    current_challenge = Challenge.objects.get(pk=challengeid)
    for devs in current_challenge.developers.all():
        if devs.pk == userid:
            return True
    return False