def remocao_eleitores():
    import mysql.connector
    import conexao_banco as conect

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    print('Qual método quer usar para encontrar o eleitor: \n 1 - CPF \n 2 - Título de Eleitor')
    opcao = int(input('Opção escolhida: '))

    match opcao:
        case 1:
            # from Verificadores.validacao_cpf import validacao_de_cpf
            busca = input('CPF: ')
            # check = validacao_de_cpf(busca):
            # while check != True:
            #     busca = input('CPF inválido, tente novamente: ')
            cursor.execute('SELECT id FROM eleitores WHERE cpf = %s', (busca,))
        case 2:
            # from Verificadores.validacao_cpf import validacao_titulo
            busca = input('Título de Eleitor: ')
            # check = validacao_titulo()
            # while check != true:
            #     busca = input('Título de eleitor invalido, digite novamente: ')
            cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s', (busca,))
        case _:
            return 'Opção Inválida, escolha entre 1 e 2.'

    eleitor = cursor.fetchone()
    if eleitor is None:
        return 'Eleitor não encontrado.'
    id_eleitor = eleitor[0]

    cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
    print('\n - Eleitor a ser removido - ')
    print(cursor.fetchone())

    cursor.execute('DELETE FROM eleitores WHERE id = %s', (id_eleitor,))
    conexao.commit()

    cursor.close()
    conexao.close()
    return 'Eleitor removido com sucesso.'

remocao_eleitores()