"""
Contains helper functions needed for internal purposes of the
simtwin library. Not intended for direct use!
"""
from struct import pack, unpack
import os
import numpy as np
import rootpath
from . import exceptions


def serialize_list(lst):
    """
    Serializes a list to a stream ob bytes.
    """
    res = len(lst).to_bytes(64, 'little')
    for item in lst:
        item_byts = obj_to_bytes(item)
        res += (str(type(item)) + '|' + str(len(item_byts))).ljust(256).encode('UTF-8')
        res += item_byts
    return res


def deserialize_list(byts):
    """
    Deserializes a stream ob bytes into a list.
    """
    res = []
    n_items = int.from_bytes(byts[:64], 'little')
    seeker = 64
    for _n in range(n_items):
        item_header = byts[seeker:seeker + 256].decode('UTF-8').strip()
        item_type = item_header.split('|')[0]
        item_len = int(item_header.split('|')[1])
        seeker += 256
        item_bytes = byts[seeker: seeker + item_len]
        res += [obj_frm_bytes(item_bytes, item_type)]
        seeker += item_len
    return res


def serialize_dict(dct):
    """
    Serializes a dictionary to a stream ob bytes.
    """
    res = len(dct).to_bytes(64, 'little')
    for key in dct:
        key_byts = obj_to_bytes(key)
        value_byts = obj_to_bytes(dct[key])
        res += (str(type(key)) + '|' + str(len(key_byts))).ljust(256).encode('UTF-8')
        res += key_byts
        res += (str(type(dct[key])) + '|' + str(len(value_byts))).ljust(256).encode('UTF-8')
        res += value_byts
    return res


def deserialize_dict(byts):
    """
    Deserializes a stream ob bytes into a dictionary.
    """
    res = {}
    n_items = int.from_bytes(byts[:64], 'little')
    seeker = 64
    for _n in range(n_items):
        key_header = byts[seeker:seeker + 256].decode('UTF-8').strip()
        key_type = key_header.split('|')[0]
        key_len = int(key_header.split('|')[1])
        seeker += 256
        key_bytes = byts[seeker: seeker + key_len]
        key = obj_frm_bytes(key_bytes, key_type)
        seeker += key_len

        value_header = byts[seeker:seeker + 256].decode('UTF-8').strip()
        value_type = value_header.split('|')[0]
        value_len = int(value_header.split('|')[1])
        seeker += 256
        value_bytes = byts[seeker: seeker + value_len]
        value = obj_frm_bytes(value_bytes, value_type)
        seeker += value_len

        res[key] = value
    return res


def get_id_list(obj):
    """
    Returns a list of IDs from a list of simtwin objects
    """
    return [item.obj_index for item in obj]


def cmp_list(lst_a, lst_b, ignore_order=True):
    """
    Returns true if all the lists contain the same items and no others.
    If ignore_order is set, the order of items is ignored for the comparison.
    """
    if len(lst_a) != len(lst_b):
        return False
    if ignore_order:
        for item in lst_a:
            if item not in lst_b:
                return False
    else:
        for i, _ in enumerate(lst_a):
            if not lst_a[i] == lst_b[i]:
                return False
    return True


def cmp_dict(dct_a, dct_b):
    """
    Compares to dictionaries. Returns true if both contain the same keys and values.
    """
    if len(dct_a) != len(dct_b):
        res = False
    else:
        res = True
    for key in dct_a:
        if key not in dct_b:
            res = False
            break
        if not dct_a[key].__class__ == dct_b[key].__class__:
            res = False
            break
        if isinstance(dct_a[key], np.ndarray):
            if not dct_a[key].shape == dct_b[key].shape:
                res = False
                break
            res = (dct_a[key] == dct_b[key]).all() or res
        else:
            res = dct_a[key] == dct_b[key]
    return res


def obj_frm_bytes(byts, type_str):
    """
    Deserializes an object to a stream of bytes.
    Throws an exception if the type of the object is not supported.
    """
    # pylint: disable=R0911
    if type_str == "<class 'int'>":
        return int.from_bytes(byts, 'little')
    if type_str == "<class 'float'>":
        return unpack('<d', byts)[0]
    if type_str == "<class 'str'>":
        return byts.decode('UTF-8')
    if type_str == "<class 'bool'>":
        return bool.from_bytes(byts, 'little')
    if type_str == "<class 'list'>":
        return deserialize_list(byts)
    if type_str == "<class 'numpy.ndarray'>":
        return deserialize_array(byts)
    if type_str == "<class 'NoneType'>":
        return None
    if type_str == "<class 'bytes'>":
        return byts
    raise exceptions.SerializationException('Object of type ' + type_str + 'cannot be serialized.')


def obj_to_bytes(obj):
    """
    Tests the serializability of an object and returns the serialized bytes
    """
    if hasattr(obj, 'to_bytes'):
        byts = obj.to_bytes(64, 'little')
    elif hasattr(obj, '__serialize__'):
        byts = obj.__serialize__()
    elif hasattr(obj, 'encode'):
        byts = obj.encode('UTF-8')
    elif isinstance(obj, float):
        byts = pack('<d', obj)
    elif isinstance(obj, list):
        byts = serialize_list(obj)
    elif isinstance(obj, dict):
        byts = serialize_dict(obj)
    elif isinstance(obj, np.ndarray):
        byts = serialize_array(obj)
    elif isinstance(obj, bytes):
        byts = obj
    elif obj is None:
        byts = bytes(0)
    else:
        raise exceptions.SerializationException('Object of type ' + str(type(obj)) + 'cannot be serialized.')
    return byts


def serialize_array(arr):
    """
    Serializes a numpy array
    """
    return (str(arr.dtype).ljust(8) + str(arr.shape).ljust(16)).encode() + arr.tobytes()


def deserialize_array(byts):
    """
    Forms a numpy array from serialized data
    """
    dtype = byts[:8].decode().strip()
    shape_str = byts[8:24].decode().strip()[1:-1]
    shape = []
    for segment in shape_str.split(','):
        if segment.strip() != '':
            shape += [int(segment)]
    return np.frombuffer(byts[24:], dtype=dtype).reshape(shape)


def rcv_bytes(connection, size=256):
    """
    Receives the designated number of bytes from the provided connection.
    """
    res = bytes()
    chunck_size = 1024
    for _n in range(int(size / chunck_size) + 2):
        bytes_read = connection.recv(min(size - len(res), chunck_size))
        res += bytes_read
        if len(res) == size:
            break
    return res


def find_cert_file():
    """
    Locates SSL certificate file
    """
    module_dir = rootpath.detect()
    crt_files = []
    for dirpath, _, filenames in os.walk(module_dir):
        for filename in filenames:
            if filename.endswith('.crt'):
                crt_files.append(os.path.join(dirpath, filename))
    crt_files.sort()
    if len(crt_files) == 0:
        exceptions.DrqException('No SSL certificate found in root dir.')
    return crt_files[0]
