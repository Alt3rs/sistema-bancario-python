menu = """
=============== Menu =============== 
[d] - Depositar
[s] - Sacar
[e] - Extrato
[q] - Sair
====================================
"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor a ser depositado: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Falha! Valor para depósito incorreto.") 
    
    elif opcao == "s":
        valor = float(input("Informe o valor a ser sacado: "))

        if valor > saldo:
            print("Falha! Saldo insuficiente.")

        elif valor > limite:
            print("Falha! Valor excede o limite de saque")

        elif numero_saques >= LIMITE_SAQUES:
            print("Falha! Número de saques excedidos.")
        
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        
        else:
            print("Falha! Valor informado incorreto.")
    
    elif opcao == "e":
        print("======================== Extrato ======================== ")
        
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("========================================================= ")

    elif opcao == "q":
        break

    else: 
        print("Operação inválida, por favor selecione novamente a operação desejada.")