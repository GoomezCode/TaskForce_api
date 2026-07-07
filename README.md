<h1 align="center"> 📝 TaskForce API</h1>

<p align="center"> API RESTful simples para gerenciamento de tarefas (to-do list), construída com <b>FastAPI</b> e persistência de dados em arquivo <b>JSON</b>. </p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/FastAPI-0.139.0-009688?logo=fastapi&logoColor=white">
    <img src="https://img.shields.io/badge/Uvicorn-0.50.2-informational">
    <img src="https://img.shields.io/badge/license-MIT-green">
</p>

---

## 📌 Sobre o projeto

O **TaskForce API** é uma API desenvolvida para praticar os conceitos de **FastAPI**, oferecendo operações básicas de um CRUD de tarefas:

- Criar tarefas
- Listar tarefas
- Marcar/desmarcar tarefas como concluídas
- Deletar tarefas

Os dados são armazenados localmente em um arquivo `task.json`, sem a necessidade de configurar um banco de dados externo — ideal para estudo e testes rápidos.

---

## 🚀 Tecnologias utilizadas

- [Python 3](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) — framework web para construção da API
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- Armazenamento em **JSON** (sem banco de dados)

---

## 📂 Estrutura do projeto

```
TaskForce_api/
├── api/
│   └── apiTask.py        # Rotas/endpoints da API
├── classes/
│   └── Classes.py        # Modelo (schema) da tarefa (Pydantic)
├── util/
│   └── jsonFile.py        # Lógica de leitura/escrita no arquivo JSON
├── main.py                 # Ponto de entrada da aplicação
├── requeriments.txt        # Dependências do projeto
└── README.md
```

---

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/GoomezCode/TaskForce_api.git
cd TaskForce_api
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requeriments.txt
```

### 4. Execute a aplicação

```bash
python main.py
```

A API estará disponível em:

```
http://localhost:8000
```

A documentação interativa (Swagger UI) gerada automaticamente pelo FastAPI pode ser acessada em:

```
http://localhost:8000/docs
```

---

## 📖 Endpoints da API

| Método   | Rota                        | Descrição                                    |
|----------|-----------------------------|-----------------------------------------------|
| `GET`    | `/task/get`                 | Lista todas as tarefas cadastradas            |
| `POST`   | `/task/create/{task}`       | Cria uma nova tarefa                          |
| `PUT`    | `/task/put/marcar/{idTask}` | Marca/desmarca uma tarefa como concluída      |
| `DELETE` | `/task/delete/{idTask}`     | Remove uma tarefa pelo ID                     |

### Exemplo — Criar uma tarefa

```http
POST /task/create/Estudar%20FastAPI
```

### Exemplo — Listar tarefas

```http
GET /task/get
```

**Resposta:**
```json
[
    {
        "id": 1,
        "tarefa": "Estudar FastAPI",
        "feito": false,
        "data": "06/07/26",
        "hora": "14:32:10"
    }
]
```

### Exemplo — Marcar tarefa como concluída

```http
PUT /task/put/marcar/1
```

### Exemplo — Deletar tarefa

```http
DELETE /task/delete/1
```

---

## 💾 Persistência dos dados

As tarefas são salvas automaticamente no arquivo `pathJson/task.json`, criado na primeira execução da API. Não é necessário configurar nenhum banco de dados.

---

## 🛠️ Melhorias futuras

- [ ] Migrar a persistência de dados para um banco de dados relacional (ex: SQLite/PostgreSQL)
- [ ] Adicionar autenticação de usuários
- [ ] Adicionar testes automatizados
- [ ] Adicionar suporte a edição do texto da tarefa
- [ ] Tratar melhor os erros de validação de entrada

---

## 👤 Autor

Desenvolvido por [**GoomezCode**](https://github.com/GoomezCode).
