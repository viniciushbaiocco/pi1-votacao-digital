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
    """
    Cria ou atualiza o log de ocorrência para tentativas falhas de validação de mesários.

    A função abre o arquivo de log especificado em modo de anexação (append), captura
    o carimbo de data e hora corrente do sistema (com resolução de segundos, limpando
    os microssegundos) e grava uma nova linha de registro identificando um alerta de
    falha de validação/autenticação para a sessão eleitoral fornecida.

    Args:
        id_sessao (str ou int): O identificador exclusivo da sessão de urna ativa
            onde a falha de autenticação ocorreu.

    Returns:
        None: A função realiza exclusivamente escritas físicas em arquivos de log em disco.
    """
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] ALERTA: Validação do mesário negado")


def imprimir_ocorrencia_acesso_negado():
    """
    Lê o arquivo de log e exibe todas as ocorrências de acesso negado no terminal.

    A rotina tenta abrir o arquivo mapeado para leitura de fluxo contínuo. Caso existam
    registros salvos, renderiza o texto bruto no terminal. A flag `markup=False` assegura
    que as marcações cronológicas estruturadas com colchetes não sofram parsing do
    interpretador de tags do Rich.

    Exceções de arquivo inexistente (FileNotFoundError) ou violações de IO/permissões
    são devidamente capturadas de modo a exibir avisos coloridos na tela sem interromper
    o script principal. Ambas as saídas pausam o terminal exigindo interação de confirmação.

    Args:
        None.

    Returns:
        None: A função atua apenas na leitura de arquivos locais e saídas visuais na CLI.
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
    Remove permanentemente o arquivo físico de log de acessos negados armazenado em disco.

    Realiza uma checagem condicional prévia via módulo `os.path` para validar se o
    recurso referenciado por `CAMINHO_ARQUIVO` reside no diretório especificado,
    prevenindo que o interpretador dispare interrupções de IO não tratadas.

    Args:
        None.

    Returns:
        None: A função executa unicamente a remoção física do arquivo em disco.
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
