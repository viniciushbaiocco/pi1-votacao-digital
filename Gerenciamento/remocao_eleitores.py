def remocao_eleitores():
    """
    A função exibe opções para receber valores str de cpf ou titulo de eleitor para remoção do eleitor no banco de dados.
    Utiliza de funções de criptografia, validação e gerenciamento de entrada.

    Args:
        none

    Returns:
        Exibe (print) os dados do eleitor a ser removido na tela para o usuário.
        Realiza a exclusão do eleitor no banco de dados após confirmação.
        Exibe opções de novas remoções ou troca de Menu.

    """

    import Menu.sub_menus as sb
    from database import conexao_banco as conect
    from Verificadores import gerenciador_de_entrada as ge
    from Verificadores import validacao_cpf as val_cpf
    from criptografia import criptografia as crip

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    print("\n--- 3 - Excluir Eleitores ---")
    print("\nOpção 1: Remover pelo CPF")
    print("\nOpção 2: Remover pelo Título de eleitor")
    print("\nOpção 3: Voltar ao Menu de Gerenciamento de Eleitores")

    #enquanto a opção estiver fora do intervalo, continua pedindo um valor válido (min,max)
    opcao = ge.obter_entrada_inteira_valida("\nDigite uma opção: ", 1, 3)

    #enquanto não for escolhido a opção voltar (3), a remoção continua disponível
    while opcao != 3:

        #MUDANÇA: inicializo eleitor=none no começo do loop para reaproveitar o mesmo bloco de exibição/confirmação fora do match (evita duplicar código nos dois cases)
        eleitor = None

        match opcao:
            case 1:
                #valida o CPF digitado
                cpf = str(input("\nDigite o número do CPF a ser removido: "))
                validacao_cpf = val_cpf.validacao_de_cpf(cpf)

                if validacao_cpf == True:
                    #criptografa o CPF digitado para comparar com o cifrado no banco
                    cpf_criptografado = crip.criptografar_cpf(cpf)
                    cursor.execute('SELECT * FROM eleitores WHERE cpf = %s', (cpf_criptografado,))
                    eleitor = cursor.fetchone()

                    #se eleitor não cadastrado, avisa o usuário
                    if eleitor is None:
                        print("\nEleitor não cadastrado.")
                else:
                    print("\nPor favor, refaça sua busca!")

            case 2:
                #valida o tamanho do título de eleitor digitado
                titulo_eleitor = str(input("\nDigite o número do Título de Eleitor a ser removido: "))

                if len(titulo_eleitor) == 12:
                    cursor.execute('SELECT * FROM eleitores WHERE titulo_eleitor = %s', (titulo_eleitor,))
                    eleitor = cursor.fetchone()

                    #se eleitor não cadastrado, avisa o usuário
                    if eleitor is None:
                        print("\nEleitor não cadastrado.")
                else:
                    print("\nTítulo de Eleitor inválido. Por favor, refaça sua busca!")

        #se eleitor encontrado, exibe os dados e confirma a remoção
        if eleitor is not None:

            #exibe os dados do eleitor
            print('=' * 50)
            print(' - Eleitor a ser removido - ')
            print('=' * 50)
            print(f' ID: {eleitor['id']}')
            print(f' Nome: {eleitor['nome']}')
            #MUDANÇA: o CPF está cifrado no banco; descriptografo antes de exibir para o usuário ver o CPF real (a listagem_eleitores ainda mostra o cifrado)
            print(f' CPF: {crip.descriptografar_cpf(eleitor['cpf'])}')
            print(f' Título de Eleitor: {eleitor['titulo_eleitor']}')
            print(f' Mesário: {eleitor['mesario']}')
            print(f' Status de Votação: {eleitor['status_votacao']}')
            print('=' * 50)

            #MUDANÇA: passo extra de confirmação antes do DELETE para evitar exclusão acidental (não existe no busca_eleitores pq lá não tem operação destrutiva)
            print("\nDeseja realmente remover este eleitor? \n 1 - Sim \n 2 - Não")
            confirmacao = ge.obter_entrada_inteira_valida("Opção escolhida: ", 1, 2)

            if confirmacao == 1:
                cursor.execute('DELETE FROM eleitores WHERE id = %s', (eleitor['id'],))
                conexao.commit()
                print("\nEleitor removido com sucesso.")
            else:
                print("\nRemoção cancelada pelo usuário.")

    cursor.close()
    conexao.close()
#usando esse if para poder rodar o teste dentro deste arquivo e nao na main.py

if __name__ == "__main__":
    remocao_eleitores()

#NEXT STEPS
#substituir a verificação len() != 12 do título pela função validar_titulo quando ela for adicionada em Verificadores
