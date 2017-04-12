import fnmatch
import os

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
        # Get form input data
        path = self.environ['PATH_INFO']
        input_length = self.environ.get('CONTENT_LENGTH')
        if not input_length == '':
            input_data = self.environ['wsgi.input'].read(int(input_length))
            self.session['input_data'] = input_data.decode('utf-8').split('\r\n')[3]

        # Create urls routes
        self.views_mapping = [('/static/*', views.make_static_application, '/static/', 'static', self.environ),
                              ('/', views.counter, self.session),
                              ('/hello', views.hello),
                              ('/goodbye', views.goodbye),
                              ('/contact', views.contact),
                              ('/list', views.list),
                              ('/add_list', views.add_list, self.session),
                              ('/list/detail/*', views.detail, path.split('/')[-1]),
                              ('/list/edit/*', views.edit_list, self.session, path.split('/')[-1]),
                              ('/list/delete/*', views.delete_list, path.split('/')[-1]),
                              ('/list/*/add_item', views.add_item, self.session, path.split('/')[-2]),
                              ('/item/detail/*', views.item_detail, path.split('/')[-1]),
                              ('/item/edit/*', views.edit_item, self.session, path.split('/')[-1]),
                              ('/item/delete/*', views.delete_item, path.split('/')[-1], path.split('/')[-2]),
                              ('/check-box/*', views.check_box, path.split('/')[-2], path.split('/')[-1]),
                              ]

        # Check urls
        def url_checker():
            for path, view, *args in self.views_mapping:
                if fnmatch.fnmatch(self.environ['PATH_INFO'], path):
                    response = view(*args)
                    return self.get_response(response)
            response = views.errors()
            return self.get_response(response)
        yield url_checker()

    def get_response(self, response):
        self.start(response.status_code, response.headers)
        return response.content

app = SessionMiddleware(App)
if __name__ == '__main__':
    httpd = make_server('localhost', 8000, app)
    print("Serving HTTP on port 8000...")
    httpd.serve_forever()
