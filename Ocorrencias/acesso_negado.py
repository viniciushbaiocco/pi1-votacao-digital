from colorama import Fore,Style
from datetime import datetime
from Validadores import confirmacao
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.join(BASE_DIR, "Acesso_Negado.txt")

def ocorrencia_acesso_negado():
    '''
    Cria o log de ocorrencia para acesso negado do mesário, e insere informações nele

    Args: None

    Returns: None
    '''
    try:
        with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
            agora = datetime.now()
            sem_milisegundos = agora.replace(microsecond=0)
            arq.write(Fore.RED + Style.BRIGHT + f"\n[{sem_milisegundos}] ALERTA: Validação do mesário negado")
    except FileNotFoundError:
        with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
            arq.write(Fore.RED + Style.BRIGHT + f"\n[{sem_milisegundos}] ALERTA: Validação do mesário negado")

def imprimir_ocorrencia_acesso_negado():
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
        print(Fore.YELLOW + Style.BRIGHT +"\nNenhum Log de Acesso Negado Registrado")
        confirmacao.confirmacao()
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\nErro ao ler o log de Acesso Negado {e}")
        confirmacao.confirmacao()

def excluir_ocorrencia_acesso_negado():
    """
    Exclui o log de ocorrencia de acesso negado

    Args: None

    Returns: None
    """
    arquivo = CAMINHO_ARQUIVO
    os.remove(arquivo)