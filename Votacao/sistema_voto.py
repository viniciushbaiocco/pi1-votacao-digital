import os
from database import conexao_banco as conect
from Ocorrencias import voto_computado
from Ocorrencias import voto_duplo
from Validadores import gerenciador_de_entrada as ge, validacao_voto as val_voto
from criptografia import criptografia as crip
from Verificadores import verificacao_cpf_votacao as ver_cpf_vot
from Verificadores import verificacao_eleitor_voto as ver_eleit_vot
from Verificadores import verificacao_chave_acesso_banco as ver_chave
from Validadores import validacao_cpf_votacao as val_cpf_vot, validacao_chave_acesso as val_chave
#futuros imports pras outras ocorrências

def sistema_voto ():
    print('--- Eleição 2026 ---')

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute('SELECT * FROM candidatos')
    total_candidatos = cursor.fetchall()

    #recolher os dados do eleitor e validar
    cpf_4 = input('\n''Digite os 4 primeiros digitos de seu CPF: ')
    while val_cpf_vot.validar_cpf_voto(cpf_4) == False:
        cpf_4 = input('\n''Digite os 4 primeiros digitos de seu CPF novamente: ')

    chave_acesso = input('\nDigite sua chave de acesso: ').upper()
    while val_chave.validar_chave_acesso(chave_acesso) == False:
        chave_acesso = input('\nDigite sua chave de acesso novamente: ').upper()

    #criptografar, encontrar no BD e verificar se ja votou 
    cpf_4 = crip.criptografar_cpf(cpf_4)
    chave_acesso = crip.criptografar_chave_acesso(chave_acesso)
    ver_votou = ver_eleit_vot.verificacao_eleitor_voto(chave_acesso)
        
    if ver_cpf_vot.verificar_cpf_voto(cpf_4) == (1,) and ver_chave.verificar_chave_acesso_banco(chave_acesso) == (1,):
        #iniciar processo de votação apenas se o eleitor não votou
        if ver_votou == (0,):
            #listagem de todos os candidatos do banco de dados para o usuário escolher entre eles
            print('\n --- Listagem de Candidatos ---')
            for candidatos in (total_candidatos):
                print('=' * 50)
                print(f' Nome: {candidatos['nome']}')
                print(f' Partido: {candidatos['partido']}')
                print(f' Número Eleitoral: {candidatos['numero_votacao']}')
            print('=' *50)
            print(f' Total de Candidatos Cadastrados: {len(total_candidatos)}')

            #verificação pro voto e variavel para atualizar o eleitor depois de votar
            voto = val_voto.validacao_voto()
            votou = 0

            #verificação do número eleitoral no banco de dados
            query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
            cursor.execute(query, (voto, ))
            resultado = cursor.fetchone()
            if resultado == (0,):
                print('Você digitou um candidato inexistente, caso erre novamente o voto será considerado nulo.')
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
                        votou = 1
                        voto_computado.voto_computado()
                    case 2:
                        print('Encerrando operação...')
            #segunda tentativa de votação
            if resultado == (0,):
                voto = val_voto.validacao_voto()
                query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
                cursor.execute(query, (voto, ))
                resultado = cursor.fetchone()

                #se a segunda tentativa foi falha, voto será nulo
                if resultado == (0,):
                    print('Você digitou um candidato inexistente novamente, o voto será considerado nulo.')
                    votou = 1
                    voto = 0
                    voto_computado.voto_computado()

                #se a segunda tentativa for sucesso
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
                            votou = 1
                            voto_computado.voto_computado()
                        case 2:
                            print('Encerrando operação...')
        #encerrar processo caso eleitor ja tenha votado    
        else:
            print('\nErro, tentativa de voto duplo.')
            voto_duplo.ocorrencia_voto_duplo()
        
        #atualizar no BD o eleitor para já votou
        if votou == 1:
            query = 'UPDATE eleitores SET status_votacao = %s WHERE chave_acesso = %s'
            cursor.execute(query, (votou), (chave_acesso, ))
    else: 
        print('Erro ao verificar CPF ou chave de acesso do eleitor.')


    cursor.close()
    conexao.close()

#NEXT STEPS
#otimizar essa logica de programação lixosa q eu tive