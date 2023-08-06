from abml_dataclass import Abml_Registry
from abml_helpers import Abml_Helpers, cprint
from abaqusConstants import USER_DEFINED, UNSET, UNIFORM, SET, UNSET
from regionToolset import Region


@Abml_Registry.register("bcs")
class Abml_Bc(Abml_Helpers):
    def __init__(self, name, model, type, **kwargs):
        self.name = name
        self.step = kwargs.get("step", "Initial")
        self.model = model
        self.type = type
        self.faces = self.convert_position_list(kwargs.get("faces", []))
        self.edges = self.convert_position_list(kwargs.get("edges", []))
        self.cells = self.convert_position_list(kwargs.get("cells", []))
        self.kwargs = kwargs

        self.map = {
            "x_symm": self.x_symm,
            "y_symm": self.y_symm,
            "z_symm": self.z_symm,
            "disp_rot": self.disp_rot,
        }

        self.set_map = {
            "set": SET,
            "unset": UNSET,
            1: SET,
            0: UNSET,
        }
        self.create()

    def create(self):
        self.map[self.type]()

    def x_symm(self):
        region = Region(faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["faces"]))
        self.model.m.XsymmBC(name=self.name, createStepName=self.step, region=region, localCsys=None)

    def y_symm(self):
        region = Region(faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["faces"]))
        self.model.m.YsymmBC(name=self.name, createStepName=self.step, region=region, localCsys=None)

    def z_symm(self):
        region = Region(faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["faces"]))
        self.model.m.ZsymmBC(name=self.name, createStepName=self.step, region=region, localCsys=None)

    def disp_rot(self):
        region = Region(faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["faces"]))
        self.model.m.DisplacementBC(
            name=self.name,
            createStepName=self.step,
            region=region,
            u1=self.set_map[self.kwargs.get("u1", 0)],
            u2=self.set_map[self.kwargs.get("u2", 0)],
            u3=self.set_map[self.kwargs.get("u3", 0)],
            ur1=self.set_map[self.kwargs.get("ur1", 0)],
            ur2=self.set_map[self.kwargs.get("ur2", 0)],
            ur3=self.set_map[self.kwargs.get("ur3", 0)],
            amplitude=UNSET,
            distributionType=UNIFORM,
            fieldName="",
            localCsys=None,
        )


# symm:
#     xsymm:
#         faces: [platte1.E]
# test2:
#     disp_rot:
#         faces: [platte2.E]
#         u1: 1
#         u2: 1
#         u3: 1

# self.model = part.model
# self.faces = self.convert_position_list(faces)
# self.edges = self.convert_position_list(edges)
# self.cells = self.convert_position_list(cells)
# self.kwargs = kwargs
# self.partition_map = {"plane": self.create_face_plane}

# self.create()

# def create(self):
# self.partition_map[self.method]()

# def create_face_plane(self):
# part_ = self.model.p[self.part.name]
# planes = array([self.kwargs.get("planes", [])]).flatten()

# for plane in planes:
#     id_ = part_.features[plane].id

#     if self.faces is not None:
#         face_seq = self.part.geometry.get_sequence_from_list(self.faces, "face")
#         if face_seq is not None:
#             part_.PartitionFaceByDatumPlane(datumPlane=part_.datums[id_], faces=face_seq)

#     if self.cells is not None:
#         cell_seq = self.part.geometry.get_sequence_from_list(self.cells, "cell")
#         if cell_seq is not None:
#             part_.PartitionCellByDatumPlane(datumPlane=part_.datums[id_], cells=cell_seq)

#     if self.edges is not None:
#         edge_seq = self.part.geometry.get_sequence_from_list(self.edges, "edge")
#         if edge_seq is not None:
#             part_.PartitionEdgeByDatumPlane(datumPlane=part_.datums[id_], edges=edge_seq)
