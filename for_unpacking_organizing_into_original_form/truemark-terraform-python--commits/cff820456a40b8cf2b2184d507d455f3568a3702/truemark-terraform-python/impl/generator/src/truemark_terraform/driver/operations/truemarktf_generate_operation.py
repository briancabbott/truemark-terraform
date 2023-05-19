from __future__ import annotations
import subprocess

from typing import List
from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

class TruemarkTFGenerateOperationInput(object):
    def __init__(self, py_files: List[str] = None, *py_instances):
        self.py_files = py_files
        self.py_instances = py_instances

    def to_dict(self) -> dict:
        d = dict()
        d['py_files'] = self.py_files
        d['py_instances'] = self.py_instances
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> TruemarkTFGenerateOperationInput:
        input = TruemarkTFGenerateOperationInput(py_files = d['py_files'], py_instances = d['py_instances'])
        return input

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> TruemarkTFGenerateOperationInput:
        d = dict_to_json(json_str)
        return TruemarkTFGenerateOperationInput.from_dict(d)


class TruemarkTFGenerateOperationOutput(object):
    def __init__(self, hcl_contents: List[str]):
        self.hcl_contents = hcl_contents

    @staticmethod
    def from_process(process: subprocess.CompletedProcessocess[str]) -> TruemarkTFGenerateOperationOutput:
        pass

    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(cls, d: dict) -> TruemarkTFGenerateOperationOutput:
        pass

    def to_json_dict(self) -> dict:
        pass

    def to_json(self) -> str:
        pass

    @staticmethod
    def from_json(cls, json_str: str) -> TruemarkTFGenerateOperationOutput:
        pass