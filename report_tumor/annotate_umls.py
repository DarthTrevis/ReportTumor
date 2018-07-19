import json
import socket
from json import JSONDecodeError


class AnnotateUMLS(object):

    def __init__(self):
        self.BUFFER_SIZE = 2048
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 9999
        self.connect()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP, self.TCP_PORT))

    def annotate(self, report):
        data = {}
        data['text'] = report
        json_data = json.dumps(data)
        json_data_crlf = json_data+'\r\n'
        print("send " + json_data)
        self.s.sendall(json_data_crlf.encode('Cp1255'))

        data_response = self.recvall()
        data_response_obj = {}
        try:
            data_response_obj['response'] = json.loads(data_response.decode("utf-8"))
            print('received data={} '.format(data_response_obj['response']))
            return data_response_obj['response']
        except JSONDecodeError:
            print("JSONDecodeError " + json_data)
            self.close()
            self.connect()
            return None

    def recvall(self):
        data = b''
        while True:
            part = self.s.recv(self.BUFFER_SIZE)
            data += part
            if len(part) < self.BUFFER_SIZE:
                break
        return data

    def close(self):
        self.s.close()
