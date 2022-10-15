from sqlite3 import Cursor
import mysql.connector

def connect_to_my_db():
    global mydb,mycursor
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="anis")
    mycursor = mydb.cursor()
    return mydb,mycursor