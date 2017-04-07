from db_connection import get_lists, get_list_detail, create_list, destroy_list, edit_list_name
from environment import Response
from environment import Template


def counter(session):
    count = session['count'] if 'count' in session else 1
    session['count'] = count + 1
    template = Template('counter.html', {'count': count})
    message = template.get_message()
    return Response(message)


def hello(session):
    template = Template('hello.html', {'name': 'Oleg'})
    message = template.get_message()
    return Response(message)


def goodbye(session):
    message = 'Goodbye World!\n'
    return Response(message)


def errors(session):
    message = '404 Not Found\n'
    return Response(message, '404 Not Found')


def contact(session):
    template = Template('contact.html', {'name': 'Vasia13'})
    message = template.get_message()
    return Response(message)


def list(session):
    data = get_lists()
    template = Template('list.html', {'lists': data})
    message = template.get_message()
    return Response(message)


def detail(session, list_id):
    data = get_list_detail(list_id)
    template = Template('detail.html', {'data': data[0]})
    message = template.get_message()
    return Response(message)


def add_list(session):
    try:
        session['input_data']
        create_list(session['input_data'], 1)  # Temporary user_id set to 1
        del session['input_data']
        return list(session)
    except KeyError:
        template = Template('add_list.html')
        message = template.get_message()
        return Response(message)


def edit_list(session, list_id):
    try:
        session['input_data']
        edit_list_name(list_id, session['input_data'])
        del session['input_data']
        return detail(session, list_id)
    except KeyError:
        data = get_list_detail(list_id)
        template = Template('edit_list.html', {'data': data[0]})
        message = template.get_message()
        return Response(message)


def delete_list(session, list_id):
    destroy_list(list_id)
    return list(session)
