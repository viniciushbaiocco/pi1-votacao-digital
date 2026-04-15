from Menu import gerenciador_de_entrada as ge, sub_menus as sm

def menu_completo():
    """
    Gerencia a navegação completa entre os menus da aplicação (principal, gerenciamento e votação).
    Permite ao usuário interagir com as diferentes funcionalidades do sistema.

    Args:
        None

    Returns:
        None
    """
    executando_menu = 0 # Substitui o True
    while (executando_menu == 0):

        sm.exibir_menu_principal()
        escolha = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 4)

        match (escolha):
            case 1:  # Entra na parte de gerenciamento
                sm.exibir_menu_gerenciamento()
                escolha_gerenciamento = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                match (escolha_gerenciamento):
                    case 1:
                        sm.exibir_menu_eleitores()
                        escolha_eleitor = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 5)

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
                        sm.exibir_menu_candidatos()
                        escolha_candidatao = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 5)

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
                sm.exibir_menu_votacao()
                escolha_votacao = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                match (escolha_votacao):
                    case 1:
                        sm.exibir_menu_sistema_votacao()
                        escolha_sistema_votacao = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                        match escolha_sistema_votacao:
                            case 1:
                                print("Em desenvolvimento...")
                            case 2:
                                print("Em desenvolvimento...")

                    case 2:
                        sm.exibir_menu_restultados_votacao()
                        escolha_resultado_votacao = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 4)

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
                sm.exibir_menu_auditoria()
                escolha_auditoria = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

                match escolha_auditoria:
                    case 1:
                        print("Em desenvolvimento...")
                    case 2:
                        print("Em desenvolvimento...")

            case 4:
                print("Saindo...")
                executando_menu = 1
