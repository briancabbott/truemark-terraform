from __future__ import annotations

from truemark_terraform.model.core.hashimetaobj import HashiObj
from truemark_terraform.model.core.hashiregistry import HashiReg
from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

class Terraform(HashiObj): 
    HASHI_TYPE = "TERRAFORM"

    def __init__(self, *args, **kwargs):
        super().__init__(HashiReg.generate_hashi_id(), "terraform")
        self.workspace = "default"
        self.provider_properties = kwargs
        HashiReg.instance().reg_hashi(self)

    