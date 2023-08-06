from abml_dataclass import Abml_Registry
from abml_helpers import Abml_Helpers, cprint, get_objects
from regionToolset import Region
from abaqusConstants import ON, OFF, COMPUTED, SPECIFIED
from abaqus import mdb, session


@Abml_Registry.register("constraints")
class Abml_Constraints(Abml_Helpers):
    def __init__(self, name, model, **kwargs):  # noqa
        self.name = name
        self.model = model
        self.kwargs = kwargs

        self.tolerance_map = {"computed": COMPUTED, "specified": SPECIFIED}

        self.create()

    def create(self):
        position_tolerance_method = self.kwargs.get("position_tolerance_method", "computed").lower()

        kwargs = {
            "name": self.name,
            "master": Region(side1Faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["master"])),
            "slave": Region(side1Faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["slave"])),
            "positionToleranceMethod": self.tolerance_map[position_tolerance_method],
            "adjust": self.kwargs.get("adjust", True),
            "tieRotations": self.kwargs.get("tie_rotations", True),
            "thickness": self.kwargs.get("thickness", True),
        }

        self.model.m.Tie(**kwargs)
