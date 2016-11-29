from point import Point
import socket
import json

class Connection:
    def __init__(self, host, port, is_server):
        self._tcp_socket = socket.socket()
        self.curve = None

        if is_server:
            # reuse the port if needed
            self._tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._tcp_socket.bind((host,port))
            self._tcp_socket.listen(1)
            print("Connection listing on {}:{}\n".format(host, port))
            self.connection, address = self._tcp_socket.accept()
        else:
            self._tcp_socket.connect((host,port))
            self.connection = self._tcp_socket
            print("Connection attempting to connect to {}:{}\n".format(host, port))

    def send(self, obj):
        # make points safe for serialization
        if isinstance(obj, Point):
            obj = { 'x': obj.x, 'y': obj.y }

        string = json.dumps(obj)
        self.connection.send(string.encode())

    def read(self):
        buffer = ""
        while True:
            data = self.connection.recv(1024).decode()
            if not data:
                continue

            data = str(data)

            if data:
                buffer += data

            if len(data) == 1024:
                continue # we need to read more data
            else:
                break

        parsed = json.loads(buffer)
        parsed = self.clean(parsed)

        return parsed

    def close(self):
        self.connection.close()
        if self.connection != self._tcp_socket:
            self._tcp_socket.close()

    def clean(self, parsed):
        if self.curve and isinstance(parsed, dict) and 'x' in parsed and 'y' in parsed:
            parsed = Point(parsed['x'], parsed['y'], self.curve)

        return parsed
