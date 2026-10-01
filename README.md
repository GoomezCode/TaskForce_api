<h1 align="center"> 📝 TaskForce API</h1>

<p align="center"> API RESTful simples para gerenciamento de tarefas (to-do list), construída com <b>FastAPI</b> e persistência de dados em arquivo <b>JSON</b>. </p>

---

## 📌 Sobre o projeto

O **TaskForce API** oferece um CRUD de tarefas:

- Criar tarefas
- Listar tarefas com busca, filtro e paginação
- Marcar/desmarcar tarefas como concluídas
- Editar o texto da tarefa
- Deletar tarefas

Os dados são armazenados localmente em `storage/tasks.json`, sem banco externo.

---

## 🚀 Tecnologias utilizadas

- [Python 3](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://docs.pydantic.dev/)
- Armazenamento em **JSON** (sem banco de dados)

---

## 📂 Estrutura do projeto

```
TaskForce_api/
├── app/
│   ├── main.py                 # Factory + app FastAPI (uvicorn app.main:app)
│   ├── core/
│   │   ├── config.py           # Settings via .env (TASKFORCE_*)
│   │   └── exceptions.py       # Erros 404/409 + handlers
│   ├── api/
│   │   ├── dependencies.py     # Injeção do TaskService
│   │   └── v1/routes/
│   │       └── tasks.py        # Rotas /api/v1/tasks
│   ├── schemas/
│   │   └── task.py             # TaskCreate/TaskUpdate/Task/TaskList
│   ├── services/
│   │   └── task_service.py     # Regra de negócio
│   └── repositories/
│       └── json_task_repository.py # Persistência JSON atômica
├── storage/                    # tasks.json (ignorado pelo git)
├── tests/                      # pytest + TestClient
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Como executar o projeto

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API em `http://localhost:8000` e docs em `http://localhost:8000/docs`.

Variáveis opcionais (ver `.env.example`):

```
TASKFORCE_STORAGE_PATH=storage/tasks.json
TASKFORCE_CORS_ORIGINS=http://localhost:3000
```

---

## 📖 Endpoints da API

| Método   | Rota                          | Descrição                              |
|----------|-------------------------------|----------------------------------------|
| `GET`    | `/api/v1/tasks`               | Lista com `search,is_done,page,size`   |
| `GET`    | `/api/v1/tasks/stats`         | Contadores total/done/pending          |
| `POST`   | `/api/v1/tasks`               | Cria (`{"title": "..."}`) → 201        |
| `GET`    | `/api/v1/tasks/{id}`          | Busca por ID                           |
| `PATCH`  | `/api/v1/tasks/{id}/done`     | Alterna concluída                      |
| `PATCH`  | `/api/v1/tasks/{id}`          | Edita `title` e/ou `done`              |
| `DELETE` | `/api/v1/tasks/{id}`          | Remove → 204                           |
| `GET`    | `/health`                     | Healthcheck                            |

Exemplos:

```bash
curl -X POST localhost:8000/api/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title": "Estudar FastAPI"}'

curl 'localhost:8000/api/v1/tasks?search=fastapi&page=1&size=10'
curl -X PATCH localhost:8000/api/v1/tasks/1/done
curl -X DELETE localhost:8000/api/v1/tasks/1 -i
```

---

## 💾 Persistência dos dados

Arquivo `storage/tasks.json` criado na primeira execução. Escritas atômicas (`.tmp` + replace) e backup `.bak` se o JSON corromper.

---

## ✅ Testes

```bash
pytest
```

---

## 👤 Autor

Desenvolvido por [**GoomezCode**](https://github.com/GoomezCode).
