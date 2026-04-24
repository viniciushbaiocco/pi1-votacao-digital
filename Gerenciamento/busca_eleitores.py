# entrada: CPF ou Título eleitor
# processamento: busca no banco de dados a correspondencia de inputs.
# o cpf está cifrado no banco, logo o input precisa passar pela cifragem para encontrar a correspondencia no banco
# exibe: nome eleitor, titulo eleitor, se mesário, se votou


def busca_eleitor():

    print("\n--- 4 - Buscar Eleitores ---")
    print("\nOpção 1: Busca pelo CPF")
    print("\nOpção 2: Busca pelo Título de eleitor")
    print("\nOpção 3: Voltar ao Menu de Gerenciamento de Eleitores")

    from Menu import gerenciador_de_entrada as ge
    from Menu import sub_menus as sb
    import verificacao_cpf
    from database import conexao_banco as conect

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    opcao = ge.obter_entrada_inteira_valida("\nDigite uma opção: ", 1, 3)

    while opcao != 3:

        if opcao == 1:

            cpf = str(input("\nDigite o número do CPF a ser consultado: "))
            # validacao_cpf = verificacao_cpf.validacao_de_cpf(cpf)
            # criptografar o cpf digitado
            comando = (
                "SELECT nome, mesario, titulo_eleitor, status_votacao FROM eleitores WHERE cpf = %s")
            valores = (cpf, )

            cursor.execute(comando, valores)
            dados_eleitor = cursor.fetchone()

            nome = dados_eleitor[0]
            mesario = dados_eleitor[1]
            if mesario == 0:
                mesario = "Não"
            else:
                mesario = "Sim"
            titulo = dados_eleitor[2]
            status_votacao = dados_eleitor[3]
            if status_votacao == 0:
                status_votacao = "NÃO VOTOU"
            else:
                status_votacao = "VOTOU"
            print(f"\nNome eleitor: {nome}"
                  f"\nTítulo de eleitor: {titulo}"
                  f"\nMesário: {mesario}"
                  f"\nStatus votação: {status_votacao}")

        if opcao == 2:
            titulo_eleitor = str(
                input("Digite o número do Título de eleitor a ser consultado: "))
            # validar o titulo digitado
            comando = (
                "SELECT nome, mesario, titulo_eleitor, status_votacao FROM eleitores WHERE titulo_eleitor = %s")
            valores = (titulo_eleitor, )

            cursor.execute(comando, valores)
            dados_eleitor = cursor.fetchone()

            nome = dados_eleitor[0]
            mesario = dados_eleitor[1]
            if mesario == 0:
                mesario = "Não"
            else:
                mesario = "Sim"
            titulo = dados_eleitor[2]
            status_votacao = dados_eleitor[3]
            if status_votacao == 0:
                status_votacao = "NÃO VOTOU"
            else:
                status_votacao = "VOTOU"
            print(f"\nNome eleitor: {nome}"
                  f"\nTítulo de eleitor: {titulo}"
                  f"\nMesário: {mesario}"
                  f"\nStatus votação: {status_votacao}")

        print("\n--- Deseja buscar um novo eleitor? ---")
        print("\nOpção 1: Busca pelo CPF")
        print("\nOpção 2: Busca pelo Título de eleitor")
        print("\nOpção 3: Voltar ao Menu de Gerenciamento de Eleitores")

        opcao = ge.obter_entrada_inteira_valida(
            "\nDigite uma opção: ", 1, 3)

    cursor.close()
    conexao.close()

    print("\n")
    sb.exibir_menu_eleitores()
    print("\n")

# fazer a busca dos inputs com seus correspondentes no banco de dados
# retonar com nome eleitor


if __name__ == "__main__":
    busca_eleitor()


# usando esse if para poder rodar o teste dentro deste arquivo e nao na main.py

# Next steps:
# Proteger a devolucao caso cpf ou titulo de eleitor invalido
# Proteger caso cpf ou titulo nao encontrado no banco
# incluir validacao de CPF e criptografia
# Se pesquisar pelo titulo, devolver CPF tipo xxxxxxxxx-08?

# Proteger a devolucao caso a opcao digitada seja diferente de 1, 2 e 3 - funcao gerenciador de entradas
# ajustar saída: legível e amigável para o usuário ok!
# Ao exibir o resultado, voltar para o menu de busca, permitindo novas buscas ou voltar pra o menu eleitores - ok
