import os
import mysql.connector


def conectar():

    conexao = mysql.connector.connect(

        host=os.getenv("MYSQLHOST"),

        port=int(os.getenv("MYSQLPORT")),

        user=os.getenv("MYSQLUSER"),

        password=os.getenv("MYSQLPASSWORD"),

        database=os.getenv("MYSQLDATABASE")

    )

    return conexao