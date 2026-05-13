from database import conexao_banco as conect
from Validadores import confirmacao
from colorama import Fore, Style

def listagem_eleitores ():

    """
    A função lista todos os eleitores da tabela eleitores.

    Args:
        None

    Returns:
        Os eleitores da tabela eleitores

    """

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        #deve listar tudo da tabela eleitores (nome, cpf, titulo, etc)
        cursor.execute('SELECT * FROM eleitores')
        total_eleitores = cursor.fetchall()

        if len(total_eleitores) == 0:
            print(Fore.YELLOW + Style.BRIGHT + '\n Nenhum eleitor cadastrado no sistema.')
        else:
            print(Fore.WHITE + Style.BRIGHT + '\n --- 5 - Listagem de Eleitores ---')

            for eleitores in (total_eleitores):
                print(Fore.WHITE + Style.BRIGHT + '=' * 50)
                print(Fore.WHITE + Style.BRIGHT + f' ID: {eleitores["id"]}')
                print(Fore.WHITE + Style.BRIGHT + f' Nome: {eleitores["nome"]}')
                print(Fore.WHITE + Style.BRIGHT + f' Título de Eleitor: {eleitores["titulo_eleitor"]}')

                #para ficar melhor pro usuário transformarei 1 em sim 0 em não
                if eleitores['mesario'] == 1:
                    mesario = Fore.WHITE + Style.BRIGHT + 'Sim'
                else:
                    mesario = Fore.WHITE + Style.BRIGHT + 'Não'
                if eleitores['status_votacao'] == 1:
                    status_votacao = Fore.WHITE + Style.BRIGHT + 'Já Votou'
                else:
                    status_votacao = Fore.WHITE + Style.BRIGHT + 'Não Votou'

                print(Fore.WHITE + Style.BRIGHT + f' Mesário: {mesario}')
                print(Fore.WHITE + Style.BRIGHT + f' Status de Votação: {status_votacao}')

            print(Fore.WHITE + Style.BRIGHT + '=' * 50)
            print(Fore.WHITE + Style.BRIGHT + f' Total de Eleitores Cadastrados: {len(total_eleitores)}')

    except Exception as erro:
        print(Fore.RED + Style.BRIGHT + f'\n Erro ao listar eleitores: {erro}')

    confirmacao.confirmacao()

    cursor.close()
    conexao.close()