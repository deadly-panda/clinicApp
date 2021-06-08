from django import template

register = template.Library()
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_group_admin')
def has_group_admin(user):
    return not user.groups.filter(name='admin').exists()

@register.filter(name='has_group_doctor')
def has_group_admin(user):
    return not user.groups.filter(name='doctor').exists()

@register.filter(name='has_group_patient')
def has_group_admin(user):
    return not user.groups.filter(name='patient').exists()
