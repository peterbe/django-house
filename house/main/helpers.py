from django.db.utils import IntegrityError
from django.template.defaultfilters import filesizeformat
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


DOCUMENT_ICONS = {
    'default': {
        'src': 'main/images/icons/default.png',
        'size': '32x32',
    },
    'pdf': {
        'src': 'main/images/icons/pdf.png',
        'size': '32x32',
    },
    'jpg': {
        'src': 'main/images/icons/jpg.png',
        'size': '30x32',
    },
    'png': {
        'src': 'main/images/icons/png.png',
        'size': '30x32',
    },
    'txt': {
        'src': 'main/images/icons/txt.png',
        'size': '32x32',
    },
    'xls': {
        'src': 'main/images/icons/excel.png',
        'size': '32x32',
    },
    'doc': {
        'src': 'main/images/icons/word.png',
        'size': '32x32',
    },
}
for k, v in DOCUMENT_ICONS.items():
    v['width'] = v['size'].split('x')[0]
    v['height'] = v['size'].split('x')[1]

DOCUMENT_ICON_ALIASES = {
    'jpeg': 'jpg',
    'xlsx': 'xls',
    'csv': 'xls',
    'docx': 'doc',
}

@register.function
def document_icon(document_type):
    if not document_type:
        return DOCUMENT_ICONS['default']
    document_type = document_type.lower()
    if document_type not in DOCUMENT_ICONS and document_type in DOCUMENT_ICON_ALIASES:
        document_type = DOCUMENT_ICON_ALIASES[document_type]
    if document_type in DOCUMENT_ICONS:
        return DOCUMENT_ICONS[document_type]
    return DOCUMENT_ICONS['default']


@register.function
def plain_text_extract(text, max_length=100):
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text


@register.function
def file_size(bytes):
    return filesizeformat(bytes)
