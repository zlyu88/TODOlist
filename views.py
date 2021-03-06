import os
from mimetypes import guess_type

from db_connection import get_lists, get_list_detail, create_list, destroy_list, edit_list_name
from db_connection import create_item, get_item_detail, edit_item_name, destroy_item, item_check_box
from db_connection import create_subtask, destroy_subtask
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
    template = Template('detail.html', {'list_data': data['list_data'],
                                        'items_data': data['items_data']})
    message = template.get_message()
    return Response(message)


def add_list(request_method, new_member):
    if request_method == 'POST':
        create_list(new_member, 1)  # Temporary user_id set to 1
        return list()
    elif request_method == 'GET':
        template = Template('add_list.html')
        message = template.get_message()
        return Response(message)


def edit_list(list_id, request_method, new_name):
    if request_method == 'POST':
        edit_list_name(list_id, new_name)
        return detail(list_id)
    elif request_method == 'GET':
        data = get_list_detail(list_id)
        template = Template('edit_list.html', {'data': data['list_data']})
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
            content_type = guess_type(path.split('/')[-1])[0]
            headers = [('Content-Type', content_type)]
            return Response(content, status_code='200 OK', headers=headers)


def item_detail(item_id):
    data = get_item_detail(item_id)
    template = Template('item_detail.html', {'item_data': data['item_data'],
                                             'subtask_data': data['subtask_data']})
    message = template.get_message()
    return Response(message)


def add_item(list_id, request_method, new_member):
    if request_method == 'POST':
        create_item(new_member, list_id)
        return detail(list_id)
    elif request_method == 'GET':
        template = Template('add_item.html', {'list_id': list_id})
        message = template.get_message()
        return Response(message)


def edit_item(item_id, request_method, new_name):
    if request_method == 'POST':
        edit_item_name(item_id, new_name)
        return item_detail(item_id)
    elif request_method == 'GET':
        data = get_item_detail(item_id)
        template = Template('edit_item.html', {'data': data['item_data']})
        message = template.get_message()
        return Response(message)


def delete_item(item_id, list_id):
    destroy_item(item_id)
    return detail(list_id)


def check_box(item_id, value):
    item_check_box(item_id, value)
    return item_detail(item_id)


def add_subtask(item_id, request_method, new_member):
    if request_method == 'POST':
        create_subtask(new_member, item_id)
        return item_detail(item_id)
    elif request_method == 'GET':
        template = Template('add_subtask.html', {'item_id': item_id})
        message = template.get_message()
        return Response(message)


def delete_subtask(subtask_id, item_id):
    destroy_subtask(subtask_id)
    return item_detail(item_id)
