def listagem_eleitores ():
    import mysql.connector
    import conexao_banco as conect
    
    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    #deve listar tudo da tabela eleitores (nome, cpf, titulo, etc)
    cursor.execute('SELECT * FROM eleitores')
    eleitores = cursor.fetchall()
    return eleitores

    cursor.close()
    conexao.close()

    #NEXT STEPS 
    #Ver se utilizar o try/except para caso não houver eleitores na tabela
    #Testar no MYSQL no pc da PUC 
    #Ao exibir resultado voltar para o menu de buscas ou menu eleitores
    
