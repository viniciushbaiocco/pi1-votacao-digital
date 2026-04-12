import mysql.connector

def conexao_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="seu_usuario",
            password="sua_senha",
            database = "seu_banco"
    )
        print("Conexão bem sucedida!")
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None



