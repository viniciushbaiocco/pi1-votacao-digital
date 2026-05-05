import mysql.connector

def conexao_banco():

    try:
        """
        Tenta estabelecer uma conexão com um banco de dados MySQL usando variáveis de ambiente.

        Args:
            None

        Returns: 
            Retorna um objeto de conexão MySQL se a conexão for bem-sucedida,      
            caso contrário, retorna None.
        """

        conexao = mysql.connector.connect(
            host="localhost",
            user="seu_usuario",
            password="sua_senha",
            database="peu_banco"
        )
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None
