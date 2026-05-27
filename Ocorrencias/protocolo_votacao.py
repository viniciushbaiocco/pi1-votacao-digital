from rich.console import Console
from Ocorrencias.registro import registrar_ocorrencia
from Validadores import confirmacao
import os

console = Console(highlight=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)
CAMINHO_ARQUIVO = os.path.join(PASTA_ARMAZENAMENTO, "Protocolo_Votacao.txt")


def ocorrencia_protocolo_votacao(id_sessao):
    """
    Cria ou atualiza o log de ocorrência para protocolo de votação.

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
    registrar_ocorrencia(CAMINHO_ARQUIVO, id_sessao, "Protocolo de Votação Gerado")


def imprimir_ocorrencia_protocolo_votacao():
    """
    Lê o arquivo de log e exibe todas as ocorrências de protocolo de votação no terminal.

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
        console.print("\nNenhum Log de Protocolo de Votação Registrado", style="bold yellow")
        confirmacao.confirmacao()
    except Exception as e:
        console.print(f"\nErro ao ler o log de Protocolo de Votação {e}", style="bold red")
        confirmacao.confirmacao()


def excluir_ocorrencia_protocolo_votacao():
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