import mysql.connector as mc
from mysql.connector import Error, MySQLConnection
from dotenv import load_dotenv
from os import getenv
from typing import Optional

class Database:

    def __init__(self) -> None:
        load_dotenv()
        self.host = getenv("DB_HOST")
        self.user = getenv("DB_USER")
        self.password = getenv("DB_PSWD")
        self.database = getenv("DB_NAME")
        self.connection: MySQLConnection | None = None
        self.cursor: Optional[mc.cursor.MySQLCursor] = None


    def conectar(self) -> None:
        """Estabelece a conexão com o banco de dados MySQL.
        """
        try:
            self.connection = mc.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Conexão bem-sucedida ao banco de dados.")
        except Error as e:
            print(f"Erro ao conectar-se ao banco de dados: {e}")
            self.connection = None
            self.cursor = None

    def desconectar(self) -> None:
        """Encerra a conexão com o banco de dados MySQL.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexão ao banco de dados encerrada.")