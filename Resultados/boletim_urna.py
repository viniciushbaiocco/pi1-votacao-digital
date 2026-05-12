from database import conexao_banco
from colorama import Fore, Style

def exibir_boletim_urna():
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    query_listagem_candidatos = ('SELECT c.nome, c.partido, '
                                         'COUNT(v.id) AS total_votos '
                                         'FROM candidatos c '
                                         'LEFT JOIN votos v '
                                         'ON c.id = v.id_candidato '
                                         'GROUP BY c.id, c.nome, c.partido '
                                         'ORDER BY nome ASC')

    cursor.execute(query_listagem_candidatos)
    total_candidatos = cursor.fetchall()

    print(Fore.WHITE + Style.BRIGHT + '\n --- Listagem de Candidatos ---')
    for candidatos in (total_candidatos):
            print(Fore.WHITE + Style.BRIGHT + '=' * 50)
            print(Fore.WHITE + Style.BRIGHT + f' Nome: {candidatos['nome']}')
            print(Fore.WHITE + Style.BRIGHT + f' Partido: {candidatos['partido']}')
            print(Fore.WHITE + Style.BRIGHT + f' Total de Votos: {candidatos['total_votos']}')
    print(Fore.WHITE + Style.BRIGHT + '=' * 50)
    print(Fore.WHITE + Style.BRIGHT + f' Total de Candidatos Cadastrados: {len(total_candidatos)}')

exibir_boletim_urna()