from django.db.utils import IntegrityError
from sorl.thumbnail import get_thumbnail
from jingo import register


@register.function
def thumbnail(filename, geometry, **options):
    try:
        return get_thumbnail(filename, geometry, **options)
    except IOError:
        return None
    except IntegrityError:
        # annoyingly, this happens sometimes because kvstore in sorl
        # doesn't check before writing properly
        # try again
        time.sleep(1)
        return thumbnail(filename, geometry, **options)
