from __future__ import annotations

import json
import string

from terraform_schema.model.type import Type

class DataObject():
    def __init__(self, name: str = None, 
                       fields: list[DataField] = []):
        self.name = name
        self.fields = fields

    def reindent(self, s, numSpaces):
        s = s.split('\n')
        s = [(numSpaces * ' ') + line.lstrip() for line in s]
        s = '\n'.join(s)
        return s

    def to_python(self):
        fields_param_py = ["{name}".format(name = f.field_name) for f in self.fields]
        params = ", ".join(fields_param_py)

        fields_ctor_py = ["       self.{name} = {name}".format(name=f.field_name) for f in self.fields]
        ctor = "\n".join(fields_ctor_py)
        ctor = self.reindent(ctor, 8)
        
        py_str = "class {data_obj}():\n" \
                 "    def __init__(self, {params}):\n"
        py_str = py_str + ctor
        py_str = py_str.format(data_obj = self.name, params = params)
        return py_str

    def __dict__(self) -> dict:
        d = {}
        d['name'] = self.name
        df_l = []
        for df in self.fields:
            df_l.append(df.__dict__())
        d['fields'] = df_l
        return d

    def to_dict(self) -> dict:
        return self.__dict__()

    @staticmethod
    def from_dict(d: dict) -> DataObject:
        data_obj = DataObject()
        data_obj.name = d['name']
        data_obj.fields = d['fields']
        return data_obj

    def to_json(self) -> str:
        json_str = json.dumps(self.to_dict())
        return json_str

    @staticmethod
    def from_json(json_str: str) -> DataObject:
        json_dict = json.loads(json_str)
        return DataObject.from_dict(json_dict)

class DataField():    
    def __init__(self, field_name: str = None, 
                       field_type: Type = None, 
                       computed: bool = None, 
                       optional: bool = None) -> None:
        self.field_name = field_name
        self.field_type = field_type
        self.computed = computed
        self.optional = optional

    def to_python(self) -> str:
        pass

    def __dict__(self) -> dict:
        d = {}
        d['field_name'] = self.field_name
        d['field_type'] = self.field_type
        d['computed'] = self.computed
        d['optional'] = self.optional
        return d

    def to_dict(self):
        return self.__dict__()

    @staticmethod
    def from_dict(d: dict) -> DataField:
        data_def = DataField()
        data_def.field_name = d['field_name']
        data_def.field_type = d['field_type']
        data_def.computed = d['computed']
        data_def.optional = d['optional']
        return data_def

    def to_json(self) -> str:
        json_str = json.dumps(self.to_dict())
        return json_str

    @staticmethod
    def from_json(json_str: str) -> DataField:
        json_obj = json.loads(json_str)
        return DataField.from_dict(json_obj)