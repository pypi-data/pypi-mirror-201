import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from time import sleep


SERVER_PORT = os.getenv('SERVER_PORT', 8000)
SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
ENABLED = os.getenv('ENABLED', False)


class StreamHandler(BaseHTTPRequestHandler):
    consumers = {}

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        path = self.path
        print(f"Path: {path}")

    def do_GET(self):
        # get path
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "status": "OK",
                        "time": datetime.now().isoformat(),
                        "topics": TestServer.topics
                    }
                ).encode('utf-8')
            )
            return
        # self.send_response(200)
        # self.send_header('Content-type', 'text/plain')
        # self.end_headers()

    @classmethod
    def add_consume(cls, topic, handler):
        print(f"Adding consumer for topic: {topic} with handler: {handler}")
        # cls.consumers[topic] = consumer


class TestServer(Thread):
    daemon = True
    handler = StreamHandler
    server = HTTPServer((SERVER_HOST, SERVER_PORT), handler)
    topics = []

    @classmethod
    def add_consume(cls, topic, handler):
        cls.handler.add_consume(topic, handler)

    @classmethod
    def run(cls):
        print("Starting server")
        cls.server.serve_forever()

    @classmethod
    def stop(cls):
        print("Stopping server")
        cls.server.shutdown()


if __name__ == '__main__':
    print(f"Server port: {SERVER_PORT}")
    print(f"Enabled: {ENABLED}")
    # TestServer.add_consume("test")
    # TestServer.add_consume("test2")
    TestServer.run()
    sleep(10)
