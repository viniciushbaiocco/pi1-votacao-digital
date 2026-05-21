from Validadores import gerenciador_de_entrada as ge
from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validar_nome():
    nome_validado = False
    while not nome_validado:

        nome = ge.input_cancelavel("Digite o nome completo", "NOME")
        if nome is None:
            return None

        nome_ajustado = nome.split()

        letras_validas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áàãâéêíóôõúüçÁÀÃÂÉÊÍÓÔÕÚÜÇ-'"

        nome_letras = False
        for i in nome:
            if i in letras_validas:
                nome_letras = True
            else:
                nome_letras = False

        if nome_letras == False:
            console.print("O nome não pode ser espaço vazio e deve conter apenas letras!", style="bold yellow")
            sleep(1.5)
            limpar_tela()
        else:
            if len(nome_ajustado) < 2:
                nome_validado = False
                console.print("Nome inválido! Necessário nome completo (nome e sobrenome).", style="bold red")
                sleep(1.5)
                limpar_tela()
            else:

                if len(nome_ajustado[0]) < 2:
                    nome_validado = False
                    console.print("Nome inválido! Primeiro nome precisa ter mínimo de 3 letras.", style="bold red")
                    sleep(1.5)
                    limpar_tela()
                else:
                    if len(nome_ajustado[1]) < 1:
                        nome_validado = False
                        console.print("Sobrenome inválido! Sobrenome precisa ter mínimo de 2 letras.", style="bold red")
                        sleep(1.5)
                        limpar_tela()
                    else:
                        nome_validado = True

    return nome
