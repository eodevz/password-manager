import csv
import os
from collections import defaultdict
from InquirerPy import inquirer

ARQUIVO = "senhas.csv"

os.system("cls" if os.name == "nt" else "clear")
if not os.path.exists(ARQUIVO):
    print("Você deve ter um arquivo chamado senhas.csv! Talvez alguém tenha deletado ele...")
    print("Mas, em compensação, o programa criará automaticamente um novo arquivo.")
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["App", "Username", "Senha"])


def carregar_dados():
    dados = defaultdict(list)
    with open(ARQUIVO, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dados[row["App"]].append({
                "Username": row["Username"],
                "Senha": row["Senha"]
            })
    return dados


def salvar_dados(dados):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["App", "Username", "Senha"])
        for app, contas in dados.items():
            for conta in contas:
                writer.writerow([app, conta["Username"], conta["Senha"]])


def ver_senhas():
    dados = carregar_dados()
    if not dados:
        print("\n⚠ Não há nenhuma senha cadastrada.\n")
        return

    app = inquirer.select(
        message="Qual senha você quer receber?",
        choices=list(dados.keys())
    ).execute()

    contas = dados[app]

    username = inquirer.select(
        message=f"Qual conta do {app}?",
        choices=[c["Username"] for c in contas]
    ).execute()

    for conta in contas:
        if conta["Username"] == username:
            print("\n📌 Resultado:")
            print(f"App: {app}")
            print(f"Usuário: {conta['Username']}")
            print(f"Senha: {conta['Senha']}\n")
            break


def adicionar_senha():
    dados = carregar_dados()

    app = inquirer.text(message="Nome do App:").execute()
    username = inquirer.text(message="Username:").execute()
    senha = inquirer.secret(message="Senha:").execute()

    dados[app].append({
        "Username": username,
        "Senha": senha
    })

    salvar_dados(dados)
    print("\n✅ Senha adicionada com sucesso!\n")


def remover_senha():
    dados = carregar_dados()
    if not dados:
        print("\n⚠ Nenhuma senha cadastrada.\n")
        return

    app = inquirer.select(
        message="De qual App deseja remover?",
        choices=list(dados.keys())
    ).execute()

    contas = dados[app]

    username = inquirer.select(
        message="Qual conta deseja remover?",
        choices=[c["Username"] for c in contas]
    ).execute()

    dados[app] = [c for c in contas if c["Username"] != username]

    if not dados[app]:
        del dados[app]

    salvar_dados(dados)
    print("\n❌ Conta removida com sucesso!\n")


def menu():
    while True:
        escolha = inquirer.select(
            message="🔐 Password Manager",
            choices=[
                "Ver senhas",
                "Adicionar senha",
                "Remover senha",
                "Sair"
            ]
        ).execute()

        if escolha == "Ver senhas":
            ver_senhas()
        elif escolha == "Adicionar senha":
            adicionar_senha()
        elif escolha == "Remover senha":
            remover_senha()
        elif escolha == "Sair":
            print("\n👋 Encerrando...")
            break


if __name__ == "__main__":
    menu()
