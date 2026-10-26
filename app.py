import redis

from database import r
from tarefas import (
    criar_tarefa,
    listar_tarefas,
    listar_por_status,
    alternar_status,
    editar_tarefa,
    remover_tarefa,
)


def mostrar(t):
    marca = "x" if t["status"] == "concluida" else " "
    print(f"[{marca}] #{t['id']} {t['titulo']} (prioridade {t['prioridade']})")


def menu():
    while True:
        print("\n=== Tarefas (Redis) ===")
        print("1 - Criar tarefa")
        print("2 - Listar tarefas")
        print("3 - Listar por status")
        print("4 - Concluir / reabrir tarefa")
        print("5 - Editar tarefa")
        print("6 - Remover tarefa")
        print("0 - Sair")

        opcao = input("> ").strip()

        if opcao == "1":
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            prioridade = int(input("Prioridade (1 a 5): "))
            tarefa_id = criar_tarefa(titulo, descricao, prioridade)
            print(f"Tarefa #{tarefa_id} criada!")

        elif opcao == "2":
            for t in listar_tarefas():
                mostrar(t)

        elif opcao == "3":
            status = input("Status (pendente/concluida): ").strip()
            for t in listar_por_status(status):
                mostrar(t)

        elif opcao == "4":
            tarefa_id = input("ID: ").strip()
            novo = alternar_status(tarefa_id)
            print(f"Agora está {novo}." if novo else "Tarefa não encontrada.")

        elif opcao == "5":
            tarefa_id = input("ID: ").strip()
            titulo = input("Novo título: ")
            descricao = input("Nova descrição: ")
            prioridade = int(input("Nova prioridade (1 a 5): "))
            ok = editar_tarefa(tarefa_id, titulo, descricao, prioridade)
            print("Tarefa atualizada!" if ok else "Tarefa não encontrada.")

        elif opcao == "6":
            tarefa_id = input("ID: ").strip()
            ok = remover_tarefa(tarefa_id)
            print("Tarefa removida!" if ok else "Tarefa não encontrada.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


try:
    r.ping()
except (redis.ConnectionError, redis.TimeoutError):
    print("Não foi possível conectar ao Redis. Rode: docker compose up -d")
else:
    menu()
