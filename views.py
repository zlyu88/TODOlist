from environment import Response


def counter(session):
    count = session['count'] if 'count' in session else 1
    session['count'] = count + 1
    return Response('Counter: %d\n' % count)


def hello(session):
    message = 'Hello World!\n'
    return Response(message)


def goodbye(session):
    message = 'Goodbye World!\n'
    return Response(message)


def errors(session):
    message = '404 Not Found\n'
    return Response(message, '404 Not Found')
