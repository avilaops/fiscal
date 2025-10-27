"""
Azure Functions entry point for Django application
"""
import azure.functions as func
import logging
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xml_manager.settings_production')

import django
django.setup()

from django.core.handlers.wsgi import WSGIHandler

# Create Django WSGI application
django_app = WSGIHandler()

app = func.FunctionApp()

@app.function_name(name="HttpTrigger")
@app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main HTTP trigger that routes all requests to Django
    """
    logging.info(f'Python HTTP trigger function processed request: {req.method} {req.url}')

    # Prepare WSGI environ
    environ = {
        'REQUEST_METHOD': req.method,
        'SCRIPT_NAME': '',
        'PATH_INFO': '/' + (req.route_params.get('route') or ''),
        'QUERY_STRING': req.url.split('?')[1] if '?' in req.url else '',
        'CONTENT_TYPE': req.headers.get('Content-Type', ''),
        'CONTENT_LENGTH': str(len(req.get_body())),
        'SERVER_NAME': req.headers.get('Host', 'localhost'),
        'SERVER_PORT': '443' if req.url.startswith('https') else '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https' if req.url.startswith('https') else 'http',
        'wsgi.input': req.get_body(),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }

    # Add HTTP headers
    for key, value in req.headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value

    # Call Django
    response_data = []
    response_status = [200]
    response_headers = []

    def start_response(status, headers):
        response_status[0] = int(status.split()[0])
        response_headers.extend(headers)
        return response_data.append

    try:
        result = django_app(environ, start_response)
        for data in result:
            response_data.append(data)

        body = b''.join(response_data)

        # Create response
        headers = {key: value for key, value in response_headers}
        return func.HttpResponse(
            body=body,
            status_code=response_status[0],
            headers=headers
        )
    except Exception as e:
        logging.error(f'Error processing request: {str(e)}', exc_info=True)
        return func.HttpResponse(
            f"Internal Server Error: {str(e)}",
            status_code=500
        )
