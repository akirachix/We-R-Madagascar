from django import template
from datetime import date



register = template.Library()

@register.filter(name='approve')
def approve(value, arg):
    filter1 = value.filter(status='Approved')
    count = 0
    for x in filter1:
        if x.uav_uuid.unid == arg:
            count += 1

    
    return count

@register.filter(name='pending')
def pending(value, arg):
    filter1 = value.filter(status='Pending')
    count = 0
    for x in filter1:
        if x.uav_uuid.unid == arg:
            count += 1

    
    return count

@register.filter(name='rejected')
def rejected(value, arg):
    filter1 = value.filter(status='Rejected')
    count = 0
    for x in filter1:
        if x.uav_uuid.unid == arg:
            count += 1

    
    return count