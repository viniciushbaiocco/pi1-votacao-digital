def listagem_eleitores ():
    from database import conexao_banco as conect
    from Verificadores import confirmacao

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    #deve listar tudo da tabela eleitores (nome, cpf, titulo, etc)
    cursor.execute('SELECT * FROM eleitores')
    total_eleitores = cursor.fetchall()

    print('\n --- 5 - Listagem de Eleitores ---')

    for eleitores in (total_eleitores):
        print('=' * 50)
        print(f' ID: {eleitores['id']}')
        print(f' Nome: {eleitores['nome']}')
        print(f' Título de Eleitor: {eleitores['titulo_eleitor']}')

        #para ficar melhor pro usuário transformarei 1 em sim 0 em não 
        if eleitores['mesario'] == 1: 
            mesario = 'Sim'
        else:
            mesario = 'Não' 
        if eleitores['status_votacao'] == 1:
            status_votacao = 'Já Votou'
        else:
            status_votacao = 'Não Votou'

        print(f' Mesário: {mesario}')
        print(f' Status de Votação: {status_votacao}')

    print('=' *50)
    print(f' Total de Eleitores Cadastrados: {len(total_eleitores)}')

    confirmacao.confirmacao()

    cursor.close()
    conexao.close()

    #NEXT STEPS 
    #ver se utilizar o try/except para caso não houver eleitores na tabela    
    #tentar otimizar os ifs e else