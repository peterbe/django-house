import re
import datetime
import functools
import json
from pipes import quote
import subprocess

from django import http


# https://github.com/erikrose/shiva/blob/master/shiva_deployer/tools.py
def run(command, **kwargs):
    """Return the output of a command, and raise CalledProcessError on failure.

Pass in any kind of shell-executable line you like, with one or more
commands, pipes, etc. Any kwargs will be shell-escaped and then subbed into
the command using ``format()``::

>>> run('echo hi')
"hi"
>>> run('echo {name}', name='Fred')
"Fred"

This is optimized for callsite readability. Internalizing ``format()``
keeps noise off the call. If you use named substitution tokens, individual
commands are almost as readable as in a raw shell script. The command
doesn't need to be read out of order, as with anonymous tokens.

"""
    return subprocess.check_output(
        command.format(**dict((k, quote(v)) for k, v in kwargs.iteritems())),
        shell=True)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def json_view(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kw):
        response = f(request, *args, **kw)
        if isinstance(response, http.HttpResponse):
            return response
        else:
            indent = 0
            if request.REQUEST.get('pretty') == 'print':
                indent = 2
            return http.HttpResponse(
                _json_clean(json.dumps(
                    response,
                    cls=DateTimeEncoder,
                    indent=indent
                )),
                content_type='application/json; charset=UTF-8'
            )
    return wrapper


def _json_clean(value):
    """JSON-encodes the given Python object."""
    # JSON permits but does not require forward slashes to be escaped.
    # This is useful when json data is emitted in a <script> tag
    # in HTML, as it prevents </script> tags from prematurely terminating
    # the javscript.  Some json libraries do this escaping by default,
    # although python's standard library does not, so we do it here.
    # http://stackoverflow.com/questions/1580647/json-why-are-forward-slashe\
    # s-escaped
    return value.replace("</", "<\\/")


def filename2title(filename):
    filename = filename.replace('_', ' ')
    filename = re.sub('\.\w{2,4}$', '', filename)
    return filename


def filename2document_type(filename):
    filename = filename.lower()
    return filename.split('.')[-1]
