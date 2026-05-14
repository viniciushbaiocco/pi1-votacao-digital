import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conexao_banco():
    try:
        conexao = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
        )
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None
