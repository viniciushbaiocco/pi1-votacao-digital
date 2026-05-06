import database.conexao_banco as conect
import Verificadores. gerenciador_de_entrada as ge
import Verificadores.validacao_cpf as val_cpf
import Verificadores.validacao_titulo as val_titulo
import Verificadores.verificacao_cpf_banco as ver_cpf
import Verificadores.verificacao_titulo_banco as ver_titulo
import criptografia.criptografia as cripto
from Verificadores import confirmacao
from colorama import Fore, Style, init

init(autoreset=True)

def busca_eleitor():

    """
    A função exibe opções para receber valores str de cpf ou titulo de eleitor para consulta do eleitor no banco de dados.
    Utiliza de funções de criptografia, validacao e verificacao de CPF e título de eleitor.

    Args:
        none

    Returns:
        Exibe (print) os dados selecionados do eleitor na tela para o usuário.
        Exibe opções de novas buscas ou troca de Menu.

    """

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    print(Fore.WHITE + Style.BRIGHT + "\n--- 4 - Buscar Eleitores ---")
    print(Fore.WHITE + Style.BRIGHT + "\nOpção 1: Buscar pelo CPF")
    print(Fore.WHITE + Style.BRIGHT + "\nOpção 2: Buscar pelo Título de eleitor")

    # Enquanto a opção estiver fora do intervalo, continua pedindo um valor válido
    opcao = ge.obter_entrada_inteira_valida("\nDigite uma opção: ", 1, 2)

    # Enquanto não for escolhido a opção Voltar (3), a busca continua disponível
    while opcao != 3:

        if opcao == 1:

            # Valida o CPF digitado
            cpf = str(input(Fore.WHITE + Style.BRIGHT + "\nDigite o número do CPF a ser consultado: "))
            validacao_cpf = val_cpf.validacao_de_cpf(cpf)

            if validacao_cpf == True:
                # Criptografa o CPF digitado
                cpf_criptografado = cripto.criptografar_cpf(cpf)

                # Verifica a existência do CPF criptografado no banco
                verificacao_cpf_banco = ver_cpf.verificar_cpf_banco(
                    cpf_criptografado)

                # Se eleitor cadastrado, busca dados no banco e exibe ao usuário
                if verificacao_cpf_banco[0] == 1:
                    comando = (
                        "SELECT nome, mesario, titulo_eleitor, status_votacao FROM eleitores WHERE cpf = %s")
                    valores = (cpf_criptografado, )

                    cursor.execute(comando, valores)
                    dados_eleitor = cursor.fetchone()

                    nome = dados_eleitor[0]
                    mesario = dados_eleitor[1]
                    if mesario == 0:
                        mesario = Fore.WHITE + Style.BRIGHT + "Não"
                    else:
                        mesario = Fore.WHITE + Style.BRIGHT + "Sim"
                    titulo = dados_eleitor[2]
                    status_votacao = dados_eleitor[3]
                    if status_votacao == 0:
                        status_votacao = Fore.WHITE + Style.BRIGHT + "NÃO VOTOU"
                    else:
                        status_votacao = Fore.WHITE + Style.BRIGHT + "VOTOU"

                    print(Fore.WHITE + Style.BRIGHT + f"\n --- Dados do eleitor ---"
                          f"\nNome eleitor: {nome}"
                          f"\nTítulo de eleitor: {titulo}"
                          f"\nMesário: {mesario}"
                          f"\nStatus votação: {status_votacao}"
                          "\n")
                # Se usuário não cadastrado, sugere cadastramento indicando o Menu correto
                else:
                    print(Fore.YELLOW + Style.BRIGHT +
                        "\n*** Eleitor não cadastrado! *** \nRealizar o cadastramento no Menu Gerenciamento de Eleitores.")

            else:
                print(Fore.YELLOW + Style.BRIGHT + "\nPor favor, refaça sua busca!")

        if opcao == 2:
            # Valida o título de eleitor digitado
            titulo_eleitor = str(
                input(Fore.WHITE + Style.BRIGHT + "Digite o número do Título de eleitor a ser consultado: "))

            titulo_validado = val_titulo.validar_titulo(titulo_eleitor)

            if titulo_validado == True:
                # Verifica a existência do título de eleitor no banco de dados
                verificar_titulo = ver_titulo.verificar_titulo_de_eleitor_banco(
                    titulo_eleitor)
                # Se o título de eleitor existir no banco de dados, busca informações e exibe ao usuário
                if verificar_titulo[0] == 1:
                    comando = (
                        "SELECT nome, mesario, titulo_eleitor, status_votacao FROM eleitores WHERE titulo_eleitor = %s")
                    valores = (titulo_eleitor, )

                    cursor.execute(comando, valores)
                    dados_eleitor = cursor.fetchone()

                    nome = dados_eleitor[0]
                    mesario = dados_eleitor[1]
                    if mesario == 0:
                        mesario = Fore.WHITE + Style.BRIGHT + "Não"
                    else:
                        mesario = Fore.WHITE + Style.BRIGHT + "Sim"
                    titulo = dados_eleitor[2]
                    status_votacao = dados_eleitor[3]
                    if status_votacao == 0:
                        status_votacao = Fore.WHITE + Style.BRIGHT + "NÃO VOTOU"
                    else:
                        status_votacao = Fore.WHITE + Style.BRIGHT + "VOTOU"

                    print(Fore.WHITE + Style.BRIGHT + f"\n --- Dados do eleitor ---"
                          f"\nNome eleitor: {nome}"
                          f"\nTítulo de eleitor: {titulo}"
                          f"\nMesário: {mesario}"
                          f"\nStatus votação: {status_votacao}"
                          "\n")

                # Se usuário não cadastrado, sugere cadastramento indicando o Menu correto
                else:
                    print(Fore.YELLOW + Style.BRIGHT +
                        "*** Eleitor não cadastrado! *** \nRealizar o cadastramento no Menu Gerenciamento de Eleitores.\n")

            else:
                print(Fore.YELLOW + Style.BRIGHT + "\nPor favor, refaça sua busca!")
        break

    confirmacao.confirmacao()

    cursor.close()
    conexao.close()

    # Se opção 3 escolhida, exibe o Menu de Gerenciamento
