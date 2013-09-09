from django.conf import settings


def base(request):
    context = {}
    context['PROJECT_TITLE'] = settings.PROJECT_TITLE
    context['page_title'] = settings.PROJECT_TITLE  # default
    return context
