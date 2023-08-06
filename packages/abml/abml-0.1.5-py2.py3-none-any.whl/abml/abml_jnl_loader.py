# from abaqus import Mdb
from json import JSONEncoder, dumps
from numpy import ndarray, empty, array, vstack
import __main__

import argparse
import os
from io import open

from abaqus import Mdb
from abaqus import *  # noqa # type: ignore[import-star]
from abml import abml_helpers


parser = argparse.ArgumentParser()
parser.add_argument("--filename")
parser.add_argument("--calls", "-c", nargs="+", help="sequence calls")

args, _ = parser.parse_known_args()

os.environ["ABAQUS_NO_MPI"] = "true"


class NumpyArrayEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ndarray):
            return o.round(10).tolist()
        if isinstance(o, dict):
            new_dict = {}
            for k, v in o.items():
                if isinstance(v, ndarray):
                    new_dict[k] = v.round(10).tolist()
                elif isinstance(v, dict):
                    new_dict[k] = self.default(v)
                else:
                    new_dict[k] = v
            return new_dict
        return JSONEncoder.default(self, o)


def extract_hierarchy(input_str):
    hierarchy = []
    current = ""
    is_quoted = False

    for char in input_str:
        if char == "'":
            is_quoted = not is_quoted
        elif is_quoted:
            current += char
        elif char == "[":
            if current:
                hierarchy.append(current)
            current = ""
        elif char == "]":
            if current:
                hierarchy.append(current)
            current = ""
        elif char == ".":
            if current:
                hierarchy.append(current)
            current = ""
        else:
            current += char

    if current:
        hierarchy.append(current)

    return hierarchy


def get_vertices(repositories, vertices):
    repositories = array([repositories]).flatten()

    vertices_extract = empty((len(repositories), 3))
    for repository in repositories:
        for vertex_index in repository.getVertices():
            vertices_extract = vstack((vertices_extract, vertices[vertex_index].pointOn))

    return vertices_extract


def get_nested_value(d, *keys):
    for key in keys:
        if not isinstance(d, (dict, object)):
            return None
        if isinstance(d, dict):
            d = d.get(key)
            if isinstance(d, dict):
                for val in d.values():
                    if not isinstance(val, object):
                        return None
        elif isiterable(d):
            try:
                d = getattr(d, key)
            except AttributeError:
                d = d[int(key)]
        else:
            try:
                d = getattr(d, key)
            except AttributeError:
                d = d[key]

    return d


def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


# def load_data_from_jnl(jnl, model_name="Model-1"):
#     mdb = Mdb()
#     execfile(jnl, __main__.__dict__)  # noqa

#     m = mdb.models[model_name]
#     p = m.parts

#     data = {}
#     data["parts"] = {}
#     for part_key, part in p.items():
#         data["parts"][part_key] = {}
#         data_part = data["parts"][part_key]
#         data_part["vertices"] = {"cells": get_vertices(part.vertices)}
#         data_part["sets"] = get_part_sets(part.sets)

#     return data


def drop_strings(input_list, strings_to_drop):
    return [elem for elem in input_list if elem not in strings_to_drop]


def del_files():
    for file in os.listdir("."):
        if ".rpy" in file or ".rec" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass


if __name__ == "__main__":
    mdb = Mdb()
    execfile(args.filename, __main__.__dict__)  # noqa

    m = mdb.models
    abml_helpers.print_to_console(args.calls)
    for call in args.calls:
        call = extract_hierarchy(call)

        repository_call = drop_strings(call, ["mdb", "models"])
        repository = get_nested_value(m, *repository_call)

        vertices_call = repository_call[:-1]
        vertices_call.append("vertices")
        vertices = get_nested_value(m, *vertices_call)
        vertices_export = get_vertices(repository, vertices)

        abml_helpers.print_to_console(repository, "#+#")
        abml_helpers.print_to_console(vertices_export, "#+#")

        with open(args.filename.replace(".jnl", ".json"), mode="w", encoding="utf8") as f:
            json_str = dumps(vertices_export, ensure_ascii=False, cls=NumpyArrayEncoder, indent=2)

            if isinstance(json_str, str):
                json_str = json_str.decode("utf-8")

            f.write(json_str)
            # dump(vertices, f, cls=NumpyArrayEncoder, indent=2, ensure_ascii=False)

    del_files()
    # todo: jnl-gen -k Model-1 -k parts -k Part-1 -k faces -k [0]

    # mdb.saveAs(pathName="my_model.cae")

    # with open(args.filename.replace(".jnl", ".json"), mode="w", encoding="utf-8") as f:
    #     dump(data, f, cls=NumpyArrayEncoder)
