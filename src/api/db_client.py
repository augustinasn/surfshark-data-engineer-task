import sqlite3
import os
import datetime

import streamlit as st
import pandas as pd

from constants import *
from .data_acquisition_client import get_soiaf_data
from .pandas_client import query_to_df, replace_urls_with_col_vals

def init_db():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"db_{timestamp}.sqlite"

    try:
        db = sqlite3.connect(os.path.join(DB_FOLDERPATH, filename))
    except:
        raise "Couldn't open the DB, is it deleted?"

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
    
    db.close()

    return filename


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


def total_count_of_each_entity(db_name):
    query_sql = '''
        SELECT 'characters' AS table_name, COUNT(*) AS count_of_rows
        FROM characters
        UNION ALL
          SELECT 'books', COUNT(*)
          FROM books
          UNION ALL
            SELECT 'houses', COUNT(*)
            FROM houses;
        '''
    df = read_table_by_query(db_name, query_sql)

    return df, query_sql


def books_and_characters(db_name):
    query_sql = '''
        SELECT name, authors, released, characters
        FROM books;
        SELECT url, name, gender, titles, aliases
        FROM characters;
        
        /* Did the rest using Pandas.
        I am pretty convinced by now that it's not possible in SQLite, however
        if this was MySQL or something similiar, I would have used something from here:
        https://stackoverflow.com/questions/17942508/sql-split-values-to-multiple-rows */
        '''
    
    df_books = read_table_by_cols(db_name, table_name="books", cols=["url", "name", "authors", "released", "characters"])
    df_characters = read_table_by_cols(db_name, table_name="characters", cols=["url", "name", "authors", "released", "characters"])
    df_books["characters"] = df_books["characters"].apply(replace_urls_with_col_vals, df=df_characters, cols=["name", "gender", "titles", "aliases"])

    return df_books, query_sql


def character_names_and_played_by(db_name):
    query_sql = '''
        SELECT name, aliases, playedBy
        FROM characters;
        '''
    
    df_characters = read_table_by_query(db_name, query_sql) 

    return df_characters, query_sql


def houses_info(db_name):
    query_sql = '''
        SELECT name, region, overlord, swornMembers
        FROM houses;
        SELECT url, name, alias
        FROM characters;
        -- Rest is done with Pandas ;)
        '''
    df_houses = read_table_by_cols(db_name, "houses", "url, name, region, overlord, swornMembers")
    df_characters = read_table_by_cols(db_name, "characters", "url, name, aliases")

    df_houses["overlord"] = df_houses["overlord"].apply(replace_urls_with_col_vals, df=df_houses, cols=["name"])
    df_houses["swornMembers"] = df_houses["swornMembers"].apply(replace_urls_with_col_vals, df=df_characters, cols=["name", "aliases"])

    return df_houses, query_sql


def read_table_by_cols(db_name, table_name, cols="*"):
    db = read_db(db_name)
    cur = db.cursor()
    query = cur.execute(f'''SELECT {cols}
                            FROM {table_name}''')
    df = query_to_df(query)
    db.close()

    return df


def read_table_by_query(db_name, query):
    db = read_db(db_name)
    cur = db.cursor()
    query = cur.execute(query)
    df = query_to_df(query)
    db.close()

    return df

def delete_db(db_name):
    db_fp = os.path.join(DB_FOLDERPATH, db_name)
    try:
        os.remove(db_fp)
    except:
        raise "Can't delete this DB, perhapts it's already deleted?"
