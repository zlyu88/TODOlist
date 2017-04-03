from os import environ

from paste.session import SessionMiddleware
from wsgiref.simple_server import make_server

import views


class Response(object):
    def __init__(self, content='', status_code='200 OK', headers=(('Content-type', 'text/html'), )):
        self.status_code = status_code
        self.headers = list(headers)
        self.content = content.encode('utf-8')


class App:
    session = environ.get('paste.session.factory', lambda: {})()

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):

        self.views_mapping = {
            '/': views.counter,
            '/hello': views.hello,
            '/goodbye': views.goodbye
        }

        response = self.views_mapping.get(self.environ['PATH_INFO'], views.errors)(self.session)
        yield self.get_response(response)

    def get_response(self, response):
        self.start(response.status_code, response.headers)
        return response.content

app = SessionMiddleware(App)
if __name__ == '__main__':
    httpd = make_server('localhost', 8000, app)
    print("Serving HTTP on port 8000...")
    httpd.serve_forever()
