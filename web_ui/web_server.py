import logging
from multiprocessing import Process
from contextlib import contextmanager
from pkg_resources import resource_filename

from jeeves_commons.storage.storage import get_storage_client
from jeeves_commons.utils import which


import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options
from tornado.process import Subprocess

SOCKET_TAIL_SCRIPT = resource_filename('web_ui.resources', 'sock_listener.py')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = {}
    minion_sockets = {}
    curr_data = {}

    def __init__(self, *args, **kwargs):
        self.task_id = None
        super(SocketHandler, self).__init__(*args, **kwargs)

    def send_to_all(self, message):
        self._update_task(message)
        for c in SocketHandler.clients.get(self.task_id):
            c.write_message(message)

    def open(self, task_id):
        self.task_id = task_id
        self._add_client()
        if not SocketHandler.minion_sockets.get(task_id):
            task = get_storage_client().tasks.get(task_id)
            self._start_data_stream(task.minion_ip, task.workflow_id)
        else:
            data = SocketHandler.curr_data.get(task_id, '')
            self.write_line_to_client(data=data)

    def _add_client(self):
        clients = SocketHandler.clients.get(self.task_id, set())
        clients.add(self)
        SocketHandler.clients[self.task_id] = clients

    def _remove_client(self):
        clients = SocketHandler.clients.get(self.task_id)
        clients.remove(self)
        SocketHandler.clients[self.task_id] = clients

    def _add_proc(self, proc):
        SocketHandler.minion_sockets[self.task_id] = proc

    def _update_task(self, message):
        data = SocketHandler.curr_data.get(self.task_id, '')
        data += message
        SocketHandler.curr_data[self.task_id] = data

    def _remove_proc(self):
        proc = SocketHandler.minion_sockets.get(self.task_id)
        if proc:
            proc.proc.terminate()
            proc.proc.wait()
        SocketHandler.minion_sockets[self.task_id] = None

    def _start_data_stream(self, minion_ip, workflow_id):
        sock_path = "ws://{0}:7777/tail/{1}/{2}".format(minion_ip,
                                                        workflow_id,
                                                        self.task_id)
        tail_proc = Subprocess(
            [which('python'), SOCKET_TAIL_SCRIPT, sock_path],
            stdout=Subprocess.STREAM,
            bufsize=1)
        self._add_proc(tail_proc)
        tail_proc.set_exit_callback(self.on_close)
        tail_proc.stdout.read_until('\n', self.write_line_to_clients)

    def on_close(self, *args, **kwargs):
        self._remove_client()
        if len(SocketHandler.clients.get(self.task_id)) == 0:
            logging.info('All clients disconnected. Killing tail process for '
                         'task {0}'.format(self.task_id))
            self._remove_proc()
            self._update_task('')

    def write_line_to_clients(self, data):
        logging.info("Returning to clients: %s" % data.strip())
        self.send_to_all(data.strip())
        tail_proc = SocketHandler.minion_sockets.get(self.task_id)
        tail_proc.stdout.read_until('\n', self.write_line_to_clients)

    def write_line_to_client(self, data):
        logging.info("Returning to client: %s" % data.strip())
        self.write_message(data.strip())


class LogStreamHttpServer(object):

    def __init__(self):
        self.tornado_proc = None

    @staticmethod
    def _start_tornado_instance(port):
        app = tornado.web.Application(
            handlers=[(r'/', IndexHandler),
                      (r'/tail/(.*)', SocketHandler)],
            template_path=resource_filename('web_ui', 'resources'),
            static_path=resource_filename('web_ui.resources', 'static')
        )
        # define('port',
        #        default=self.port,
        #        help='Run server on port {}'.format(self.port),
        #        type=int)
        server = tornado.httpserver.HTTPServer(app)
        tornado.options.parse_command_line()
        server.listen(port, address='0.0.0.0')
        logging.info('Execution logs available at http://localhost:{}/tail'
                     .format(port))
        tornado.ioloop.IOLoop.instance().start()

    @contextmanager
    def with_start(self, port):

        self.tornado_proc = Process(target=self._start_tornado_instance,
                                    args=[port])
        try:
            self.tornado_proc.start()
            yield self
        finally:
            self._close()

    def start(self, port):
        self.tornado_proc = Process(target=self._start_tornado_instance,
                                    args=[port])
        self.tornado_proc.start()

    def _join(self):
        self.tornado_proc.join()

    def _close(self):
        self.tornado_proc.terminate()


streamer = LogStreamHttpServer()

#
# if __name__ == '__main__':
#     with streamer.with_start(7778) as stream:
#         stream._join()
