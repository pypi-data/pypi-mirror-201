""" To make a library for making a database translaator """

import os
import json
import sqlite3

def create_database_dist(file):
    """To create a destination folder"""
    os.mkdir(file)

def parse_json(path_folder, file_name):
    """To parse the json files"""
    os.chdir(path_folder)
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data_dict = json.load(json_file)
    os.chdir('..')
    return data_dict

def get_create_connection(db_name):
    """To create an database connection for the given name"""
    conn = sqlite3.connect(db_name, timeout=5.0)
    conn.close()

def create_database(src, dist):
    """To create a connection"""
    list_of_file = os.listdir(src)
    create_database_dist(os.path.join(os.getcwd(), dist))
    os.chdir(dist)
    for file in list_of_file:
        if file.endswith('.json'):
            get_create_connection(file.replace('.json', '.db'))
    os.chdir('..')

def create_tables(table_name, db_name=''):
    """To create database tables"""
    if db_name:
        conn = sqlite3.connect(db_name)
        conn.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)')
        conn.close()

lis = []

def get_all(src, file):
    """To get all the parameters"""
    dict_equivalent = parse_json(src, file)
    for key, value in dict_equivalent.items():
        for d_k, d_v in value.items():
            k = d_v['d_type']
            v = d_v['constraints']
            data_str = f'{key} {d_k} {k} {v}'
            lis.append(data_str)

def add_columns(lis__, db_name=''):
    """To create database tables"""
    for st in lis__:
        d_l = st.split()
        if len(d_l) > 4 and d_l[3].upper() == 'NOT':
            #for not null constraint
            const = d_l[3] + ' ' + d_l[4]
        if len(d_l) > 4 and d_l[3].upper() == 'FOREIGN':
            #for not null constraint
            const = f'{d_l[3]} {d_l[4]} {d_l[5]} {d_l[6]} {d_l[7]} {d_l[8]}'
        elif d_l[3] == 'UNIQUE':
            const = d_l[3]
        constraint = const
        table_name = d_l[0]
        col_type = d_l[2]
        col_name = d_l[1]
        if db_name:
            create_tables(table_name, db_name)
            conn = sqlite3.connect(db_name)
            if constraint != 'UNIQUE':
                conn.execute(f'ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type} {constraint} ;')
            if constraint == 'UNIQUE':
                conn.execute(f'ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type};')
                conn.execute(f'CREATE UNIQUE INDEX {table_name}_{col_name}_index ON {table_name}({col_name}) ;')
            conn.close()

def get_tables(db_name):
    """To get the tables in a database"""
    os.chdir('dist')
    conn = sqlite3.connect(db_name).cursor()
    conn.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
    print(conn.fetchall())
    conn.close()
    os.chdir('..')

def main(src, dist):
    """main function"""
    create_database(src, dist)
    l = os.listdir(src)
    lo = os.listdir(dist)
    global lis
    for i in range(0, len(l)):
        get_all(src, l[i])
        add_columns(lis, f'{dist}/{lo[i]}')
        lis = []
