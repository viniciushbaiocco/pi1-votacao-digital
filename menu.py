def exibir_menu_principal():
    """
    Exibe o menu principal da aplicação com as opções de gerenciamento, votação e saída.

    Args:
        None

    Returns:
        None
    """
    print("\n--- Menu Principal ---")
    print("1 - Gerenciamento")
    print("2 - Votação")
    print("3 - Sair")

def exibir_menu_gerenciamento():
    """
    Exibe o menu de gerenciamento com as opções de eleitores e candidatos.

    Args:
        None

    Returns:
        None
    """
    print("\n-- Gerenciamento")
    print("1 - Eleitores")
    print("2 - Candidatos")

def exibir_menu_eleitores():
    """
    Exibe o menu de eleitores com as opções de cadastrar, editar, excluir, buscar e visualizar eleitores.

    Args:
        None

    Returns:
        None
    """
    print("1 - Cadastrar Novos Eleitores")
    print("2 - Editar Eleitores")
    print("3 - Excluir Eleitores")
    print("4 - Buscar Eleitores")
    print("5 - Visualizar Eleitores")

def exibir_menu_candidatos():
    """
    Exibe o menu de eleitores com as opções de cadastrar, editar, excluir, buscar e visualizar candidatos.

    Args:
        None

    Returns:
        None
    """
    print("1 - Cadastrar Novos Candidatos")
    print("2 - Editar Candidatos")
    print("3 - Excluir Candidatos")
    print("4 - Buscar Candidatos")
    print("5 - Visualizar Candidatos")

def exibir_menu_votacao():
    """
    Exibe o menu de votação com as opções de abrir o sistema de votação e resultados da votação.

    Args:
        None

    Returns:
        None
    """
    print("\n--- Votação ---")
    print("1 - Abrir Sistema De Votação")
    print("2 - Resultados Da Votação")

def exibir_menu_sistema_votacao():
    """
    Exibe o menu de sistema de votação com as opções votar e encessar o sistema de votação.

    Args:
        None

    Returns:
        None
    """
    print("1 - Votar")
    print("2 - Encerrar Sistema De Votação")

def exibir_menu_restultados_votacao():
    """
    Exibe o menu de resultados da voação com as opções de boletim de urna, estastísticas de comparecimento,
    votos por partido e validação por integridade.

    Args:
        None

    Returns:
        None
        """
    print("1 - Boletim De Urna")
    print("2 - Estatísticas De Comparecimento")
    print("3 - Votos Por Partido")
    print("4 - Validação De Integridade")

def obter_entrada_inteira_valida(mensagem, min_val, max_val):
    """
    Solicita uma entrada inteira ao usuário e valida se está dentro de um intervalo.
    Continua pedindo até que uma entrada válida seja fornecida.

    Args:
        mensagem(str): A mensagem que deve ser inserida após a apresentação do menu.
        min_val(int): Valor mínimo para determinada escolha do menu.
        max_val(int): Valor máximo para determinada escolha do menu.

    Returns:
        int: Retorna o valor inteiro (opção) escolhida pelo usuário.

    """
    while True:
        try:
            escolha = int(input("\n"+mensagem))
            if min_val <= escolha <= max_val:
                return escolha
            else:
                print(f"Opção inválida. Por favor, escolha uma opção entre {min_val} e {max_val}.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def menu_completo():
    """
    Gerencia a navegação completa entre os menus da aplicação (principal, gerenciamento e votação).
    Permite ao usuário interagir com as diferentes funcionalidades do sistema.

    Args:
        None

    Returns:
        None
    """
    while True: # Mantém o menu ativo

        exibir_menu_principal()
        escolha = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 3)

        match (escolha):
            case 1:  # Entra na parte de gerenciamento
                exibir_menu_gerenciamento()
                escolha_gerenciamento = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                match (escolha_gerenciamento):
                    case 1:
                        exibir_menu_eleitores()
                        escolha_eleitor = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 5)

                        match escolha_eleitor:
                            case 1:
                                print("Em desenvolvimento...")
                            case 2:
                                print("Em desenvolvimento...")
                            case 3:
                                print("Em desenvolvimento...")
                            case 4:
                                print("Em desenvolvimento...")
                            case 5:
                                print("Em desenvolvimento...")

                    case 2:
                        exibir_menu_candidatos()
                        escolha_candidatao = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 5)

                        match escolha_candidatao:
                            case 1:
                                print("Em desenvolvimento...")
                            case 2:
                                print("Em desenvolvimento...")
                            case 3:
                                print("Em desenvolvimento...")
                            case 4:
                                print("Em desenvolvimento...")
                            case 5:
                                print("Em desenvolvimento...")

                # Após a execução do sub-menu, o loop principal continua e exibe o menu principal novamente

            case 2:  # Entra na parte de votação
                exibir_menu_votacao()
                escolha_votacao = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                match (escolha_votacao):
                    case 1:
                        exibir_menu_sistema_votacao()
                        escolha_sistema_votacao = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                        match escolha_sistema_votacao:
                            case 1:
                                print("Em desenvolvimento...")
                            case 2:
                                print("Em desenvolvimento...")

                    case 2:
                        exibir_menu_restultados_votacao()
                        escolha_resultado_votacao = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 4)

                        match escolha_resultado_votacao:
                            case 1:
                                print("Em desenvolvimento...")
                            case 2:
                                print("Em desenvolvimento...")
                            case 3:
                                print("Em desenvolvimento...")
                            case 4:
                                print("Em desenvolvimento...")

                # Após a execução do sub-menu, o loop principal continua e exibe o menu principal novamente

            case 3:
                print("Saindo...")
                break  # Sai do loop 'while True', encerrando o programa