from django import template

register = template.Library()

# 将新浪微博返回的http头像转换为https
@register.simple_tag
def translate_avatar_ssl(avatar_url):
    avatar_url_ssl = avatar_url.replace('http', 'https')
    return avatar_url_ssl