from abml_dataclass import Abml_Registry
from abml_helpers import Abml_Helpers
from abml_helpers import cprint


@Abml_Registry.register("sections")
class Abml_Section(Abml_Helpers):
    def __init__(self, model, name, category, type, material, **kwargs):  # noqa
        self.model = model
        self.name = name
        self.category = category
        self.type = type
        self.material = material
        self.map = {}

        self.section_map = {("homogeneous", "solid"): self.homogeneous_solid}
        self.create()

    def homogeneous_solid(self):
        kwargs = {
            "name": self.name,
            "material": self.material,
        }
        self.model.m.HomogeneousSolidSection(**kwargs)

    def create(self):
        self.section_map[(self.type, self.category)]()
