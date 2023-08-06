from abml_helpers import Abml_Helpers
import abml_helpers
from abml_parts import Abml_Part
from abml_assembly import Abml_Assembly
from abml_dataclass import Abml_Registry
from abml_dataclass import Abml_Model
from abaqusConstants import FREE, FINER, FIXED, STRUCTURED
from abaqusConstants import TET, HEX
from abaqusConstants import STANDARD, DEFAULT, OFF
from abaqusConstants import C3D8, C3D8R, C3D6, C3D4, C3D20, C3D20R, C3D15, C3D10
from regionToolset import Region
import mesh


@Abml_Registry.register("mesh")
class Abml_Mesh_Command(Abml_Helpers):
    def __init__(self, cmd, part=None, assembly=None, **kwargs):
        self.part = part
        self.assembly = assembly
        self.cmd = cmd
        self.kwargs = kwargs

        if part is not None:
            self.abaqus_object = self.part.geometry  # noqa
            self.model = part.model
        elif assembly is not None:
            self.abaqus_object = self.assembly
            self.model = assembly.model

        self.map = {
            "seed_edge_by_size": self.seed_edge_size,
            "seed_edge_by_number": self.seed_edge_by_number,
            "mesh_controls": self.mesh_controls,
            "element_type": self.element_type,
        }

        self.elem_shape_map = {"tet": TET, "hex": HEX}
        self.technique_map = {"free": FREE, "structured": STRUCTURED}
        self.constraint_map = {"free": FREE, "finer": FINER, "fixed": FIXED}
        self.element_types_map = {
            ("linear", True): self._element_type_linear_reduced,
            ("quadratic", True): self._element_type_quadratic_reduced,
            ("linear", False): self._element_type_linear,
            ("quadratic", False): self._element_type_quadratic,
        }
        self.create()

    def create(self):
        self.map.get(self.cmd, lambda: None)()

    def seed_edge_size(self):
        # edges = abaqus_object.get_sequence_from_list(self.convert_position_list(self.kwargs["edges"]), "edge")
        kwargs = {
            "edges": 0,
            "size": self.kwargs["size"],
            "constraint": self.constraint_map[self.kwargs.get("constraint", "finer").lower()],
            "deviationFactor": self.kwargs.get("deviationFactor", None),
            "minSizeFactor": self.kwargs.get("minSizeFactor", None),
        }
        self.abaqus_object.seedEdgeBySize(**kwargs)

    def seed_edge_by_number(self):
        edges_list = self.convert_position_list(self.kwargs.get("edges", None))
        set_list = self.convert_position_list(self.kwargs.get("sets", None))
        edge_seq = None
        if edges_list is not None:
            seq = self.abaqus_object.get_sequence_from_list(edges_list, "edge")
            edge_seq = seq
        if set_list is not None:
            seq = self.abaqus_object.get_sequence_from_list(set_list, "set_edges")
            if edge_seq is None:
                edge_seq = seq
            else:
                edge_seq += seq
        kwargs = {
            "edges": edge_seq,
            "number": self.kwargs["number"],
            "constraint": self.constraint_map[self.kwargs.get("constraint", "finer").lower()],
        }

        self.model.p[self.part.name].seedEdgeByNumber(**kwargs)

    def mesh_controls(self):
        cells = self.abaqus_object.get_sequence_from_list(self.convert_position_list(self.kwargs["cells"]), "cell")

        kwargs = {
            "regions": cells,
            "elemShape": self.elem_shape_map[self.kwargs["shape"]],
            "technique": self.technique_map[self.kwargs.get("technique", "free")],
        }
        self.model.p[self.part.name].setMeshControls(**kwargs)

    def element_type(self):
        cell_list = self.convert_position_list(self.kwargs["cells"])

        if cell_list is not None:
            cells = self.abaqus_object.get_sequence_from_list(cell_list, "cell")

            elemType1, elemType2, elemType3 = self.element_types_map[
                (self.kwargs.get("order"), self.kwargs.get("reduced"))
            ]()

            kwargs = {
                "regions": Region(cells=cells),
                "elemTypes": (elemType1, elemType2, elemType3),
            }
            # self.model.p[self.part.name].setMeshControls(**kwargs)

            self.model.p[self.part.name].setElementType(**kwargs)

    def _element_type_linear_reduced(self):
        elemType1 = mesh.ElemType(
            elemCode=C3D8R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT
        )
        elemType2 = mesh.ElemType(
            elemCode=C3D6, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT
        )
        elemType3 = mesh.ElemType(
            elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT
        )

        return elemType1, elemType2, elemType3

    def _element_type_linear(self):
        elemType1 = mesh.ElemType(
            elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT
        )
        elemType2 = mesh.ElemType(
            elemCode=C3D6, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT
        )
        elemType3 = mesh.ElemType(
            elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT
        )

        return elemType1, elemType2, elemType3

    def _element_type_quadratic_reduced(self):
        elemType1 = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
        elemType3 = mesh.ElemType(
            elemCode=C3D10, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT
        )

        return elemType1, elemType2, elemType3

    def _element_type_quadratic(self):
        elemType1 = mesh.ElemType(elemCode=C3D20, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
        elemType3 = mesh.ElemType(
            elemCode=C3D10, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT
        )

        return elemType1, elemType2, elemType3
