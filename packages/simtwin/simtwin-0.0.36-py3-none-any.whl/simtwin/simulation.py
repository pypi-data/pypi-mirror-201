"""
Contains classes to configure and run simulations
"""

# pylint: disable=C0103

from struct import pack, unpack
import numpy as np
import gmsh
from . import utils
from . import geometry as geo
from . import mesh
from .simtwin_base_classes import SimtwinEnum, SimtwinObjectBase

if not gmsh.isInitialized():
    gmsh.initialize()


class BcType(SimtwinEnum):
    """
    Types of boundary conditions
    """
    FORCE = 1
    DEFLECTION = 2


class SolutionType(SimtwinEnum):
    """
    Available types of solutions
    """
    DEFLECTION = 1
    STRESS = 2
    STRAIN = 3
    SJ = 4


class Simulation(SimtwinObjectBase):
    """
    Represents a simulation.
    """

    # pylint: disable=R0902

    def __init__(self, server, obj_index=None):
        if isinstance(obj_index, int):
            self._geometry = None
            self._mesh = None
        else:
            self._geometry = geo.Geometry(server)
            self._mesh = mesh.Mesh(server, geometry=self._geometry)
        self._t_e = 1.
        self._bcs = []
        self._questions = {}
        self._coordinate_systems = [CoordinateSystem(server)]
        self.methods = {'solve': self.solve}
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        self.__lazy_pull__()
        return self.geometry == other.geometry and \
            self.mesh == other.mesh and \
            self.t_e == other.t_e and \
            self.bcs == other.bcs and \
            utils.cmp_dict(self.questions, other.questions) and \
            utils.cmp_list(self.coordinate_systems, other.coordinate_systems)

    def __hash__(self):
        self.__lazy_pull__()
        return self.obj_index

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        res += self.geometry.obj_index.to_bytes(8, 'little')
        res += self.mesh.obj_index.to_bytes(8, 'little')
        res += pack('<d', self.t_e)
        bc_IDs = utils.get_id_list(self.bcs)
        bcs_bytes = utils.serialize_list(bc_IDs)
        res += int.to_bytes(len(bcs_bytes), 8, 'little')
        res += bcs_bytes

        question_dict = {}
        for q, a in self.questions.items():
            question_dict[q.obj_index] = a.obj_index

        question_bytes = utils.serialize_dict(question_dict)

        res += int.to_bytes(len(question_bytes), 8, 'little')
        res += question_bytes
        cs_list = [item.obj_index for item in self.coordinate_systems]
        cs_bytes = utils.serialize_list(cs_list)
        res += int.to_bytes(len(cs_bytes), 8, 'little')
        res += cs_bytes
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8

        obj_id = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        if isinstance(self.geometry, geo.Geometry):
            self.geometry = self._server.objs[obj_id]
        else:
            self.geometry = self._server.objs[obj_id]

        obj_id = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        if isinstance(self.mesh, mesh.Mesh):
            self.mesh = self._server.objs[obj_id]
        else:
            self.mesh = self._server.objs[obj_id]
        self.mesh.obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')

        self._t_e = unpack('<d', data[seeker:seeker + 8])[0]
        seeker += 8

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_bytes = data[seeker:seeker + data_len]
        seeker += data_len
        bc_list = utils.deserialize_list(data_bytes)
        self._bcs = []
        for obj_id in bc_list:
            self._bcs += [self._server.objs[obj_id]]

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_bytes = data[seeker:seeker + data_len]
        seeker += data_len
        question_dct = utils.deserialize_dict(data_bytes)
        for q_obj_index, s_obj_index in question_dct.items():
            self._questions[self._server.objs[q_obj_index]] = self._server.objs[s_obj_index]

        data_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        data_bytes = data[seeker:seeker + data_len]
        cs_list = utils.deserialize_list(data_bytes)
        self._coordinate_systems = []
        for obj_id in cs_list:
            self._coordinate_systems += [self._server.objs[obj_id]]

    @property
    def mesh(self):
        """
        contains the current mesh for the geometry
        """
        self.__lazy_pull__()
        return self._mesh

    @mesh.setter
    def mesh(self, msh):
        self._mesh = msh
        self.__update_remote__()

    @property
    def questions(self):
        """
        Dictionary of all questions associated with the simulation.
        Answers are values of the dictionary. Open questions have the value None.
        """
        self.__lazy_pull__()
        return self._questions

    @questions.setter
    def questions(self, questions):
        self._questions = questions
        self.__update_remote__()

    @property
    def geometry(self):
        """
        contains the current geometry of the simulation
        """
        self.__lazy_pull__()
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        self._geometry = geometry
        self.__update_remote__()

    @property
    def t_e(self):
        """
        contains the current geometry of the simulation
        """
        self.__lazy_pull__()
        return self._t_e

    @t_e.setter
    def t_e(self, t_e):
        self._t_e = t_e
        self.__update_remote__()

    @property
    def bcs(self):
        """
        contains the current geometry of the simulation
        """
        self.__lazy_pull__()
        return self._bcs

    @bcs.setter
    def bcs(self, bcs):
        self._bcs = bcs
        self.__update_remote__()

    @property
    def coordinate_systems(self):
        """
        contains the current geometry of the simulation
        """
        self.__lazy_pull__()
        return self._coordinate_systems

    @coordinate_systems.setter
    def coordinate_systems(self, coordinate_Systems):
        self._coordinate_systems = coordinate_Systems
        self.__update_remote__()

    def solve(self, base_solution=None):
        """
        Solves the simulation
        """
        self.__lazy_pull__()
        if not self._server.is_remote_server:
            return True
        res = self.call_method('solve', {'base_solution': base_solution}, "<class 'bool'>")
        return res


