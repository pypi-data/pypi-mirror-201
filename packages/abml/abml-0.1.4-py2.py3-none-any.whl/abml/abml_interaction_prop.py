from abml_dataclass import Abml_Registry, to_object_key_based_type
from abaqusConstants import FRICTIONLESS, PENALTY, ISOTROPIC, FRACTION
from abaqusConstants import HARD, DEFAULT
from abaqusConstants import ALL_NODES
from abaqusConstants import ON, OFF


@Abml_Registry.register("interaction_properties")
@Abml_Registry.register("interaction_props")
class Abml_Interaction_Prop:
    def __init__(self, name, type, behaviors, model, **kwargs):  # noqa
        self.name = name
        self.type = type
        self.model = model

        self.create()
        self.behaviors = to_object_key_based_type(behaviors, interaction=self)

    def create(self):
        self.model.m.ContactProperty(self.name)


@Abml_Registry.register("tangential")
class Abml_Tangential_Behavior:
    def __init__(self, formulation, interaction, **kwargs):
        self.formulation = formulation
        self.interaction = interaction
        self.interaction_prop = interaction.model.m.interactionProperties[interaction.name]
        self.formulation_map = {"frictionless": FRICTIONLESS, "penalty": PENALTY}
        self.create_map = {
            "frictionless": self.create_frictionless,
            "penalty": self.create_penalty,
        }
        self.kwargs = kwargs
        self.create()

    def create(self):
        self.create_map[self.formulation]()

    def create_frictionless(self):
        kwargs = {"formulation": self.formulation_map[self.formulation]}
        self.interaction_prop.TangentialBehavior(**kwargs)

    def create_penalty(self):
        kwargs = {
            "formulation": self.formulation_map[self.formulation],
            "directionality": ISOTROPIC,
            "slipRateDependency": OFF,
            "pressureDependency": OFF,
            "temperatureDependency": OFF,
            "dependencies": 0,
            "table": ((self.kwargs["friction_coeff"],),),
            "shearStressLimit": None,
            "maximumElasticSlip": FRACTION,
            "fraction": 0.005,
            "elasticSlipStiffness": None,
        }

        self.interaction_prop.TangentialBehavior(**kwargs)


@Abml_Registry.register("normal")
class Abml_Normal_Behavior:
    def __init__(self, overclosure, constraint, seperation, interaction):
        self.overclosure = overclosure
        self.constraint = constraint
        self.seperation = seperation
        self.interaction = interaction
        self.interaction_prop = interaction.model.m.interactionProperties[interaction.name]
        self.overclosure_map = {"hard_contact": HARD}
        self.constraint_map = {"default": DEFAULT}

        self.create()

    def create(self):
        kwargs = {
            "pressureOverclosure": self.overclosure_map[self.overclosure],
            "allowSeparation": self.seperation,
            "constraintEnforcementMethod": self.constraint_map[self.constraint],
        }

        self.interaction_prop.NormalBehavior(**kwargs)


@Abml_Registry.register("cohesive")
class Abml_Cohesive_Behavior:
    def __init__(self, interaction, **kwargs):
        self.interaction = interaction
        self.interaction_prop = interaction.model.m.interactionProperties[interaction.name]
        self.kwargs = kwargs
        self.create()

    def create(self):
        kwargs = {
            "eligibility": ALL_NODES,
            "defaultPenalties": OFF,
            "table": ((self.kwargs["knn"], self.kwargs["kss"], self.kwargs["ktt"]),),
        }

        self.interaction_prop.CohesiveBehavior(**kwargs)


@Abml_Registry.register("damage")
class Abml_Damage_Behavior:
    def __init__(self, interaction, **kwargs):
        self.interaction = interaction
        self.interaction_prop = interaction.model.m.interactionProperties[interaction.name]
        self.kwargs = kwargs
        self.create()

    def create(self):
        kwargs = {
            "initTable": ((self.kwargs["normal_only"], self.kwargs["shear_1_only"], self.kwargs["shear_2_only"]),),
            "useEvolution": ON,
            "evolTable": ((self.kwargs["total_plastic_displacement"],),),
        }

        self.interaction_prop.Damage(**kwargs)
