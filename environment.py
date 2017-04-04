import os
import re
from os import environ

from jinja2 import Environment, FileSystemLoader
from paste.session import SessionMiddleware
from wsgiref.simple_server import make_server

import views


class Template:
    def __init__(self, file, content=None):
        self.file = file
        self.content = content

    def get_message(self):
        template_loader = FileSystemLoader(searchpath=os.path.dirname(__file__))
        jinja_env = Environment(loader=template_loader)
        template = jinja_env.get_template(self.file)
        body = template.render(self.content)
        css = ''.join(('<style>\n', open('static/style.css', 'r').read(), '</style>'))
        body = re.sub("(<link[^>]+>)", css, body)
        js = ''.join(('<script>\n', open('static/js.js', 'r').read(), '</script>'))
        body = re.sub("(<script[^>]+>)", js, body)
        return body


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
            '/goodbye': views.goodbye,
            '/contact': views.contact
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
