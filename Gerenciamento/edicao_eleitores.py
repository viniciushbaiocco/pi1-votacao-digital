from database import conexao_banco as conect
from criptografia import criptografia as crip
from Verificadores import verificacao_cpf_banco as ver_cpf
from Verificadores import verificacao_titulo_banco as ver_tit
from Cadastro import chave_acesso as chave
from Validadores import confirmacao, gerenciador_de_entrada as ge, validacao_cpf as val_cpf, validacao_nome as val_nome, \
    validacao_titulo as val_tit
from colorama import Fore, Style

def edicao_eleitores():
    
    """
    A função exibe opções para receber valores str de cpf ou titulo de eleitor para editar um eleitor.

    Args:
        None

    Returns:
        O eleitor editado

    """

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    #utilizar entre CPF e Título para encontrar o eleitor no BD
    print(Fore.WHITE + Style.BRIGHT + '\n--- 2 - Edição de Eleitores --- \n\n Opção 1: Busca pelo CPF \n\n Opção 2: Busca pelo Título de Eleitor')
    opcao = ge.obter_entrada_inteira_valida('\nDigite uma opção: ', 1, 2)
    match opcao:
        case 1:
            cpf = input(Fore.WHITE + Style.BRIGHT + '\nCPF: ')
            while val_cpf.validacao_de_cpf(cpf) == False:
                cpf = input(Fore.WHITE + Style.BRIGHT + '\nCPF inválido, digite novamente: ')
            cursor.execute('SELECT id FROM eleitores WHERE cpf = %s', (crip.criptografar_cpf(cpf),))
            if ver_cpf.verificar_cpf_banco(crip.criptografar_cpf(cpf)) == (0,):
                print(Fore.YELLOW + Style.BRIGHT +
                      "\n*** Eleitor não cadastrado! *** \nRealizar o cadastramento no Menu Gerenciamento de Eleitores.")
        case 2:
            tit = input(Fore.WHITE + Style.BRIGHT + '\nTítulo de Eleitor: ')
            while val_tit.validar_titulo(tit) == False:
                tit = input(Fore.WHITE + Style.BRIGHT + '\nTítulo de Eleitor inválido, digite novamente: ')
            cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s', (tit,))
            if ver_cpf.verificar_cpf_banco(tit) == (0,):
                print(Fore.YELLOW + Style.BRIGHT +
                      "\n*** Eleitor não cadastrado! *** \nRealizar o cadastramento no Menu Gerenciamento de Eleitores.")

    #verificar a existência do eleitor no BD
    eleitor = cursor.fetchone()
    if eleitor is None:
        return confirmacao.confirmacao()
    id_eleitor = eleitor['id']

    # listar o eleitor antes da edição
    cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
    eleitor = cursor.fetchone()
    if eleitor['mesario'] == 1:
        mesario = Fore.WHITE + Style.BRIGHT + 'Sim'
    else:
        mesario = Fore.WHITE + Style.BRIGHT + 'Não'

    print(Fore.WHITE + Style.BRIGHT + '\n === Eleitor a Ser Editado === ')
    print(Fore.WHITE + Style.BRIGHT + '=' * 50)
    print(Fore.WHITE + Style.BRIGHT + f'ID: {eleitor['id']}')
    print(Fore.WHITE + Style.BRIGHT + f'Nome: {eleitor['nome']}')
    cpf = eleitor['cpf']
    cpf_desc_print = crip.descriptografar_cpf(cpf)
    print(Fore.WHITE + Style.BRIGHT + f'CPF: {cpf_desc_print}')
    print(Fore.WHITE + Style.BRIGHT + f'Título de Eleitor: {eleitor['titulo_eleitor']}')
    print(Fore.WHITE + Style.BRIGHT + f'Mesário: {mesario}')
    print(Fore.WHITE + Style.BRIGHT + '=' * 50)

    # confirmar se o usuário quer editar
    print(Fore.WHITE + Style.BRIGHT + '\n Deseja realmente editar esse eleitor? \n1 - Sim \n2 - Não')
    opcao2 = ge.obter_entrada_inteira_valida('\nDigite uma opção: ',1 ,2)

    match opcao2:
        case 1:
            #edição dos dados do eleitor
            novo_nome = val_nome.validar_nome()

            novo_titulo = input(Fore.WHITE + Style.BRIGHT + '\nDigite o novo Título de Eleitor: ')
            while val_tit.validar_titulo(novo_titulo) == False:
                novo_titulo = input(Fore.WHITE + Style.BRIGHT + '\nNovo Título de Eleitor inválido, digite novamente: ')
            while ver_tit.verificar_titulo_de_eleitor_banco(novo_titulo) == (1,):
                novo_titulo = input(Fore.YELLOW + Style.BRIGHT + '\nTítulo de Eleitor já cadastrado, digite novamente: ')
            novo_titulo_verificado = novo_titulo


            novo_cpf = input(Fore.WHITE + Style.BRIGHT + '\nDigite o novo CPF: ')
            novo_cpf_criptografado = crip.criptografar_cpf(novo_cpf)
            while val_cpf.validacao_de_cpf(novo_cpf) == False:
                novo_cpf = input(Fore.WHITE + Style.BRIGHT + '\nNovo CPF inválido, digite novamente: ')
            while ver_cpf.verificar_cpf_banco(novo_cpf_criptografado) == (1,):
                novo_cpf = input(Fore.YELLOW + Style.BRIGHT + '\nCPF já cadastrado, digite novamente: ')
                novo_cpf_criptografado = crip.criptografar_cpf(novo_cpf)

            novo_mesario = ge.obter_entrada_inteira_valida(Fore.WHITE + Style.BRIGHT +
                                                    '\nMesário: \n 1 - SIM \n 2 - NÃO \n Escolha: ',1, 2)

            novo_cpf_descriptografado = crip.descriptografar_cpf(novo_cpf_criptografado)

            #criar nova chave de acesso
            chave_acesso = chave.geracao_chave_acesso(novo_nome)

            #atualizar BD
            cursor.execute('''
                           UPDATE eleitores SET nome = %s,
                                                cpf = %s, titulo_eleitor = %s, mesario = %s, chave_acesso = %s WHERE id = %s
                           ''', (novo_nome, novo_cpf_criptografado, novo_titulo_verificado, novo_mesario, chave_acesso, id_eleitor))
            conexao.commit()

            #listar o eleitor após edição
            cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
            eleitor = cursor.fetchone()
            if eleitor['mesario'] == 1:
                mesario = Fore.WHITE + Style.BRIGHT + 'Sim'
            else:
                mesario = Fore.WHITE + Style.BRIGHT + 'Não'
            print(Fore.WHITE + Style.BRIGHT + '\n === Eleitor Depois da Edição === ')
            print(Fore.WHITE + Style.BRIGHT + '=' * 50)
            print(Fore.WHITE + Style.BRIGHT + f'ID: {eleitor['id']}')
            print(Fore.WHITE + Style.BRIGHT + f'Nome: {eleitor['nome']}')
            print(Fore.WHITE + Style.BRIGHT + f'CPF: {novo_cpf_descriptografado}')
            print(Fore.WHITE + Style.BRIGHT + f'Título de Eleitor: {eleitor['titulo_eleitor']}')
            print(Fore.WHITE + Style.BRIGHT + f'Mesário: {mesario}')
            print(Fore.WHITE + Style.BRIGHT + f'Chave de Acesso: {chave_acesso}')
            print(Fore.WHITE + Style.BRIGHT + '=' * 50)

            cursor.close()
            conexao.close()
            return confirmacao.confirmacao()
        case 2:
            return confirmacao.confirmacao()
        

#NEXT STEPS
#tentar otimizar mais de algum jeito
#gerar nova chave de acesso (validacao_nome)

