from Verificadores import verificacao_chave_acesso_banco
from Validadores import validacao_chave_acesso, confirmacao
from Validadores import gerenciador_de_entrada as ge
from database import conexao_banco
from Votacao import autenticacao_mesario
from criptografia import criptografia as cripto
from Ocorrencias import encerramento_urna, geral
from colorama import Fore, Style
from Visual.visual import limpar_tela

def encerrar_sistema_votacao(id_sessao):
    """
    Realiza o encerramento oficial do sistema de votação.

    Args:
        id_sessao (str): O ID único da sessão de urna que está sendo encerrada.

    Returns:
        bool: True se o encerramento for realizado com sucesso, False caso contrário.
    """

    # 1. Tentar autenticar o mesário, passando o session_id

    limpar_tela()

    if not autenticacao_mesario.autenticar_mesario(id_sessao):
        return False

    conexao = conexao_banco.conexao_banco() #mudei o import pq o nome tava diferente

    try:
        cursor = conexao.cursor()

        resposta = ge.obter_entrada_inteira_valida(Fore.WHITE + Style.BRIGHT + "\nDeseja realmente encerrar a votação? \n[1] - Sim \n [X] - Não ")

        if resposta.lower() != 1:
            print(Fore.YELLOW + Style.BRIGHT + "\nEncerramento cancelado.") #mudei a msg aqui
            confirmacao.confirmacao()
            return False

        print(Fore.GREEN + Style.BRIGHT + "\nSistema de votação encerrado.")

        encerramento_urna.ocorrencia_encerramento_urna(id_sessao)
        geral.ocorrencia_encerramento_urna(id_sessao)
        confirmacao.confirmacao()

        return True

    except:
        print(Fore.RED+ Style.BRIGHT + "\nErro ao registrar encerramento.")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if conexao:
            cursor.close()
            conexao.close()
