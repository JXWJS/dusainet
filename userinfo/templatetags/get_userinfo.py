from django import template

from userinfo.models import UserInfo

register = template.Library()

@register.simple_tag
def get_userinfo(user_id):
    """
    获取UserInfo实例
    :param user_id: User的id
    """
    try:
        userinfo = UserInfo.objects.get(user_id=user_id)
    except:
        userinfo = None
    return userinfo