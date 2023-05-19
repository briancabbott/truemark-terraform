from __future__ import annotations
import subprocess

from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

class TerraformValidateOperationInput(object):
    def __init__(self, json = None, no_color = None):
        self.json = json 
        self.no_color = no_color

    def to_dict(self) -> dict:
        d = dict()
        d['json'] = self.json 
        d['no_color'] = self.no_color
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformValidateOperationInput:
        input = TerraformValidateOperationInput(json = d['json'], no_color = d['no_color'])
        return input 

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformValidateOperationInput:
        d = dict_to_json(json_str)
        return TerraformValidateOperationInput.from_dict(d)

class TerraformValidateOperationOutput(object):
    def __init__(self):
        pass
    
    @staticmethod
    def from_process(process: subprocess.CompletedProcessocess[str]) -> TerraformValidateOperationOutput:
        pass
    
    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformValidateOperationOutput:
        pass

    def to_json_dict(self) -> dict:
        pass

    def to_json(self) -> str:
        pass

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformValidateOperationOutput:
        pass