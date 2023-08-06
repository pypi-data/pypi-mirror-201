import types
import json
import inspect
from collections import OrderedDict
from collections import defaultdict
import sys
import yaml
from io import open
from abaqus import mdb
from abaqusConstants import STANDARD_EXPLICIT
from abml import abml_helpers
import interaction
from abaqus import openMdb


class Abml_Registry:
    registry = defaultdict(lambda: OrderedDict)

    @classmethod
    def register(cls, key):
        def decorator(dataclass):
            cls.registry[key] = dataclass
            return dataclass

        return decorator


@Abml_Registry.register("cae")
class Abml_Cae:
    def __init__(self, models, **kwargs):
        self.kwargs = kwargs

        cae_path = self.kwargs.get("cae", None)
        cae_path = models.pop("cae") if "cae" in models else None
        if cae_path is not None:
            self.open_cae(cae_path)

        self.models = to_object_key_mode(models["models"], type_="models")

    def open_cae(self, path):
        openMdb(pathName=path)

    def save_cae(self, filename):
        mdb.saveAs(pathName=filename)


@Abml_Registry.register("models")
class Abml_Model:
    """
    Creates an Abaqus/Standard model using the provided input.

    Parameters
    ----------
    name : str
        The name of the Abaqus/Standard model.
    **kwargs : dict
        A dictionary of inputs for creating the model. The dictionary can contain the following keys:

        - materials : dict, optional
            A dictionary of materials to be added to the model.
        - sections : dict, optional
            A dictionary of sections to be added to the model.
        - parts : dict, optional
            A dictionary of parts to be added to the model.
        - assembly : dict, optional
            A dictionary describing the assembly of parts in the model.
        - steps : dict, optional
            A dictionary of steps to be added to the model.
        - interaction_props : dict, optional
            A dictionary of interaction properties to be added to the model.
        - interactions : dict, optional
            A dictionary of interactions to be added to the model.
        - constraints : dict, optional
            A dictionary of constraints to be added to the model.
        - bcs : dict, optional
            A dictionary of boundary conditions to be added to the model.
        - loads : dict, optional
            A dictionary of loads to be added to the model.
        - jobs : dict, optional
            A dictionary of jobs to be added to the model.
        - modules : dict, optional
            A dictionary of sub-modules to be created within the model.

        Methods
        -------
        create()
            Creates an instance of a model in the cae
        create_instances(**kwargs)
            Creates instances of materials, sections, parts, etc. in the model.
        create_materials(**kwargs)
            creates material
        create_sections(**kwargs)
            creates sections
        create_parts(**kwargs)
            creates material
        create_assembly(**kwargs)
            creates the assembly
        create_steps(**kwargs)
            creates steps
        create_interaction_props(**kwargs)
            creates interaction props
        create_interactions(**kwargs)
            creates interactionss
        create_constraints(**kwargs)
            creates constraints
        create_bcs(**kwargs)
            creates bcs
        create_loads(**kwargs)
            creates loads
        create_jobs(**kwargs)
            creates jobs
        create_modules(**kwargs)
            creates modules


        Returns
        -------
        None
    """

    def __init__(self, name, **kwargs):
        self.name = name

        self.create()
        self.m, self.a, self.p = abml_helpers.get_objects(self.name)
        self.kwargs = kwargs

        self.materials = {}
        self.sections = {}
        self.parts = {}
        self.assembly = {}
        self.steps = {}
        self.interaction_props = {}
        self.interactions = {}
        self.constraints = {}
        self.bcs = {}
        self.loads = {}
        self.jobs = {}
        self.sketches = {}

        self.create_instances(**kwargs)

    def create_instances(self, **kwargs):
        create_order = [
            self.create_sketches,
            self.create_materials,
            self.create_sections,
            self.create_parts,
            self.create_assembly,
            self.create_steps,
            self.create_interaction_props,
            self.create_interactions,
            self.create_constraints,
            self.create_bcs,
            self.create_loads,
            self.create_jobs,
            self.create_modules,
        ]

        for creation in create_order:
            creation(**kwargs)

    def update_nested_dict(self, nested_dict, update_dict):
        """
        Recursively update a nested dictionary with a dictionary of key-value pairs
        if the keys are not already present.
        """
        for k, v in update_dict.iteritems():
            if isinstance(v, dict):
                # Recursively update nested dictionaries
                nested_dict[k] = self.update_nested_dict(nested_dict.get(k, {}), v)
            elif k not in nested_dict:
                # Key is not present, update the dictionary
                nested_dict[k] = v
        return nested_dict

    def create_sketches(self, **kwargs):
        sketches_list = [value for key, value in kwargs.items() if "sketches" in key]
        for sketches in sketches_list:
            if sketches is not None:
                sketches = OrderedDict(sorted(sketches.items()))

                sketch_name = sketches.keys()[0]
                sketch_cmds = sketches.values()[0]

                self.sketches.update(
                    {sketch_name: to_object_cmd_mode(sketch_cmds, "sketch", model=self, name=sketch_name)}
                )

    def create_materials(self, **kwargs):
        materials_list = [value for key, value in kwargs.items() if "materials" in key]
        for materials in materials_list:
            if materials is not None:
                materials = OrderedDict(sorted(materials.items()))
                self.materials.update(to_object_key_mode(materials, "materials", model=self))

    def create_sections(self, **kwargs):
        sections_list = [value for key, value in kwargs.items() if "sections" in key]
        for sections in sections_list:
            if sections is not None:
                sections = OrderedDict(sorted(sections.items()))
                self.sections.update(to_object_key_mode(sections, "sections", model=self))

    def create_parts(self, **kwargs):
        parts_list = [value for key, value in kwargs.items() if "parts" in key]
        for parts in parts_list:
            if parts is not None:
                parts = OrderedDict(sorted(parts.items()))
                self.parts.update(to_object_key_mode(parts, "parts", model=self))

    def create_assembly(self, **kwargs):
        assembly_list = [value for key, value in kwargs.items() if "assembly" in key]
        for assembly in assembly_list:
            if assembly is not None:
                self.assembly = to_object_hierachy_mode(assembly, "assembly", model=self)

    def create_steps(self, **kwargs):
        steps_list = [value for key, value in kwargs.items() if "steps" in key]
        for steps in steps_list:
            if steps is not None:
                steps = OrderedDict(sorted(steps.items()))
                self.interaction_props.update(to_object_key_mode(steps, "steps", model=self))

    def create_interaction_props(self, **kwargs):
        interaction_props_list = [value for key, value in self.kwargs.items() if "interaction_props" in key]
        for interaction_props in interaction_props_list:
            if interaction_props is not None:
                interaction_props = OrderedDict(sorted(interaction_props.items()))
                self.interaction_props.update(to_object_key_mode(interaction_props, "interaction_props", model=self))

    def create_interactions(self, **kwargs):
        interactions_list = [value for key, value in kwargs.items() if "interactions" in key]
        for interactions in interactions_list:
            if interactions is not None:
                interactions = OrderedDict(sorted(interactions.items()))
                self.interactions.update(to_object_key_mode(interactions, "interactions", model=self))

    def create_constraints(self, **kwargs):
        constraints_list = [value for key, value in kwargs.items() if "constraints" in key]
        for constraints in constraints_list:
            if constraints is not None:
                constraints = OrderedDict(sorted(constraints.items()))
                self.constraints.update(to_object_key_mode(constraints, "constraints", model=self))

    def create_bcs(self, **kwargs):
        bcs_list = [value for key, value in kwargs.items() if "bcs" in key]
        for bcs in bcs_list:
            if bcs is not None:
                bcs = OrderedDict(sorted(bcs.items()))
                self.bcs.update(to_object_key_mode(bcs, "bcs", model=self))

    def create_loads(self, **kwargs):
        loads_list = [value for key, value in kwargs.items() if "loads" in key]
        for loads in loads_list:
            if loads is not None:
                loads = OrderedDict(sorted(loads.items()))
                self.loads.update(to_object_key_mode(loads, "loads", model=self))

    def create_jobs(self, **kwargs):
        jobs_list = [value for key, value in kwargs.items() if "jobs" in key]
        for jobs in jobs_list:
            if jobs is not None:
                jobs = OrderedDict(sorted(jobs.items()))
                self.jobs.update(to_object_key_mode(jobs, "jobs", model=self))

    def create_modules(self, **kwargs):
        modules_list = kwargs.get("modules", [])
        # abml_helpers.cprint("############## {}".format(modules_list[0]))
        modules_list = [value for key, value in kwargs.items() if "modules" in key]
        # abml_helpers.cprint(modules_list[0])
        for modules in modules_list:
            if modules is not None:
                if isinstance(modules, dict):
                    modules = OrderedDict(sorted(modules.items()))
                    self.create_instances(**modules)
                elif isinstance(modules, list):
                    for module in modules:
                        module = OrderedDict(sorted(module.items()))
                        self.create_instances(**module)

    def create(self):
        if self.name not in mdb.models.keys():
            mdb.Model(modelType=STANDARD_EXPLICIT, name=self.name)

        if "Model-1" in mdb.models.keys():
            del mdb.models["Model-1"]


