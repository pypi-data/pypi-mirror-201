from abml_dataclass import Abml_Registry, to_object_key_based_type
from abaqusConstants import UNIFORM, ISOTROPIC


@Abml_Registry.register("materials")
class Abml_Material:
    """
    A class representing a material in an abml.

    Parameters
    ----------
    model : AbaqusModel stored in mdb
        The Abaqus model to which the material belongs.
    name : str
        The name of the material.
    behaviors : dict
        A dictionary of material behaviors, where the keys are the behavior names
        and the values are the corresponding behavior parameters.
    description : str, optional
        A description of the material.
    **kwargs
        Additional keyword arguments to be passed to the Abaqus API.

    Methods
    -------
    create()
        Creates the material in the Abaqus model.

    Notes
    -----
    This class is a wrapper around the Abaqus/Standard API for creating and managing
    materials in a finite element simulation. It provides a more user-friendly
    interface for defining material properties and behaviors.

    Examples
    --------
    materials:
      material_1:
        behaviors:
          density:
            distribution: "uniform"
            density: 1e-9
          elastic:
            type: isotropic
            E: 450
            nu: 0.3
    """

    def __init__(self, model, name, behaviors={}, description="", **kwargs):  # noqa
        self.model = model
        self.description = description
        self.name = name
        self.create()
        self.behaviors = to_object_key_based_type(behaviors, material=self)

    def create(self):
        self.model.m.Material(name=self.name, description=self.description)


@Abml_Registry.register("density")
class Abml_Density:
    """
    A class representing a density distribution of a material in Abaqus/CAE.

    Parameters
    ----------
    density : float
        The value of the material density in units of mass per unit volume.
    material : Abml_Material
        An instance of the `Abml_Material` class representing the material.
    distribution : str, optional
        The type of density distribution to use. Possible values are "uniform" (default).

    Methods
    -------
    create():
        Creates the density distribution in the Abaqus/CAE model.

    Notes
    -----
    The `create()` method uses the Abaqus/CAE API to create a density distribution
    of the specified type in the material model.

    Examples
    --------
    behaviors:
      density:
        distribution: "uniform"
        density: 1e-9
    """

    def __init__(self, density, material, distribution="uniform"):
        self.material = material
        self.distribution = distribution
        self.density = float(density)

        self.create()

    def create(self):
        distribution_type = {"uniform": UNIFORM}
        kwargs = {"table": ((self.density,),), "distributionType": distribution_type[self.distribution]}
        self.material.model.m.materials[self.material.name].Density(**kwargs)


@Abml_Registry.register("elastic")
class Abml_Elastic:
    """
    A class representing the elastic properties of a material in Abaqus/CAE.

    Parameters
    ----------
    E : float
        The Young's modulus of the material in units of pressure.
    nu : float
        The Poisson's ratio of the material.
    material : Abml_Material
        An instance of the `Abml_Material` class representing the material.
    type : str, optional
        The type of elastic behavior to use. Possible values are "isotropic" (default).

    Methods
    -------
    create():
        Creates the elastic behavior in the Abaqus/CAE model.
    isotropic():
        Creates an isotropic elastic behavior in the Abaqus/CAE model.

    Notes
    -----
    The `create()` method uses the Abaqus/CAE API to create the specified elastic behavior
    in the material model. The supported elastic behaviors are currently limited to
    isotropic behavior.


    Examples
    --------
    behaviors:
      elastic:
        type: isotropic
          E: 450
          nu: 0.3
    """

    def __init__(self, E, nu, material, type="isotropic"):  # noqa
        self.material = material
        self.E = float(E)
        self.nu = float(nu)
        self.type = type
        self.types_map = {
            "isotropic": ISOTROPIC,
        }

        self.elastic_map = {"isotropic": self.isotrtopic}

        self.create()

    def create(self):
        self.elastic_map[self.type]()

    def isotrtopic(self):
        kwargs = {"table": ((self.E, self.nu),), "type": self.types_map[self.type]}
        self.material.model.m.materials[self.material.name].Elastic(**kwargs)
