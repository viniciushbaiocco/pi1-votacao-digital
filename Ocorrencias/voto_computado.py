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
    Cria ou atualiza o log em disco para registrar que um voto foi computado com sucesso.

    A função abre o arquivo especificado em modo de anexo (append), captura o carimbo
    de data e hora atual do sistema (removendo os microssegundos) e grava uma nova entrada
    para registrar que um eleitor concluiu o processo de voto na sessão eleitoral ativa.

    Args:
        id_sessao (str ou int): O identificador exclusivo da sessão de urna ativa onde
        o voto foi registrado.

    Returns:
        None: A função realiza exclusivamente escritas físicas em arquivos de log em disco.
    """
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milisegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milisegundos}] Voto Computado!")


def imprimir_voto_computado():
    """
    Lê o arquivo de log e exibe o histórico de todos os votos computados no terminal.

    A função abre o arquivo para leitura física contínua. Caso existam registros salvos,
    o conteúdo é renderizado no console utilizando a flag `markup=False` no `console.print`,
    evitando que as marcações estruturais com colchetes de tempo sejam interpretadas pelo Rich.

    Erros de arquivos não encontrados (FileNotFoundError) ou violações gerais de I/O são
    tratados localmente por blocos de exceção genéricos, emitindo alertas amigáveis na
    tela. Todas as saídas de fluxo forçam uma pausa exigindo confirmação de leitura.

    Args:
        None.

    Returns:
        None: A função manipula fluxos de leitura e saídas visuais no terminal.
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
    Remove permanentemente do disco o arquivo físico de log contendo os votos computados.

    Executa de forma preventiva uma validação de existência de diretório via `os.path.exists`
    para garantir que o comando de deleção física não cause interrupções por arquivos ausentes.

    Args:
        None.

    Returns:
        None: A função executa unicamente a remoção física do arquivo em disco.
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
