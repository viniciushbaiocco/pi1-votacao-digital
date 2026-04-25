def edicao_eleitores():
    from database import conexao_banco as conect
    from Verificadores import gerenciador_de_entrada as ge
    from criptografia import criptografia as crip

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    #utilizar entre CPF e Título para encontrar o eleitor no BD
    print('Escolha um método para buscar o eleitor: \n 1 - CPF \n 2 - Título de Eleitor')
    opcao = ge.obter_entrada_inteira_valida('Digite uma opção: ', 1, 3)

    match opcao:
        case 1:
            busca = input('CPF: ')
            cursor.execute('SELECT id FROM eleitores WHERE cpf = %s', (crip.criptografar_cpf(busca),))
        case 2:
            busca = input('Título de Eleitor: ')
            cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s', (busca,))

    #verificar a existência do eleitor no BD
    eleitor = cursor.fetchone()
    if eleitor is None:
        return 'Eleitor não encontrado.'
    id_eleitor = eleitor[0]

    #edição dos dados do eleitor
    novo_nome = input('Digite o novo nome: ')
    novo_cpf = input('Digite o novo CPF: ')
    novo_titulo = input('Digite o novo Título de Eleitor: ')
    novo_mesario = ge.obter_entrada_inteira_valida('Digite o novo mesário: \n 1 - SIM \n 2 - NÃO \n Escolha: ',1, 3)
    
    #criptografar o cpf novamente para colocar no banco de dados
    novo_cpf = crip.criptografar_cpf(novo_cpf)

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
        cpf = %s, titulo_eleitor = %s, mesario = %s WHERE id = %s
    ''', (novo_nome, novo_cpf, novo_titulo, novo_mesario, id_eleitor))
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
#mudar a listagem do antes e depois para o mesmo tipo de listagem que usei no listagem_eleitores para ficar melhor visualmente pro usuario
#após a função de verificação ficar pronta, tentar substituir no código 

