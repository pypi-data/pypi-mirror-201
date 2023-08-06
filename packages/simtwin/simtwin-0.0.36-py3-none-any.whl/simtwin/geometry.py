# pylint: disable=C0116
# pylint: disable=C0302
"""
Contains classes to represent simulation geometry
"""

from dataclasses import dataclass
from os.path import exists
from os import remove
import tempfile
import numpy as np
import gmsh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from . import utils, exceptions
from .simtwin_base_classes import SimtwinEnum, SimtwinObjectBase


class Geometry(SimtwinObjectBase):
    """
    Holds simulation geometry
    """
    # pylint: disable=R0902
    def __init__(self, server, obj_index=None):
        self._slds = []
        self._srfs = []
        self._crvs = []
        self._cnrs = []
        self._files = []
        self._tessellation = Tessellation(server)
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        return utils.cmp_list(self.slds, other.slds) and \
            utils.cmp_list(self.srfs, other.srfs) and \
            utils.cmp_list(self.crvs, other.crvs) and \
            utils.cmp_list(self.cnrs, other.cnrs) and \
            utils.cmp_list(self.files, other.files) and \
            self.tessellation == other.tessellation

    def __hash__(self):
        return self.obj_index

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')

        ids = utils.get_id_list(self.slds)
        slds_bytes = utils.serialize_list(ids)
        res += int.to_bytes(len(slds_bytes), 8, 'little')
        res += slds_bytes

        ids = utils.get_id_list(self._srfs)
        srfs_bytes = utils.serialize_list(ids)
        res += int.to_bytes(len(srfs_bytes), 8, 'little')
        res += srfs_bytes

        ids = utils.get_id_list(self._crvs)
        crvs_bytes = utils.serialize_list(ids)
        res += int.to_bytes(len(crvs_bytes), 8, 'little')
        res += crvs_bytes

        ids = utils.get_id_list(self._cnrs)
        cnrs_bytes = utils.serialize_list(ids)
        res += int.to_bytes(len(cnrs_bytes), 8, 'little')
        res += cnrs_bytes

        ids = utils.get_id_list(self._files)
        files_bytes = utils.serialize_list(ids)
        res += int.to_bytes(len(files_bytes), 8, 'little')
        res += files_bytes
        tessellation_bytes = self._tessellation.__serialize__()
        res += int.to_bytes(len(tessellation_bytes), 8, 'little')
        res += tessellation_bytes
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8

        data_bytes = data[seeker:seeker + data_len]
        seeker += data_len
        slds_list = utils.deserialize_list(data_bytes)
        self._slds = []
        for sld in slds_list:
            self._slds += [self._server.objs[sld]]

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_bytes = data[seeker:seeker + data_len]
        seeker += data_len
        srfs_list = utils.deserialize_list(data_bytes)
        self._srfs = []
        for srf in srfs_list:
            self._srfs += [self._server.objs[srf]]

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_bytes = data[seeker:seeker + data_len]
        seeker += data_len
        crvs_list = utils.deserialize_list(data_bytes)
        self._crvs = []
        for crv in crvs_list:
            self._crvs += [self._server.objs[crv]]

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_bytes = data[seeker:seeker + data_len]
        seeker += data_len
        crnr_list = utils.deserialize_list(data_bytes)
        self._cnrs = []
        for crnr in crnr_list:
            self._cnrs += [self._server.objs[crnr]]

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_bytes = data[seeker:seeker + data_len]
        seeker += data_len

        files_list = utils.deserialize_list(data_bytes)
        self._files = []
        for file_obj_index in files_list:
            self._files += [self._server.objs[file_obj_index]]

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_bytes = data[seeker:seeker + data_len]
        seeker += data_len
        self.tessellation.__deserialize__(data_bytes)

    @property
    def slds(self):
        """
        List of all solids in the geometry
        """
        return self._slds

    @property
    def srfs(self):
        """
        List of all surfaces in the geometry
        """
        return self._srfs

    @property
    def crvs(self):
        """
        List of all curves in the geometry
        """
        return self._crvs

    @property
    def cnrs(self):
        """
        List of all corners in the geometry
        """
        return self._cnrs

    @property
    def files(self):
        """
        List of all files composing the geometry
        """
        return self._files

    @files.setter
    def files(self, files):
        self._files = files
        self.__push__()
        self.__pull__()

    @property
    def tessellation(self):
        """
        Tesselation of the geometry for rendering
        """
        return self._tessellation


