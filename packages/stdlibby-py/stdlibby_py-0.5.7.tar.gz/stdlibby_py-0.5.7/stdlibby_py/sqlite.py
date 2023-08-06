import sqlite3
import json
from typing import TypedDict, Any

class Column(TypedDict):
    cid: int
    name: str
    type: str
    notnull: int
    dlft_value: Any
    pk: int

class TableDef(TypedDict):
    table_name: str
    init_sql: str
    num_columns: int
    columns: Column

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_tables(con: sqlite3.Connection):
    """
    Returns the name of every table in the default DB
    """
    cur = con.cursor()
    res = cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
    p = [{"table_name": x[1], "init_sql": x[-1], "columns": x[3]} for x in res.fetchall()]
    cur.row_factory = dict_factory
    for i in p:
         r = cur.execute(f"pragma table_info({i['table_name']})")
         i["column_data"] = r.fetchall()
    cur.close()
    return p

def has_table_definition_changed(con: sqlite3.Connection):
    pass

def is_table(con: sqlite3.Connection, table_name: str):
    if table_name in get_tables(con):
        return True
    else:
        return False

def init_sqlite(tables: list[TableDef])->sqlite3.Connection:
    print(tables)

def backup_table(con: sqlite3.Connection, table_name: str):
    pass

def dict_to_where_clause(d: dict)->str:
    res = []
    for kv in d.items():
        if " " in kv[0]:
            key = kv[0].replace(" ", "_")
        else:
            key = kv[0]

        if isinstance(kv[1], str):
            val = f"'{kv[1]}'"
        else:
            val = kv[1]
        res.append(f"{key}={val}")
    return ", ".join(res)

if __name__ == "__main__":
    t = get_tables(sqlite3.connect("/shared/todos/default.db"))
    print(json.dumps(t, indent=4))
