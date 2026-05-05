from database import conexao_banco as conect
from Ocorrencias import voto_computado, voto_duplo
from colorama import Fore,Style
#futuros imports pras outras ocorrências

def sistema_voto ():
    print('--- Eleição 2026 ---')
    print('--- Candidatos ---')

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute('SELECT * FROM candidatos')
    total_candidatos = cursor.fetchall()

    #listagem de todos os candidatos do banco de dados para o usuário escolher entre eles
    print('\n --- Listagem de Candidatos ---')
    for candidatos in (total_candidatos):
        print('=' * 50)
        print(f' Nome: {candidatos['nome']}')
        print(f' Partido: {candidatos['partido']}')
        print(f' Número Eleitoral: {candidatos['numero_votacao']}')
    print('=' *50)
    print(f' Total de Candidatos Cadastrados: {len(total_candidatos)}')

    #verificação pro voto 
    executando_entrada = 0
    while (executando_entrada == 0):
        try:
            voto = int(input('\n Digite o número eleitoral do candidato que deseja votar: '))
            if voto <0:
                print(f'{Fore.RED}{Style.BRIGHT}Erro: Opção inválida. Por favor, escolha uma opção positiva. {Style.RESET_ALL}')
            else:
                executando_entrada = 1
        except ValueError:
            print(f'{Fore.RED}{Style.BRIGHT}Erro: Entrada inválida. Por favor, digite um número inteiro.{Style.RESET_ALL}')

    #verificação do número eleitoral no banco de dados
    query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
    cursor.execute(query, (voto, ))
    resultado = cursor.fetchone()
    
    cursor.close()
    conexao.close()