from conexao_banco import  conexao_banco
import random

def geracao_chave_acesso(nome):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    numero = random.randint(1000, 9999)

    partes_nome = nome.split()
    primeiro_nome = partes_nome[0]
    primeiro_sobrenome = partes_nome[1]

    iniciais_nome = primeiro_nome[:2].upper()
    inicial_sobrenome = primeiro_sobrenome[0].upper()

    chave_acesso = iniciais_nome + inicial_sobrenome + str(numero)

    print(f"Chave de acesso {chave_acesso} criada para o eleitor {nome}")

    """
    Teste para ver se a chave estava indo para o banco
    sql_formula = 'UPDATE cadastro_eleitores SET chave_acesso = %s WHERE id = %s'
    try:
        cursor = conexao.cursor()
        cursor.execute(sql_formula, (chave_acesso, id))
        conexao.commit()
        print(f"Chave de acesso {chave_acesso} criada para o eleitor {nome}")
    except Exception as e:
        print(f"Erro ao criar chave de acesso: {e}")
        conexao.rollback()
    finally:
        if ("cursor" in locals() and cursor):
            cursor.close()
        if (conexao):
            conexao.close()
    """


geracao_chave_acesso("Jonas da Silva")


