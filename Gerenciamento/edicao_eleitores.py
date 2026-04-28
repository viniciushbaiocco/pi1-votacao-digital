def edicao_eleitores():
    from database import conexao_banco as conect
    from Verificadores import gerenciador_de_entrada as ge
    from criptografia import criptografia as crip
    from Verificadores import validacao_cpf as val_cpf
    from Verificadores import validacao_titulo as val_tit

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    #utilizar entre CPF e Título para encontrar o eleitor no BD
    print('Escolha um método para buscar o eleitor: \n 1 - CPF \n 2 - Título de Eleitor')
    opcao = ge.obter_entrada_inteira_valida('Digite uma opção: ', 1, 3)
    match opcao:
        case 1:
            cpf = input('CPF: ')
            while val_cpf.validacao_de_cpf(cpf) == False:
                cpf = input('CPF inválido, digite novamente: ')
            cursor.execute('SELECT id FROM eleitores WHERE cpf = %s', (crip.criptografar_cpf(cpf),))
        case 2:
            tit = input('Título de Eleitor: ')
            while val_tit.validar_titulo(tit) == False:
                tit = input('Título de eleitor inválido, digite novamente: ')
            cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s', (tit,))

    #verificar a existência do eleitor no BD
    eleitor = cursor.fetchone()
    if eleitor is None:
        return 'Eleitor não encontrado.'
    id_eleitor = eleitor['id']

    #edição dos dados do eleitor
    novo_nome = input('Digite o novo nome: ')
    novo_titulo = input('Digite o novo Título de Eleitor: ')
    novo_mesario = ge.obter_entrada_inteira_valida('Mesário: \n 1 - SIM \n 2 - NÃO \n Escolha: ',1, 3)
    novo_cpf = input('Digite o novo CPF: ')
    status_votacao = 0
    
    #validar o novo cpf e novo titulo
    while val_cpf.validacao_de_cpf(novo_cpf) == False:
        novo_cpf = input('Novo CPF inválido, digite novamente: ')
    while val_tit.validar_titulo(novo_titulo) == False:
        novo_titulo = input('Novo Título de Eleitor inválido, digite novamente: ')

    #criptografar o cpf novamente para colocar no banco de dados
    novo_cpf = crip.criptografar_cpf(novo_cpf)

    #listar o eleitor antes da edição
    cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
    eleitor = cursor.fetchone()
    if eleitor['mesario'] == 1: 
        mesario = 'Sim'
    else:
        mesario = 'Não'
    if eleitor['status_votacao'] == 1:
        status_votacao == 'Já Votou'
    else:
        status_votacao == 'Não Votou'

    print('\n === Eleitor Antes da Edição === ')
    print('=' * 50)
    print(f'ID: {eleitor['id']}')
    print(f'Nome: {eleitor['nome']}')
    print(f'CPF: {eleitor['cpf']}')
    print(f'Título de Eleitor: {eleitor['titulo_eleitor']}')
    print(f'Mesário: {mesario}')
    print(f'Status da Votação: {status_votacao}')
    print('=' * 50)


    #atualizar BD
    cursor.execute(''' 
        UPDATE eleitores SET nome = %s,
        cpf = %s, titulo_eleitor = %s, mesario = %s WHERE id = %s
    ''', (novo_nome, novo_cpf, novo_titulo, novo_mesario, id_eleitor))
    conexao.commit()

    #listar o eleitor após edição
    cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
    eleitor = cursor.fetchone()
    if eleitor['mesario'] == 1: 
        mesario = 'Sim'
    else:
        mesario = 'Não'
    if eleitor['status_votacao'] == 1:
        status_votacao == 'Já Votou'
    else:
        status_votacao == 'Não Votou'
    print('\n === Eleitor Depois da Edição === ')
    print('=' * 50)
    print(f'ID: {eleitor['id']}')
    print(f'Nome: {eleitor['nome']}')
    print(f'CPF: {eleitor['cpf']}')
    print(f'Título de Eleitor: {eleitor['titulo_eleitor']}')
    print(f'Mesário: {mesario}')
    print(f'Status de Votação: {status_votacao}')
    print('=' * 50)

    cursor.close()
    conexao.close()
    return '\n=== Eleitor Editado com Sucesso! === ' 

edicao_eleitores()
#NEXT STEPS
#tentar otimizar mais de algum jeito