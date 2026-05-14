import os
import mysql.connector
from dotenv import load_dotenv


#################### MUDANCA IMPORTANTE!!!!!!
# crie um arquivo chamado .env(literalmente, só crie um .env sem nome nenhum) fora de qualquer pasta
# bota as suas credenciais do banco de dados. igual esse modelo, substituindo o texto apos o = pelo oq vc usa:

#   DB_HOST=localhost
#   DB_USER=root
#   DB_PASSWORD=sua_senha
#   DB_NAME=projeto_integrador

# o arquivo .env.example já tem o modelo pronto pra copiar
# nao commite o .env com senha real, ele já está no .gitignore (obrigado deus baiocco)
# essa mudança foi necessaria pra evitar trabalho pesado de commitar toda vez tendo que alterar credencial do banco de dados

# precisa de uma biblioteca nova (instale uma vez):
#   pip install python-dotenv

load_dotenv() #pega as credenciais no .env, pra substituir ali em baixo

def conexao_banco():
    try:
        conexao = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"), #localhost é 2° opcao, caso nao tenha nada la no .env
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
        )
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None
