from wsgiref.simple_server import make_server

import re


class Application:
    headers = []

    def __init__(self, urls=(), func_vars=None):
        self._urls = urls
        if func_vars is None:
            func_vars = {}
        self._func_vars = func_vars
        self._status = '200 OK'
        self._encoding = 'utf-8'

    # def __iter__(self):
    #     result = self.delegate()
    #     self.start(self.status, self._headers)
    #
    #     if isinstance(result, str):
    #         result = result.encode(self.encoding)
    #     return iter([result])

    def __call__(self, environ, start_response):
        del self.headers[:]
        result = self._delegate(environ)
        start_response(self._status, self.headers)

        if isinstance(result, str):
            result = result.encode(self._encoding)
        return iter([result])

    def _delegate(self, environ):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        for pattern, name in self._urls:
            m = re.match('^'+pattern+'$', path)
            if m:
                args = m.groups()
                # 这里方法名小写,大写不符合pep8规范
                func_name = method.lower()
                # 根据字符串去查找类对象,如果查找到则继续找他的属性方法
                cls = self._func_vars.get(name)
                if hasattr(cls, func_name):
                    func = getattr(cls, func_name)
                    return func(cls(), *args)
        return self._not_found()

    @classmethod
    def set_header(cls, name, value):
        cls.headers.append((name, value))

    def get_index(self):
        self.set_header('Content-type', 'text/plain')
        return "Welcome!\n"

    def get_hello(self, name):
        self.set_header('Content-type', 'text/plain')
        return "Hello, %s!\n" % name

    def _not_found(self):
        self._status = '404 Not Found'
        self.set_header('Content-type', 'text/plain')
        return "Not Found\n"

if __name__ == '__main__':
    # httpd = make_server('', 8080, demo_app)
    # httpd = make_server('', 8080, simple_app)
    httpd = make_server('', 8080, Application)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()
    pass
