from django import template

register = template.Library()


@register.filter(name="get_last_element")
def get_last_element(string: str, splitter):
    return [word for word in string.split(splitter) if word != ""][-1]


@register.filter(name="tostring")
def tostring(obj):
    if type(obj) is list:
        return str(obj[0])
    return str(obj)
