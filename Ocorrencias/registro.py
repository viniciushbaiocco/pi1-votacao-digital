from datetime import datetime


def registrar_ocorrencia(caminho_arquivo, id_sessao, mensagem):
    """
    Anexa uma linha de log de auditoria ao arquivo informado, com data/hora padronizada.

    Centraliza a escrita de logs usada pelos módulos de ocorrências (o log unificado
    `geral.py` e os logs por tipo), garantindo o mesmo formato de carimbo de tempo
    (sem microssegundos) e o mesmo modo de anexação (append). Substitui a lógica que
    antes estava duplicada em cada função `ocorrencia_*`.

    Args:
        caminho_arquivo (str): Caminho absoluto do arquivo de log de destino.
        id_sessao (str ou int): Identificador da sessão de urna ativa.
        mensagem (str): Texto do evento a registrar (sem o prefixo de sessão/horário).

    Returns:
        None: A função realiza apenas escrita física em disco (I/O).
    """
    with open(caminho_arquivo, "a", encoding="utf-8") as arq:
        sem_milissegundos = datetime.now().replace(microsecond=0)
        arq.write(f"\n[SESSÃO: {id_sessao}] [{sem_milissegundos}] {mensagem}")
