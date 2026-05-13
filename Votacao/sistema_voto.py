from database import conexao_banco as conect
from Ocorrencias import voto_computado
from Ocorrencias import voto_duplo
from Validadores import gerenciador_de_entrada as ge, validacao_voto as val_voto
from criptografia import criptografia as crip
from Verificadores import verificacao_cpf_votacao as ver_cpf_vot
from Verificadores import verificacao_eleitor_voto as ver_eleit_vot
from Verificadores import verificacao_chave_acesso_banco as ver_chave
from Validadores import validacao_cpf_votacao as val_cpf_vot, validacao_chave_acesso as val_chave, confirmacao
from Validadores import validacao_titulo as val_tit
from Verificadores import verificacao_titulo_banco as ver_tit
from Votacao import protoco_votacao as prot_vot
from datetime import datetime
from colorama import Fore, Style


def sistema_voto():
    print(Fore.CYAN + Style.BRIGHT + '\n--- Eleição 2026 ---')

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    # recolher os dados do eleitor e validar
    cpf_4 = input(Fore.WHITE + Style.BRIGHT +
                  '\n''Digite os 4 primeiros digitos de seu CPF: ')
    while val_cpf_vot.validar_cpf_voto(cpf_4) == False:
        cpf_4 = input(Fore.WHITE + Style.BRIGHT +
                      '\n''Digite os 4 primeiros digitos de seu CPF novamente: ')
        
    titulo = input(Fore.WHITE + Style.BRIGHT +
                   '\n''Digite seu título de eleitor: ')
    while val_tit.validar_titulo(titulo) == False:
        titulo = input(Fore.WHITE + Style.BRIGHT +
                       '\n''Digite seu título de eleitor novamente: ')

    chave_acesso = input(Fore.WHITE + Style.BRIGHT +
                         '\nDigite sua chave de acesso: ').upper()
    while val_chave.validar_chave_acesso(chave_acesso) == False:
        chave_acesso = input(Fore.WHITE + Style.BRIGHT +
                             '\nDigite sua chave de acesso novamente: ').upper()

    # criptografar, encontrar no BD e verificar se ja votou
    cpf_4 = crip.criptografar_cpf(cpf_4)
    chave_acesso = crip.criptografar_chave_acesso(chave_acesso)
    ver_votou = ver_eleit_vot.verificacao_eleitor_voto(chave_acesso)
    votou = 0
    opcao = 2

    while opcao == 2:
        if ver_cpf_vot.verificar_cpf_voto(cpf_4) == (1,) and ver_chave.verificar_chave_acesso_banco(chave_acesso) == (1,) and ver_tit.verificar_titulo_de_eleitor_banco(titulo) == (1,):
            # iniciar processo de votação apenas se o eleitor não votou
            if ver_votou == (0,):
                
                # verificação pro voto e variavel para atualizar o eleitor depois de votar
                voto = val_voto.validacao_voto()

                # verificação do número eleitoral no banco de dados e pegar o id
                query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
                cursor.execute(query, (voto,))
                resultado = cursor.fetchone()

                if resultado == {'COUNT(*)': 0}:
                    print(Fore.YELLOW + Style.BRIGHT +
                        'Atenção: Número não cadastrado. Se confirmar, o voto será considerado nulo. Deseja prosseguir?'
                        '\n[1] Sim \n[2] Não \nDigite uma opção: ')
                    voto_nulo_opcao = ge.obter_entrada_inteira_valida('\n1 - Sim \n2 - Não \nDigite uma opção: ', 1, 2)
                    match voto_nulo_opcao:
                        case 1:
                            voto = 0
                            votou = 1
                            print(Fore.GREEN + Style.BRIGHT +
                                    '\nVoto Computado!')
                            query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
                            cursor.execute(query, (voto,))
                            resultado = cursor.fetchone()
                            cursor.execute(
                            
                            'SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
                            candidato = cursor.fetchone()
                            id_candidato = candidato['id']
                        case 2:
                            print('')

                else:
                    # listar o candidato para confirmação do voto
                    cursor.execute(
                        'SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
                    candidato = cursor.fetchone()
                    id_candidato = candidato['id']
                    print(Fore.WHITE + Style.BRIGHT + '=' * 50)
                    print(Fore.WHITE + Style.BRIGHT +
                        f' Nome: {candidato['nome']}')
                    print(Fore.WHITE + Style.BRIGHT +
                        f' Partido: {candidato['partido']}')
                    print(Fore.WHITE + Style.BRIGHT +
                        f' Número Eleitoral: {candidato['numero_votacao']}')
                    print(Fore.WHITE + Style.BRIGHT + '=' * 50)
                    opcao = ge.obter_entrada_inteira_valida(
                        '\nCerteza que deseja votar nesse candidato? \n1 - Sim \n2 - Não \nDigite uma opção: ', 1, 2)
                    match opcao:
                        case 1:
                            print(Fore.GREEN + Style.BRIGHT + '\nVoto Computado!')
                            votou = 1
                            opcao = 1
                        case 2:
                            print('')

                # segunda tentativa de votação
                if resultado == {'COUNT(*)': 0}:
                    voto = val_voto.validacao_voto()
                    query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
                    cursor.execute(query, (voto,))
                    resultado = cursor.fetchone()

                    # se a segunda tentativa foi falha, voto será nulo
                    if resultado == {'COUNT(*)': 0}:
                        print(Fore.YELLOW + Style.BRIGHT +
                            'Você digitou um candidato inexistente novamente, o voto será considerado nulo.')
                        votou = 1
                        voto = 0

                        #pegar o id do candidato
                        cursor.execute(
                            'SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
                        candidato = cursor.fetchone()
                        id_candidato = candidato['id']

                        print(Fore.GREEN + Style.BRIGHT +
                                    '\nVoto Computado!')
                        
                    # se a segunda tentativa for sucesso
                    else:
                        # listar o candidato para confirmação do voto
                        cursor.execute(
                            'SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
                        candidato = cursor.fetchone()
                        id_candidato = candidato['id']
                        print(Fore.WHITE + Style.BRIGHT + '=' * 50)
                        print(Fore.WHITE + Style.BRIGHT +
                            f' Nome: {candidato['nome']}')
                        print(Fore.WHITE + Style.BRIGHT +
                            f' Partido: {candidato['partido']}')
                        print(Fore.WHITE + Style.BRIGHT +
                            f' Número Eleitoral: {candidato['numero_votacao']}')
                        print(Fore.WHITE + Style.BRIGHT + '=' * 50)
                        opcao = ge.obter_entrada_inteira_valida(
                            '\nCerteza que deseja votar nesse candidato? \n 1 - Sim \n 2 - Não \nDigite uma opção: ', 1, 2)
                        match opcao:
                            case 1:
                                print(Fore.GREEN + Style.BRIGHT +
                                    '\nVoto Computado!')
                                votou = 1
                                opcao = 1
                            case 2:
                                print('')
            # encerrar processo caso eleitor ja tenha votado
            else:
                print(Fore.RED + Style.BRIGHT + '\nErro, tentativa de voto duplo.')
                voto_duplo.ocorrencia_voto_duplo()
                confirmacao.confirmacao()

            # atualizar no BD o eleitor para já votou
            if votou == 1:
                # gerar protocolo e computar voto
                protocolo = prot_vot.gerar_protocolo_votacao(voto)
                print(Fore.WHITE + Style.BRIGHT +
                    f"Seu protocolo de votação é: {protocolo}")
                confirmacao.confirmacao()
                protocolo = crip.criptografar_protocolo(protocolo)
                voto_computado.voto_computado()
                data_hora = datetime.now()
                sem_milissegundos = data_hora.replace(microsecond=0)

                # inserir o voto no BD
                query_voto = 'INSERT INTO votos (id_candidato, data_hora, protocolo_votacao) VALUES (%s, %s, %s)'
                cursor.execute(query_voto, (id_candidato,
                            sem_milissegundos, protocolo))

                # atualizar o BD
                query = 'UPDATE eleitores SET status_votacao = %s WHERE chave_acesso = %s'
                cursor.execute(query, (votou, chave_acesso))

                conexao.commit()
        else:
            print(Fore.RED + Style.BRIGHT +
                'Erro ao verificar CPF ou chave de acesso do eleitor.')
            confirmacao.confirmacao()

    cursor.close()
    conexao.close()

# NEXT STEPS
# otimizar o codigo

sistema_voto()