import sqlite3
import os
import datetime

import streamlit as st
import pandas as pd

from constants import *

from .data_acquisition_client import get_soiaf_data
from .pandas_client import query_to_df

def init_db():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"db_{timestamp}.sqlite"
    db = sqlite3.connect(os.path.join(DB_FOLDERPATH, filename))
    cur = db.cursor()
    
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
    
    return db, filename

def insert_to_table(cur, item, entity):
    query = f'''INSERT INTO {entity} VALUES
                    ({",".join([ "?" for i in range(len(DB_SCHEMAS[entity])) ])})
             '''
    values = tuple([ ";".join(i) if isinstance(i, list) else i for i in item.values() ])

    cur.execute(query, values)

def read_db(db_name):
    db = sqlite3.connect(os.path.join(DB_FOLDERPATH, db_name))
    return db

def table_row_count(table_name, db):
    cur = db.cursor()
    count_query = cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    for row in count_query:
        count = row[0]
    return count

def show_db_info(db, db_name):
    cur = db.cursor()
    timestamp = db_name.split("_")[1]
    table_names_query = cur.execute('''SELECT name AS table_name
                                       FROM sqlite_master
                                       WHERE type='table'
                                    ''')
    table_names_df = query_to_df(table_names_query)
    table_names_df["row_count"] = table_names_df["table_name"].apply(table_row_count, db=db)
    table_names_df["creation_date"] = table_names_df["table_name"].apply(lambda x: timestamp)

    return table_names_df

def total_count_of_each_entity(db_name):
    db = read_db(db_name)
    cur = db.cursor()

    query_sql = '''
        SELECT 'characters' AS table_name, COUNT(*) AS count_of_rows
        FROM characters
        UNION ALL
          SELECT 'books', count(*)
          FROM books
          UNION ALL
            SELECT 'houses', count(*)
            FROM houses
        '''

    query = cur.execute(query_sql)

    df = query_to_df(query)
    db.close()

    return df, query_sql


def read_table(db_name, table_name):
    db = read_db(db_name)
    cur = db.cursor()

    rows = cur.execute(f"SELECT * FROM {table_name}")
    
    results = []

    for row in rows:
        results.append({ k:row[ix] for ix, k in enumerate(DB_SCHEMAS[table_name].keys()) })
    
    db.close()

    return results