class GeometryFile(SimtwinObjectBase):
    """Holds information on a loaded file and applied transformations"""
    # pylint: disable=R0902

    def __init__(self, server, file_path='', translation=np.zeros(3), rotations=None, obj_index=None):
        # pylint: disable=R0913
        self._is_tmp_file = False
        if file_path != '':
            if not exists(file_path):
                raise FileExistsError
        self._path = file_path
        self._translation = translation
        if rotations is None:
            self.rotations = []
        elif isinstance(rotations, Rotation):
            self.rotations = [rotations]
        elif isinstance(rotations, list):
            self.rotations = rotations
        else:
            raise exceptions.DrqException('Unknown rotation type')
        self._file = None
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        return self.file_bytes == other.file_bytes and \
            (self._translation == other.translation).all() and \
            self._rotations == other.rotations

    def __hash__(self):
        return self.obj_index

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        if self._path == '':
            file_data = bytes()
        else:
            file_data = self.file_bytes

        res += len(file_data).to_bytes(8, 'little')
        res += file_data

        data = utils.obj_to_bytes(self.translation)
        res += len(data).to_bytes(8, 'little')
        res += data

        rot_ids = utils.get_id_list(self.rotations)
        data = utils.serialize_list(rot_ids)
        res += len(data).to_bytes(8, 'little')
        res += data
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._is_tmp_file = True
        file_bytes_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        file_byte = data[seeker:seeker+file_bytes_len]
        seeker += file_bytes_len
        # pylint: disable=R1732
        self._file = tempfile.NamedTemporaryFile(delete=False, suffix='.step')
        self._path = self._file.name

        with open(self.path, 'wb') as fp:
            fp.write(file_byte)

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self.translation = utils.deserialize_array(data[seeker:seeker + data_len])
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        rot_ids = utils.deserialize_list(data[seeker:seeker + data_len])
        seeker += data_len
        for obj_index in rot_ids:
            self.rotations += [self._server.objs[obj_index]]

    def __del__(self):
        if self.path != '' and self._is_tmp_file:
            remove(self.path)
        super().__del__()

    @property
    def path(self):
        """
        Path to the file
        """
        return self._path

    @property
    def file_bytes(self):
        """
        Returns the bytes of the underlying geometry file.
        """
        if self._path == '':
            return bytes()
        with open(self._path, 'rb') as fp:
            file_bytes = fp.read()
        return file_bytes

    @property
    def translation(self):
        """
        Translation applied to the geometry of the file
        """
        return self._translation

    @translation.setter
    def translation(self, translation):
        self._translation = translation

    @translation.deleter
    def translation(self):
        self._translation = np.zeros(3)

    @property
    def rotations(self):
        """
        List of rotations applied to the geometry of the file
        """
        return self._rotations

    @rotations.setter
    def rotations(self, rotations):
        self._rotations = rotations

    @rotations.deleter
    def rotations(self):
        self.rotations = []


