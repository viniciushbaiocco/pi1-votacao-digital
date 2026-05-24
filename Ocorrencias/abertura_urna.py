from rich.console import Console
from Ocorrencias.registro import registrar_ocorrencia
from Validadores import confirmacao
import os

console = Console(highlight=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)
CAMINHO_ARQUIVO = os.path.join(PASTA_ARMAZENAMENTO, "Abertura_Urna.txt")


def ocorrencia_abertura_urna(id_sessao):
    """
    Cria ou atualiza o log de ocorrência para a abertura de urna após a emissão da Zerésima.

    A função abre o arquivo de logs configurado em modo de anexo (append), captura
    o carimbo de data e hora atual do sistema (removendo os microssegundos para manter
    a padronização visual dos logs) e insere uma linha registrando o início bem-sucedido
    da votação para a sessão eleitoral informada.

    Args:
        id_sessao (int ou str): O identificador numérico da sessão eleitoral correspondente
            à abertura do ciclo de votação.

    Returns:
        None: A função realiza apenas escrita em arquivo físico (I/O), sem retornar valor.
    """
    registrar_ocorrencia(CAMINHO_ARQUIVO, id_sessao, "ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")


def imprimir_ocorrencia_abertura_urna():
    """
    Lê e imprime o conteúdo completo do log de abertura de urna no terminal.

    A função tenta abrir o arquivo físico em modo de leitura. Se o arquivo existir,
    seu conteúdo textual é exibido de forma bruta no console. O parâmetro `markup=False`
    é utilizado no `console.print` para evitar que colchetes presentes nos logs (como
    `[SESSÃO: X]`) sejam interpretados acidentalmente como tags de estilização do Rich.

    Se o arquivo ainda não tiver sido gerado, ou se ocorrer um erro inesperado de
    leitura/permissão, mensagens amigáveis de aviso são exibidas. Em todos os cenários,
    a rotina aguarda a confirmação do usuário antes de liberar a tela.

    Args:
        None.

    Returns:
        None: A função lida apenas com leitura de arquivos e saída em terminal.
    """
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            console.print(conteudo, markup=False)
            confirmacao.confirmacao()
    except FileNotFoundError:
        console.print("\nNenhum Log de Abertura de Urna Registrado", style="bold yellow")
        confirmacao.confirmacao()
    except Exception as e:
        console.print(f"\nErro ao ler o log de Abertura de Urna {e}", style="bold red")
        confirmacao.confirmacao()


def excluir_ocorrencia_abertura_urna():
    """
    Exclui permanentemente o arquivo de log de ocorrência de abertura de urna do disco.

    A função verifica de forma preventiva se o arquivo mapeado em `CAMINHO_ARQUIVO`
    realmente existe no diretório do sistema operacional antes de invocar o comando
    de remoção, evitando falhas ou exceções de IO em tempo de execução.

    Args:
        None.

    Returns:
        None: A função realiza apenas a deleção do arquivo físico em disco.
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
