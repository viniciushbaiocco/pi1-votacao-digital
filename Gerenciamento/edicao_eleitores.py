def edicao_eleitores():
    import mysql.connector
    import conexao_banco as conect

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    #utilizar entre CPF e Título para encontrar o eleitor no BD
    print('Qual método quer usar para fazer a edição: \n 1 - CPF \n 2 - Título de Eleitor')
    opcao=int(input('Opção escolhida: '))

    match opcao:
        case 1:
            busca = input('CPF: ')
            cursor.execute('SELECT id FROM eleitores WHERE cpf = %s', (busca,))
        case 2:
            busca = input('Título de Eleitor: ')
            cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s', (busca,))
        case _:
            return 'Opção Inválida, escolha entre 1 e 2.'

    #verificar a existência do eleitor no BD
    eleitor = cursor.fetchone()
    if eleitor is None:
        return 'Eleitor não encontrado.'
    id_eleitor = eleitor[0]

    #edição dos dados do eleitor
    novo_nome = input('Digite o novo nome: ')
    novo_cpf = input('Digite o novo CPF: ')
    novo_titulo = input('Digite o novo Título de Eleitor: ')

    #verificar se o CPF ou Título é valido 
    if len(novo_cpf) != 11:
        return 'CPF Inválido'
    if len(novo_titulo) != 12:
        return 'Título de Eleitor Inválido'

    #verificar unicidade do CPF
    cursor.execute('SELECT id FROM eleitores WHERE cpf = %s AND id != %s', (novo_cpf, id_eleitor))
    if cursor.fetchone():
        return 'CPF já cadastrado.'

    #verificar unicidade do Título de Eleitor
    cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s AND id != %s', (novo_titulo, id_eleitor))
    if cursor.fetchone():
        return 'Título de Eleitor já cadastrado.'
    
    #listar o eleitor antes da edição
    cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
    print('\n - Eleitor antes da edição - ')
    print(cursor.fetchone())

    #atualizar BD
    cursor.execute(''' 
        UPDATE eleitores SET nome = %s,
        cpf = %s, titulo_eleitor = %s WHERE id = %s
    ''', (novo_nome, novo_cpf, novo_titulo, id_eleitor))
    conexao.commit()

    #listar o eleitor após edição
    cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
    print('\n - Eleitor depois da edição - ')
    print(cursor.fetchone())

    cursor.close()
    conexao.close()
    return 'Eleitor editado com sucesso.'

#NEXT STEPS
#tentar otimizar mais de algum jeito
#perguntar se precisar editar algo a mais alem do nome cpf e titulo
#após a função de verificação ficar pronta, tentar substituir no código 
#tentar usar a função de obter entrada no match case 
