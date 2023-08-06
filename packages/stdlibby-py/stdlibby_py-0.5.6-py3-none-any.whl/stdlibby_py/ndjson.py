import orjson as json
import os
from pathlib import Path

def to_ndjson(l: list)-> str:
   return "\n".join([json.dumps(x) for x in l]) + "\n"

def load_ndjson(filepath: str)->list|None:
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return [json.loads(x) for x in f.readlines()]
    else:
        raise Exception(f"{filepath} is not a file")

def dump_ndjson(filepath: str, data: list)->tuple:
    nd = to_ndjson(data)
    try:
        with open(filepath, "w") as f:
            f.write(nd)
            return (True,)
    except Exception as e:
        return False, e

def append_ndjson(filepath: str, data: list, create_if_not_exists: bool=False):
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

if __name__ == "__main__":
    d = [{"key": "val", "num": 22}, ["hio", 123, 44, "fffff"]]
    p = dump_ndjson("/home/nmlss/testing.ndjson", d)
    print(p)
    append_ndjson("/home/nmlss/testing.ndjson", [{"roar": "hi"}])
    dd = load_ndjson("/home/nmlss/testing.ndjson")
    print(dd)