def data_to_object(data, type_="models", key_based=True, **kwargs):
    """
    Converts input data into objects of specified type.

    Parameters
    ----------
    data : dict, list, or None
        Input data to be converted into objects. If `None`, returns `None`.
    type_ : str, optional
        Type of objects to be created. Defaults to "models".
    key_based : bool, optional
        Whether to create objects based on the keys in `data` (if `True`) or create a single object
        from `data` (if `False`). Defaults to `True`.
    **kwargs
        Additional keyword arguments to pass to object constructors.

    Returns
    -------
    object_
        If `data` is a dictionary, returns a dictionary of objects, where each key in `data`
        corresponds to an object created from the corresponding value. If `key_based` is `False`
        and `data` is a dictionary, returns a single object created from the values in `data`.
        If `data` is a list, returns a list of objects created from the elements in `data`.
        If `data` is `None`, returns `None`.

    """
    if data is not None:
        object_ = {}
        if isinstance(data, dict):
            object_ = {}
            if key_based:
                for key, value in data.items():
                    if isinstance(value, dict):
                        value.update(kwargs)
                        object_[key] = Abml_Registry.registry[type_](name=key, **value)
                    elif isinstance(value, (list)):
                        object_[key] = Abml_Registry.registry[type_](name=key, *value)
            else:
                data.update(kwargs)
                object_ = Abml_Registry.registry[type_](**data)
        elif isinstance(data, list):
            object_ = []
            for value in data:
                value.update(kwargs)
                object_.append(Abml_Registry.registry[type_](**value))

        return object_
    return None


