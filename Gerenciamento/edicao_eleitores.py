def edicao_eleitores(id_eleitor, novo_nome, novo_cpf, novo_titulo):
    import mysql.connector
    import conexao_banco as conect

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT id FROM eleitores WHERE cpf = %s AND id != %s', (novo_cpf, id_eleitor))
    #verificação unicidade CPF
    if cursor.fetchone():
        return 'CPF já cadastrado.'
    
    cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s AND id != %s ', (novo_titulo, id_eleitor))
    #verificação unicidade TITULO
    if cursor.fetchone():
        return 'Título já cadastrado.'

    #atualização banco de dados
    cursor.execute('''
        UPDATE eleitores SET nome = %s,
        cpf = %s, titulo_eleitor = %s WHERE id = %s
        ''', (novo_nome, novo_cpf, novo_titulo, id_eleitor))
    
    conexao.commit()
    cursor.close()
    conexao.close()
    return 'Eleitor editado com sucesso.'


#NEXT STEPS
#tentar otimizar mais de algum jeito
#perguntar se pode usar o %s
#adicionar uma listagem do eleitor ja editado
#testar no pc da puc
