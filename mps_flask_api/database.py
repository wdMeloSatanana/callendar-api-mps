import mysql.connector

from flask import g
from dotenv import dotenv_values

config = dotenv_values("../.env")


mydb = mysql.connector.connect(
    host=config['DB_HOST'],
    user=config['DB_USER'],
    password=config['DB_PASS'],
    database=config['DB_NAME']
)

print("Conectado em: ", mydb.get_server_info())

if mydb.is_connected():
    db_info = mydb.get_server_info()
    print('Conectado ao servidor MySQL', db_info)
    cursor = mydb.cursor()
    cursor.execute("SHOW TABLES")
    listaDB = [str(val[0]) for val in cursor]
    print(listaDB)

    tabelas = [['users'], ['event']]
    if (tabelas[0] not in listaDB) or (tabelas[1] not in listaDB):
        #cursor.execute("CREATE DATABASE users")
        mydb.database=config['DB_NAME']
        
        try:
            cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, active TINYINT NOT NULL DEFAULT 1)")
        except:
            print("Criação de tabela 'users' rejeitada")
        
        try:
            cursor.execute("CREATE TABLE event (id INTEGER PRIMARY KEY AUTO_INCREMENT, author_id INTEGER NOT NULL, CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(), title TEXT NOT NULL, body TEXT NOT NULL, time TEXT NOT NULL, FOREIGN KEY (author_id) REFERENCES users (id), active TINYINT NOT NULL DEFAULT 1)")
        except:
            print("Criação de tabela events rejeitada")


        mydb.commit()
    mydb.database=config['DB_NAME']

def get_db():
    db = define_db().cursor(dictionary=True)
    db.execute(
        'SELECT p.id, title, body, created, author_id, username, time'
        ' FROM event p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC')
    posts = db.fetchall()
    return posts

def define_db():
    if 'db' not in g: 
        g.db = mysql.connector.connect(
        host=config['DB_HOST'],
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME']
    )
    return g.db


if mydb.is_connected():
    cursor.close()
    mydb.close()
    print("Conexão MySQL encerrada.")


