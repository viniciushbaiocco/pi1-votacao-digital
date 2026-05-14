import time

from Menu import sub_menus
from database import conexao_banco
from colorama import Fore, Style
from Validadores import confirmacao, gerenciador_de_entrada
import os
from time import sleep
from Visual import visual

COR_BRANCA = Fore.WHITE + Style.BRIGHT
COR_AMARELA = Fore.YELLOW + Style.BRIGHT

def exibir_boletim_urna():
    """
    Gerencia a exibição do boletim de urna, permitindo ao usuário listar candidatos
    com seus respectivos votos ou determinar o vencedor da eleição.

    Args:
        None

    Returns:
        Listagem ou o Vencedor
    """
    conexao = None
    cursor = None
    try:
        conexao = conexao_banco.conexao_banco()
        cursor = conexao.cursor(dictionary=True)

        executando_entrada = 1
        while executando_entrada == 1:
            sub_menus.exibir_menu_boletim_urna()
            escolha = gerenciador_de_entrada.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 3)

            match escolha:
                # Opção 1: Listar todos os candidatos com seus votos
                case 1:
                    query_listagem_candidatos = ('SELECT c.nome, c.partido, '
                                                 'COUNT(v.id) AS total_votos '
                                                 'FROM candidatos c '
                                                 'LEFT JOIN votos v '
                                                 'ON c.id = v.id_candidato '
                                                 'GROUP BY c.id, c.nome, c.partido '
                                                 'ORDER BY nome ASC')

                    cursor.execute(query_listagem_candidatos)
                    total_candidatos = cursor.fetchall()
                    print("Listando Candidatos...")
                    time.sleep(3)
                    print(COR_BRANCA + '\n --- Listagem de Candidatos ---')
                    for candidatos in (total_candidatos):
                        print(COR_BRANCA + '=' * 50)
                        print(COR_BRANCA + f' Nome: {candidatos['nome']}')
                        print(COR_BRANCA + f' Partido: {candidatos['partido']}')
                        print(COR_BRANCA + f' Total de Votos: {candidatos['total_votos']}')
                    print(COR_BRANCA + '=' * 50)
                    print(COR_BRANCA + f' Total de Candidatos Cadastrados: {len(total_candidatos)}')

                    confirmacao.confirmacao()
                    visual.limpar_tela()

                # Opção 2: Exibir o vencedor da eleição
                case 2:
                    query_verificar_tabela_votos = ('SELECT * FROM votos')
                    cursor.execute(query_verificar_tabela_votos)
                    verificar_tabela = cursor.fetchall()

                    if not verificar_tabela:
                        visual.carregar_pontos_loop(3, "Verificando Vencedor")
                        time.sleep(2)
                        print(COR_AMARELA + "\nNenhum Voto Registrado")
                        print(COR_AMARELA + "Vencedor não pode ser definido..")

                        confirmacao.confirmacao()
                        visual.limpar_tela()

                    # Se houver votos, tenta determinar o vencedor
                    else:
                        query_verificar_vencedor =  ('SELECT c.nome, c.partido, '
                                                     'COUNT(v.id) AS total_votos '
                                                     'FROM candidatos c '
                                                     'LEFT JOIN votos v '
                                                     'ON c.id = v.id_candidato '
                                                     'GROUP BY c.id, c.nome, c.partido '
                                                     ' ORDER BY total_votos DESC')
                        cursor.execute(query_verificar_vencedor)
                        vencedor = cursor.fetchone()
                        # Consome o restante dos resultados para evitar erros em futuras operações do cursor
                        cursor.fetchall()

                        if vencedor:
                            visual.carregar_pontos_loop(3, "Verificando Vencedor")
                            time.sleep(2)
                            print(Fore.CYAN + Style.BRIGHT + "\n----VENCEDOR----")
                            print(COR_BRANCA + f'\n Nome: {vencedor['nome']}')
                            print(COR_BRANCA + f' Partido: {vencedor['partido']}')
                            print(COR_BRANCA + f' Total de Votos: {vencedor['total_votos']}')
                        # Caso não seja possível determinar um vencedor (improvável com a query atual, mas como fallback)
                        else:
                            visual.carregar_pontos_loop(3, "Verificando Vencedor")
                            time.sleep(2)
                            print(COR_AMARELA + "\nNão foi possível determinar um vencedor, mesmo com votos registrados.")

                        # Pausa e limpa a tela após exibir o resultado
                        confirmacao.confirmacao()
                        visual.limpar_tela()
                case 3:
                    executando_entrada = 0
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
