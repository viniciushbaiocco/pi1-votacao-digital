from Validadores import gerenciador_de_entrada as ge
from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validar_nome():
    """
    Realiza a captura e validação sintática do nome completo para cadastro.

    A função executa um loop de persistência no terminal para garantir que a string
    informada atenda aos critérios rígidos de validação eleitoral:

    1. Permite o cancelamento voluntário do fluxo via `ge.input_cancelavel`.
    2. Avalia caractere por caractere se o texto contém apenas letras (incluindo
        caracteres acentuados da língua portuguesa, hífens e apóstrofos), barrando
        números ou símbolos especiais.
    3. Exige a presença de pelo menos dois termos (nome e sobrenome) utilizando
        o .split().
    4. Valida limites de tamanho mínimos para o primeiro nome e o sobrenome sequencial.

    Se alguma das regras falhar, o sistema exibe um alerta colorido correspondente no
    console via Rich, pausa a execução por 1.5 segundos, limpa o terminal e solicita
    o dado novamente.

    Returns:
        str ou None: Retorna a string do nome validado caso o preenchimento atenda
        a todas as diretrizes de formato; retorna `None` se o usuário optar por
        cancelar o fluxo digitando 'X'.
    """
    nome_validado = False
    while not nome_validado:

        nome = ge.input_cancelavel("Digite o nome completo", "NOME")
        if nome is None:
            return None

        nome_ajustado = nome.split()

        letras_validas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áàãâéêíóôõúüçÁÀÃÂÉÊÍÓÔÕÚÜÇ-'"

        nome_letras = True
        for i in nome:
            if i not in letras_validas:
                nome_letras = False
                break

        if not nome_letras:
            console.print("\nO nome não pode ser espaço vazio e deve conter apenas letras!", style="bold yellow")
            sleep(1.5)
            limpar_tela()
        else:
            if len(nome_ajustado) < 2:
                nome_validado = False
                console.print("\nNome inválido! Necessário nome completo (nome e sobrenome).", style="bold red")
                sleep(1.5)
                limpar_tela()
            else:

                if len(nome_ajustado[0]) < 2:
                    nome_validado = False
                    console.print("\nNome inválido! Primeiro nome precisa ter no mínimo 2 letras.", style="bold red")
                    sleep(1.5)
                    limpar_tela()
                else:
                    if len(nome_ajustado[1]) < 1:
                        nome_validado = False
                        console.print("\nSobrenome inválido! Sobrenome precisa ter no mínimo 1 letra.", style="bold red")
                        sleep(1.5)
                        limpar_tela()
                    else:
                        nome_validado = True

    return nome
