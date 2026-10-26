# Gerenciador de Tarefas com Redis

Trabalho substitutivo da P1 – Laboratório de Banco de Dados (NoSQL) – FATEC
Aluno: Matheus Di Sabatino Pires

Aplicação de linha de comando (CLI) em Python que faz o CRUD de tarefas usando o **Redis**, um banco de dados NoSQL do tipo **chave-valor** que armazena os dados em memória.

## Vídeo de apresentação

_(link do vídeo)_

## Por que Redis?

- No projeto API, meu grupo usa **PostgreSQL** (relacional) e **MongoDB** (NoSQL de documentos). Escolhi o Redis para estudar um modelo NoSQL diferente: o **chave-valor**.
- Ele guarda os dados em memória, então leituras e escritas são muito rápidas.
- Tem estruturas de dados prontas (Hash, Set, Sorted Set), que permitiram ordenar e filtrar as tarefas de forma simples.
- É muito usado no mercado, principalmente como cache, para sessões de login, rankings e contadores, geralmente junto com outro banco principal.

## Como os dados são guardados

O Redis não tem tabelas nem coleções, apenas chaves. Cada informação fica em uma chave:

| Chave | Tipo | Conteúdo |
|---|---|---|
| `tarefa:proximo_id` | String | Contador que gera os IDs das tarefas (`INCR`) |
| `tarefa:<id>` | Hash | Campos da tarefa: id, titulo, descricao, prioridade, status |
| `tarefas:por_prioridade` | Sorted Set | IDs das tarefas, ordenados pela prioridade |
| `tarefas:pendente` | Set | IDs das tarefas pendentes |
| `tarefas:concluida` | Set | IDs das tarefas concluídas |

Como o Redis não tem consultas do tipo `WHERE` ou `find()`, os Sets e o Sorted Set funcionam como **índices criados manualmente**: toda vez que uma tarefa é criada, editada ou removida, o código também atualiza esses índices.

## Estrutura do projeto

```
labBD-redis/
├── docker-compose.yml   # sobe o Redis e o RedisInsight
├── requirements.txt     # dependências do Python
├── .env.example         # modelo das configurações (host e porta do Redis)
├── database.py          # conexão com o Redis (lê as configurações do .env)
├── tarefas.py           # funções do CRUD (operações no banco)
└── app.py               # menu da aplicação
```

## Funcionalidades

1. Criar tarefa
2. Listar tarefas (ordenadas por prioridade)
3. Listar por status (pendente ou concluída)
4. Concluir / reabrir tarefa
5. Editar tarefa
6. Remover tarefa

## Como rodar

Requisitos: **Python 3** e **Docker Desktop**.

1. Subir o Redis:
   ```
   docker compose up -d
   ```
2. Criar e ativar o ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instalar as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Criar o arquivo de configuração a partir do modelo:
   ```
   copy .env.example .env
   ```
5. Rodar a aplicação:
   ```
   python app.py
   ```

Para visualizar o banco, acesse o **RedisInsight** em http://localhost:8001.

## Vantagens do Redis

- **Velocidade:** os dados ficam em memória, então as respostas são muito rápidas.
- **Estruturas de dados prontas:** o Sorted Set ordenou as tarefas por prioridade e os Sets separaram por status, sem código extra de ordenação.
- **Simplicidade:** o modelo chave-valor é fácil de entender.
- **Recursos extras:** permite expiração automática de chaves (TTL), muito útil para cache e sessões.

## Desvantagens do Redis

- **Sem consultas complexas:** não existe `WHERE` nem `JOIN`; foi preciso criar e manter os índices manualmente.
- **Consistência depende do código:** se o programa esquecer de atualizar um índice, os dados ficam desencontrados.
- **Memória:** todos os dados precisam caber na RAM, o que fica caro com grandes volumes.
- **Persistência limitada:** o Redis salva em disco de tempos em tempos, então pode perder os dados mais recentes se o servidor cair.
