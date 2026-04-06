import SubMenus

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
    while 1: # Substitui while True
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
    executando_menu = 1 # Substitui o True
    while executando_menu:

        SubMenus.exibir_menu_principal()
        escolha = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 3)

        match (escolha):
            case 1:  # Entra na parte de gerenciamento
                SubMenus.exibir_menu_gerenciamento()
                escolha_gerenciamento = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                match (escolha_gerenciamento):
                    case 1:
                        SubMenus.exibir_menu_eleitores()
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
                        SubMenus.exibir_menu_candidatos()
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
                SubMenus.exibir_menu_votacao()
                escolha_votacao = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                match (escolha_votacao):
                    case 1:
                        SubMenus.exibir_menu_sistema_votacao()
                        escolha_sistema_votacao = obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                        match escolha_sistema_votacao:
                            case 1:
                                print("Em desenvolvimento...")
                            case 2:
                                print("Em desenvolvimento...")

                    case 2:
                        SubMenus.exibir_menu_restultados_votacao()
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
                executando_menu = 0
menu_completo()