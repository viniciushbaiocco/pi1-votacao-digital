def listagem_eleitores ():
    from database import conexao_banco as conect

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    #deve listar tudo da tabela eleitores (nome, cpf, titulo, etc)
    cursor.execute('SELECT * FROM eleitores')
    total_eleitores = cursor.fetchall()
    
    for eleitores in (total_eleitores):
        print('=' * 50)
        print(f' ID: {eleitores['id']}')
        print(f' Nome: {eleitores['nome']}')
        print(f' CPF: {eleitores['cpf']}')
        print(f' Título de Eleitor: {eleitores['titulo_eleitor']}')
        print(f' Mesário: {eleitores['mesario']}')
        print(f' Status de Votação: {eleitores['status_votacao']}')
    print('=' *50)
    print(f' Total de Eleitores Cadastrados: {len(total_eleitores)}')

    cursor.close()
    conexao.close()

    #NEXT STEPS 
    #ver se utilizar o try/except para caso não houver eleitores na tabela
    #ao exibir resultado voltar para o menu de buscas ou menu eleitores
    