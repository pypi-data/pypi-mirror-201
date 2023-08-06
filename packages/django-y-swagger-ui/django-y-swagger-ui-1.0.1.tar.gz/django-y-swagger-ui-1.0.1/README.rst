============
Y-SWAGGER-UI
============

Y-SWAGGER-UI is a Django app to show swagger ui for your API. 

Use swagger-ui v4.18.2 https://github.com/swagger-api/swagger-ui/releases/tag/v4.18.2

Quick start
-----------

1. Add "y-swagger-ui" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "y_swagger_ui",
    ]

2. Configure Y_SWAGGER_UI in settings.py. You can use openapi_spec_example.yaml in repository root dir as an example. For OpenAPI specification, see https://swagger.io/specification/::

    Y_SWAGGER_UI = {
        'OPENAPI_SPEC_FILE': BASE_DIR / 'openapi_spec.yaml'      # OpenAPI spec yaml file
    }

3. Include the URLconf in your project urls.py like this::

    path("api/", include("y_swagger_ui.urls")),


4. Start the development server and visit http://127.0.0.1:8000/api/swagger_ui.html
