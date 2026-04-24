# entrada: CPF ou Título eleitor
# processamento: busca no banco de dados a correspondencia de inputs.
# o cpf está cifrado no banco, logo o input precisa passar pela cifragem para encontrar a correspondencia no banco
# exibe: nome eleitor, titulo eleitor, se mesário, se votou


def busca_eleitor():

    from Verificadores import gerenciador_de_entrada as ge
    from Menu import sub_menus as sb
    import Verificadores.validacao_cpf as val_cpf
    import Verificadores.verificacao_cpf_banco as ver_cpf
    import Verificadores.verificacao_titulo_banco as ver_titulo
    import conexao_banco as conect

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()

    print("\n--- 4 - Buscar Eleitores ---")
    print("\nOpção 1: Busca pelo CPF")
    print("\nOpção 2: Busca pelo Título de eleitor")
    print("\nOpção 3: Voltar ao Menu de Gerenciamento de Eleitores")

    opcao = ge.obter_entrada_inteira_valida("\nDigite uma opção: ", 1, 3)

    while opcao != 3:

        if opcao == 1:

            cpf = str(input("\nDigite o número do CPF a ser consultado: "))
            validacao_cpf = val_cpf.validacao_de_cpf(cpf)
            while validacao_cpf != True:
                cpf = str(
                    input("\nDigite novamente o número do CPF a ser consultado: "))
                validacao_cpf = val_cpf.validacao_de_cpf(cpf)

            # Criptografia: tem que entar aqui. CPF criptografado deve ser entrada para ver_CPF_banco

            verificacao_cpf_banco = ver_cpf.verificar_cpf_banco(
                cpf)  # tem que ser CPF criptografado

            if verificacao_cpf_banco[0] == 1:
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

                print(f"\n --- Dados do eleitor ---"
                      f"\nNome eleitor: {nome}"
                      f"\nTítulo de eleitor: {titulo}"
                      f"\nMesário: {mesario}"
                      f"\nStatus votação: {status_votacao}")
            else:
                print(
                    "Eleitor não cadastrado. Realizar o cadastramento no Menu Gerenciamento Eleitores.")

        if opcao == 2:

            titulo_eleitor = str(
                input("Digite o número do Título de eleitor a ser consultado: "))
            # inserir validacao do título

            verificar_titulo = ver_titulo.verificar_titulo_de_eleitor_banco(
                titulo_eleitor)

            if verificar_titulo[0] == 1:
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

                print(f"\n --- Dados do eleitor ---"
                      f"\nNome eleitor: {nome}"
                      f"\nTítulo de eleitor: {titulo}"
                      f"\nMesário: {mesario}"
                      f"\nStatus votação: {status_votacao}")
            else:
                print(
                    "Eleitor não cadastrado. Realizar o cadastramento no Menu Gerenciamento Eleitores.")

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


# usando esse if para poder rodar o teste dentro deste arquivo e nao na main.py
if __name__ == "__main__":
    busca_eleitor()


# Next steps:
# Proteger a devolucao do titulo de eleitor invalido
# incluir criptografia

# Finalizados:
# incluir validacao de CPF e  Proteger a devolucao caso cpf caso invalido ok
# Proteger caso cpf ou titulo nao encontrado no banco ok
# Proteger a devolucao caso a opcao digitada seja diferente de 1, 2 e 3 - funcao gerenciador de entradas
# ajustar saída: legível e amigável para o usuário ok!
# Ao exibir o resultado, voltar para o menu de busca, permitindo novas buscas ou voltar pra o menu eleitores - ok
