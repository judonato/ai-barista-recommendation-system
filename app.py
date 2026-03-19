from src.barista_ai import ask_barista

print("☕ Seu Barista virtual está pronto! Digite 'sair' para encerrar.\n")

while True:

    question = input("CLIENTE: ")

    if question.lower() == "sair":
        break

    answer = ask_barista(question)

    print("\nBARISTA VIRTUAL:", answer, "\n")

