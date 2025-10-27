import logging
import azure.functions as func
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xml_manager.settings_production')

import django
django.setup()

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Azure Function HTTP trigger for Django application"""
    logging.info('Python HTTP trigger function processed a request.')

    # Convert Azure Functions request to WSGI environ
    environ = {
        'REQUEST_METHOD': req.method,
        'SCRIPT_NAME': '',
        'PATH_INFO': req.url.split('?')[0].replace('/api/HttpTrigger', ''),
        'QUERY_STRING': req.url.split('?')[1] if '?' in req.url else '',
        'CONTENT_TYPE': req.headers.get('Content-Type', ''),
        'CONTENT_LENGTH': str(len(req.get_body())),
        'SERVER_NAME': req.headers.get('Host', 'localhost').split(':')[0],
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
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

    # Call Django WSGI application
    response_started = False
    status_code = 200
    headers = {}
    body = []

    def start_response(status, response_headers):
        nonlocal response_started, status_code, headers
        response_started = True
        status_code = int(status.split()[0])
        headers = dict(response_headers)
        return lambda s: body.append(s)

    # Get response from Django
    response_data = application(environ, start_response)
    for data in response_data:
        body.append(data)

    # Return Azure Functions response
    return func.HttpResponse(
        body=b''.join(body),
        status_code=status_code,
        headers=headers
    )
