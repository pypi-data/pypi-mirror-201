"""
Contains the server class
"""

from sys import maxsize
from weakref import WeakValueDictionary
from os.path import exists
import socket
import ssl
import configparser
from .__init__ import __version__  # pylint: disable=E0402
from . import utils
from . import exceptions


class Server:
    """
    An instance of the class object represents the connection to a numeric server.
    """
    # pylint: disable=R0913
    # pylint: disable=R0902
    def __init__(self, config_path='', server='', port=-1, api_key='', timeout=5., cert_path=''):
        if exists(config_path):
            self.__init_with_config__(api_key, config_path, port, server, cert_path)
        elif server == '' or port == -1 or api_key == '':
            raise exceptions.CommunicationException('Port, server or API key to connect to not specified!')
        else:
            self._address = server
            self._port = port
            self._api_key = api_key
            self._cert_path = cert_path
        if not exists(self._cert_path):
            self._cert_path = utils.find_cert_file()
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations(cafile=self._cert_path)
        self.is_remote_server = True
        self._objs = WeakValueDictionary()
        self._socket = socket.socket()
        self._socket = self.context.wrap_socket(self._socket, server_hostname=self._address)
        self._socket.settimeout(timeout)
        self._socket.connect((self._address, self._port))

        self._socket.sendall(__version__.ljust(256).encode())
        self._socket.sendall(self._api_key.ljust(256).encode())
        answer = utils.rcv_bytes(self._socket).decode('UTF-8').strip()
        if answer == 'OK':
            return
        if answer == 'INVALID_API_KEY':
            raise exceptions.AuthenticationException('API key is not valid')

    def add_obj(self, obj):
        """
        Adds an object to the server and returns the obj_index it was registered with.
        """
        obj_index = self.__get_free_id__()
        self._objs[obj_index] = obj
        return obj_index

    def get_obj(self, obj_index):
        """
        Returns a reference to the server managed object with the given obj_index
        """
        if obj_index not in self._objs:
            if not self.pull(obj_index):
                raise exceptions.ServerException('Object exists neither in client nor in server')
        return self._objs[obj_index]

    def push(self, obj_index, force=False):
        """
        Pushes the object stored at obj_index to the remote server.
        """
        obj = self._objs[obj_index]
        if obj.refresh_stamp <= self.get_refresh_stamp(obj_index) and not force:
            return
        type_string = str(type(obj))
        data = obj.__serialize__()
        package = ('PUSH|' + str(obj_index) + '|' + type_string + '|' + str(obj.refresh_stamp) +
                   '|' + str(len(data))).ljust(256).encode('UTF-8') + data
        self._socket.sendall(package)
        answer = utils.rcv_bytes(self._socket).decode('UTF-8')
        if answer.strip() != 'OK':
            raise exceptions.ServerException(answer.split('|')[1])

    def get_refresh_stamp(self, obj_index):
        """
        gets the current server side refresh stamp from the server
        """
        package = ('GET_STAMP|' + str(obj_index)).ljust(256).encode('UTF-8')
        self._socket.sendall(package)
        package = utils.rcv_bytes(self._socket, 256).decode('UTF-8')
        if not int(package.split('|')[1]) == obj_index:
            raise exceptions.CommunicationException('answer with different object obj_index received')
        return int(package.split('|')[2])

    def pull(self, obj_index, force=False):
        """
        Pulls the object sored at obj_index from the server and returns true on success.
        """
        stamp_at_server = self.get_refresh_stamp(obj_index)
        if stamp_at_server <= self._objs[obj_index].refresh_stamp and not force:
            return True

        package = ('PULL|' + str(obj_index)).ljust(256).encode('UTF-8')
        self._socket.sendall(package)
        header = utils.rcv_bytes(self._socket).decode('UTF-8')
        if header[0][:15] == 'NO_OBJECT_AT_ID':
            return False
        if str(obj_index) != header.split('|')[1]:
            raise exceptions.CommunicationException('answer with different object obj_index received')
        data = utils.rcv_bytes(self._socket, int(header.split('|')[2]))
        self._objs[obj_index].__deserialize__(data)
        return True

    def remove(self, obj_index):
        """
        Removes the object sored at obj_index from the server
        """
        package = ('REMOVE|' + str(obj_index)).ljust(256).encode('UTF-8')
        self._socket.sendall(package)
        del self._objs[obj_index]

    def call_method(self, name, obj_index, args, return_type="<class 'bool'>"):
        """
        Calls a method of on object on the remote server and passes back eventual results.
        """
        arg_bytes = utils.serialize_dict(args)
        package = ('CALL|' + str(obj_index) + '|' + name + '|' + str(len(arg_bytes))).ljust(256).encode()
        self._socket.sendall(package)
        self._socket.sendall(arg_bytes)
        reply = utils.rcv_bytes(self._socket).decode('UTF-8')
        if reply.strip() == 'OK':
            reply = utils.rcv_bytes(self._socket).decode('UTF-8')
            return_len = int(reply.split('|')[1])
            return_data = utils.rcv_bytes(self._socket, return_len)
            return utils.obj_frm_bytes(return_data, return_type)
        if '|' not in reply:
            raise exceptions.ServerException('Unknown server error')
        raise exceptions.ServerException(reply.split('|')[1])

    def __get_free_id__(self):
        """
        Returns the smallest free obj_index
        """
        res = 0
        for obj_index in range(maxsize):
            if obj_index not in self._objs:
                res = obj_index
                break
        return res

    def __init_with_config__(self, api_key, config_path, port=-1, server='', cert_path=''):
        """
        Initializes a server object using a config file
        """
        config = configparser.ConfigParser()
        config.read(config_path)
        if server == '':
            self._address = config['DEFAULT']['server']
            if self._address in ('localhost', '127.0.0.1'):
                self._address = socket.gethostname()
        else:
            self._address = server
        if port == -1:
            self._port = int(config['DEFAULT']['port'])
        else:
            self._port = port
        if api_key == '':
            self._api_key = config['DEFAULT']['api_key']
        else:
            self._api_key = api_key
        if cert_path == '':
            self._cert_path = config['DEFAULT']['cert_path']
        else:
            self._cert_path = cert_path

    def __eq__(self, other):
        return self._address == other._address and self._port == other._port

    def close(self):
        """
        Orders the server to close
        """
        package = 'CLOSE'.ljust(256).encode()
        self._socket.sendall(package)

    def __del__(self):
        self.close()
