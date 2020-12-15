from django import template

from birdspotter.accounts.models import User

register = template.Library()


# return value from dictionary as dictionary lookup cannot occur in a template
@register.filter
def get_item(dictionary, key):
    """Helper function to return value for supplied key in dictionary
    
    Args:
        dictionary (dict): The dictionary supplied by the template
        key (str): dict key                   
    
    Returns:
        any: returns any value from dictionary
    """
    return dictionary[key]


@register.filter
def get_date(dictionary, key):
    """Helper function to return date for supplied key in dictionary
    
    Args:
        dictionary (dict): Dictionary containing datetime at specified key
        key (str): dict key
    
    Returns:
        datetime.date: date component of datetime
    """
    if val := dictionary[key]:
        return val.date()
    else:
        return val


@register.filter
def get_username(dictionary, key):
    """Get's user's username for given user_id
    
    Args:
        dictionary (dict): dict with a user id
        key (str): dict key
    
    Returns:
        User: User model for supplied user_id
    """
    return User.objects.get(pk=dictionary[key])
