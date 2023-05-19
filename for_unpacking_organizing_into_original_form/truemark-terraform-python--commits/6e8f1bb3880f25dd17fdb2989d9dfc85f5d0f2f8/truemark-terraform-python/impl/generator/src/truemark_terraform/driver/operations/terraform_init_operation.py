from __future__ import annotations
import subprocess

from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

class TerraformInitOperationInput(object):

    def __init__(self, backend = None, backend_config = None, force_copy = None, from_module = None, get = None, 
                       get_plugins = None, input = None, lock = None, lock_timeout = None,
                       no_color = None, plugin_dir = None, reconfigure = None, upgrade = None, verify_plugins = None):
        self.backend = backend
        self.backend_config = backend_config 
        self.force_copy = force_copy
        self.from_module = from_module
        self.get = get
        self.get_plugins = get_plugins
        self.input = input
        self.lock = lock
        self.lock_timeout = lock_timeout
        self.no_color = no_color
        self.plugin_dir = plugin_dir
        self.reconfigure = reconfigure
        self.upgrade = upgrade
        self.verify_plugins = verify_plugins

    def __str__(self):
        return f'TerraformInitOperationInput(\n\t \
            backend = {self.backend}, \n\t \
            backend_config = {self.backend_config}, \n\t \
            force_copy = {self.force_copy}, \n\t \
            from_module = {self.from_module}, \n\t \
            get = {self.get}, \n\t \
            get_plugins = {self.get_plugins}, \n\t \
            input = {self.input}, \n\t \
            lock = {self.lock}, \n\t \
            lock_timeout = {self.lock_timeout}, \n\t \
            no_color = {self.no_color}, \n\t \
            plugin_dir = {self.plugin_dir}, \n\t \
            reconfigure = {self.reconfigure}, \n\t \
            upgrade = {self.upgrade}, \n\t \
            verify_plugins = {self.verify_plugins})'

    def __repr__(self):
        return f'TerraformInitOperationInput(backend = {self.backend}, backend_config = {self.backend_config}, \n\
            force_copy = {self.force_copy}, from_module = {self.from_module}, get = {self.get}, get_plugins = {self.get_plugins}, \n\
            input = {self.input}, lock = {self.lock}, lock_timeout = {self.lock_timeout}, no_color = {self.no_color}, \n\
            plugin_dir = {self.plugin_dir}, reconfigure = {self.reconfigure}, upgrade = {self.upgrade}, verify_plugins = {self.verify_plugins})'

    def to_dict(self) -> dict:
        d = dict()
        d['backend'] = self.backend
        d['backend_config'] = self.backend_config
        d['force_copy'] = self.force_copy
        d['from_module'] = self.from_module
        d['get'] = self.get
        d['get_plugins'] = self.get_plugins
        d['input'] = self.input
        d['lock'] = self.lock
        d['lock_timeout'] = self.lock_timeout
        d['no_color'] = self.no_color
        d['plugin_dir'] = self.plugin_dir
        d['reconfigure'] = self.reconfigure
        d['upgrade'] = self.upgrade
        d['verify_plugins'] = self.verify_plugins
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformInitOperationInput:
        input = TerraformInitOperationInput(backend =           d['backend'],
                                            backend_config =    d['backend_config'], 
                                            force_copy =        d['force_copy'],
                                            from_module =       d['from_module'],
                                            get =               d['get'],
                                            get_plugins =       d['get_plugins'],
                                            input =             d['input'],
                                            lock =              d['lock'],
                                            lock_timeout =      d['lock_timeout'],
                                            no_color =          d['no_color'],
                                            plugin_dir =        d['plugin_dir'],
                                            reconfigure =       d['reconfigure'],
                                            upgrade =           d['upgrade'],
                                            verify_plugins =    d['verify_plugins'])
        return input

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformInitOperationInput:
        d = dict_to_json(json_str)
        return TerraformInitOperationInput.from_dict(d)


class TerraformInitOperationOutput(object):

    def __init__(self):
        pass

    @staticmethod
    def from_process(process: subprocess.CompletedProcessocess[str]) -> TerraformInitOperationOutput:
        pass

    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(cls, d: dict) -> TerraformInitOperationOutput:
        pass

    def to_json_dict(self) -> dict:
        pass

    def to_json(self) -> str:
        pass

    @staticmethod
    def from_json(cls, json_str: str) -> TerraformInitOperationOutput:
        pass