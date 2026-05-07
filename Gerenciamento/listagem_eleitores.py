from database import conexao_banco as conect
from Verificadores import confirmacao
from colorama import Fore, Style, init

init(autoreset=True)

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

    #deve listar tudo da tabela eleitores (nome, cpf, titulo, etc)
    cursor.execute('SELECT * FROM eleitores')
    total_eleitores = cursor.fetchall()

    print(Fore.WHITE + Style.BRIGHT + '\n --- 5 - Listagem de Eleitores ---')

    for eleitores in (total_eleitores):
        print(Fore.WHITE + Style.BRIGHT + '=' * 50)
        print(Fore.WHITE + Style.BRIGHT + f' ID: {eleitores['id']}')
        print(Fore.WHITE + Style.BRIGHT + f' Nome: {eleitores['nome']}')
        print(Fore.WHITE + Style.BRIGHT + f' Título de Eleitor: {eleitores['titulo_eleitor']}')

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

    print(Fore.WHITE + Style.BRIGHT + '=' *50)
    print(Fore.WHITE + Style.BRIGHT + f' Total de Eleitores Cadastrados: {len(total_eleitores)}')

    confirmacao.confirmacao()

    cursor.close()
    conexao.close()

    #NEXT STEPS 
    #ver se utilizar o try/except para caso não houver eleitores na tabela    
    #tentar otimizar os ifs e else