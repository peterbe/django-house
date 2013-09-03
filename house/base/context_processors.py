from django.conf import settings


def base(request):
    context = {}
    context['page_title'] = settings.PROJECT_TITLE
    return context
