import os
from datetime import datetime
from rich.console import Console
from Validadores import confirmacao

console = Console(highlight=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)
CAMINHO_ARQUIVO = os.path.join(PASTA_ARMAZENAMENTO, "Voto_Computado.txt")


def ocorrecia_voto_computado(id_sessao):
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


def imprimir_voto_computado():
    """
    Faz a leitura do arquivo de voto computado caso houver.

    Args:
        None

    Returns:
        None
    """
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            console.print(conteudo, markup=False)
            confirmacao.confirmacao()
    except FileNotFoundError:
        console.print("\nNenhum Log de Voto Registrado", style="bold yellow")
        confirmacao.confirmacao()
    except Exception as e:
        console.print(f"\nErro ao ler o log de Voto {e}", style="bold red")
        confirmacao.confirmacao()


def excluir_arquivo_voto_computado():
    """
    Exclui o arquivo de voto computado caso houver.

    Args:
        None

    Returns:
        None
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
