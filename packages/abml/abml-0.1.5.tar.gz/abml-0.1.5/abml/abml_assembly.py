from regionToolset import Region
from abml_dataclass import Abml_Registry, to_object_key_mode, to_object_cmd_mode
from abml_helpers import Abml_Helpers, cprint
from abaqusConstants import ON, OFF, CARTESIAN
from abaqusConstants import DELETE, SUPPRESS
from numpy import array


@Abml_Registry.register("assembly")
class Abml_Assembly(Abml_Helpers):
    def __init__(self, model, **kwargs):  # noqa
        self.model = model
        instances = kwargs.get("instances")
        surfaces = kwargs.get("surfaces")
        sets = kwargs.get("sets")
        cut = kwargs.get("cut")
        if instances is not None:
            self.instances = to_object_key_mode(instances, "instances", model=self.model)
        if cut is not None:
            self.cuts = to_object_key_mode(cut, "cut", model=self.model)
        if surfaces is not None:
            self.surfaces = to_object_key_mode(surfaces, "assembly_surfaces", model=model, assembly=self)
        if sets is not None:
            self.sets = to_object_key_mode(sets, "assembly_sets", model=model, assembly=self)
        # if commands is not None:
        #     self.commands = to_object_cmd_mode(commands, "assembly_commands", model=model, assembly=self)

    def get_seq_from_surface_list(self, surfaces):
        surfaces = self.convert_position_list(surfaces)
        instances = self.instances
        face_seq = None

        if surfaces is not None:
            surface_keys = set(surfaces) & set(self.model.a.surfaces.keys())
            for surface_key in surface_keys:
                seq = self.model.a.surfaces[surface_key]
                if face_seq is None:
                    face_seq = seq
                else:
                    face_seq += seq

            faces = (set(surfaces) ^ set(self.model.a.surfaces.keys())) & set(surfaces)
            for instance in instances.values():
                seq = instance.get_sequence_from_list(faces, "face")
                if face_seq is None:
                    face_seq = seq
                elif seq is not None:
                    face_seq += seq
            return face_seq
        return None

    def get_seq_from_edge_list(self, edges):
        edges = self.convert_position_list(edges)
        instances = self.instances
        edge_seq = None

        edge_keys = set(edges) & set(self.model.a.sets.keys())
        for edge_key in edge_keys:
            seq = self.model.a.sets[edge_key].edges
            if edge_seq is None:
                edge_seq = seq
            else:
                edge_seq += seq

        edges_ = (set(edges) ^ set(self.model.a.sets.keys())) & set(edges)
        for instance in instances.values():
            seq = instance.get_sequence_from_list(edges_, "edge")
            if edge_seq is None:
                edge_seq = seq
            elif seq is not None:
                edge_seq += seq
        return edge_seq

    def get_seq_from_cell_list(self, cells):
        cells = self.convert_position_list(cells)
        instances = self.instances
        cell_seq = None

        cell_keys = set(cells) & set(self.model.a.sets.keys())
        for cell_key in cell_keys:
            seq = self.model.a.sets[cell_key].cells
            if cell_seq is None:
                cell_seq = seq
            else:
                cell_seq += seq

        cell_ = (set(cells) ^ set(self.model.a.sets.keys())) & set(cells)
        for instance in instances.values():
            seq = instance.get_sequence_from_list(cell_, "cell")
            if cell_seq is None:
                cell_seq = seq
            elif seq is not None:
                cell_seq += seq
        return cell_seq


@Abml_Registry.register("cut")
class Abml_Cut:
    def __init__(self, name, model, **kwargs):
        self.model = model
        self.name = name
        self.instances = array([kwargs["instance"]]).flatten()
        self.cutters = array([kwargs["cutter"]]).flatten()
        self.original_instance = kwargs.get("original_instance", "delete")

        self.original_instance_map = {"delete": DELETE, "surpress": SUPPRESS, "place": SUPPRESS}

        self.create()

    def create(self):
        cutting_instances = [self.model.a.instances[cutter] for cutter in self.cutters]

        for instance in self.instances:
            self.model.a.InstanceFromBooleanCut(
                name="{}-1".format(self.name),
                instanceToBeCut=self.model.a.instances[instance],
                cuttingInstances=cutting_instances,
                originalInstances=self.original_instance_map[self.original_instance],
            )
            if self.name in self.model.p:
                del self.model.p[self.name]
            self.model.p.changeKey(fromName="{}-1".format(self.name), toName=self.name)

        if self.original_instance == "place":
            del self.model.a.instances[self.name]
            self.model.a.features.changeKey(fromName="{}-1-1".format(self.name), toName=self.name)
            for cutter in cutting_instances:
                self.model.a.features[cutter.name].resume()