@dataclass()
class Rotation(SimtwinObjectBase):
    """
    Represents a rotation
    cnt: any point on the rotation axis
    axis: vector of the rotation axis
    angle: rotation angle in degrees
    """

    def __init__(self, server, cnt=np.zeros(3), axis=np.zeros(3), angle=0., obj_index=None):  # pylint: disable=R0913
        self._cnt = cnt
        self._axis = axis
        self._angle = angle
        super().__init__(server, obj_index)

    @property
    def cnt(self):
        self.__pull__(force=True)
        return self._cnt

    @cnt.setter
    def cnt(self, cnt):
        self._cnt = cnt
        self.__push__()

    @property
    def axis(self):
        self.__pull__(force=True)
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis
        self.__push__()

    @property
    def angle(self):
        self.__pull__(force=True)
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self.__push__(force=True)

    def __eq__(self, other):
        return (self._cnt == other.cnt).all() and (self._axis == other.axis).all() and self._angle == other.angle

    def __hash__(self):
        return self.obj_index

    def __serialize__(self):
        """
        Serializes the rotation to bytes
        """
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        res += utils.serialize_list([self._cnt, self._axis, np.array(self._angle)])
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data = utils.deserialize_list(data[8:])
        self._cnt = data[0]
        self._axis = data[1]
        self._angle = data[2]


class GeometrySelectionType(SimtwinEnum):
    """
    Types of geometry selection
    """
    NONE = 0
    VERTEX = 1
    CURVE = 2
    FACE = 3
    BODY = 4
    ALL = 5


class GeometrySelection(SimtwinObjectBase):
    """
    Represents a user selection of geometry
    """
    def __init__(self, server, selection_type=GeometrySelectionType.BODY, geometry_id=0, obj_index=None):
        self.selection_type = selection_type
        self.geometry_id = geometry_id
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        return self.selection_type == other.selection_type and self.geometry_id == other.geometry_id

    def __hash__(self):
        return self.obj_index

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        res += self.selection_type.value.to_bytes(8, 'little')
        res += self.geometry_id.to_bytes(8, 'little')
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self.selection_type = GeometrySelectionType(int.from_bytes(data[seeker:seeker + 8], 'little'))
        seeker += 8
        self.geometry_id = int.from_bytes(data[seeker:seeker + 8], 'little')


