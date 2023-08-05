import secrets

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
