import os
from datetime import datetime
from colorama import Fore, Style
from Validadores import confirmacao

# pasta do arquivo atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# cria o caminho da pasta Armazenamento
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")

# cria a pasta caso ela não exista
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)

# caminho completo do arquivo
CAMINHO_ARQUIVO = os.path.join(
    PASTA_ARMAZENAMENTO,
    "Voto_Duplo.txt"
)

def ocorrencia_voto_duplo():
    """
        Cria o arquivo que armazena os logs de voto duplo e insere os logs nele.
        
        Args:
            None

        Returns:
            None
    """
    try:
        with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
            agora = datetime.now()
            sem_milisegundos = agora.replace(microsecond=0)
            arq.write(Fore.RED + Style.BRIGHT + f"\n[{sem_milisegundos}] ALERTA: Tentativa de Voto Duplo")
    except FileNotFoundError:
        with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
            arq.write(Fore.RED + Style.BRIGHT + f"\n[{sem_milisegundos}] ALERTA: Tentativa de Voto Duplo")

def imprimir_voto_duplo():
    """
        Faz a leitura do arquivo de voto duplo caso houver.

        Args:
            None

        Returns:
            None
    """
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            print(conteudo)
            confirmacao.confirmacao()
    except FileNotFoundError:
        print(Fore.YELLOW + Style.BRIGHT +"\nNenhum Log de Voto Duplo Registrado")
        confirmacao.confirmacao()
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\nErro ao ler o log de Voto Duplo {e}")
        confirmacao.confirmacao()

def excluir_arquivo_voto_duplo():
    """
        Exclui o arquivo de voto duplo caso houver.

        Args:
            None

        Returns:
            None
    """
    arquivo = CAMINHO_ARQUIVO
    os.remove(arquivo)
