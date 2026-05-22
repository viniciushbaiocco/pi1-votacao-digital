from Menu import sub_menus as sm
from Validadores import gerenciador_de_entrada as ge
from Gerenciamento import busca_eleitores, edicao_eleitores, listagem_eleitores, remocao_eleitores, recuperacao_chave
from Gerenciamento import busca_candidatos, edicao_candidatos, listagem_candidatos, remocao_candidatos
from Cadastro import cadastro_eleitores, cadastro_candidatos
from Ocorrencias import acesso_negado, voto_computado, voto_duplo, abertura_urna, encerramento_urna, geral
from Votacao import abertura_votacao, encerramento_votacao, sistema_voto
from rich.console import Console
from Resultados import boletim_urna, estatistica_comparecimento, votos_partido, validacao_integridade
from Visual.visual import limpar_tela

console = Console(highlight=False)


def menu_completo():
    """
    Atua como o orquestrador principal de rotas e navegação de menus do sistema da urna eleitoral.

    Esta função gerencia loops aninhados que estruturam os submenus da aplicação,
    permitindo uma navegaçao hierárquica e bidirecional (avançar e voltar) entre as
    seguintes seções:

    1. Menu de Gerenciamento: Subdividido no CRUD e relatórios de Eleitores e Candidatos.
    2. Menu de Votação: Responsável pelo ciclo de abertura de sessão, votação em tempo
       real, encerramento e auditoria.
    3. Resultados da Votação: Emissão de relatórios consolidados como Boletim de Urna,
       Estatísticas de Comparecimento, Votos por Partido e Validação de Integridade.
    4. Menu de Ocorrências: Histórico de logs de auditoria e segurança da urna.

    A função mantém o estado da 'sessao' atual e garante que, ao finalizar a execução
    do menu principal de forma voluntária, todos os arquivos de logs temporários de
    auditoria criados em disco sejam eliminados de maneira segura para preservar o
    sigilo e a integridade do encerramento da urna.

    Args:
        None.

    Returns:
        None: A função gerencia o ciclo de vida completo da execução do programa,
        não retornando nenhum valor.
    """
    executando_menu_principal = 1
    sessao = 0 # Começa a sessão como 0
    while executando_menu_principal:
        sm.exibir_menu_principal()
        escolha_principal = ge.obter_entrada_inteira_valida(
            "Escolha uma opção: ", 1, 2)

        if escolha_principal == 1:  # Gerenciamento
            executando_menu_gerenciamento = 1
            while executando_menu_gerenciamento == 1:
                sm.exibir_menu_gerenciamento()
                escolha_gerenciamento = ge.obter_entrada_inteira_valida(
                    "Escolha uma opção: ", 1, 2)

                if escolha_gerenciamento == 1:  # Eleitores
                    executando_menu_eleitores = 1
                    while executando_menu_eleitores:
                        sm.exibir_menu_eleitores()
                        escolha_eleitor = ge.obter_entrada_inteira_valida(
                            "Escolha uma opção: ", 1, 6)

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
                            case 6:
                                recuperacao_chave.recuperar_chave()
                            case False:  # Voltar
                                executando_menu_eleitores = 0
                elif escolha_gerenciamento == 2:  # Candidatos
                    executando_menu_candidatos = 1
                    while executando_menu_candidatos == 1:
                        sm.exibir_menu_candidatos()
                        escolha_candidato = ge.obter_entrada_inteira_valida(
                            "Escolha uma opção: ", 1, 5)

                        match escolha_candidato:
                            case 1:
                                cadastro_candidatos.cadastrar_candidato()
                            case 2:
                                edicao_candidatos.edicao_candidatos()
                            case 3:
                                remocao_candidatos.remocao_candidatos()
                            case 4:
                                busca_candidatos.busca_candidato()
                            case 5:
                                listagem_candidatos.listagem_candidatos()
                            case False:  # Voltar
                                executando_menu_candidatos = 0
                elif escolha_gerenciamento == False:  # Voltar
                    executando_menu_gerenciamento = 0

        elif escolha_principal == 2:  # Votação
            executando_menu_votacao = 1
            while executando_menu_votacao == 1:
                sm.exibir_menu_votacao()
                escolha_votacao = ge.obter_entrada_inteira_valida(
                    "Escolha uma opção: ", 1, 3)

                if escolha_votacao == 1: # Abre a opção de iniciar a votação
                    sessao += 1 # Contabiliza a sessão após essa abertura
                    if abertura_votacao.abrir_sistema_votacao(sessao): # Se confirmado abre o sistema
                        executando_menu_sistema_votacao = 1
                        while executando_menu_sistema_votacao == 1:
                            sm.exibir_menu_sistema_votacao()
                            escolha_sistema_votacao = ge.obter_entrada_inteira_valida(
                                "Escolha uma opção: ", 1, 2)

                            match escolha_sistema_votacao:
                                case 1:
                                    sistema_voto.sistema_voto(sessao)
                                case 2:
                                    if encerramento_votacao.encerrar_sistema_votacao(sessao):
                                        executando_menu_sistema_votacao = 0

                elif escolha_votacao == 2:  # Resultados Da Votação
                    executando_menu_resultados_votacao = 1
                    while executando_menu_resultados_votacao == 1:
                        sm.exibir_menu_resultados_votacao()
                        escolha_resultado_votacao = ge.obter_entrada_inteira_valida(
                            "Escolha uma opção: ", 1, 4)

                        match escolha_resultado_votacao:
                            case 1:
                                boletim_urna.exibir_boletim_urna()
                            case 2:
                                estatistica_comparecimento.exibir_estatistica_comparecimento()
                            case 3:
                                votos_partido.votos_por_partido()
                            case 4:
                                validacao_integridade.validar_integridade()
                            case False:  # Voltar
                                executando_menu_resultados_votacao = 0
                elif escolha_votacao == 3:
                    executando_menu_ocorrencias = 1
                    while executando_menu_ocorrencias == 1:
                        sm.exibir_menu_ocorrencias()
                        escolha_ocorrencia = ge.obter_entrada_inteira_valida(
                            "Escolha uma opção: ", 1, 6)

                        match escolha_ocorrencia:
                            case 1:
                                limpar_tela()
                                abertura_urna.imprimir_ocorrencia_abertura_urna()
                            case 2:
                                limpar_tela()
                                acesso_negado.imprimir_ocorrencia_acesso_negado()
                            case 3:
                                limpar_tela()
                                encerramento_urna.imprimir_ocorrencia_encerramento_urna()
                            case 4:
                                limpar_tela()
                                voto_computado.imprimir_voto_computado()
                            case 5:
                                limpar_tela()
                                voto_duplo.imprimir_voto_duplo()
                            case 6:
                                limpar_tela()
                                geral.imprimir_ocorrencias_por_sessao()
                            case False:
                                executando_menu_ocorrencias = 0  # Voltar
                elif escolha_votacao == False:  # Voltar
                    executando_menu_votacao = 0

        elif escolha_principal == False:  # Sair
            console.print("Sistema Finalizado", style="bold green")
            acesso_negado.excluir_ocorrencia_acesso_negado()
            abertura_urna.excluir_ocorrencia_abertura_urna()
            encerramento_urna.excluir_ocorrencia_encerramento_urna()
            voto_computado.excluir_arquivo_voto_computado()
            voto_duplo.excluir_arquivo_voto_duplo()
            geral.excluir_arquivo_ocorrencias_gerais()
            executando_menu_principal = 0