class CoordinateSystemType(SimtwinEnum):
    """
    Types of geometry selection
    """
    CARTESIAN = 0
    CYLINDER = 1
    SPHERE = 2


class CoordinateSystem(SimtwinObjectBase):
    """
    Represents a coordinate system within the simulation
    """

    # pylint: disable=R0913
    def __init__(self, server, origin=np.array([0., 0., 0.]),
                 dirs=np.array([[1., 0., 0.], [0., 1., 0.]]), cs_type=CoordinateSystemType.CARTESIAN, base_cs=None,
                 obj_index=None):
        self._cs_type = cs_type
        self._origin = origin
        self._dirs = dirs
        self._base_cs = base_cs
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        self.__lazy_pull__()
        if not (self.cs_type == other.cs_type and
                (self.origin == other.origin).all() and
                (self.dirs == other.dirs).all()):
            return False
        if self.base_cs is None and other.base_cs is None:
            return True
        if self.base_cs is None and isinstance(other.base_cs, CoordinateSystem) or \
                other.base_cs is None and isinstance(self.base_cs, CoordinateSystem):
            return False
        return self.base_cs.obj_index == other.base_cs.obj_index

    def __hash__(self):
        self.__lazy_pull__()
        return self.obj_index

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        res += self.cs_type.value.to_bytes(8, 'little')
        arr_data = utils.serialize_array(self.origin)
        res += len(arr_data).to_bytes(8, 'little')
        res += arr_data
        arr_data = utils.serialize_array(self.dirs)
        res += len(arr_data).to_bytes(8, 'little')
        res += arr_data
        res += (self._base_cs is None).to_bytes(1, 'little')
        if self._base_cs is None:
            res += (0).to_bytes(8, 'little')
        else:
            res += self.base_cs.obj_index.to_bytes(8, 'little')
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._cs_type = CoordinateSystemType(int.from_bytes(data[seeker:seeker + 8], 'little'))
        seeker += 8
        arr_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._origin = utils.deserialize_array(data[seeker:seeker + arr_len])
        seeker += arr_len
        arr_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._dirs = utils.deserialize_array(data[seeker:seeker + arr_len])
        seeker += arr_len
        no_base_cs_present = bool.from_bytes(data[seeker:seeker+1], 'little')
        seeker += 1
        if no_base_cs_present:
            self._base_cs = None
        else:
            base_cs_id = int.from_bytes(data[seeker:seeker + 8], 'little')
            self._base_cs = self._server.objs[base_cs_id]

    @property
    def dirs(self):
        """
        Directions of the basis vectors of the coordinate system in the base coordinate system
        """
        self.__lazy_pull__()
        return self._dirs

    @dirs.setter
    def dirs(self, dirs):
        """
        Directions of the basis vectors of the coordinate system in the base coordinate system
        """
        self._dirs = dirs
        self.__update_remote__()

    @property
    def cs_type(self):
        """
        Type of the coordinate system
        """
        self.__lazy_pull__()
        return self._cs_type

    @cs_type.setter
    def cs_type(self, cs_type):
        """
        Type of the coordinate system
        """
        self._cs_type = cs_type
        self.__update_remote__()

    @property
    def origin(self):
        """
        Origin of the coordinate system in the base coordinate system
        """
        self.__lazy_pull__()
        return self._origin

    @origin.setter
    def origin(self, origin):
        """
        Origin of the coordinate system in the base coordinate system
        """
        self._origin = origin
        self.__update_remote__()

    @property
    def base_cs(self):
        """
        Base coordinate system of the coordinate system.
        If none the global CS is used
        """
        self.__lazy_pull__()
        return self._base_cs

    @base_cs.setter
    def base_cs(self, base_cs):
        """
        Base coordinate system of the coordinate system
        If none the global CS is used
        """
        self._base_cs = base_cs
        self.__update_remote__()