class Solid(SimtwinObjectBase):
    """
    Represents a geometry solid
    """
    def __init__(self, server, gmsh_id=0, obj_index=None):
        self._gmsh_id = gmsh_id
        self._srfs = []
        self._crvs = []
        self._cnrs = []
        super().__init__(server, obj_index)

    def __serialize__(self):
        byts = bytes()
        byts += self.obj_index.to_bytes(8, 'little')
        byts += self.gmsh_id.to_bytes(8, 'little')

        ids = utils.get_id_list(self.srfs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes

        ids = utils.get_id_list(self.crvs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes

        ids = utils.get_id_list(self.cnrs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes
        return byts

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._gmsh_id = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._srfs += [self._server.objs[obj_index]]
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._crvs += [self._server.objs[obj_index]]
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._cnrs += [self._server.objs[obj_index]]
        seeker += data_len

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index

        return self.obj_index == other.obj_index and \
            utils.cmp_list(utils.get_id_list(self.srfs), utils.get_id_list(other.srfs)) and \
            utils.cmp_list(utils.get_id_list(self.crvs), utils.get_id_list(other.crvs)) and \
            utils.cmp_list(utils.get_id_list(self.cnrs), utils.get_id_list(other.cnrs))

    def __hash__(self):
        return hash(hash(type(self)) + self.obj_index)

    @property
    def gmsh_id(self):
        return self._gmsh_id

    @gmsh_id.setter
    def gmsh_id(self, gmsh_id):
        self._gmsh_id = gmsh_id
        self.__update_remote__()

    @property
    def srfs(self):
        """
        References to all surfaces the solid is a part of.
        """
        return self._srfs

    @property
    def crvs(self):
        """
        References to all curves the solid is a part of.
        """
        return self._crvs

    @property
    def cnrs(self):
        """
        References to all corner the solid is a part of.
        """
        return self._cnrs


class Surface(SimtwinObjectBase):
    """
    Represents a geometry solid
    """

    def __init__(self, server, gmsh_id=0, obj_index=None):
        self._gmsh_id = gmsh_id
        self._slds = []
        self._crvs = []
        self._cnrs = []
        super().__init__(server, obj_index)

    def __serialize__(self):
        byts = bytes()
        byts += self.obj_index.to_bytes(8, 'little')
        byts += self.gmsh_id.to_bytes(8, 'little')

        ids = utils.get_id_list(self.slds)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes

        ids = utils.get_id_list(self.crvs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes

        ids = utils.get_id_list(self.cnrs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes
        return byts

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._gmsh_id = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._slds += [self._server.objs[obj_index]]
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._crvs += [self._server.objs[obj_index]]
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._cnrs += [self._server.objs[obj_index]]
        seeker += data_len

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        return self.obj_index == other.obj_index and \
            utils.cmp_list(utils.get_id_list(self.slds), utils.get_id_list(other.slds)) and \
            utils.cmp_list(utils.get_id_list(self.crvs), utils.get_id_list(other.crvs)) and \
            utils.cmp_list(utils.get_id_list(self.cnrs), utils.get_id_list(other.cnrs))

    def __hash__(self):
        return hash(hash(type(self)) + self.obj_index)

    @property
    def gmsh_id(self):
        return self._gmsh_id

    @gmsh_id.setter
    def gmsh_id(self, gmsh_id):
        self._gmsh_id = gmsh_id
        self.__update_remote__()

    @property
    def slds(self):
        """
        References to all solids the surface is a part of.
        """
        return self._slds

    @property
    def crvs(self):
        """
        References to all curves the surface is a part of.
        """
        return self._crvs

    @property
    def cnrs(self):
        """
        References to all corner the surface is a part of.
        """
        return self._cnrs


class Curve(SimtwinObjectBase):
    """
    Represents a geometry solid
    """

    def __init__(self, server, gmsh_id=0, obj_index=None):
        self._gmsh_id = gmsh_id
        self._slds = []
        self._srfs = []
        self._cnrs = []
        super().__init__(server, obj_index)

    def __serialize__(self):
        byts = bytes()
        byts += self.obj_index.to_bytes(8, 'little')
        byts += self.gmsh_id.to_bytes(8, 'little')

        ids = utils.get_id_list(self.slds)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes

        ids = utils.get_id_list(self.srfs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes

        ids = utils.get_id_list(self.cnrs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes
        return byts

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._gmsh_id = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._slds += [self._server.objs[obj_index]]

        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._srfs += [self._server.objs[obj_index]]

        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._cnrs += [self._server.objs[obj_index]]

        seeker += data_len

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        return self.obj_index == other.obj_index and \
            utils.cmp_list(utils.get_id_list(self.slds), utils.get_id_list(other.slds)) and \
            utils.cmp_list(utils.get_id_list(self.srfs), utils.get_id_list(other.srfs)) and \
            utils.cmp_list(utils.get_id_list(self.cnrs), utils.get_id_list(other.cnrs))

    def __hash__(self):
        return hash(hash(type(self)) + self.obj_index)

    @property
    def gmsh_id(self):
        return self._gmsh_id

    @gmsh_id.setter
    def gmsh_id(self, gmsh_id):
        self._gmsh_id = gmsh_id
        self.__update_remote__()

    @property
    def slds(self):
        """
        References to all solids the curve is a part of.
        """
        return self._slds

    @property
    def srfs(self):
        """
        References to all surfaces the curve is a part of.
        """
        return self._srfs

    @property
    def cnrs(self):
        """
        References to all corner the curve is a part of.
        """
        return self._cnrs


class Corner(SimtwinObjectBase):
    """
    Represents a geometry solid
    """

    def __init__(self, server, gmsh_id=0, obj_index=None):
        self._gmsh_id = gmsh_id
        self._slds = []
        self._crvs = []
        self._srfs = []
        super().__init__(server, obj_index)

    def __serialize__(self):
        byts = bytes()
        byts += self.obj_index.to_bytes(8, 'little')
        byts += self.gmsh_id.to_bytes(8, 'little')

        ids = utils.get_id_list(self.slds)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes

        ids = utils.get_id_list(self.crvs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes

        ids = utils.get_id_list(self.srfs)
        ids_bytes = utils.serialize_list(ids)
        byts += len(ids_bytes).to_bytes(8, 'little')
        byts += ids_bytes
        return byts

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._gmsh_id = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._slds += [self._server.objs[obj_index]]
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._crvs += [self._server.objs[obj_index]]
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        lst = utils.deserialize_list(data[seeker:seeker + data_len])
        for obj_index in lst:
            self._srfs += [self._server.objs[obj_index]]

        seeker += data_len

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        return self.obj_index == other.obj_index and \
            utils.cmp_list(utils.get_id_list(self.slds), utils.get_id_list(other.slds)) and \
            utils.cmp_list(utils.get_id_list(self.crvs), utils.get_id_list(other.crvs)) and \
            utils.cmp_list(utils.get_id_list(self.srfs), utils.get_id_list(other.srfs))

    def __hash__(self):
        return hash(hash(type(self)) + self.obj_index)

    @property
    def gmsh_id(self):
        return self._gmsh_id

    @gmsh_id.setter
    def gmsh_id(self, gmsh_id):
        self._gmsh_id = gmsh_id
        self.__update_remote__()

    @property
    def slds(self):
        """
        References to all solids the corner is a part of.
        """
        return self._slds

    @property
    def crvs(self):
        """
        References to all curves the corner is a part of.
        """
        return self._crvs

    @property
    def srfs(self):
        """
        References to all surfaces the corner is a part of.
        """
        return self._srfs


class Tessellation(SimtwinObjectBase):
    """
    Contains information required to render geometry.
    """
    # pylint: disable=R0902

    def __init__(self, server, obj_index=None):
        self._nc = np.zeros([0, 3])  # Coordinates of all nodes
        self._inz = np.zeros([0, 3], dtype=int)
        self._ed = np.zeros([0, 2], dtype=int)
        self._srfs = np.zeros(0, dtype=int)
        self._slds = np.zeros(0, dtype=int)
        self._crvs = np.zeros(0, dtype=int)
        self._cnrs = np.zeros(0, dtype=int)
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        self.__lazy_pull__()
        if not other.up_to_date:
            other.__pull__()
        if self.nc.shape[0] == 0 and self.inz.shape[0] == 0 and \
                other.nc.shape[0] == 0 and other.inz.shape[0] == 0:
            return True
        if not self.nc.shape == other.nc.shape and self.inz.shape == other.inz.shape:
            return False
        if not (self.nc == other.nc).all() and (self.inz == other.inz).all():
            return False
        return (self.srfs == other.srfs).all() and \
            (self.slds == other.slds).all() and \
            (self.crvs == other.crvs).all() and \
            (self.cnrs == other.cnrs).all()

    def __hash__(self):
        self.__lazy_pull__()
        return self.obj_index

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')

        nc_bytes = utils.obj_to_bytes(self._nc)
        res += int.to_bytes(len(nc_bytes), 8, 'little')
        res += nc_bytes

        inz_bytes = utils.obj_to_bytes(self._inz)
        res += int.to_bytes(len(inz_bytes), 8, 'little')
        res += inz_bytes

        ed_bytes = utils.obj_to_bytes(self._ed)
        res += int.to_bytes(len(ed_bytes), 8, 'little')
        res += ed_bytes

        faces_bytes = utils.obj_to_bytes(self._srfs)
        res += int.to_bytes(len(faces_bytes), 8, 'little')
        res += faces_bytes

        solids_bytes = utils.obj_to_bytes(self._slds)
        res += int.to_bytes(len(solids_bytes), 8, 'little')
        res += solids_bytes

        corners_bytes = utils.obj_to_bytes(self._crvs)
        res += int.to_bytes(len(corners_bytes), 8, 'little')
        res += corners_bytes

        corners_bytes = utils.obj_to_bytes(self._cnrs)
        res += int.to_bytes(len(corners_bytes), 8, 'little')
        res += corners_bytes
        return res

    def __deserialize__(self, data):
        seeker = 0

        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._nc = utils.obj_frm_bytes(data[seeker:seeker + data_len], "<class 'numpy.ndarray'>")
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._inz = utils.obj_frm_bytes(data[seeker:seeker + data_len], "<class 'numpy.ndarray'>")
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._ed = utils.obj_frm_bytes(data[seeker:seeker + data_len], "<class 'numpy.ndarray'>")
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._srfs = utils.obj_frm_bytes(data[seeker:seeker + data_len], "<class 'numpy.ndarray'>")
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._slds = utils.obj_frm_bytes(data[seeker:seeker + data_len], "<class 'numpy.ndarray'>")
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._crvs = utils.obj_frm_bytes(data[seeker:seeker + data_len], "<class 'numpy.ndarray'>")
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._cnrs = utils.obj_frm_bytes(data[seeker:seeker + data_len], "<class 'numpy.ndarray'>")
        seeker += data_len

    @property
    def nc(self):
        """
        n x 3 matrix of the coordinates of all nodes
        """
        self.__lazy_pull__()
        return self._nc

    @property
    def inz(self):
        """
        n x 3 matrix of the nodes of each triangle
        """
        self.__lazy_pull__()
        return self._inz

    @property
    def ed(self):
        """
        n x 2 matrix of all edges of the tesselation
        """
        self.__lazy_pull__()
        return self._ed

    @property
    def srfs(self):
        """
        Numpy array of the face indicis for all triangles
        """
        self.__lazy_pull__()
        return self._srfs

    @property
    def slds(self):
        """
        Numpy array of the solid indicis for all triangles
        """
        self.__lazy_pull__()
        return self._slds

    @property
    def crvs(self):
        """
        Numpy array with the curve indicis for all edges
        Edges which are not on a curve are denoted with -1
        """
        self.__lazy_pull__()
        return self._crvs

    @property
    def cnrs(self):
        """
        Numpy array with the corner indicis for all nodes
        Nodes which are not on a curve are denoted with -1
        """
        self.__lazy_pull__()
        return self._cnrs

    def plot_fltk(self):
        """
        Plots the tesselation using the fltk renderer of gmsh
        """
        self.__lazy_pull__()
        gmsh.model.add('plot')
        entity = {0: gmsh.model.addDiscreteEntity(0), 1: gmsh.model.addDiscreteEntity(1),
                  2: gmsh.model.addDiscreteEntity(2), 3: gmsh.model.addDiscreteEntity(3)}
        gmsh.model.mesh.addNodes(3, entity[3], np.arange(1, self.nc.shape[0] + 1), self.nc.reshape(-1))
        gmsh.model.mesh.addElements(2, entity[2], [2], [np.arange(self.inz.shape[0]) + 1], [self.inz.flatten() + 1])
        gmsh.fltk.run()
        gmsh.model.remove()

    def plot_matplotlib(self, ax=None, color=np.array([0, 0, 0])):
        """
        or matplotlib.
        Plots the tesselation using matplotlib. An axis to plot into and plotting color can be specified.
        Returns the axis which was provided or created.
        """
        self.__lazy_pull__()
        if isinstance(color, list):
            color = np.array(color)
        if isinstance(color, int):
            color = float(color)
        elif isinstance(color, float):
            color = np.tile(color, (self.ed.shape[0], 3))
        elif len(color.shape) == 1:
            if color.shape[0] == 3:
                color = np.tile(color.T, (self.ed.shape[0], 1))
            elif color.shape[0] == 1:
                color = np.tile(color.T, (self.ed.shape[0], 3))
            else:
                color = np.stack([color, 1 - color, np.zeros_like(color)]).T
        if ax is None:
            fig = plt.figure()
            ax = Axes3D(fig, auto_add_to_figure=False)
            fig.add_axes(ax)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

        for i in range(self.ed.shape[0]):
            ax.plot(self.nc[self.ed[i], 0], self.nc[self.ed[i], 1], self.nc[self.ed[i], 2], color=color[i])
        return ax
