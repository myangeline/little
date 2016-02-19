from wsgiref.simple_server import make_server

from web.appilcation import Application

urls = (
    ('/', 'Index'),
    ('/hello/(.*)', 'Hello')
)


class Index:
    def get(self):
        Application.set_header('Content-type', 'text/plain')
        return "Welcome!\n"


class Hello:
    def get(self, name):
        Application.set_header('Content-type', 'text/plain')
        return "Hello %s!\n" % name

wsgi_app = Application(urls, globals())

if __name__ == '__main__':
    httpd = make_server('', 8080, wsgi_app)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()
