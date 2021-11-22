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
            FROM houses;
        '''

    query = cur.execute(query_sql)

    df = query_to_df(query)
    db.close()

    return df, query_sql

def books_and_characters(db_name):
    db = read_db(db_name)
    cur = db.cursor()

    query_sql_books = '''
        SELECT b.name, b.authors, b.released, b.characters
        FROM books b;
        '''
    query_sql_characters = '''
        SELECT c.url, c.name, c.gender, c.titles, c.aliases
        FROM characters c;
    '''
    
    query_books = cur.execute(query_sql_books)
    df_books = query_to_df(query_books)
    query_characters = cur.execute(query_sql_characters)
    df_characters = query_to_df(query_characters)

    db.close()

    def fetch_character_attr(url, attr):
        row = df_characters.loc[df_characters["url"] == url]
        if not row.empty:
            val = row.iloc[0][attr]
        else:
            val = "-"
        return val
    
    def replace_char_urls_with_attrs(urls):
        output = ""
        CACHE = {}

        for url in urls.split(";"):
            if url in CACHE.keys():
                return CACHE[url]
            # Name:
            name = fetch_character_attr(url, "name")
            if not name:
                aliases =  fetch_character_attr(url, "aliases")
                if aliases:
                    try:
                        name = " | ".join(aliases.split(";"))
                    except:
                        name = aliases
                else:
                    name = " - "
            # Gender
            gender = fetch_character_attr(url, "gender")
            if not gender:
                gender = " - "
            # Titles:
            titles = fetch_character_attr(url, "titles")
            if titles:
                try:
                    titles = " | ".join(titles.split(";"))
                except:
                    pass
            else:
                titles = " - "

            val = f"- Name: {name}, gender: {gender}, titles: {titles};\\n"
            output += val

            CACHE[url] = val

        return output

    df_books["characters"] = df_books["characters"].apply(replace_char_urls_with_attrs)

    df = df_books
    query_sql = '''Spent way too long on this query, ended up using Pandas.
        I am pretty convinced by now that it's not possible in SQLite, however
        if this was MySQL I would have used something from here:
        https://stackoverflow.com/questions/17942508/sql-split-values-to-multiple-rows'''

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

