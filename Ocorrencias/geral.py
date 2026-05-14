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
    "Geral.txt"
)

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
        arq.write(Fore.GREEN + Style.BRIGHT +
                  f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")

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
        arq.write(Fore.RED + Style.BRIGHT +
                  f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ALERTA: Validação do mesário negado")

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
                  f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ENCERRAMENTO: Votação encerrada. Total de votos registrados.")

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
        arq.write(Fore.GREEN + Style.BRIGHT +
                  f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] Voto Computado!")

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
        arq.write(Fore.RED + Style.BRIGHT +
                  f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ALERTA: Tentativa de Voto Duplo")

def imprimir_ocorrencias_por_sessao():
    """
        Lê o arquivo de logs e imprime as ocorrências agrupadas por sessão.
    """

    try:

        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:

            conteudo = arq.read()
            print(conteudo)
        confirmacao.confirmacao()

    except FileNotFoundError:
        print(Fore.YELLOW + Style.BRIGHT +
              "\nNenhum Log de Ocorrência Registrado")
        confirmacao.confirmacao()

    except Exception as e:
        print(Fore.RED + Style.BRIGHT +
              f"\nErro ao ler o log de Ocorrência: {e}")
        confirmacao.confirmacao()

def excluir_arquivo_ocorrencias_gerais():
    """
        Exclui o arquivo de voto duplo caso houver.

        Args:
            None

        Returns:
            None
    """
    arquivo = CAMINHO_ARQUIVO
    if os.path.exists(arquivo):
        os.remove(arquivo)
