from __future__ import annotations
import subprocess

from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

class TerraformPlanOperationInput(object):
    def __init__(self, compact_warnings = None, destroy = None, detailed_exitcode = None, 
                       input = None, lock = None, lock_timeout = None, 
                       no_color = None, out = None, parallelism = None, refresh = None, 
                       state = None, target = None, var = None, var_file = None):
        self.compact_warnings = compact_warnings
        self.destroy = destroy
        self.detailed_exitcode = detailed_exitcode 
        self.input = input
        self.lock = lock
        self.lock_timeout = lock_timeout 
        self.no_color = no_color
        self.out = out
        self.parallelism = parallelism
        self.refresh = refresh
        self.state = state
        self.target = target
        self.var = var
        self.var_file = var_file

    def to_dict(self) -> dict:
        d = dict()
        d['compact_warnings'] = self.compact_warnings
        d['destroy'] = self.destroy
        d['detailed_exitcode'] = self.detailed_exitcode 
        d['input'] = self.input
        d['lock'] = self.lock
        d['lock_timeout'] = self.lock_timeout 
        d['no_color'] = self.no_color
        d['out'] = self.out
        d['parallelism'] = self.parallelism
        d['refresh'] = self.refresh
        d['state'] = self.state
        d['target'] = self.target
        d['var'] = self.var
        d['var_file'] = self.var_file
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformPlanOperationInput:
        input = TerraformPlanOperationInput(compact_warnings =  d['compact_warnings'],
                                            destroy =           d['destroy'],
                                            detailed_exitcode = d['detailed_exitcode'], 
                                            input =             d['input'],
                                            lock =              d['lock'],
                                            lock_timeout =      d['lock_timeout'], 
                                            no_color =          d['no_color'],
                                            out =               d['out'],
                                            parallelism =       d['parallelism'],
                                            refresh =           d['refresh'],
                                            state =             d['state'],
                                            target =            d['target'],
                                            var =               d['var'],
                                            var_file =          d['var_file'])
        return input

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformPlanOperationInput:
        d = dict_to_json(json_str)
        return TerraformPlanOperationInput.from_dict(d)



class TerraformPlanOperationOutput(object):
    def __init__(self):
        pass

    @staticmethod
    def from_process(process: subprocess.CompletedProcessocess[str]) -> TerraformPlanOperationOutput:
        pass
    
    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformPlanOperationOutput:
        pass

    def to_json_dict(self) -> dict:
        pass

    def to_json(self) -> str:
        pass

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformPlanOperationOutput:
        pass