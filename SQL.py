import os

import mariadb
from dotenv import load_dotenv

load_dotenv()
PW = os.getenv('SQL_PW')
DB = os.getenv('SQL_DB')
USER = os.getenv('SQL_USER')


def setupSQL():
    conn = mariadb.connect(user=USER, password=PW, host="localhost", database=DB)
    conn.cursor().close()
    cur = conn.cursor()
    try:
        # Creating a new table
        query = ("CREATE TABLE mal (`discord_user` VARCHAR(45) NOT NULL, `mal_user` VARCHAR(45) NOT NULL, PRIMARY KEY "
                 + "(`discord_user`));")
        cur.execute(query)
        conn.close()
    except mariadb.Error as e:
        print(f"Error d1: {e}")


def execute():
    conn = mariadb.connect(user=USER, password=PW, host="localhost", database=DB)
    conn.cursor().close()
    cur = conn.cursor()
    try:
        result = None
        for cur in cur:
            result = cur
        return result
    except mariadb.Error as e:
        print(f"Error b1: {e}")


def checkLink(discord):
    conn = mariadb.connect(user=USER, password=PW, host="localhost", database=DB)
    conn.cursor().close()
    cur = conn.cursor()
    try:
        result = []
        command = f"SELECT * FROM mal WHERE discord_user='{discord}';"
        cur.execute(command)
        for (mal_user) in cur:
            result.append(f"{mal_user}")
        return result
    except mariadb.Error as e:
        print(f"Error a1: {e}")


def addLink(discord, mal):
    conn = mariadb.connect(user=USER, password=PW, host="localhost", database=DB)
    conn.cursor().close()
    cur = conn.cursor()
    try:
        command = f"INSERT INTO mal(discord_user, mal_user) VALUES ('{discord}', '{mal}');"
        cur.execute(command)
        conn.commit()
        cur.close()
    except mariadb.Error as e:
        if str(e).__contains__('Duplicate entry'):
            return "duplicate"
        print(f"Error g1: {e}")


def delLink(discord):
    conn = mariadb.connect(user=USER, password=PW, host="localhost", database=DB)
    conn.cursor().close()
    cur = conn.cursor()
    try:
        command = f"DELETE FROM mal WHERE discord_user='{discord}';"
        cur.execute(command)
        conn.commit()
        cur.close()
    except mariadb.Error as e:
        print(f"Error g1: {e}")
