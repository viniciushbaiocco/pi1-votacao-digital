from Verificadores import verificacao_chave_acesso_banco
from Validadores import validacao_chave_acesso, confirmacao
from Validadores import gerenciador_de_entrada as ge
from database import conexao_banco
from Votacao import autenticacao_mesario
from criptografia import criptografia as cripto
from Ocorrencias import encerramento_urna, geral
from rich.console import Console
from Visual.visual import limpar_tela

console = Console(highlight=False)

def encerrar_sistema_votacao(id_sessao):
    """
    Realiza o encerramento oficial do sistema de votação.

    Args:
        id_sessao (int): O ID único da sessão de urna que está sendo encerrada.

    Returns:
        bool: True se o encerramento for realizado com sucesso, False caso contrário.
    """

    limpar_tela()

    if not autenticacao_mesario.autenticar_mesario(id_sessao):
        return False

    conexao = conexao_banco.conexao_banco()

    try:

        cursor = conexao.cursor()

        resposta = ge.obter_entrada_inteira_valida("\nDeseja realmente encerrar a votação? \n[1] - Sim \n[X] - Não \nDigite uma opção: ", 1, 1)

        if not resposta:
            console.print("\nEncerramento cancelado.", style="bold yellow")
            confirmacao.confirmacao()
            return False

        confirmacao_chave = input("\nConfirme sua chave de acesso pessoal: ")

        if not validacao_chave_acesso.validar_chave_acesso(confirmacao_chave):
            console.print("\nEncerramento cancelado.", style="bold yellow")
            confirmacao.confirmacao()
            return False

        confirmacao_chave_criptografada = cripto.criptografar_chave_acesso(confirmacao_chave)

        if verificacao_chave_acesso_banco.verificar_chave_acesso_banco(confirmacao_chave_criptografada) == (0,):
            console.print("\nChave de acesso não confere. Encerramento cancelado.", style="bold yellow")
            confirmacao.confirmacao()
            return False

        console.print("\nSistema de votação encerrado.", style="bold green")

        encerramento_urna.ocorrencia_encerramento_urna(id_sessao)
        geral.ocorrencia_encerramento_urna(id_sessao)
        confirmacao.confirmacao()

        return True

    except:
        console.print("\nErro ao registrar encerramento.", style="bold red")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if conexao:
            cursor.close()
            conexao.close()
