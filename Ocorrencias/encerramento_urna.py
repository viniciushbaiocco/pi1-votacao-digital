from rich.console import Console
from datetime import datetime
from Validadores import confirmacao
import os

console = Console(highlight=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)
CAMINHO_ARQUIVO = os.path.join(PASTA_ARMAZENAMENTO, "Encerramento_Urna.txt")


def ocorrencia_encerramento_urna(id_sessao):
    """
    Cria ou atualiza o log de ocorrência para o encerramento da sessão de votação da urna.

    A função abre o arquivo físico em modo de anexo (append), captura o carimbo de data
    e hora atual do sistema (truncando os microssegundos para manter a conformidade visual)
    e insere uma nova linha registrando a conclusão definitiva das atividades de votação
    para a sessão eleitoral informada.

    Args:
        id_sessao (str ou int): O identificador exclusivo da sessão de urna ativa que
            está sendo encerrada.

    Returns:
        None: A função realiza exclusivamente escritas físicas em arquivos de log em disco.
    """
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as arq:
        agora = datetime.now()
        sem_milissegundos = agora.replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milissegundos}] ENCERRAMENTO: Votação encerrada. Total de votos registrados.")


def imprimir_ocorrencia_encerramento_urna():
    """
    Lê o arquivo de log e exibe todas as ocorrências de encerramento de urna no terminal.

    A função tenta abrir o arquivo mapeado para leitura. Se houver registros gravados,
    o texto bruto é impresso no terminal utilizando a flag `markup=False` no `console.print`,
    o que impede o interpretador do Rich de processar erroneamente os colchetes dos metadados
    cronológicos do log.

    Erros decorrentes de arquivos não encontrados (FileNotFoundError) ou falhas gerais de
    I/O são tratados localmente por blocos de exceção específicos, exibindo avisos
    coloridos sem derrubar o script principal. Ambas as rotas pausam a tela aguardando
    confirmação de leitura do usuário.

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
        console.print("\nNenhum Log de Encerramento de Urna Registrado", style="bold yellow")
        confirmacao.confirmacao()
    except Exception as e:
        console.print(f"\nErro ao ler o log de Encerramento de Urna {e}", style="bold red")
        confirmacao.confirmacao()


def excluir_ocorrencia_encerramento_urna():
    """
    Remove permanentemente o arquivo físico de log de encerramento de urna armazenado em disco.

    A rotina executa uma validação preventiva utilizando `os.path.exists` antes de invocar
    a deleção real do recurso pelo sistema operacional, mitigando possíveis interrupções
    de fluxo por erros de I/O de arquivo inexistente.

    Args:
        None.

    Returns:
        None: A função executa unicamente a remoção física do arquivo em disco.
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
