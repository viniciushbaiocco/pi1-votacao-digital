from colorama import Fore, Style
from datetime import datetime
from Validadores import confirmacao
import os

# pasta do arquivo atual

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# cria o caminho da pasta Armazenamento

PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")

# cria a pasta caso ela não exista

os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)

# caminho completo do arquivo

CAMINHO_ARQUIVO = os.path.join(

    PASTA_ARMAZENAMENTO,

    "Encerramento_Urna.txt"

)

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
        arq.write(Fore.GREEN + Style.BRIGHT +
                  f"\n[{sem_milisegundos}] [SESSAO: {id_sessao}] ENCERRAMENTO: Votação encerrada. Total de votos registrados.")


def imprimir_ocorrencia_encerramento_urna():

    """

    Imprime o log de ocorrencia no terminal

    Args: None

    Returns: None

    """

    try:

        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:

            conteudo = arq.read()

            print(conteudo)

            confirmacao.confirmacao()

    except FileNotFoundError:

        print(Fore.YELLOW + Style.BRIGHT +

              "\nNenhum Log de Encerramento de Urna Registrado")

        confirmacao.confirmacao()

    except Exception as e:

        print(Fore.RED + Style.BRIGHT +

              f"\nErro ao ler o log de Encerramento de Urna {e}")

        confirmacao.confirmacao()

def excluir_ocorrencia_encerramento_urna():

    """

    Exclui o log de ocorrencia de encerramento de urna

    Args: None

    Returns: None

    """

    arquivo = CAMINHO_ARQUIVO
    if os.path.exists(arquivo):
        os.remove(arquivo)