class BC(SimtwinObjectBase):
    """
    Represents a boundary condition
    """

    # pylint: disable=R0913
    def __init__(self, server, bc_type=BcType.FORCE, geometry_selection=None, t=np.array([[0, 1]]),
                 values=np.zeros((1, 3)), coordinate_system=None, obj_index=None):
        if not isinstance(geometry_selection, geo.GeometrySelection):
            geometry_selection = geo.GeometrySelection(server, geometry_id=0)
        if not isinstance(coordinate_system, CoordinateSystem):
            coordinate_system = CoordinateSystem(server)
        self._bc_type = bc_type
        self._geometry_selection = geometry_selection
        self._t = t
        self._values = values
        self._coordinate_system = coordinate_system
        super().__init__(server, obj_index)

    @property
    def geometry(self):
        """
        Reference to the geometry of the boundary condition
        """
        self.__lazy_pull__()
        return self._geometry_selection

    @geometry.setter
    def geometry(self, geometry):
        """
        Reference to the geometry of the boundary condition
        """
        self._geometry_selection = geometry
        self.__update_remote__()

    @property
    def bc_type(self):
        """
        Type of the boundary condition
        """
        self.__lazy_pull__()
        return self._bc_type

    @bc_type.setter
    def bc_type(self, bc_type):
        """
        Type of the boundary condition
        """
        self._bc_type = bc_type
        self.__update_remote__()

    @property
    def t(self):
        """
        time scope as 2xn numpy array
        first columns are start time second end times
        """
        self.__lazy_pull__()
        return self._t

    @t.setter
    def t(self, t):
        """
        time scope as 2xn numpy array
        first columns are start time second end times
        """
        self._t = t
        self.__update_remote__()

    @property
    def values(self):
        """
        3xn numpy array of values to be assigned for each time slot
        """
        self.__lazy_pull__()
        return self._values

    @values.setter
    def values(self, values):
        """
        3xn numpy array of values to be assigned for each time slot
        """
        self._values = values
        self.__update_remote__()

    @property
    def coordinate_system(self):
        """
        Coordinate system for the boundary condition
        """
        self.__lazy_pull__()
        return self._coordinate_system

    @coordinate_system.setter
    def coordinate_system(self, coordinate_system):
        """
        Coordinate system for the boundary condition
        """
        self._coordinate_system = coordinate_system
        self.__update_remote__()

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        self.__lazy_pull__()
        return self.bc_type == other.bc_type and \
            self._geometry_selection == other.geometry and \
            (self.t == other.t).all() and \
            (self.values == other.values).all() and \
            self.coordinate_system == other.coordinate_system

    def __hash__(self):
        self.__lazy_pull__()
        return self.obj_index

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        res += int.to_bytes(self.bc_type.value, 8, 'little')
        res += int.to_bytes(self._geometry_selection.obj_index, 8, 'little')
        arr_bytes = utils.serialize_array(self.t)
        res += int.to_bytes(len(arr_bytes), 8, 'little')
        res += arr_bytes
        arr_bytes = utils.serialize_array(self.values)
        res += int.to_bytes(len(arr_bytes), 8, 'little')
        res += arr_bytes
        res += self.coordinate_system.obj_index.to_bytes(8, 'little')
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._bc_type = BcType(int.from_bytes(data[seeker:seeker + 8], 'little'))
        seeker += 8
        self._geometry_selection.obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        arr_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._t = utils.deserialize_array(data[seeker:seeker + arr_len])
        seeker += arr_len
        arr_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._values = utils.deserialize_array(data[seeker:seeker + arr_len])
        seeker += arr_len
        cs_ID = int.from_bytes(data[seeker:seeker + 8], 'little')
        self._coordinate_system = self._server.objs[cs_ID]


