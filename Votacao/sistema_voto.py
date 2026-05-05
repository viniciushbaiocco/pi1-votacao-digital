from database import conexao_banco as conect
from Ocorrencias import voto_computado, voto_duplo
from colorama import Fore,Style
from Verificadores import validacao_voto as val_voto, gerenciador_de_entrada as ge

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
    voto = val_voto()

    #verificação do número eleitoral no banco de dados
    query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
    cursor.execute(query, (voto, ))
    resultado = cursor.fetchone()
    if resultado == (0,):
        print('Você digitou um candidato inexistente, caso erre novamente o voto será considerado nulo.')
        voto = val_voto()
    else:
        #listar o candidato para confirmação do voto
        cursor.execute('SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
        candidato = cursor.fetchone()
        print('=' * 50)
        print(f' Nome: {candidato['nome']}')
        print(f' Partido: {candidato['partido']}')
        print(f' Número Eleitoral: {candidato['numero_votacao']}')
        print('=' *50)
        opcao = ge.obter_entrada_inteira_valida('\nCerteza que deseja votar nesse candidato? \n 1 - Sim \n 2 - Não ', 1, 2)
        match opcao:
            case 1:
                print('Voto Computado!')
                voto_computado()

    cursor.close()
    conexao.close()