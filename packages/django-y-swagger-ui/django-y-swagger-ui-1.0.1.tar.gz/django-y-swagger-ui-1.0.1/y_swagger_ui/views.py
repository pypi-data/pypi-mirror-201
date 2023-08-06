from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ImproperlyConfigured

def swagger_ui(request):
    return render(request, template_name="y_swagger_ui/swagger_ui.html")


def openapi_spec_yaml(request):
    if not hasattr(settings, 'Y_SWAGGER_UI'):
        raise ImproperlyConfigured('You should define Y_SWAGGER_UI in your settings')

    y_swagger_ui_conf = settings.Y_SWAGGER_UI

    if 'OPENAPI_SPEC_FILE' not in y_swagger_ui_conf:
        raise ImproperlyConfigured('You should define OPENAPI_SPEC_FILE in your Y_SWAGGER_UI settings')

    file_location = y_swagger_ui_conf['OPENAPI_SPEC_FILE']
    try:
        with open(file_location, 'r') as f:
            file_data = f.read()
        # sending response 
        response = HttpResponse(file_data, content_type='application/x-yaml')
        response['Content-Disposition'] = 'attachment; filename="openapi.yaml"'
    except IOError:
        # handle file not exist case here
        response = HttpResponseNotFound()
    return response

