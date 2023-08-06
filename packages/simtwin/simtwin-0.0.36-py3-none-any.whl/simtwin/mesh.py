"""
Contains the mesh class and helper classes to work on and generate meshes.
"""
from dataclasses import dataclass
from struct import pack, unpack
import numpy as np
import gmsh
from . import utils
from . import geometry as geo
from . import exceptions
from .simtwin_base_classes import SimtwinEnum, SimtwinObjectBase


class MeshType(SimtwinEnum):
    """
    Supported types of mesh
    """
    LINEAR = 1
    SERENDIPITY = 2
    FULL = 3


class MeshingMethod(SimtwinEnum):
    """
    Supported meshing methods
    """
    TET = 1
    HEX = 2


class Mesh(SimtwinObjectBase):
    """
    Represents a mesh
    """

    # pylint: disable=R0902
    def __init__(self, server, obj_index=None, geometry=None):
        self._msh_type = MeshType.LINEAR
        self._method = MeshingMethod.TET
        self._sizing = -1.
        self._nc = np.zeros([3, 0])
        self._inz = {}
        self._gp_loc = {}
        self._sj = {}
        self._srf_nodes = np.zeros(0, dtype=int)
        self._srf_inz = {}
        if isinstance(geometry, geo.Geometry):
            self._geometry = geometry
        elif isinstance(obj_index, int):
            self._geometry = None
        else:
            self._geometry = geo.Geometry(server)
        self.methods = {'generate': self.generate,
                        'export': self.export}
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        self.__lazy_pull__()
        res = True
        if not self.msh_type == other.msh_type and \
                self.method == other.method and \
                self.nc.shape == other.nc.shape:
            res = False
        if not (self.nc == other.nc).all():
            res = False
        if not utils.cmp_dict(self.inz, other.inz):
            res = False

        if not utils.cmp_dict(self.srf_inz, other.srf_inz):
            res = False

        for et, inz in self.inz.items():
            if not (inz.shape == other.inz[et].shape and (inz == other.inz[et]).all()):
                res = False

        for et, inz in self.srf_inz.items():
            if not (inz.shape == other.srf_inz[et].shape and (inz == other.srf_inz[et]).all()):
                res = False
        return res

    def __hash__(self):
        self.__lazy_pull__()
        return self.obj_index

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        data = self._msh_type.__serialize__()
        res += data

        data = self.method.__serialize__()
        res += data

        res += pack('<d', self.sizing)

        data = utils.obj_to_bytes(self._nc)
        res += len(data).to_bytes(8, 'little')
        res += data

        data = utils.serialize_dict(self._inz)
        res += len(data).to_bytes(8, 'little')
        res += data

        data = utils.serialize_dict(self._gp_loc)
        res += len(data).to_bytes(8, 'little')
        res += data

        data = utils.serialize_dict(self._sj)
        res += len(data).to_bytes(8, 'little')
        res += data

        data = utils.obj_to_bytes(self._srf_nodes)
        res += len(data).to_bytes(8, 'little')
        res += data

        data = utils.serialize_dict(self._srf_inz)
        res += len(data).to_bytes(8, 'little')
        res += data

        res += self.geometry.obj_index.to_bytes(8, 'little')
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8

        self._msh_type = MeshType(int.from_bytes(data[seeker:seeker + 8], 'little'))
        seeker += 8

        self._method = MeshingMethod(int.from_bytes(data[seeker:seeker + 8], 'little'))
        seeker += 8

        self._sizing = unpack('<d', data[seeker:seeker + 8])
        seeker += 8

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._nc = utils.deserialize_array(data[seeker:seeker + data_len])
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._inz = utils.deserialize_dict(data[seeker:seeker + data_len])
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._gp_loc = utils.deserialize_dict(data[seeker:seeker + data_len])
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._sj = utils.deserialize_dict(data[seeker:seeker + data_len])
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._srf_nodes = utils.deserialize_array(data[seeker:seeker + data_len])
        seeker += data_len

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._srf_inz = utils.deserialize_dict(data[seeker:seeker + data_len])
        seeker += data_len

        geometry_id = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        if isinstance(self.geometry, geo.Geometry):
            self.geometry.obj_index = geometry_id
        else:
            self.geometry = self._server.objs[geometry_id]

    def generate(self):
        """
        Generates the mesh for the object. Returns true if sucessfull.
        """
        if not self._server.is_remote_server:
            self._refresh_stamp += 1
            return True
        self.__lazy_pull__()
        res = self.call_method('generate', {}, "<class 'bool'>")
        return res

    def export(self, file_path):
        """
        Exports the mesh to a file. The format is inferred from the extension.
        """
        if '.' not in file_path:
            raise exceptions.DrqException('The provided file name has no extension')
        if not self._server.is_remote_server:
            return bytes()
        self.__lazy_pull__()
        res = self.call_method('export', {'file_path': file_path}, "<class 'bytes'>")
        with open(file_path, 'wb') as fp:
            fp.write(res)
        return True

    def to_gmsh(self):
        """
        Loads the mesh into gmsh
        """
        self.__lazy_pull__()
        entity = gmsh.model.addDiscreteEntity(3)
        if len(self.inz) > 0:
            if self.msh_type == MeshType.LINEAR:
                gmsh.model.mesh.setOrder(1)
            else:
                gmsh.model.mesh.setOrder(2)
        gmsh.model.mesh.addNodes(3, entity, np.arange(1, self.nc.shape[0] + 1), self.nc.reshape(-1))
        e = 1
        elem_tags = {}
        for et, inz in self.inz.items():
            elem_tags[et] = np.arange(e, e + inz.shape[0])
            e = inz.shape[0] + 1

        for et, inz in self.inz.items():
            gmsh.model.mesh.addElements(3, entity, [et], [elem_tags[et]], [inz.reshape(-1) + 1])

    def plot(self):
        """
        Plots the mesh using gmsh
        """
        self.__lazy_pull__()
        self.to_gmsh()
        gmsh.fltk.run()

    @property
    def method(self):
        """
        The used meshing method
        """
        self.__lazy_pull__()
        return self._method

    @method.setter
    def method(self, method):
        """
        The used meshing method
        """
        self._method = method
        self.__update_remote__()

    @property
    def sizing(self):
        """
        The sizing target for the mesh
        """
        self.__lazy_pull__()
        return self._sizing

    @sizing.setter
    def sizing(self, sizing):
        """
        The underlying geometry of the mesh
        """
        self._sizing = sizing
        self.__update_remote__()

    @property
    def geometry(self):
        """
        The underlying geometry of the mesh
        """
        self.__lazy_pull__()
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """
        The underlying geometry of the mesh
        """
        self._geometry = geometry
        self.__update_remote__()

    @property
    def msh_type(self):
        """
        Type of the mesh
        """
        self.__lazy_pull__()
        return self._msh_type

    @msh_type.setter
    def msh_type(self, msh_type):
        """
        Type of the mesh
        """
        self._msh_type = msh_type
        self.__update_remote__()

    @property
    def nc(self):
        """
        n x 3 matrix of all node coordinates of the mesh
        """
        self.__lazy_pull__()
        return self._nc

    @nc.setter
    def nc(self, nc):
        """
        n x 3 matrix of all node coordinates of the mesh
        """
        self._nc = nc
        self.__update_remote__()

    @property
    def inz(self):
        """
        inz is a dictionary of the incidence matrices for all element types of the mesh.
        Key of the dictionaries are the type IDs.
        """
        self.__lazy_pull__()
        return self._inz

    @inz.setter
    def inz(self, inz):
        """
        n x 3 matrix of all node coordinates of the mesh
        """
        self._inz = inz
        self.__update_remote__()

    @property
    def gp_loc(self):
        """
        Dictionary of the coordinates of all gauss points for each element and each element type.
        Key of the dictionaries are the type IDs.
        """
        self.__lazy_pull__()
        return self._gp_loc

    @property
    def sj(self):
        """
        Dictionary of the scaled jacobians of all gauss points for each element and each element type.
        Key of the dictionaries are the element type IDs.
        """
        self.__lazy_pull__()
        return self._sj

    @property
    def srf_nodes(self):
        """
        A vector of all node indices which are on the surface of the mesh
        """
        self.__lazy_pull__()
        return self._srf_nodes

    @property
    def srf_inz(self):
        """
        A dictionary with the incidence matrices of all surface element types.
        Key of the dictionaries are the surface element type IDs.
        """
        return self._srf_inz


@dataclass
class ElementType:
    """holdes information for one element type"""

    def __init__(self):
        self.obj_index = 0
        self.npe = 0
        self.ngp = 0
        self.shp = np.zeros([0, 0, 0])
        self.gp_loc = np.zeros([0, 3])
        self.node_loc = np.zeros([0, 3])
        self.weights = np.zeros(0)
