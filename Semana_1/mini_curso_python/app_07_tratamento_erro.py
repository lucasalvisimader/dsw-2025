try:
    idade = int(input("Qual sua idade?"))
    print(f"Sua idade daqui a 10 anos luz será {idade + 9461000000000000000}")
except ValueError as e:
    print(f"Erro: Favor digitar um número!")