def to_object_key_mode(data, type_, **kwargs):
    """
    Create objects of a specified type from a dictionary of data, where each key in the dictionary represents an object to be created.

    Parameters
    ----------
    data : dict
        A dictionary where each key represents an object to be created, and each value contains
        the data necessary to create the object.
    type_ : str
        The type of object to be created. This must correspond to a valid key in the `registry`
        dictionary of the `Abml_Registry` class.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the object constructor.

    Returns
    -------
    dict
        A dictionary where each key is the name of the object, and each value is the object itself.

    """
    object_ = {}
    for key, value in data.items():
        value.update(kwargs)
        object_[key] = Abml_Registry.registry[type_](name=key, **value)

    return object_


def to_object_option_mode(data, type_, **kwargs):
    """
    Convert a dictionary of data to an object of the specified type.

    Parameters
    ----------
    data : dict
        A dictionary containing the data to convert to an object.
    type_ : str
        The type of object to create.
    **kwargs : dict
        Additional keyword arguments to pass to the object constructor.

    Returns
    -------
    object_
        An object of the specified type containing the data from the dictionary.
    """
    data.update(kwargs)
    object_ = Abml_Registry.registry[type_](**data)

    return object_


def to_object_key_based_type(data, **kwargs):
    """
    Converts a dictionary of data into a collection of objects based on the key.

    Parameters
    ----------
    data : dict
        The dictionary of data to be converted into objects.
    **kwargs : keyword arguments, optional
        Additional arguments to be passed to the object constructor.

    Returns
    -------
    object_ : dict
        A dictionary of objects created from the data, where each object is associated with its corresponding key in the input dictionary.

    Notes
    -----
    This function assumes that each key in the input dictionary corresponds to the name of a class in the `Abml_Registry` registry. It creates an instance of each class with the corresponding data value as constructor arguments, and returns a dictionary where each object is associated with its corresponding key.

    """
    object_ = {}
    for key, value in data.items():
        value.update(kwargs)
        object_[key] = Abml_Registry.registry[key](**value)

    return object_


def to_object_cmd_mode(data, type_, **kwargs):
    """
    Convert a list of dictionaries representing command data into a list of objects.

    Parameters
    ----------
    data : list of dict
        List of dictionaries containing command data.
    type_ : str
        The type of object to create from the command data.
    **kwargs : dict, optional
        Optional keyword arguments to be passed to the object constructor.

    Returns
    -------
    list of object
        A list of objects created from the command data.

    Notes
    -----
    This function expects each dictionary in the `data` list to have a single key-value pair,
    where the key is the command name and the value is a dictionary containing the command arguments.
    The `type_` parameter specifies the type of object to create from the command data, and must be a
    string that matches the name of a class registered with the `Abml_Registry.registry` dictionary.

    Examples
    --------
    **python
    >>> data = [{'command1': {'arg1': 1, 'arg2': 2}}, {'command2': {'arg1': 3, 'arg2': 4}}]
    >>> objects = to_object_cmd_mode(data, 'MyClass', arg3=5)
    >>> objects[0].arg1
    1
    >>> objects[1].arg2
    4
    """

    object_ = []
    for cmd in data:
        value = cmd.values()[0]
        key = cmd.keys()[0]
        value.update(kwargs)
        object_.append(Abml_Registry.registry[type_](cmd=key, **value))

    return object_


def to_object_hierachy_mode(data, type_, **kwargs):
    """
    Create an object from a hierarchical dictionary representation of the object's attributes.

    Parameters
    ----------
    data : dict
        A hierarchical dictionary representation of the object's attributes.
    type_ : str
        The name of the class to create the object from.
    **kwargs : dict, optional
        Optional keyword arguments to be passed to the object constructor.

    Returns
    -------
    object
        An instance of the specified class, with attributes set according to the data dictionary.

    Notes
    -----
    This function expects the `data` dictionary to be hierarchical, with each key representing an attribute
    name and each value representing the attribute value. If a value is itself a dictionary, the attribute
    is treated as a sub-object, and this function is recursively called to create the sub-object. The `type_`
    parameter specifies the name of the class to create the object from, and must be a string that matches the
    name of a class registered with the `Abml_Registry.registry` dictionary.

    """
    data.update(kwargs)
    object_ = Abml_Registry.registry[type_](**data)

    return object_
