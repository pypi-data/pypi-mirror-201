import abml_helpers
from abaqusConstants import THREE_D, DEFORMABLE_BODY, XZPLANE  # noqa
from abaqusConstants import XYPLANE, YZPLANE, XZPLANE  # noqa
from abaqusConstants import MIDDLE_SURFACE, FROM_SECTION  # noqa
from abaqusConstants import ON, OFF, STANDALONE  # noqa
from regionToolset import Region
from abml_dataclass import Abml_Registry
from abml_dataclass import to_object_option_mode, to_object_key_mode, to_object_cmd_mode
from abml_helpers import Abml_Helpers
from abml_sketch import Abml_Sketch
from numpy import array, abs
from abaqus import mdb


@Abml_Registry.register("parts")
class Abml_Part:
    """
    A class representing a part in an Abaqus/Explicit model.

    Parameters
    ----------
    name : str
        The name of the part.
    model : :ref:`Abml_Model <Abml_Model>`
        The parent model to which the part belongs.
    **kwargs
        Additional keyword arguments that specify the geometry, planes, partitions,
        surfaces, sets, section assignments, and mesh associated with the part.

    Attributes
    ----------
    model : :ref:`Abml_Model <Abml_Model>`
        The parent model to which the part belongs.
    name : str
        The name of the part.
    geometry : abaqus.geom.GeometryObject or None
        The geometry object associated with the part, if any.
    planes : abaqus.core.AbaqusDict or None
        The planes associated with the part, if any.
    partitions : abaqus.core.AbaqusDict or None
        The partitions associated with the part, if any.
    surfaces : abaqus.core.AbaqusDict or None
        The surfaces associated with the part, if any.
    sets : abaqus.core.AbaqusDict or None
        The sets associated with the part, if any.
    section_assignments : abaqus.core.AbaqusDict or None
        The section assignments associated with the part, if any.
    mesh : abaqus.core.AbaqusDict or None
        The mesh associated with the part, if any.

    Methods
    -------
    create()
        Creates the part in the model.
    get_sequence_from_set_list(set_list)
        Returns a dictionary of sequences of faces, cells, and edges for the specified sets.
    generate_mesh()
        Generates the mesh for the part.

    """

    def __init__(self, name, model, **kwargs):  # noqa
        self.model = model
        self.name = name
        self.create()

        if self.name in model.parts:
            self.inherit(model.parts[self.name])

        geometry = kwargs.get("geometry")
        if geometry is not None:
            params = {
                "data": geometry,
                "type_": "geometry",
                "part": self,
            }
            self.geometry = to_object_option_mode(**params)

        planes = kwargs.get("planes")
        if planes is not None:
            params = {
                "data": planes,
                "type_": "planes",
                "part": self,
            }
            self.planes = to_object_key_mode(**params)

        partitions = kwargs.get("partitions")
        if partitions is not None:
            params = {
                "data": partitions,
                "type_": "partitions",
                "part": self,
            }
            self.partitions = to_object_cmd_mode(**params)

        surfaces = kwargs.get("surfaces")
        if surfaces is not None:
            params = {
                "data": surfaces,
                "type_": "surfaces",
                "part": self,
            }
            self.surfaces = to_object_key_mode(**params)
            # to_object_key_mode(**params)

        sets = kwargs.get("sets")

        if sets is not None:
            params = {
                "data": sets,
                "type_": "sets",
                "part": self,
            }
            self.sets = to_object_key_mode(**params)

        section_assignments = kwargs.get("section_assignments")
        if section_assignments is not None:
            params = {
                "data": section_assignments,
                "type_": "section_assignments",
                "part": self,
            }
            self.section_assignments = to_object_key_mode(**params)

        mesh = kwargs.get("mesh")
        if mesh is not None:
            params = {
                "data": mesh,
                "type_": "mesh",
                "part": self,
            }

            self.mesh = to_object_cmd_mode(**params)
            self.generate_mesh()

    def inherit(self, other):
        if isinstance(other, Abml_Part):
            for attr in dir(other):
                if not attr.startswith("__") and not callable(getattr(other, attr)):
                    setattr(self, attr, getattr(other, attr))

    def create(self):
        if self.name not in self.model.parts.keys():
            self.model.m.Part(dimensionality=THREE_D, name=self.name, type=DEFORMABLE_BODY)

    def get_sequence_from_set_list(self, set_list):
        face_seq = None
        cell_seq = None
        edge_seq = None
        for set_ in set_list:
            seq = self.model.p[self.name].sets[set_].faces
            if face_seq is None:
                face_seq = seq
            else:
                face_seq += seq

            seq = self.model.p[self.name].sets[set_].cells
            if cell_seq is None:
                cell_seq = seq
            else:
                cell_seq += seq

            seq = self.model.p[self.name].sets[set_].edges
            if edge_seq is None:
                edge_seq = seq
            else:
                edge_seq += seq

        kwargs = {
            "faces": face_seq,
            "cells": cell_seq,
            "edges": edge_seq,
        }

        return kwargs

    def generate_mesh(self):
        self.model.p[self.name].generateMesh()


