import json
import datetime

from collections.abc import Iterable

def iterable(obj):
    return isinstance(obj, Iterable)

def datetime_handler(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def serialize_obj_to_json(obj):
    json_obj = None
    if hasattr(obj, "to_json_dict"):
        json_obj = obj.to_json_dict()
    else:
        json_obj = obj
    pretty_json = json.dumps(json_obj, sort_keys=True, indent=4, default=datetime_handler, ensure_ascii=False)
    return pretty_json

def deserialize_obj_from_json(obj):
    database_dict = json.loads(obj)
    return database_dict

def write_obj(filepath, obj):
    with open(filepath, 'w') as filehandle:
        filehandle.write(obj)

def read_obj(filepath):
    with open (filepath, "r") as filestream:
        json = filestream.read()
        return json

def write_json(filepath, obj):
    if hasattr(obj, "to_json_dict"):
        write_obj(filepath, serialize_obj_to_json(obj.to_json_dict()))
    else:
        write_obj(filepath, serialize_obj_to_json(obj))

def read_json(filepath):
    json = read_obj(filepath)
    return deserialize_obj_from_json(json)

def print_json(obj):
    json_pretty = serialize_obj_to_json(obj)
    print(json_pretty)

def array_to_json(arr):
    if arr != None and iterable(arr) and len(arr) > 0:
        json_arr = []
        for elem in arr:
            if hasattr(elem, "to_json_dict"):
                json_arr.append(elem.to_json_dict())
            else:
                json_arr.append(elem)
        return json_arr
    else:
        return []

def json_to_array(arr):
    return deserialize_obj_from_json(arr)

def dict_to_json(dict_val):
    keys = dict_val.keys()
    json_dict = {}
    for key in keys:
        val = dict_val.get(key)
        if hasattr(val, "to_json_dict"):
            json_dict[key] = val.to_json_dict()
        elif isinstance(val, list):
            elems_list = []
            for inst in val:
                if hasattr(inst, "to_json_dict"):
                    elems_list.append(inst.to_json_dict())
                else:
                    print("WARNING: Appending non-json-able object-instance to dictionary list.")
                    elems_list.append(inst)
            json_dict[key] = val
    return json_dict