class Question(SimtwinObjectBase):
    """
    Represents a solution of a simulation
    """
    # pylint: disable=R0913
    def __init__(self, server, t=np.array([1.]), solution_type=SolutionType.DEFLECTION,
                 pnts=np.zeros([0, 3]), obj_index=None):
        self._t = t
        self._pnts = pnts
        self._solution_type = solution_type
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        self.__lazy_pull__()
        return (self.t == other.t).all() and (
                    self.pnts == other.pnts).all() and self.solution_type == other.solution_type

    def __hash__(self):
        self.__lazy_pull__()
        return self.obj_index

    @property
    def t(self):
        """
        Numpy vector listing all times for which the question is to be answered
        """
        self.__lazy_pull__()
        return self._t

    @t.setter
    def t(self, t):
        """
        Numpy vector listing all times for which the question is to be answered
        """
        self._t = t
        self.__update_remote__()

    @property
    def pnts(self):
        """
        3xn numpy array listing all special points for which the question is to be answered
        """
        self.__lazy_pull__()
        return self._pnts

    @pnts.setter
    def pnts(self, pnts):
        """
        3xn numpy array listing all special points for which the question is to be answered
        """
        self._pnts = pnts
        self.__update_remote__()

    @property
    def solution_type(self):
        """
        Type of solution
        """
        self.__lazy_pull__()
        return self._solution_type

    @solution_type.setter
    def solution_type(self, solution_type):
        """
        Type of solution
        """
        self._solution_type = solution_type
        self.__update_remote__()

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        arr_bytes = utils.serialize_array(self.t)
        res += int.to_bytes(len(arr_bytes), 8, 'little')
        res += arr_bytes
        res += int.to_bytes(self.solution_type.value, 8, 'little')
        arr_bytes = utils.serialize_array(self.pnts)
        res += int.to_bytes(len(arr_bytes), 8, 'little')
        res += arr_bytes
        return res

    def __deserialize__(self, data):
        seeker = 0
        self._obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        arr_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._t = utils.deserialize_array(data[seeker:seeker + arr_len])
        seeker += arr_len
        self._solution_type = SolutionType(int.from_bytes(data[seeker:seeker + 8], 'little'))
        seeker += 8
        arr_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._pnts = utils.deserialize_array(data[seeker:seeker + arr_len])
        seeker += arr_len


class Solution(SimtwinObjectBase):
    """
    Represents a solution to a question brought up for a simulation
    """
    def __init__(self, server, obj_index=None):
        self._val = np.zeros([0])
        super().__init__(server, obj_index)

    def __eq__(self, other):
        if self.refresh_stamp == -1 or other.refresh_stamp == -1:
            return self.obj_index == other.obj_index
        self.__lazy_pull__()
        return (self.val == other.val).all()

    def __hash__(self):
        self.__lazy_pull__()
        return self.obj_index

    @property
    def val(self):
        """
        Values of the solution as multidimensional numpy array:
        time slot index
        pnt index
        solution date in all following dimensions
        """
        self.__lazy_pull__()
        return self._val

    def __serialize__(self):
        res = bytes()
        res += self.obj_index.to_bytes(8, 'little')
        arr_data = utils.serialize_array(self.val)
        res += len(arr_data).to_bytes(8, 'little')
        res += arr_data
        return res

    def __deserialize__(self, data):
        seeker = 0
        self.obj_index = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        arr_len = int.from_bytes(data[seeker:seeker + 8], 'little')
        seeker += 8
        self._val = utils.deserialize_array(data[seeker:seeker + arr_len])
