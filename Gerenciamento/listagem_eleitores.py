def listagem_eleitores ():
    import mysql.connector
    import conexao_banco as conect
    
    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    #deve listar tudo da tabela eleitores (nome, cpf, titulo, etc)
    
    cursor.execute('SELECT * FROM eleitores')
    total_eleitores = cursor.fetchall()
    
    for eleitores in range (total_eleitores):
        print(eleitores)

    cursor.close()
    conexao.close()

    return eleitores

    #NEXT STEPS 
    #Ver se utilizar o try/except para caso não houver eleitores na tabela
    #Testar no MYSQL no pc da PUC 
    #Ao exibir resultado voltar para o menu de buscas ou menu eleitores
    #erro no codigo, tentar usar o for