@Abml_Registry.register("instances")
class Abml_Instance:
    def __init__(self, name, model, part, **kwargs):
        self.model = model
        self.name = name
        self.part = part
        self.dependent = kwargs.get("dependent", True)
        self.translate = kwargs.get("translate", [0, 0, 0])
        self.rotate = kwargs.get("rotate", [])
        self.create()

    def create(self):
        dep_dict = {False: OFF, True: ON}

        self.model.a.DatumCsysByDefault(CARTESIAN)
        self.model.a.Instance(dependent=dep_dict[self.dependent], name=self.name, part=self.model.p[self.part])

        if len(self.rotate) != 0:
            for rot_param in self.rotate:
                angle = rot_param.get("angle")
                axisDirection = rot_param.get("axis_direction")
                axisPoint = rot_param.get("axis_point")
                self.model.a.rotate(
                    angle=angle,
                    axisDirection=axisDirection,
                    axisPoint=axisPoint,
                    instanceList=(self.name,),
                )

        self.model.a.instances[self.name].translate(vector=self.translate)

    def get_sequence_from_list(self, elements, type_):
        sequence_map = {
            "cell": self.get_cell_sequence,
            "face": self.get_face_sequence,
            "edge": self.get_edge_sequence,
        }

        type_seq = None
        for element in elements:
            if len(element) != 0:
                seq = sequence_map[type_](element)
                if type_seq is None:
                    type_seq = seq
                elif seq is not None:
                    type_seq += seq
        return type_seq

    def get_face_sequence(self, element):
        instance = self.model.a.instances[self.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            face = instance.faces.findAt(element.astype(float))  # noqa
            if face is not None:
                seq = Region(side1Faces=instance.faces[face.index : face.index + 1]).side1Faces
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            faces = instance.faces.getByBoundingBox(*element.astype(float))
            if len(faces) != 0:
                seq = faces
        elif isinstance(element.item(0), str):  # getByBoundingBox str
            instance_name, surface_name = element.item(0).split(".")
            if instance_name == self.name:
                faces = self.model.a.instances[self.name].surfaces[surface_name].faces
                seq = faces
        return seq

    def get_cell_sequence(self, element):
        instance = self.model.a.instances[self.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            cell = instance.cells.findAt(element.astype(float))
            if cell is not None:
                seq = Region(cells=instance.cells[cell.index : cell.index + 1]).cells
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            cells = instance.cells.getByBoundingBox(*element.astype(float))
            if len(cells) != 0:
                seq = cells
        return seq

    def get_edge_sequence(self, element):
        instance = self.model.a.instances[self.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            edge = instance.edges.findAt(element.astype(float))
            if isinstance(edge, type(None)):
                seq = None
            else:
                seq = Region(edges=instance.edges[edge.index : edge.index + 1]).edges
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            edges = seq = instance.edges.getByBoundingBox(*element.astype(float))
            if len(edges) != 0:
                seq = edges
        elif isinstance(element.item(0), str):
            if "point_on" in element.item(0):
                instance_name, _ = element.item(0).split(".")
                element = array([self.model.a.instances[instance_name].pointOn]).flatten()
                seq = self.get_edge_sequence(element)
        return seq


@Abml_Registry.register("assembly_surfaces")
class Abml_Assembly_Surface(Abml_Helpers):
    def __init__(self, name, model, assembly, faces=None):
        self.name = name
        self.model = model
        self.faces = self.convert_position_list(faces)
        self.assembly = assembly

        self.create_surfaces()

    def create_surfaces(self):
        instances = self.assembly.instances

        seq = None
        for face in self.faces:
            for instance in instances.values():
                face_seq = instance.get_face_sequence(face)
                if face_seq is not None:
                    if seq is None:
                        seq = face_seq
                    else:
                        seq += face_seq

        self.model.a.Surface(side1Faces=seq, name=self.name)
        del seq


@Abml_Registry.register("assembly_sets")
class Abml_Assembly_Set(Abml_Helpers):
    def __init__(self, name, model, assembly, **kwargs):
        self.name = name
        self.model = model
        self.faces = self.convert_position_list(kwargs.get("faces", None))
        self.edges = self.convert_position_list(kwargs.get("edges", None))
        self.cells = self.convert_position_list(kwargs.get("cells", None))
        self.assembly = assembly

        self.create()

    def create(self):
        assembly = self.model.a

        kwargs = {}
        face_seq = None
        instances = self.assembly.instances

        face_seq = None
        for instance in instances.values():
            seq = instance.get_sequence_from_list(self.faces, "face")
            if face_seq is None:
                face_seq = seq
            elif seq is not None:
                face_seq += seq

        if face_seq is not None:
            kwargs["faces"] = face_seq

        cell_seq = None
        for instance in instances.values():
            seq = instance.get_sequence_from_list(self.cells, "cell")
            if cell_seq is None:
                cell_seq = seq
            elif seq is not None:
                cell_seq += seq
        if cell_seq is not None:
            kwargs["cells"] = cell_seq

        edge_seq = None
        for instance in instances.values():
            seq = instance.get_sequence_from_list(self.edges, "edge")
            if cell_seq is None:
                edge_seq = seq
            elif seq is not None:
                edge_seq += seq

        if edge_seq is not None:
            kwargs["edges"] = edge_seq

        assembly.Set(name=self.name, **kwargs)
