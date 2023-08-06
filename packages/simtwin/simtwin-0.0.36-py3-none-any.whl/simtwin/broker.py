"""
The object broker manages all objects created through the API on the remote server.
"""

import socket
import signal
from sys import maxsize
import ssl
from . import utils
from . import geometry
from . import mesh
from . import simulation
from . import exceptions

object_types = {'Geometry': geometry.Geometry,
                'GeometryFile': geometry.GeometryFile,
                'Rotation': geometry.Rotation,
                'GeometrySelection': geometry.GeometrySelection,
                'Solid': geometry.Solid,
                'Surface': geometry.Surface,
                'Curve': geometry.Curve,
                'Corner': geometry.Corner,
                'Tessellation': geometry.Tessellation,
                'Mesh': mesh.Mesh,
                'Simulation': simulation.Simulation,
                'CoordinateSystem': simulation.CoordinateSystem,
                'BC': simulation.BC,
                'Question': simulation.Question,
                'Solution': simulation.Solution}


class Broker:
    """
    The broker class manages the created objects within the remote server
    """
    # pylint: disable=R0902
    def __init__(self, port=1441, key_validator=lambda x: True, cert_path='', key_path=''):
        signal.signal(signal.SIGTERM, self.__handle_signal__)
        self.is_remote_server = False
        self.objs = {}
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        self.socket = socket.socket()
        self.socket.bind(('', port))
        self.socket.listen(5)
        self.key_validator = key_validator
        self.api_key = ''
        self.connection = None
        self.addr = None
        self.drq_version = None
        self.connected = False

    def await_client(self):
        """
        Lets the broker wait for a client to login
        """
        self.connection, self.addr = self.socket.accept()  # Establish connection with client.
        self.connection = self.context.wrap_socket(self.connection, server_side=True)
        self.drq_version = utils.rcv_bytes(self.connection).decode().strip()
        self.api_key = utils.rcv_bytes(self.connection).decode().strip()
        if self.key_validator(self.api_key):
            self.connection.sendall('OK'.ljust(256).encode())
            self.connected = True
        else:
            self.connection.sendall('INVALID_API_KEY'.ljust(256).encode())
            self.api_key = ''

    def __handle_signal__(self):
        if self.socket:
            self.socket.close()

    def add_obj(self, obj, obj_index=-1):
        """
        Adds the provided object to the broker with the given obj_index
        """
        if obj_index == -1:
            obj_index = self.__get_free_id__()
        self.objs[obj_index] = obj
        return obj_index

    def __get_free_id__(self):
        for res in range(maxsize):
            if res not in self.objs:
                return res
        raise exceptions.ServerException('Too many objects in server')

    def listen(self):
        """
        Listen to the remote client for further commands
        """
        keep_server = True
        if not self.connected:
            return keep_server
        rbuff = utils.rcv_bytes(self.connection)
        command = rbuff.decode('UTF-8')

        if __is_cmd__(command, 'PUSH'):
            self.__cmd_push__(command)
        elif __is_cmd__(command, 'PULL'):
            self.__cmd_pull__(command)
        elif __is_cmd__(command, 'REMOVE'):
            self.__cmd_remove__(command)
        elif __is_cmd__(command, 'GET_STAMP'):
            self.__cmd_get_stamp__(command)

        elif __is_cmd__(command, 'CALL'):
            self.__cmd_call__(command)
            keep_server = True
        elif __is_cmd__(command, 'CLOSE'):
            self.__cmd_close__()
        return keep_server

    def __cmd_close__(self):
        self.connection.close()
        self.objs = {}

    def __cmd_call__(self, command):
        obj_index = int(command.split('|')[1])
        method_name = command.split('|')[2]
        data_len = int(command.split('|')[3])
        args_data = utils.rcv_bytes(self.connection, data_len)
        args_dict = utils.deserialize_dict(args_data)
        if method_name in self.objs[obj_index].methods:
            self.connection.sendall('OK'.ljust(256).encode())
        else:
            self.connection.sendall('NO_SUCH_METHOD_IN_OBJECT'.ljust(256).encode())
        try:
            res = self.objs[obj_index].call_method(method_name, args_dict)
            res_data = utils.obj_to_bytes(res)
            self.connection.sendall(('RETURN_VALUE|' + str(len(res_data)) + '|' + str(type(res))).ljust(256).encode())
            self.connection.sendall(res_data)
        except exceptions.ServerException as ex:
            self.connection.sendall(('ERROR|' + ex.message).ljust(256).encode())

    def __cmd_get_stamp__(self, command):
        obj_index = int(command.split('|')[1])
        if obj_index in self.objs:
            refresh_stamp = self.objs[obj_index].refresh_stamp
        else:
            refresh_stamp = -1
        package = ('STAMP|' + str(obj_index) + '|' + str(refresh_stamp)).ljust(256).encode('UTF-8')
        self.connection.sendall(package)

    def __cmd_remove__(self, command):
        obj_index = int(command.split('|')[1])
        del self.objs[obj_index]

    def __cmd_pull__(self, command):
        obj_index = int(command.split('|')[1])
        data = self.objs[obj_index].__serialize__()
        package = ('DATA|' + str(obj_index) + '|' + str(len(data))).ljust(256).encode('UTF-8') + data
        self.connection.sendall(package)

    def __cmd_push__(self, command):
        obj_index = int(command.split('|')[1])
        obj_type = command.split('|')[2]
        obj_type = obj_type.split('.')[-1].replace('>', '').replace("'", '')
        refresh_stamp = int(command.split('|')[3])
        data_len = int(command.split('|')[4])
        data = utils.rcv_bytes(self.connection, data_len)
        type_from_client = object_types[obj_type]
        if obj_index not in self.objs:
            self.objs[obj_index] = type_from_client(self, obj_index=obj_index)
        if not isinstance(self.objs[obj_index], type_from_client):
            package = ('ERROR| This index is already in use by another object of type ' +
                       str(type(self.objs[obj_index]))).ljust(256).encode('UTF-8')
            self.connection.sendall(package)
        else:
            self.objs[obj_index].__deserialize__(data)
            self.objs[obj_index]._refresh_stamp = refresh_stamp  # pylint: disable=W0212
            self.connection.sendall('OK'.ljust(256).encode())

    def push(self, obj_index, force=False):
        """
        This dummy method is required to stop a communication cycle between client and host
        """

    def pull(self, obj_index, force=False):
        """
        This dummy method is required to stop a communication cycle between client and host
        """

    def remove(self, obj_index):
        """
        This dummy method is required to stop a communication cycle between client and host
        """

    def __del__(self):
        self.socket.close()


def __is_cmd__(string, cmd):
    if len(string) < len(cmd):
        return False
    return string[:len(cmd)] == cmd
