from Verificadores import verificacao_cpf_banco
from Verificadores import verificacao_titulo_banco
from Validadores import confirmacao, validacao_cpf, validacao_nome, validacao_titulo
from database import conexao_banco
from criptografia import criptografia as cripto
from Cadastro import chave_acesso
from colorama import Fore, Style, init

init(autoreset=True)

def cadastrar_eleitor():
    """
    Realiza o cadastro completo de um eleitor no sistema, validando nome,
    CPF e título de eleitor antes de inserir os dados no banco.

    Args:
        None
    Return:
        bool: Retorna True se o cadastro válido e False caso contrário

    """
    cpf_valido = False
    while not cpf_valido:
        cpf = input(Fore.WHITE + Style.BRIGHT + "Digite o CPF do eleitor: ")

        cpf_matematicamente_valido = validacao_cpf.validacao_de_cpf(cpf)
        if cpf_matematicamente_valido == False:
            print()
        else:
            cpf_valido = True

    cpf_criptografado = cripto.criptografar_cpf(
        cpf)
    cpf_no_banco = verificacao_cpf_banco.verificar_cpf_banco(
        cpf_criptografado)

    if cpf_no_banco[0] == 0:
        nome_valido = validacao_nome.validar_nome()

        titulo_valido = False
        while not titulo_valido:
            titulo_eleitor = input(Fore.WHITE + Style.BRIGHT + "Digite o Título de eleitor: ")
            titulo_eleitor = ''.join(filter(str.isdigit, titulo_eleitor))
            titulo_validado = validacao_titulo.validar_titulo(titulo_eleitor)
            titulo_verificado = verificacao_titulo_banco.verificar_titulo_de_eleitor_banco(
                titulo_eleitor)

            if titulo_validado == False:
                print()
            elif titulo_verificado == (1,):
                print( Fore.YELLOW + Style.BRIGHT + "*** Eleitor já cadastrado! *** \n"
                       "Você pode consultar os dados deste eleitor pelo Menu Gerenciamento de Eleitores.")
                confirmacao.confirmacao()
                return True

            else:
                titulo_valido = True


        mesario_valido = False
        while not mesario_valido:
            resposta = input(Fore.WHITE + Style.BRIGHT + "Eleitor será mesário? (S/N): ").upper()

            if resposta not in ("S", "SIM", "N", "NÃO", "NAO"):
                print(Fore.RED + Style.BRIGHT + "Resposta inválida. Digite SIM ou NÃO.")

            else:
                mesario_valido = True

        if resposta in ("S", "SIM"):
            mesario = True
            retorno_mesario = Fore.WHITE + Style.BRIGHT + 'Sim'
        else:
            mesario = False
            retorno_mesario = Fore.WHITE + Style.BRIGHT + 'Não'

        chave_acesso_original = chave_acesso.geracao_chave_acesso(nome_valido)
        chave_criptografada = cripto.criptografar_chave_acesso(
            chave_acesso_original)

        conexao = conexao_banco.conexao_banco()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO eleitores
            (nome, titulo_eleitor, cpf, mesario, chave_acesso, status_votacao)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (nome_valido, titulo_eleitor, cpf_criptografado, mesario,
                             chave_criptografada, False))
        conexao.commit()

        cursor.close()
        conexao.close()

        print(Fore.WHITE + Style.BRIGHT + "\n ***** Cadastro realizado com sucesso! *****")
        print(Fore.WHITE + Style.BRIGHT + "\nNome:", nome_valido)
        print(Fore.WHITE + Style.BRIGHT + "CPF:", cpf)
        print(Fore.WHITE + Style.BRIGHT + "Título:", titulo_eleitor)
        print(Fore.WHITE + Style.BRIGHT + "Mesário:", retorno_mesario)
        print(Fore.WHITE + Style.BRIGHT + "Chave de acesso:", chave_acesso_original)
        print("\n")
        confirmacao.confirmacao()

    else:
        print(Fore.YELLOW + Style.BRIGHT + "*** Eleitor já cadastrado! *** \nVocê pode consultar os dados deste eleitor pelo Menu Gerenciamento de Eleitores.")
        confirmacao.confirmacao()
    return True
