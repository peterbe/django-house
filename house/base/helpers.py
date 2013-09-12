import jinja2
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.loader import render_to_string

from jingo import register


@register.function
def static(path):
    return staticfiles_storage.url(path)


@register.function
def pureform(form, **kwargs):
    context = dict(kwargs, form=form)
    return jinja2.Markup(
        render_to_string('_pureform.html', context)
    )


@register.filter
def js_date(dt, format='ddd, MMM D, YYYY, h:mma UTCZZ', enable_timeago=True,
            autoupdate=False):
    """ Python datetime to a time tag with JS Date.parse-parseable format. """
    dt_date = dt.strftime('%m/%d/%Y')
    dt_time = dt.strftime('%H:%M')
    dt_tz = dt.tzname() or 'UTC'
    formatted_datetime = ' '.join([dt_date, dt_time, dt_tz])
    class_ = 'timeago ' if enable_timeago else ''
    if autoupdate:
        class_ += 'autoupdate '
    return jinja2.Markup('<time datetime="%s" class="%sjstime"'
                         ' data-format="%s">%s</time>'
                         % (dt.isoformat(), class_,
                            format, formatted_datetime))
