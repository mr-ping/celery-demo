"""Demonstration of celery client."""
import json

import tornado.ioloop
import tornado.web
import gevent.monkey

import tasks
gevent.monkey.patch_all()


def make_app():
    return tornado.web.Application(
        [(r"/add", AddHandler),
         (r"/multi", MultiHandler)],
        debug=True)


class AddHandler(tornado.web.RequestHandler):
    def on_result_ready(self, result):
        res = 'Received from: %r\r\nResult: %r' % (result.id, result.result,)
        self.write(res)
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        num1, num2 = self.get_query_arguments('num')
        tasks.add.delay(int(num1), int(num2)).then(self.on_result_ready)


class MultiHandler(tornado.web.RequestHandler):
    def on_result_ready(self, result):
        res = 'Received from: %r\r\nResult: %r' % (result.id, result.result,)
        self.write(res)
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        num1, num2 = self.get_query_arguments('num')
        tasks.multi.delay(int(num1), int(num2)).then(self.on_result_ready)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
