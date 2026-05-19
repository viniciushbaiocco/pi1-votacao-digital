from rich.console import Console
from datetime import datetime
from Validadores import confirmacao
import os

console = Console(highlight=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)
CAMINHO_ARQUIVO = os.path.join(PASTA_ARMAZENAMENTO, "Geral.txt")


def ocorrencia_abertura_urna(id_sessao):
    '''
    Cria o log de ocorrencia para abertura de urna após Zerézima, e insere informações nele

    Args:
        id_sessao (str): O ID único da sessão de urna atual.

    Returns: None
    '''
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")


def ocorrencia_acesso_negado(id_sessao):
    '''
    Cria o log de ocorrencia para acesso negado do mesário, e insere informações nele

    Args:
        id_sessao (str): O ID único da sessão de urna atual.

    Returns: None
    '''
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ALERTA: Validação do mesário negado")


def ocorrencia_encerramento_urna(id_sessao):
    '''
    Cria o log de ocorrencia para encerramento de urna.

    Args:
        id_sessao (str): O ID único da sessão de urna atual.

    Returns: None
    '''
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ENCERRAMENTO: Votação encerrada. Total de votos registrados.")


def ocorrencia_voto_computado(id_sessao):
    """
    Cria o arquivo que armazena os logs de voto computado e insere os logs nele.

    Args:
        id_sessao (str): O ID único da sessão de urna atual.

    Returns:
        None
    """
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] Voto Computado!")


def ocorrencia_voto_duplo(id_sessao):
    """
    Cria o arquivo que armazena os logs de voto duplo e insere os logs nele.

    Args:
        id_sessao (str): O ID único da sessão de urna atual.

    Returns:
        None
    """
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ALERTA: Tentativa de Voto Duplo")


def imprimir_ocorrencias_por_sessao():
    """
    Lê o arquivo de logs e imprime as ocorrências agrupadas por sessão.
    """
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            console.print(conteudo, markup=False)
        confirmacao.confirmacao()
    except FileNotFoundError:
        console.print("\nNenhum Log de Ocorrência Registrado", style="bold yellow")
        confirmacao.confirmacao()
    except Exception as e:
        console.print(f"\nErro ao ler o log de Ocorrência: {e}", style="bold red")
        confirmacao.confirmacao()


def excluir_arquivo_ocorrencias_gerais():
    """
    Exclui o arquivo de ocorrências gerais caso houver.

    Args:
        None

    Returns:
        None
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