@Abml_Registry.register("geometry")
class Abml_Geometry(Abml_Helpers):
    """
    A class for creating geometries in Abaqus/CAE.

    Parameters
    ----------
    type : str
        | The type of geometry to create. Possible values are
        | solid_extrusion
        | solid_revolve
    sketch : dict
        A dictionary containing the data for the sketch to create the geometry.
    part : Part object
        The part in which to create the geometry.
    **kwargs
        Additional keyword arguments to pass to the geometry creation function.

    Methods
    -------
    create()
        Creates the geometry using the appropriate creation function based on the specified type.

    Notes
    -----
    This class is intended to be used with the Abaqus finite element analysis software.

    Examples
    --------
    part_1:
      geometry:
        type: solid_extrusion
        sketch:
          - rect:
            p1: [0.0, 0.0]
            p2: [1.0, 1.0]
        depth: 1.0
    """

    def __init__(self, type, part, **kwargs):  # noqa
        self.type = type
        self.part = part
        self.model = part.model
        self.kwargs = kwargs
        self.sketch_name = self.kwargs.get("sketch_name", "__profile__")
        params = {"data": kwargs.get("sketch", []), "type_": "sketch", "model": self.model, "name": self.sketch_name}
        self.sketch = to_object_cmd_mode(**params)

        self.map = {
            ("3d", "deformable", "solid_extrusion"): self._create_solid_extrusion,
            ("3d", "deformable", "solid_revolve"): self._create_solid_revolve,
        }

        self.create()

    def create(self):
        self.map[("3d", "deformable", self.type)]()

    def _create_solid_extrusion(self):
        if not isinstance(self.kwargs["depth"], (int, float)) or self.kwargs["depth"] == 0.0:
            error_str = "Extrusion depth for part: {} is no int, float or is 0".format(self.part.name)
            raise ValueError(error_str)
        part = self.model.p[self.part.name]
        sketch = self.model.m.sketches[self.sketch_name]
        part.BaseSolidExtrude(depth=self.kwargs["depth"], sketch=sketch)

        if "__profile__" in self.model.m.sketches:
            del self.model.m.sketches["__profile__"]

        self.aliases = {}

    def _create_solid_revolve(self):
        self.sketch[0].create_construction_line()
        if not isinstance(self.kwargs["angle"], (int, float)) or self.kwargs["angle"] == 0.0:
            error_str = "Revolve angle for part: {} is no int, float or is 0".format(self.part.name)
            raise ValueError(error_str)
        part = self.model.p[self.part.name]
        sketch = self.model.m.sketches[self.sketch_name]

        part.BaseSolidRevolve(angle=self.kwargs["angle"], sketch=sketch, flipRevolveDirection=OFF)
        del mdb.models["m1"].sketches[self.sketch_name]

        if "__profile__" in self.model.m.sketches:
            del self.model.m.sketches["__profile__"]

        self.aliases = {}

    def get_face_sequence(self, element):
        part = self.model.p[self.part.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            face = part.faces.findAt(element.astype(float))  # noqa
            if face is not None:
                seq = Region(side1Faces=part.faces[face.index : face.index + 1]).side1Faces
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            faces = part.faces.getByBoundingBox(*element.astype(float))
            if len(faces) != 0:
                seq = faces
        elif isinstance(element.item(0), str):  # getByBoundingBox str
            if any(item == element.item(0) for item in ["all"]):
                seq = part.faces[:]
            elif any(item == element.item(0) for item in part.surfaces.keys()):
                seq = part.surfaces[element.item(0)].faces
            else:
                boundaries = self.get_boundary_rect(self.sketch[0], self.kwargs["depth"], element.item(0))
                seq = part.faces.getByBoundingBox(*boundaries)

        return seq

    def get_cell_sequence(self, element):
        part = self.model.p[self.part.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            cell = part.cells.findAt(element.astype(float))
            if cell is not None:
                seq = Region(cells=part.cells[cell.index : cell.index + 1]).cells
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            cells = part.cells.getByBoundingBox(*element.astype(float))
            if len(cells) != 0:
                seq = cells
        elif isinstance(element.item(0), str):  # getByBoundingBox
            if element.item(0) == "all":
                seq = part.cells[:]
            else:
                boundaries = self.get_boundary_rect(self.sketch[0], self.kwargs["depth"], element.item(0))
                seq = part.cells.getByBoundingBox(*boundaries)
        return seq

    def get_edge_sequence(self, element):
        part = self.model.p[self.part.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            edge = part.edges.findAt(element.astype(float))
            if isinstance(edge, type(None)):
                seq = None
            else:
                seq = Region(edges=part.edges[edge.index : edge.index + 1]).edges
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            edges = part.edges.getByBoundingBox(*element.astype(float))
            if len(edges) != 0:
                seq = edges
        elif isinstance(element.item(0), str):  # getByBoundingBox
            if any(item == element.item(0) for item in ["all"]):
                seq = part.edges[:]
            else:
                boundaries = self.get_boundary_rect(self.sketch[0], self.kwargs["depth"], element.item(0))
                seq = part.edges.getByBoundingBox(*boundaries)

        return seq

    def get_set_sequence_edges(self, element):
        return Region(edges=self.model.p[self.part.name].sets[element].edges).edges

    def get_set_sequence_cells(self, element):
        return Region(cells=self.model.p[self.part.name].sets[element].cells).cells

    def get_set_sequence_faces(self, element):
        return Region(side1Faces=self.model.p[self.part.name].sets[element].faces).faces

    def get_sequence_from_list(self, elements, type_):
        sequence_map = {
            "cell": self.get_cell_sequence,
            "face": self.get_face_sequence,
            "edge": self.get_edge_sequence,
            "set_edges": self.get_set_sequence_edges,
            "set_faces": self.get_set_sequence_faces,
            "set_cells": self.get_set_sequence_cells,
        }

        type_seq = None
        for element in elements:
            if len(element) != 0:
                seq = sequence_map[type_](element)
                if type_seq is None:
                    type_seq = seq
                else:
                    type_seq += seq
        return type_seq


@Abml_Registry.register("planes")
class Abml_Plane:
    """
    A class to create datum planes in Abaqus.

    Parameters
    ----------
    name : str
        The name of the datum plane to be created.
    part : Abml_Part
        The Abml_Part object to which the datum plane belongs.
    **kwargs : dict
        Additional keyword arguments to be passed to the Abaqus API. The keys of the dictionary should be the names of
        the principal planes ('x', 'y', or 'z'), and the values should be the offsets of the datum planes from the
        origin in the corresponding directions.

    Attributes
    ----------
    name : str
        The name of the datum plane.
    part : Abml_Part
        The Abml_Part object to which the datum plane belongs.
    model : Abml_Model
        The Abml_Model object to which the datum plane belongs.
    kwargs : dict
        The keyword arguments passed to the Abaqus API.
    _principal_Plane : dict
        A dictionary mapping the names of the principal planes ('x', 'y', or 'z') to the corresponding constants in
        the Abaqus API.

    Methods
    -------
    create()
        Create the datum plane in the Abaqus model.

    Notes
    -----
    This class uses the Abaqus API to create datum planes in Abaqus. The datum planes are created in the part
    specified by the `part` parameter. The position and orientation of the datum planes are specified by the
    `**kwargs` parameter. The keys of the `**kwargs` parameter should be the names of the principal planes ('x', 'y',
    or 'z'), and the values should be the offsets of the datum planes from the origin in the corresponding directions.
    """

    def __init__(self, name, part, **kwargs):  # noqa
        self.name = name
        self.part = part
        self.model = part.model
        self.kwargs = kwargs

        self._principal_Plane = {"x": YZPLANE, "y": XZPLANE, "z": XYPLANE}
        self.create()

    def create(self):
        part = self.model.p[self.part.name]
        for key, value in self.kwargs.items():
            part.DatumPlaneByPrincipalPlane(offset=value, principalPlane=self._principal_Plane[key])
            part.features.changeKey(fromName="Datum plane-1", toName=self.name)  # noqa


@Abml_Registry.register("partitions")
class Abml_Partition(Abml_Helpers):
    """
    A class for partitioning parts in Abaqus based on faces, edges, and cells.

    Parameters
    ----------
    part : abaqus Part object
        The part to be partitioned.
    faces : list of ints, optional
        A list of face IDs to be partitioned. Defaults to None.
    edges : list of ints, optional
        A list of edge IDs to be partitioned. Defaults to None.
    cells : list of ints, optional
        A list of cell IDs to be partitioned. Defaults to None.
    **kwargs : dict
        Optional keyword arguments to be passed to the partitioning function. The supported
        keys are 'cmd' (str) and 'planes' (list of str). 'cmd' specifies the partitioning
        method to use, and 'planes' is a list of datum plane feature IDs.

    Attributes
    ----------
    method : str
        The partitioning method to use.
    part : abaqus Part object
        The part to be partitioned.
    model : abaqus Model object
        The model containing the part to be partitioned.
    faces : list of lists of ints or str
        A list of face IDs to be partitioned. If None, no faces are partitioned.
    edges : list of lists of ints or str
        A list of edge IDs to be partitioned. If None, no edges are partitioned.
    cells : list of lists of ints or str
        A list of cell IDs to be partitioned. If None, no cells are partitioned.
    kwargs : dict
        Optional keyword arguments passed to the partitioning function.
    partition_map : dict
        A dictionary containing the partitioning method names and their corresponding
        partitioning functions.

    Methods
    -------
    create()
        Calls the partitioning function specified by 'method'.
    create_face_plane()
        Partitions the faces of the part by a datum plane.

    """

    def __init__(self, part, faces=None, edges=None, cells=None, **kwargs):
        self.method = kwargs.get("cmd", "plane")
        self.part = part
        self.model = part.model
        self.faces = self.convert_position_list(faces)
        self.edges = self.convert_position_list(edges)
        self.cells = self.convert_position_list(cells)
        self.kwargs = kwargs
        self.partition_map = {"plane": self.create_face_plane}

        self.create()

    def create(self):
        self.partition_map[self.method]()

    def create_face_plane(self):
        part_ = self.model.p[self.part.name]
        planes = array([self.kwargs.get("planes", [])]).flatten()

        for plane in planes:
            id_ = part_.features[plane].id

            if self.faces is not None:
                face_seq = self.part.geometry.get_sequence_from_list(self.faces, "face")
                if face_seq is not None:
                    try:
                        part_.PartitionFaceByDatumPlane(datumPlane=part_.datums[id_], faces=face_seq)
                    except Exception as e:
                        error_msg = """
                        part_name: {part_name}
                        number of face seq found: {num_face_seq}
                        plane: {plane}

                        {e}
                        """.format(
                            part_name=self.part.name,
                            e=e,
                            num_face_seq=len(face_seq),
                            plane=plane,
                        )
                        raise ValueError(error_msg)

            if self.cells is not None:
                cell_seq = self.part.geometry.get_sequence_from_list(self.cells, "cell")
                if cell_seq is not None:
                    part_.PartitionCellByDatumPlane(datumPlane=part_.datums[id_], cells=cell_seq)

            if self.edges is not None:
                edge_seq = self.part.geometry.get_sequence_from_list(self.edges, "edge")
                if edge_seq is not None:
                    part_.PartitionEdgeByDatumPlane(datumPlane=part_.datums[id_], edges=edge_seq)


@Abml_Registry.register("surfaces")
class Abml_Surface(Abml_Helpers):
    def __init__(self, name, faces, part, **kwargs):
        self.name = name
        self.part = part
        self.model = self.part.model
        self.faces = self.convert_position_list(faces)

        self.create()

    def create(self):
        part = self.model.p[self.part.name]

        try:
            face_seq = self.part.geometry.get_sequence_from_list(self.faces, "face")
        except AttributeError:
            face_seq = self.part.model.parts[self.part.name].geometry.get_sequence_from_list(self.faces, "face")

        try:
            part.Surface(side1Faces=face_seq, name=self.name)
        except Exception as e:
            error_msg = """
            surface_name: {name}
            faces_inp: {faces}
            face_seq: {face_seq}
            part: {part}
            {e}
            """.format(
                name=self.name,
                faces=self.faces,
                face_seq=face_seq,
                part=self.part.name,
                e=e,
            )
            raise ValueError(error_msg)


@Abml_Registry.register("sets")
class Abml_Sets(Abml_Helpers):
    def __init__(self, name, part, faces=[], edges=[], cells=[]):
        self.name = name
        self.part = part
        self.model = part.model
        self.faces = self.convert_position_list(faces)
        self.edges = self.convert_position_list(edges)
        self.cells = self.convert_position_list(cells)
        self.create()

    def create(self):
        part = self.model.p[self.part.name]

        kwargs = {}
        face_seq = self.part.geometry.get_sequence_from_list(self.faces, "face")
        if face_seq is not None:
            kwargs["faces"] = face_seq

        cell_seq = self.part.geometry.get_sequence_from_list(self.cells, "cell")
        if cell_seq is not None:
            kwargs["cells"] = cell_seq

        edge_seq = self.part.geometry.get_sequence_from_list(self.edges, "edge")
        if edge_seq is not None:
            kwargs["edges"] = edge_seq

        part.Set(name=self.name, **kwargs)


@Abml_Registry.register("section_assignments")
class Abml_Section_Assignments(Abml_Helpers):
    def __init__(self, name, part, cells=None, sets=None):
        self.name = name
        self.part = part
        self.model = part.model

        self.cells = self.convert_position_list(cells)
        self.sets = self.convert_position_list(sets)
        self.create()

    def create(self):
        cell_seq = self.part.geometry.get_sequence_from_list(self.cells, "cell")
        if self.sets is not None:
            set_seq = self.part.get_sequence_from_set_list(self.sets)["cells"]
            if set_seq is not None:
                cell_seq += set_seq

        kwargs = {
            "sectionName": self.name,
            "offset": 0.0,
            "offsetType": MIDDLE_SURFACE,
            "offsetField": "",
            "thicknessAssignment": FROM_SECTION,
            "region": Region(cells=cell_seq),
        }

        self.model.p[self.part.name].SectionAssignment(**kwargs)
