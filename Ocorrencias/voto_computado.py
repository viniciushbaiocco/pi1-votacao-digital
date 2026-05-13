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
    "Voto_Computado.txt"
)


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
        arq.write(Fore.GREEN + Style.BRIGHT +
                  f"\n[{sem_milisegundos}] [SESSAO: {id_sessao}] Voto Computado!")


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
            print(conteudo)
            confirmacao.confirmacao()
    except FileNotFoundError:
        print(Fore.YELLOW + Style.BRIGHT + "\nNenhum Log de Voto Registrado")
        confirmacao.confirmacao()
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\nErro ao ler o log de Voto {e}")
        confirmacao.confirmacao()


def excluir_arquivo_voto_computado():
    """
        Exclui o arquivo de voto computado caso houver.

        Args:
            None

        Returns:
            None
    """
    arquivo = CAMINHO_ARQUIVO
    if os.path.exists(arquivo):
        os.remove(arquivo)
