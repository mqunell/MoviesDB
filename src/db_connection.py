import json
import pymysql.cursors
import os
"""
SETUP:
$ sudo mysql_secure_installation

> create user 'username'@'localhost' identified by 'password';
> create database Movies;
> grant all on Movies.* to 'username'@'localhost' identified by 'password';

$ sudo systemctl restart mariadb.service

> source {path}/CreateTables.sql;
"""


# Parse database information
with open('data/keys.json') as keys_json_file:
    db_keys = json.load(keys_json_file)['database']

# Connect to the database
connection = pymysql.connect(host=db_keys['host'],
                             user=db_keys['user'],
                             password=db_keys['password'],
                             db=db_keys['db'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_db_connection():
    return connection
