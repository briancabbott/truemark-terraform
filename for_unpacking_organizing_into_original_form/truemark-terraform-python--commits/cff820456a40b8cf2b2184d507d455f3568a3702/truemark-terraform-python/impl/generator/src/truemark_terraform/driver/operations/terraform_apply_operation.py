from __future__ import annotations
import subprocess

from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

class TerraformApplyOperationInput(object):

    def __init__(self, auto_approve = None, backup = None, compact_warnings = None, 
                       lock = None, lock_timeout = None, input = None, no_color = None, 
                       parallelism = None, refresh = None, state = None, var = None, 
                       stateout = None, target = None, var_file = None):
        self.auto_approve = auto_approve
        self.backup = backup
        self.compact_warnings = compact_warnings
        self.lock = lock
        self.lock_timeout = lock_timeout
        self.input = input
        self.no_color = no_color
        self.parallelism = parallelism
        self.refresh = refresh
        self.state = state
        self.var = var
        self.stateout = stateout
        self.target = target
        self.var_file = var_file

    def to_dict(self) -> dict:
        d = dict()
        d['auto_approve'] = self.auto_approve
        d['backup'] = self.backup
        d['compact_warnings'] = self.compact_warnings
        d['lock'] = self.lock
        d['lock_timeout'] = self.lock_timeout
        d['input'] = self.input
        d['no_color'] = self.no_color
        d['parallelism'] = self.parallelism
        d['refresh'] = self.refresh
        d['state'] = self.state
        d['var'] = self.var
        d['stateout'] = self.stateout
        d['target'] = self.target
        d['var_file'] = self.var_file
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformApplyOperationInput:
        input = TerraformApplyOperationInput(auto_approve = d['auto_approve'], 
                                             backup =       d['backup'], 
                                             compact_warnings = d['compact_warnings'], 
                                             lock =         d['lock'], 
                                             lock_timeout = d['lock_timeout'], 
                                             input =        d['input'],
                                             no_color =     d['no_color'], 
                                             parallelism =  d['parallelism'], 
                                             refresh =      d['refresh'], 
                                             state =        d['state'], 
                                             var =          d['var'], 
                                             stateout =     d['stateout'], 
                                             target =       d['target'], 
                                             var_file =     d['var_file'])
        return input

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformApplyOperationInput:
        d = dict_to_json(json_str)
        return TerraformApplyOperationInput.from_dict(d)


class TerraformApplyOperationOutput(object):

    def __init__(self):
        pass

    @staticmethod
    def from_process(process: subprocess.CompletedProcessocess[str]) -> TerraformApplyOperationOutput:
        pass

    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformApplyOperationOutput:
        pass

    def to_json_dict(self) -> dict:
        pass

    def to_json(self) -> str:
        pass

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformApplyOperationOutput:
        pass