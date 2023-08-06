from abaqus import mdb
import sys
import os
import re


class IterReg(type):
    # Register of all objects for iteration
    def __iter__(cls):
        return iter(cls._reg.values())


class Abml_Helpers(object):
    """
    A utility class that provides helper methods for various tasks.

    Methods
    -------
    map_function(cls, key)
        A decorator method that maps the specified key to the provided function.
    get_boundary_rect(cls, sketch, depth, orientation)
        Calculates and returns the boundary rectangle of the given sketch with the given depth and orientation.
    convert_position_list(cls, position_list)
        Converts the provided position list into a standard list of lists format, if necessary.
    exit_handler()
        Cleans up temporary files created by the program.
    """

    @classmethod
    def map_function(cls, key):
        def decorator(func):
            cls.map[key] = func
            return func

        return decorator

    @classmethod
    def get_boundary_rect(cls, sketch, depth, orientation):
        p1 = sketch.kwargs["p1"]
        p2 = sketch.kwargs["p2"]
        x, y, z = abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), depth

        offset = 1e-5
        boundaries = {
            "W": (-offset, 0, 0, 0, y, z),
            "N": (0, -offset, 0, x, 0, z),
            "T": (0, 0, -offset, x, y, 0),
            "top": (0, 0, -offset, x, y, 0),
            "E": (x - offset, 0, 0, x, y, z),
            "S": (0, y - offset, 0, x, y, z),
            "B": (0, 0, z - offset, x, y, z),
            "bot": (0, 0, z - offset, x, y, z),
        }

        return boundaries[orientation]

    @classmethod
    def convert_position_list(cls, position_list):
        """
        Convert the input position list to a list of lists.

        Parameters
        ----------
        position_list : list or None
            A list of positions to be converted.

        Returns
        -------
        position_list : list or None
            A list of lists of positions.

        Notes
        -----
        This method is used to convert a position list to a list of lists, where each sub-list
        contains a single position. If the input position list is already a list of lists, or if it
        is None, it is returned unmodified.

        Examples
        --------
        **python
        >>> Abml_Helpers.convert_position_list([1, 2, 3])
        [[1, 2, 3]]

        >>> Abml_Helpers.convert_position_list([[1, 2, 3], [4, 5, 6]])
        [[1, 2, 3], [4, 5, 6]]

        >>> Abml_Helpers.convert_position_list(None)
        None
        """

        if position_list is not None:

            def depth(list_):
                if isinstance(list_, list) and len(list_) != 0:
                    return 1 + max(depth(item) for item in list_)
                return 0

            depth_list = depth(position_list)
            if depth_list == 1 and all(isinstance(x, (int, float)) for x in position_list):
                position_list = [position_list]
            elif depth_list == 0:
                position_list = [position_list]
            return position_list
        return None


def exit_handler():
    """
    Deletes all files in the current directory with the extensions '.rpy', '.rec', and '.dmp' to clean up after program execution.
    """
    for file in os.listdir("."):
        if ".rpy" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass
        if ".rec" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass
        if ".dmp" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass


def cprint(string, prefix="info"):
    """
    Prints the given string with a specified prefix to the standard output.

    Parameters
    ----------
    string : str
        The string to be printed.
    prefix : str, optional
        The prefix to be added to the string (default is "info").

    Returns
    -------
    None

    Notes
    -----
    This function uses the standard output stream `sys.__stdout__` to print the message.

    Examples
    --------
    **python
    >>> cprint("This is a message.", "warning")
    warning This is a message.

    >>> cprint("This is another message.")
    info This is another message.
    """
    print >> sys.__stdout__, prefix + " " + str(string)  # type: ignore # noqa


def _camel(match):
    """
    Helper function used in regex substitution to convert a matched string from camel case to snake case.

    Parameters:
    -----------
    match: MatchObject
        The matched object containing the string to be converted.

    Returns:
    --------
    str:
        The converted string in Pascal case.
    """
    return match.group(1) + match.group(2).upper()


patter_camel_to_snake = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(name):
    """
    Convert a camelCase string to snake_case.

    Parameters
    ----------
    name : str
        The string to be converted.

    Returns
    -------
    str
        The converted string in snake_case.

    Examples
    --------
    **python
    >>> camel_to_snake("camelCaseString")
    'camel_case_string'
    >>> camel_to_snake("AnotherCamelCaseExample")
    'another_camel_case_example'
    """
    return patter_camel_to_snake.sub("_", name).lower()


patter_snake_to_camel = re.compile(r"(.*?)_([a-zA-Z])")


def snake_to_camel(name):
    """
    Convert snake_case to camelCase.

    Parameters
    ----------
    name : str
        The string to convert.

    Returns
    -------
    str
        The camelCase version of the input string.
    """
    return patter_snake_to_camel.sub(_camel, name, 0)


def get_objects(model_name):
    """
    Get the objects from a given modelname.

    Parameters
    ----------
    model_name : str
        The name of the model.

    Returns
    -------
    m : mdb.models[model_name]
        The Abaqus model object.
    a : mdb.models[model_name].assembly
        The Abaqus root assembly object.
    p : mdb.models[model_name].parts
        The Abaqus parts object.
    """

    m = mdb.models[model_name]
    a = m.rootAssembly
    p = m.parts

    return m, a, p


def get_kwargs_string(**kwargs):
    return " ".join(["{}:{}".format(key, value) for key, value in kwargs.items()])
