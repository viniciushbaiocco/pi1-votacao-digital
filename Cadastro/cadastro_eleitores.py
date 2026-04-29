from Verificadores import validacao_cpf
from Verificadores import verificacao_cpf_banco
from Verificadores import validacao_titulo
from Verificadores import verificacao_titulo_banco
from Verificadores import validacao_nome
from database import conexao_banco
from criptografia import criptografia as cripto
from Cadastro import chave_acesso


def cadastrar_eleitor():
    """
    Realiza o cadastro completo de um eleitor no sistema, validando nome,
    CPF e título de eleitor antes de inserir os dados no banco.

    Args:
        None
    Return:
        bool: Retorna True se o cadastro válido e False caso contrário

    """

    nome_valido = False
    while not nome_valido:
        nome = input("Nome completo: ")

        if nome == "":
            print("Nome não pode ser vazio.")

        else:
            tem_espaco = False
            for i in nome:
                if i == " ":
                    tem_espaco = True

            if tem_espaco == False:
                print("Informe nome e sobrenome.")

            else:
                letras_validas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áàãâéêíóôõúüçÁÀÃÂÉÊÍÓÔÕÚÜÇ-'"
                nome_invalido = False
                for i in nome:
                    if i not in letras_validas:
                        nome_invalido = True

                if nome_invalido:
                    print("Nome inválido.")
                else:
                    nome_valido = True

    cpf_valido = False
    while not cpf_valido:
        cpf = input("CPF: ")

        cpf_matematicamente_valido = validacao_cpf.validacao_de_cpf(cpf)
        if cpf_matematicamente_valido == False:
            print()

        else:
            cpf_criptografado = cripto.criptografar_cpf(
                cpf)
            cpf_no_banco = verificacao_cpf_banco.verificar_cpf_banco(
                cpf_criptografado)

            if cpf_no_banco[0] == 1:
                print("CPF já cadastrado.")
            else:
                cpf_valido = True

    titulo_valido = False
    while not titulo_valido:
        titulo_eleitor = input("Título de eleitor: ")
        titulo_validado = validacao_titulo.validar_titulo(titulo_eleitor)
        titulo_verificado = verificacao_titulo_banco.verificar_titulo_de_eleitor_banco(
            titulo_validado)

        if titulo_validado == False:
            print()
        elif titulo_verificado[0] == 1:
            print("Título de eleitor já cadastrado")
        else:
            titulo_valido = True

    mesario_valido = False
    while not mesario_valido:
        resposta = input("Será mesário? (S/N): ").upper()

        if resposta not in ("S", "SIM", "N", "NÃO", "NAO"):
            print("Resposta inválida. Digite SIM ou NÃO.")

        else:
            mesario_valido = True

    if resposta in ("S", "SIM"):
        mesario = True
        retorno_mesario = 'Sim'
    else:
        mesario = False
        retorno_mesario = 'Não'

    chave_acesso_original = chave_acesso.geracao_chave_acesso(nome)
    chave_criptografada = cripto.criptografar_chave_acesso(
        chave_acesso_original)

    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO eleitores
        (nome, titulo_eleitor, cpf, mesario, chave_acesso, status_votacao)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, titulo_eleitor, cpf_criptografado, mesario,
                   chave_criptografada, False))
    conexao.commit()

    cursor.close()
    conexao.close()

    print("\n ***** Cadastro realizado com sucesso! *****")
    print("\nNome:", nome)
    print("CPF:", cpf)
    print("Título:", titulo_eleitor)
    print("Mesário:", retorno_mesario)
    print("Chave de acesso:", chave_acesso_original)
    print("\n")

    return True

# Ajustes:
# acertar nome só com espaco


if __name__ == "__main__":
    cadastrar_eleitor()
