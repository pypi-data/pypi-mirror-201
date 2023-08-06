from abml_dataclass import Abml_Registry

# from abml_helpers import cprint
from abaqus import mdb
from abaqusConstants import ANALYSIS, DEFAULT, OFF
import os
from shutil import copy, move
from io import open
from abml_helpers import cprint


@Abml_Registry.register("jobs")
class Abml_Job:
    def __init__(self, name, model, **kwargs):  # noqa
        self.name = str(name)
        self.model = model
        self.kwargs = kwargs
        self.create()

    def create(self):
        subroutine_flag = self.kwargs.get("subroutine", False)
        if subroutine_flag:
            subroutine_path = os.path.abspath("{}.for".format(self.name))
        else:
            subroutine_path = None

        kwargs = {
            "name": self.name,
            "model": self.model.name,
            "description": self.kwargs.get("description", ""),
            "type": ANALYSIS,
            "userSubroutine": subroutine_path,
            "numCpus": self.kwargs.get("cpus", 1),
            "numGPUs": self.kwargs.get("gpus", 0),
            "multiprocessingMode": DEFAULT,
        }

        mdb.Job(**kwargs)

        if self.kwargs.get("write_input", False):
            self.write_input()
            self.add_to_header(subroutine="{}.inp".format(self.name), priority=self.kwargs.get("priority", "default"))

    def write_input(self):
        mdb.jobs[self.name].writeInput(consistencyChecking=OFF)

    def write_and_copy_input_to_path(self, path):
        self.write_input()
        self.add_to_header(subroutine="{}.inp".format(self.name), priority=self.kwargs.get("priority", "default"))
        filename = "{}.inp".format(self.name)
        copy(filename, os.path.join(path, filename))

    def write_and_move_input_to_path(self, path):
        self.write_input()
        self.add_to_header(subroutine="{}.inp".format(self.name), priority=self.kwargs.get("priority", "default"))
        filename = "{}.inp".format(self.name)
        move(filename, os.path.join(path, filename))

    def add_to_header(self, **kwargs):
        filename = "{}.inp".format(self.name)
        with open(filename, "r", encoding="utf-8") as f:
            input_file = f.readlines()

        for key, value in kwargs.items():
            input_file.insert(1, "** {key}={value}\n".format(key=key, value=value))

        with open(filename, "w", encoding="utf-8") as f:
            input_file = "".join(input_file)
            f.write(input_file)
