import secrets
import orjson
import os

def load_ndjson(filepath: str)->list:
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return list(map(lambda x: orjson.loads(x), f.readlines()))
    else:
        Exception(f"{filepath} is not a file")

def dump_ndjson(filepath: str, data: list)->tuple:
    ndjson = list(map(lambda x: orjson.dumps(x), data))
    try:
        with open(filepath, "w") as f:
            f.writelines(ndjson)
            return (True,)
    except Exception as e:
        return False, e

def gen_id(n: int=3):
    def a():
        choices = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
        return "".join(list(map(lambda _: secrets.choice(choices), range(0, 5))))
    return "-".join(list(map(lambda _: a(), range(0, n))))

def gen_id2(prefix: str):
    if len(prefix) > 2:
        raise Exception("Prefixs must be less 2 characters long")
    choices = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
    id = "".join(list(map(lambda _: secrets.choice(choices), range(0, 12))))
    return f"{prefix}:{id}"
