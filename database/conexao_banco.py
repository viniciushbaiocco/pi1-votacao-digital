import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conexao_banco():
    """
    Estabelece uma conexão com o banco de dados MySQL utilizando variáveis de ambiente.

    A função tenta abrir uma conexão utilizando as credenciais configuradas nas
    variáveis de ambiente do sistema. Caso a variável 'DB_HOST' não seja encontrada,
    ela adota 'localhost' como padrão. Em caso de falha na autenticação ou na
    comunicação com o banco, o erro é exibido no terminal.

    Args:
        None.

    Returns:
        mysql.connector.connection.MySQLConnection ou None: Retorna o objeto de
        conexão ativa se for bem-sucedido, ou None se ocorrer um erro do MySQL.

    Raises:
        KeyError: Se alguma das variáveis de ambiente obrigatórias ('DB_USER',
        'DB_PASSWORD' ou 'DB_NAME') não estiver definida no sistema.
        """
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
