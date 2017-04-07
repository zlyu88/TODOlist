import os
import re

from jinja2 import Environment, FileSystemLoader
from paste.session import SessionMiddleware
from wsgiref.simple_server import make_server

import views


class Template:
    def __init__(self, page, content={}):
        self.page = page
        self.content = content

    def get_message(self):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template(self.page)
        result = template.render(self.content)
        css = ''.join(('<style>\n', open('static/style.css', 'r').read(), '</style>'))
        result = re.subn("(<link[^>]+>)", css, result, 1)[0]
        js = ''.join(('<script>\n', open('static/js.js', 'r').read(), '</script>'))
        result = re.sub("(<script[^>]+>)", js, result)
        return result


class Response(object):
    def __init__(self, content='', status_code='200 OK', headers=(('Content-type', 'text/html'), )):
        self.status_code = status_code
        self.headers = list(headers)
        self.content = content.encode('utf-8')


class App:
    session = os.environ.get('paste.session.factory', lambda: {})()

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):

        self.views_mapping = {
            '/': views.counter,
            '/hello': views.hello,
            '/goodbye': views.goodbye,
            '/contact': views.contact,
            '/list': views.list,
            '/add_list': views.add_list,
        }
        path = self.environ['PATH_INFO']
        input_length = self.environ.get('CONTENT_LENGTH')
        if not input_length == '':
            input_data = self.environ['wsgi.input'].read(int(input_length))
            self.session['input_data'] = input_data.decode('utf-8').split('\r\n')[3]

        if path.startswith('/list/'):
            list_id = path.split('/')[-1]
            response = views.detail(self.session, list_id)
        elif path.startswith('/edit/list/'):
            list_id = path.split('/')[-1]
            response = views.edit_list(self.session, list_id)
        elif path.startswith('/delete/list/'):
            list_id = path.split('/')[-1]
            response = views.delete_list(self.session, list_id)
        else:
            response = self.views_mapping.get(path, views.errors)(self.session)
        yield self.get_response(response)

    def get_response(self, response):
        self.start(response.status_code, response.headers)
        return response.content

app = SessionMiddleware(App)
if __name__ == '__main__':
    httpd = make_server('localhost', 8000, app)
    print("Serving HTTP on port 8000...")
    httpd.serve_forever()
