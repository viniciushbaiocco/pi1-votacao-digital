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

def gerar_novo_id_sessao() -> str:
    """Gera um novo ID de sessão único baseado em timestamp e PID."""
    return f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{os.getpid()}"

def ocorrencia_abertura_urna(sessao_id):
    '''
    Cria o log de ocorrencia para abertura de urna após Zerézima, e insere informações nele

    Args:
        sessao_id (str): O ID único da sessão de urna atual.

    Returns: None
    '''
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(Fore.GREEN + Style.BRIGHT +
                  f"\n[{sem_milisegundos}] [SESSAO: {sessao_id}] ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")

def ocorrencia_acesso_negado(sessao_id):
    '''
    Cria o log de ocorrencia para acesso negado do mesário, e insere informações nele

    Args:
        sessao_id (str): O ID único da sessão de urna atual.

    Returns: None
    '''
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(Fore.RED + Style.BRIGHT +
                  f"\n[{sem_milisegundos}] [SESSAO: {sessao_id}] ALERTA: Validação do mesário negado")

def ocorrencia_encerramento_urna(sessao_id):

    '''

    Cria o log de ocorrencia para encerramento de urna.

    Args:
        sessao_id (str): O ID único da sessão de urna atual.

    Returns: None

    '''

    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(Fore.GREEN + Style.BRIGHT +
                  f"\n[{sem_milisegundos}] [SESSAO: {sessao_id}] ENCERRAMENTO: Votação encerrada. Total de votos registrados.")

def ocorrencia_voto_computado(sessao_id):
    """
        Cria o arquivo que armazena os logs de voto computado e insere os logs nele.

        Args:
            sessao_id (str): O ID único da sessão de urna atual.

        Returns:
            None
    """

    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(Fore.GREEN + Style.BRIGHT +
                  f"\n[{sem_milisegundos}] [SESSAO: {sessao_id}] Voto Computado!")

def ocorrencia_voto_duplo(sessao_id):
    """
        Cria o arquivo que armazena os logs de voto duplo e insere os logs nele.

        Args:
            sessao_id (str): O ID único da sessão de urna atual.

        Returns:
            None
    """

    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(Fore.RED + Style.BRIGHT +
                  f"\n[{sem_milisegundos}] [SESSAO: {sessao_id}] ALERTA: Tentativa de Voto Duplo")

def imprimir_ocorrencias_gerais():
    """
        Faz a leitura do arquivo de ocorrências gerais e as imprime.
        Para separar por sessão, seria necessário implementar lógica de parsing aqui.

        Args:
            None

        Returns:
            None
    """
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:
            logs_por_sessao = {}
            for linha in arq:
                if "[SESSAO:" in linha:
                    # Extrai o ID da sessão
                    start = linha.find("[SESSAO:") + len("[SESSAO:")
                    end = linha.find("]", start)
                    session_id = linha[start:end].strip()
                    
                    if session_id not in logs_por_sessao:
                        logs_por_sessao[session_id] = []
                    logs_por_sessao[session_id].append(linha.strip())
                else:
                    # Logs sem ID de sessão (ou logs antes da implementação)
                    if "SEM_SESSAO" not in logs_por_sessao:
                        logs_por_sessao["SEM_SESSAO"] = []
                    logs_por_sessao["SEM_SESSAO"].append(linha.strip())
            
            for sessao, logs in logs_por_sessao.items():
                print(f"\n--- Ocorrências da Sessão: {sessao} ---")
                for log in logs:
                    print(log)
            confirmacao.confirmacao()
    except FileNotFoundError:
        print(Fore.YELLOW + Style.BRIGHT +
              "\nNenhum Log de Ocorrência Registrado")
        confirmacao.confirmacao()
    except Exception as e:
        print(Fore.RED + Style.BRIGHT +
              f"\nErro ao ler o log de Ocorrência {e}")
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