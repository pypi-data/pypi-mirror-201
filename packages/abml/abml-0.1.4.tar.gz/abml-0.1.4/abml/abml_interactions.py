from abml_dataclass import Abml_Registry
import abml_helpers
from regionToolset import Region
from abaqusConstants import FINITE, SMALL
import logging

logger = logging.getLogger("abml_logger")


@Abml_Registry.register("interactions")
class Abml_Interaction:
    def __init__(self, name, type, model, **kwargs):  # noqa
        self.name = name
        self.type = type
        self.model = model
        self.kwargs = kwargs

        logger.debug(
            abml_helpers.get_kwargs_string(
                model=model.name,
                name=name,
                type=type,
            )
        )

        self.map = {
            "surface_to_surface": self.surface_to_surface,
            "elastic_foundation": self.elastic_foundation,
        }
        self.sliding_map = {"finite": FINITE, "small": SMALL}
        self.create()

    def create(self):
        self.map[self.type]()

    def surface_to_surface(self):
        kwargs = {
            "name": self.name,
            "master": Region(side1Faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["master"])),
            "slave": Region(side1Faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["slave"])),
            "createStepName": self.kwargs.get("step", "Initial"),
            "sliding": self.sliding_map[self.kwargs.get("sliding", "finite").lower()],
            "interactionProperty": self.kwargs["interaction_prop"],
        }

        self.model.m.SurfaceToSurfaceContactStd(**kwargs)

    def elastic_foundation(self):
        try:
            surface_region = Region(side1Faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["faces"]))
        except TypeError as e:
            error_msg = """
            model_name: {model_name}
            interaction_name: {name}
            surfaces: {surfaces}
            error: {e}
            """.format(
                model_name=self.model.name,
                name=self.name,
                e=e,
                surfaces=self.kwargs["faces"],
            )

            raise TypeError(error_msg)

        kwargs = {
            "name": self.name,
            "surface": surface_region,
            "createStepName": "Initial",
            "stiffness": self.kwargs["stiffness"],
        }

        self.model.m.ElasticFoundation(**kwargs)
