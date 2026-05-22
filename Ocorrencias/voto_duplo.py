import os
from datetime import datetime
from rich.console import Console
from Validadores import confirmacao

console = Console(highlight=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)
CAMINHO_ARQUIVO = os.path.join(PASTA_ARMAZENAMENTO, "Voto_Duplo.txt")


def ocorrencia_voto_duplo(id_sessao: str):
    """
    Cria ou atualiza o log em disco para registrar tentativas ilegais de voto duplo.

    A função abre o arquivo de logs especificado em modo de anexo (append), captura
    o carimbo de data e hora atual do sistema (removendo os microssegundos) e grava
    uma nova entrada de alerta crítico sempre que um eleitor já autenticado tentar
    votar novamente na sessão eleitoral ativa.

    Args:
        id_sessao (str): O identificador exclusivo da sessão de urna ativa onde
            a tentativa de fraude foi detectada.

    Returns:
        None: A função realiza exclusivamente escritas físicas em arquivos de log em disco.
    """
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milissegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milissegundos}] ALERTA: Tentativa de Voto Duplo")


def imprimir_voto_duplo():
    """
    Lê o arquivo de log e exibe todos os alertas de voto duplo registrados no terminal.

    A função tenta abrir o arquivo mapeado para leitura de fluxo contínuo. Se houver
    registros salvos, o conteúdo textual é impresso no console. A flag `markup=False`
    no `console.print` impede que os colchetes dos metadados de tempo sejam
    processados como formatação visual do Rich.

    Erros de arquivos não encontrados (FileNotFoundError) ou falhas gerais de leitura
    são tratados por blocos de exceção dedicados para emitir avisos claros ao usuário.
    Todas as saídas forçam uma pausa na tela aguardando confirmação.

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
        console.print("\nNenhum Log de Voto Duplo Registrado", style="bold yellow")
        confirmacao.confirmacao()
    except Exception as e:
        console.print(f"\nErro ao ler o log de Voto Duplo {e}", style="bold red")
        confirmacao.confirmacao()


def excluir_arquivo_voto_duplo():
    """
    Remove permanentemente do disco o arquivo físico contendo os logs de voto duplo.

    A rotina realiza uma validação de existência preventiva via `os.path.exists` para
    evitar falhas ou interrupções abruptas no script caso o arquivo mapeado em
    `CAMINHO_ARQUIVO` já tenha sido deletado ou não tenha sido criado.

    Args:
        None.

    Returns:
        None: A função executa unicamente a remoção física do arquivo em disco.
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
