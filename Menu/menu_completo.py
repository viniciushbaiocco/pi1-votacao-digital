from Menu import sub_menus as sm
from Verificadores import gerenciador_de_entrada as ge
from Gerenciamento import busca_eleitores, edicao_eleitores, listagem_eleitores, remocao_eleitores
from Cadastro import cadastro_eleitores
def menu_completo():
    """
    Gerencia a navegação completa entre os menus da aplicação (principal, gerenciamento e votação).
    Permite ao usuário interagir com as diferentes funcionalidades do sistema.

    Args:
        None

    Returns:
        None

    """
    executando_menu_principal = 1
    while executando_menu_principal:
        sm.exibir_menu_principal()
        escolha_principal = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 3)

        if escolha_principal == 1:  # Gerenciamento
            executando_menu_gerenciamento = 1
            while executando_menu_gerenciamento == 1:
                sm.exibir_menu_gerenciamento()
                escolha_gerenciamento = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 3)

                if escolha_gerenciamento == 1:  # Eleitores
                    executando_menu_eleitores = 1
                    while executando_menu_eleitores:
                        sm.exibir_menu_eleitores()
                        escolha_eleitor = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 6)

                        match escolha_eleitor:
                            case 1:
                                cadastro_eleitores.cadastrar_eleitor()
                            case 2:
                                edicao_eleitores.edicao_eleitores()
                            case 3:
                                remocao_eleitores.remocao_eleitores()
                            case 4:
                                busca_eleitores.busca_eleitor()
                            case 5:
                                listagem_eleitores.listagem_eleitores()
                            case 6:  # Voltar
                                executando_menu_eleitores = 0
                elif escolha_gerenciamento == 2:  # Candidatos
                    executando_menu_candidatos = 1
                    while executando_menu_candidatos == 1:
                        sm.exibir_menu_candidatos()
                        escolha_candidato = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 6)

                        match escolha_candidato:
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
                            case 6:  # Voltar
                                executando_menu_candidatos = 0
                elif escolha_gerenciamento == 3:  # Voltar
                    executando_menu_gerenciamento = 0

        elif escolha_principal == 2:  # Votação
            executando_menu_votacao = 1
            while executando_menu_votacao == 1:
                sm.exibir_menu_votacao()
                escolha_votacao = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 3)

                if escolha_votacao == 1:  # Abrir Sistema De Votação
                    executando_menu_sistema_votacao = 1
                    while executando_menu_sistema_votacao == 1:
                        sm.exibir_menu_sistema_votacao()
                        escolha_sistema_votacao = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 3)

                        match escolha_sistema_votacao:
                            case 1:
                                print("Em desenvolvimento...")
                            case 2:
                                print("Em desenvolvimento...")
                            case 3:  # Voltar
                                executando_menu_sistema_votacao = 0
                elif escolha_votacao == 2:  # Resultados Da Votação
                    executando_menu_resultados_votacao = 1
                    while executando_menu_resultados_votacao == 1:
                        sm.exibir_menu_restultados_votacao()
                        escolha_resultado_votacao = ge.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 5)

                        match escolha_resultado_votacao:
                            case 1:
                                print("Em desenvolvimento...")
                            case 2:
                                print("Em desenvolvimento...")
                            case 3:
                                print("Em desenvolvimento...")
                            case 4:
                                print("Em desenvolvimento...")
                            case 5:  # Voltar
                                executando_menu_resultados_votacao = 0
                elif escolha_votacao == 3:  # Voltar
                    executando_menu_votacao = 0

        elif escolha_principal == 3:  # Sair
            print("Saindo...")
            executando_menu_principal = 0