from django import template
from birdspotter.accounts.models import User

register = template.Library()

# return value from dictionary as dictionary lookup cannot occur in a template
@register.filter
def get_item(dictionary, key):
	return dictionary[key]

# return date component of datetime
@register.filter
def get_date(dictionary, key):
	if val := dictionary[key]:
		return val.date()
	else:
		return val

# get user_name for specified user _id
@register.filter
def get_username(dictionary, key):
	return User.objects.get(pk=dictionary[key])