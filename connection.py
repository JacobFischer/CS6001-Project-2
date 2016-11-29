from point import Point
import socket
import json


class Connection:
    """A simple TCP wrapper class that acts a client OR server with similar
    methods regardless of which it is connected as
    """
    def __init__(self, port, host=None):
        """Creates a connection, basically a simple TCP client/server wrapper

        Args:
            port: the port to connect through
            host: if set then will connect to that host as a client,
                otherwise acts a server on host "0.0.0.0"
        """
        self._tcp_socket = socket.socket()
        self.curve = None

        if not host:
            # then we are the server that connects to client(s)
            host = "0.0.0.0"

            # before connecting, reuse the port if needed
            self._tcp_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )

            # and connect to the port as a server listening for clients
            self._tcp_socket.bind((host, port))
            self._tcp_socket.listen(1)
            print("Connection listing on {}:{}\n".format(host, port))
            self.connection, address = self._tcp_socket.accept()
        else:
            # we are a client connecting to a server
            self._tcp_socket.connect((host, port))
            self.connection = self._tcp_socket
            print("Connection attempting to connect to {}:{}\n".format(
                host, port
            ))

    def send(self, obj):
        """Sends some object as json over the connection

        Args:
            obj: an object safe for json serialization
                Note: Points can be serialized
        """
        # ensure points safe for serialization
        if isinstance(obj, Point):
            obj = {'x': obj.x, 'y': obj.y}

        string = json.dumps(obj)
        self.connection.send(string.encode())

    def read(self):
        """Read (blocking) from the connection until something is sent and parsed

        Returns:
            parsed json output from the connection
        """
        buffer = ""
        while True:
            data = self.connection.recv(1024).decode()
            if not data:
                continue

            data = str(data)

            if data:
                buffer += data

            if len(data) == 1024:
                continue  # we need to read more data
            else:
                break

        parsed = self._clean(json.loads(buffer))

        return parsed

    def close(self):
        """Closes this network connection(s)
        """
        self.connection.close()
        if self.connection != self._tcp_socket:
            self._tcp_socket.close()

    def _clean(self, parsed):
        """Cleans a parsed json object to Points if need be

        Args:
            parsed: valid json object already parsed such as a dict or string

        Returns:
            if parsed looks like a Point but is a dict, it will become a Point
        """
        if (self.curve and isinstance(parsed, dict) and
            'x' in parsed and 'y' in parsed):
            parsed = Point(parsed['x'], parsed['y'], self.curve)

        return parsed
