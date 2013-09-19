import re
from jingo import register


@register.filter
def obfuscate_email(email):
    return re.sub('\w{2}(\w)@(\w)\w{2}', r'..\1@\2..', email)
