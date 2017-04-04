from environment import Response
from environment import Template


def counter(session):
    count = session['count'] if 'count' in session else 1
    session['count'] = count + 1
    template = Template('templates/counter.html', {'count': count})
    message = template.get_message()
    return Response(message)


def hello(session):
    template = Template('templates/hello.html', {'name': 'Oleg'})
    message = template.get_message()
    return Response(message)


def goodbye(session):
    message = 'Goodbye World!\n'
    return Response(message)


def errors(session):
    message = '404 Not Found\n'
    return Response(message, '404 Not Found')


def contact(session):
    template = Template('templates/contact.html', {'name': 'Vasia13'})
    message = template.get_message()
    return Response(message)
