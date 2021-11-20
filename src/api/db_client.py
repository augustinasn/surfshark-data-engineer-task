import sqlite3
import os

import streamlit as st

from constants import *
from .data_acquisition_client import get_soiaf_data

def init_db():
    exists = True if os.path.exists(DB_FILEPATH) else False
    db = sqlite3.connect(DB_FILEPATH)
    cur = db.cursor()
    
    if not exists:
        for entity, schema in DB_SCHEMAS.items():
            values = ",".join([ k + " " + v for k, v in schema.items() ])
            query = f'''CREATE TABLE {entity}
                            ({values})
                     '''
            cur.execute(query)

            data = get_soiaf_data(entity)

            for i in data:
                insert_to_table(cur, i, entity)
                db.commit()
    
    return db

def insert_to_table(cur, item, entity):
    query = f'''INSERT INTO {entity} VALUES
                    ({",".join([ "?" for i in range(len(DB_SCHEMAS[entity])) ])})
             '''
    values = tuple([ ";".join(i) if isinstance(i, list) else i for i in item.values() ])

    cur.execute(query, values)


def read_table(table_name):
    db = init_db()
    cur = db.cursor()

    rows = cur.execute(f"SELECT * FROM {table_name}")
    
    results = []

    for row in rows:
        results.append({ k:row[ix] for ix, k in enumerate(DB_SCHEMAS[table_name].keys()) })
    
    db.close()

    return results

