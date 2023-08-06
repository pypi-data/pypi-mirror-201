import orjson as json
import os
from pathlib import Path

def to_ndjson(l: list)-> str:
   return "\n".join([json.dumps(x).decode("utf-8") for x in l]) + "\n"

def load(filepath: str)->list|None:
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return [json.loads(x) for x in f.readlines()]
    else:
        raise Exception(f"{filepath} is not a file")

def dump(filepath: str, data: list)->tuple:
    nd = to_ndjson(data)
    try:
        with open(filepath, "w") as f:
            f.write(nd)
            return (True,)
    except Exception as e:
        return False, e

def append(filepath: str, data: list, create_if_not_exists: bool=False):
    if not os.path.isfile(filepath):
        if create_if_not_exists:
            Path(filepath).touch()
        else:
            raise Exception(f"{filepath} does not exist, and was not automatically created")
    nd = to_ndjson(data)
    try:
        with open(filepath, "a") as f:
            f.write(nd)
            return (True,)
    except Exception as e:
        return False, e
