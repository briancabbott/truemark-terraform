from __future__ import annotations
import subprocess

from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

class TerraformDestroyOperationInput(object):
    def __init__(self, backup = None, auto_approve = None, force = None, lock = None, lock_timeout = None, no_color = None, 
                              parallelism = None, refresh = None, state = None, state_out = None, target = None, var = None, var_file = None):
        self.backup = backup,
        self.auto_approve = auto_approve,
        self.force = force, 
        self.lock = lock,
        self.lock_timeout = lock_timeout, 
        self.no_color = no_color,
        self.parallelism = parallelism,
        self.refresh = refresh, 
        self.state = state, 
        self.state_out = state_out, 
        self.target = target, 
        self.var = var, 
        self.var_file = var_file 

    def to_dict(self) -> dict:
        d = dict()
        d['backup'] = self.backup
        d['auto_approve'] = self.auto_approve
        d['force'] = self.force
        d['lock'] = self.lock
        d['lock_timeout'] = self.lock_timeout 
        d['no_color'] = self.no_color
        d['parallelism'] = self.parallelism
        d['refresh'] = self.refresh
        d['state'] = self.state
        d['state_out'] = self.state_out 
        d['target'] = self.target
        d['var'] = self.var
        d['var_file'] = self.var_file

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformDestroyOperationInput:
        input = TerraformDestroyOperationInput(backup =            d['backup'],
                                               auto_approve =      d['auto_approve'],
                                               force =             d['force'], 
                                               lock =              d['lock'],
                                               lock_timeout =      d['lock_timeout'],
                                               no_color =          d['no_color'],
                                               parallelism =       d['parallelism'],
                                               refresh =           d['refresh'],
                                               state =             d['state'],
                                               state_out =         d['state_out'],
                                               target =            d['target'],
                                               var =               d['var'],
                                               var_file =          d['var_file'])
        return input

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformDestroyOperationInput:
        d = dict_to_json(json_str)
        return TerraformDestroyOperationInput.from_dict(d)


class TerraformDestroyOperationOutput(object):
    def __init__(self):
        pass 

    @staticmethod
    def from_process(process: subprocess.CompletedProcessocess[str]) -> TerraformDestroyOperationOutput:
        pass
    
    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformDestroyOperationOutput:
        pass

    def to_json_dict(self) -> dict:
        pass

    def to_json(self) -> str:
        pass

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformDestroyOperationOutput:
        pass