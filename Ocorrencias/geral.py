from rich.console import Console
from Ocorrencias.registro import registrar_ocorrencia
from Validadores import confirmacao
import os

console = Console(highlight=False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ARMAZENAMENTO = os.path.join(BASE_DIR, "Armazenamento")
os.makedirs(PASTA_ARMAZENAMENTO, exist_ok=True)
CAMINHO_ARQUIVO = os.path.join(PASTA_ARMAZENAMENTO, "Geral.txt")


def ocorrencia_abertura_urna(id_sessao):
    """
    Cria ou atualiza o log de ocorrência para a abertura de urna após a Zerésima.

    A função abre o arquivo de logs configurado em modo de anexo (append), captura
    o carimbo de data e hora atual do sistema (removendo os microssegundos) e insere
    uma linha registrando o início oficial da votação para a sessão informada.

    Args:
        id_sessao (str ou int): O ID único ou número da sessão de urna atual.

    Returns:
        None: A função realiza apenas escrita em arquivo físico (I/O).
    """
    registrar_ocorrencia(CAMINHO_ARQUIVO, id_sessao, "ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")


def ocorrencia_acesso_negado(id_sessao):
    """
    Cria ou atualiza o log de ocorrência para tentativas falhas de validação de mesários.

    Grava um registro de alerta em modo anexo (append) indicando que uma validação
    ou credencial de mesário foi rejeitada pelo sistema na sessão eleitoral ativa.

    Args:
        id_sessao (str ou int): O ID único ou número da sessão de urna atual.

    Returns:
        None: A função realiza apenas escrita em arquivo físico (I/O).
    """
    registrar_ocorrencia(CAMINHO_ARQUIVO, id_sessao, "ALERTA: Validação do mesário negado")


def ocorrencia_encerramento_urna(id_sessao):
    """
    Cria ou atualiza o log de ocorrência para o encerramento das atividades da urna.

    Registra de forma persistente o encerramento do ciclo de votação de uma sessão específica,
    marcando o fechamento e consolidando o estado dos votos computados.

    Args:
        id_sessao (str ou int): O ID único ou número da sessão de urna atual.

    Returns:
        None: A função realiza apenas escrita em arquivo físico (I/O).
    """
    registrar_ocorrencia(CAMINHO_ARQUIVO, id_sessao, "ENCERRAMENTO: Votação encerrada. Total de votos registrados.")


def ocorrencia_voto_computado(id_sessao):
    """
    Cria ou atualiza o log em disco para registrar que um voto foi armazenado com sucesso.

    Insere uma entrada cronológica indicando a computação bem-sucedida de um voto regular
    dentro da sessão eleitoral correspondente, mantendo o anonimato do eleitor.

    Args:
        id_sessao (str ou int): O ID único ou número da sessão de urna atual.

    Returns:
        None: A função realiza apenas escrita em arquivo físico (I/O).
    """
    registrar_ocorrencia(CAMINHO_ARQUIVO, id_sessao, "Voto Computado!")


def ocorrencia_voto_duplo(id_sessao):
    """
    Registra uma ocorrência de alerta crítico para uma tentativa de voto duplo.

    Esta função atua diretamente no log de auditoria de segurança da urna, salvando um
    aviso com data, hora e sessão sempre que um eleitor que já votou tentar realizar
    uma nova autenticação ou inserção de voto.

    Args:
        id_sessao (str ou int): O ID único ou número da sessão de urna atual.

    Returns:
        None: A função realiza apenas escrita em arquivo físico (I/O).
    """
    registrar_ocorrencia(CAMINHO_ARQUIVO, id_sessao, "ALERTA: Tentativa de Voto Duplo")

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


def imprimir_ocorrencias_por_sessao():
    """
    Lê o arquivo de logs e imprime em lote todas as ocorrências gravadas por sessão.

    A função abre o arquivo em formato de leitura e exibe  o histórico unificado de
    auditoria da urna. Utiliza `markup=False` na impressão do Rich para neutralizar
    os colchetes de estruturação dos metadados dos logs (ex: `[SESSÃO: X]`), assegurando a
    exibição das mensagens.

    Trata de forma segura cenários de arquivos inexistentes ou falhas de permissão de I/O
    exibindo alertas estilizados e pausando a tela para controle do terminal.

    Args:
        None.

    Returns:
        None: A função manipula fluxos de leitura e saídas no terminal.
    """
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            console.print(conteudo, markup=False)
        confirmacao.confirmacao()
    except FileNotFoundError:
        console.print("\nNenhum Log de Ocorrência Registrado", style="bold yellow")
        confirmacao.confirmacao()
    except Exception as e:
        console.print(f"\nErro ao ler o log de Ocorrência: {e}", style="bold red")
        confirmacao.confirmacao()


def excluir_arquivo_ocorrencias_gerais():
    """
    Remove permanentemente o arquivo de log de ocorrências gerais armazenado em disco.

    Efetua uma validação lógica de existência via módulo `os.path` antes de disparar o
    comando de exclusão física, blindando o ecossistema contra exceções de falta de recurso.

    Args:
        None.

    Returns:
        None: A função realiza unicamente a remoção do arquivo físico em disco.
    """
    if os.path.exists(CAMINHO_ARQUIVO):
        os.remove(CAMINHO_ARQUIVO)
