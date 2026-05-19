from rich.console import Console
from datetime import datetime
from Validadores import confirmacao
import os

console = Console(highlight=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)
CAMINHO_ARQUIVO = os.path.join(PASTA_ARMAZENAMENTO, "Acesso_Negado.txt")


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


def imprimir_ocorrencia_acesso_negado():
    """
    Imprime o log de ocorrencia no terminal

    Args: None

    Returns: None
    """
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            console.print(conteudo, markup=False)
            confirmacao.confirmacao()
    except FileNotFoundError:
        console.print("\nNenhum Log de Acesso Negado Registrado", style="bold yellow")
        confirmacao.confirmacao()
    except Exception as e:
        console.print(f"\nErro ao ler o log de Acesso Negado {e}", style="bold red")
        confirmacao.confirmacao()


def excluir_ocorrencia_acesso_negado():
    """
    Exclui o log de ocorrencia de acesso negado

    Args: None

    Returns: None
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
