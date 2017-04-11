import os

from db_connection import get_lists, get_list_detail, create_list, destroy_list, edit_list_name
from environment import Response
from environment import Template


def counter(session):
    count = session['count'] if 'count' in session else 1
    session['count'] = count + 1
    template = Template('counter.html', {'count': count})
    message = template.get_message()
    return Response(message)


def hello():
    template = Template('hello.html', {'name': 'Oleg'})
    message = template.get_message()
    return Response(message)


def goodbye():
    message = 'Goodbye World!\n'
    return Response(message)


def errors():
    message = '404 Not Found\n'
    return Response(message, '404 Not Found')


def contact():
    template = Template('contact.html', {'name': 'Vasia13'})
    message = template.get_message()
    return Response(message)


def list():
    data = get_lists()
    template = Template('list.html', {'lists': data})
    message = template.get_message()
    return Response(message)


def detail(list_id):
    data = get_list_detail(list_id)
    template = Template('detail.html', {'data': data[0]})
    message = template.get_message()
    return Response(message)


def add_list(session):
    try:
        session['input_data']
        create_list(session['input_data'], 1)  # Temporary user_id set to 1
        del session['input_data']
        return list()
    except KeyError:
        template = Template('add_list.html')
        message = template.get_message()
        return Response(message)


def edit_list(session, list_id):
    try:
        session['input_data']
        edit_list_name(list_id, session['input_data'])
        del session['input_data']
        return detail(list_id)
    except KeyError:
        data = get_list_detail(list_id)
        template = Template('edit_list.html', {'data': data[0]})
        message = template.get_message()
        return Response(message)


def delete_list(list_id):
    destroy_list(list_id)
    return list()


def make_static_application(basepath, staticdir, environ):
    path = environ['PATH_INFO']
    if path.startswith(basepath):
        path = path[len(basepath):]
        path = os.path.join(staticdir, path)
        if os.path.exists(path):
            h = open(path, 'r')
            content = h.read()
            h.close()
            headers = [('Content-Type', content_type(path))]
            return Response(content, status_code='200 OK', headers=headers)


def content_type(path):
    if path.endswith(".css"):
        return "text/css"
    elif path.endswith(".html"):
        return "text/html"
    elif path.endswith(".jpg"):
        return "image/jpeg"
    elif path.endswith(".js"):
        return "text/javascript"
    else:
        return "application/octet-stream"
