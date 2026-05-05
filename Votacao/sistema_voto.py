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

    #verificação do número eleitoral no banco de dados
    query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
    cursor.execute(query, (voto, ))
    resultado = cursor.fetchone()
    if resultado == (0,):
        print('Você digitou um candidato inexistente, caso erre novamente o voto será considerado nulo.')
        voto
    cursor.close()
    conexao.close()