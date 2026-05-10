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
    "Abertura_Urna.txt"
)


def ocorrencia_abertura_urna():
    '''
    Cria o log de ocorrencia para abertura de urna após Zerézima, e insere informações nele

    Args: None

    Returns: None
    '''

    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(Fore.RED + Style.BRIGHT +
                  f"\n[{sem_milisegundos}] ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")


def imprimir_ocorrencia_abertura_urna():
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
              "\nNenhum Log de Abertura de Urna Registrado")
        confirmacao.confirmacao()
    except Exception as e:
        print(Fore.RED + Style.BRIGHT +
              f"\nErro ao ler o log de Abertura de Urna {e}")
        confirmacao.confirmacao()


def excluir_ocorrencia_abertura_urna():
    """
    Exclui o log de ocorrencia de abertura de urna

    Args: None

    Returns: None
    """
    arquivo = CAMINHO_ARQUIVO
    os.remove(arquivo)
