from wsgiref.simple_server import make_server
from paste.evalexception.middleware import EvalException
from paste.session import SessionMiddleware


def app(environ, start_response):
    # Except error
    if 'error' in environ['PATH_INFO'].lower():
        raise Exception('Detect "error" in URL path')

    # Session
    session = environ.get('paste.session.factory', lambda: {})()
    if 'count' in session:
        count = session['count']
    else:
        count = 1
    session['count'] = count + 1

    # Generate response
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = 'Hello World!\nYou have been here %d times!\n' % count
    return [message.encode("utf-8"), ]

app = SessionMiddleware(app)
httpd = make_server('localhost', 8888, app)
httpd.serve_forever()
app = EvalException(app)
