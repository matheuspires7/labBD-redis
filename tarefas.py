from database import r


def criar_tarefa(titulo, descricao, prioridade):
    tarefa_id = r.incr("tarefa:proximo_id")

    r.hset(f"tarefa:{tarefa_id}", mapping={
        "id": tarefa_id,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": "pendente",
    })

    # Redis não busca por campo, então mantenho os índices manualmente
    r.zadd("tarefas:por_prioridade", {tarefa_id: prioridade})
    r.sadd("tarefas:pendente", tarefa_id)

    return tarefa_id


def buscar_tarefa(tarefa_id):
    return r.hgetall(f"tarefa:{tarefa_id}")


def listar_tarefas():
    ids = r.zrevrange("tarefas:por_prioridade", 0, -1)
    return [buscar_tarefa(tarefa_id) for tarefa_id in ids]


def listar_por_status(status):
    ids = r.smembers(f"tarefas:{status}")
    return [buscar_tarefa(tarefa_id) for tarefa_id in sorted(ids, key=int)]


def alternar_status(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)
    if not tarefa:
        return None

    atual = tarefa["status"]
    novo = "concluida" if atual == "pendente" else "pendente"

    r.hset(f"tarefa:{tarefa_id}", "status", novo)
    r.smove(f"tarefas:{atual}", f"tarefas:{novo}", tarefa_id)

    return novo


def editar_tarefa(tarefa_id, titulo, descricao, prioridade):
    if not buscar_tarefa(tarefa_id):
        return False

    r.hset(f"tarefa:{tarefa_id}", mapping={
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
    })
    r.zadd("tarefas:por_prioridade", {tarefa_id: prioridade})

    return True


def remover_tarefa(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)
    if not tarefa:
        return False

    r.delete(f"tarefa:{tarefa_id}")
    r.zrem("tarefas:por_prioridade", tarefa_id)
    r.srem(f"tarefas:{tarefa['status']}", tarefa_id)

    return True
