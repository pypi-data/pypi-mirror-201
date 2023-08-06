from abml_dataclass import Abml_Registry
from abml_helpers import cprint


@Abml_Registry.register("steps")
class Abml_Step:
    def __init__(self, name, type, pre_step, model):  # noqa
        self.name = name
        self.type = type
        self.model = model
        self.pre_step = pre_step
        self.map = {"static_general": self.static_general}
        self.create()

    def create(self):
        self.map[self.type]()

    def static_general(self):
        self.model.m.StaticStep(name=self.name, previous=self.pre_step)
