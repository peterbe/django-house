import jinja2
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.loader import render_to_string

from jingo import register


@register.function
def static(path):
    return staticfiles_storage.url(path)


@register.function
def pureform(form):
    context = {'form': form}
    return jinja2.Markup(
        render_to_string('_pureform.html', context)
    )
