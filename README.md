# Agenda Médica API

API para gerenciamento de agenda médica desenvolvida com FastAPI e SQLite.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
uvicorn main:app --reload
```

A API estará disponível em: http://localhost:8000

## Documentação da API

Acesse a documentação interativa em: http://localhost:8000/docs

## Endpoints

### Médicos

- `GET /medicos` - Listar todos os médicos
- `GET /medicos?nome={nome}` - Buscar médicos por nome (busca parcial)
- `GET /medicos/{id}` - Buscar médico por ID
- `POST /medicos` - Criar novo médico
- `PUT /medicos/{id}` - Atualizar médico
- `DELETE /medicos/{id}` - Deletar médico

### Exemplo de uso

#### Criar médico:
```bash
curl -X POST "http://localhost:8000/medicos/" \
     -H "Content-Type: application/json" \
     -d '{"nome": "Dr. João Silva", "especialidade": "Cardiologia"}'
```

#### Listar médicos:
```bash
curl -X GET "http://localhost:8000/medicos/"
```

#### Buscar médicos por nome:
```bash
curl -X GET "http://localhost:8000/medicos/?nome=João"
```

#### Buscar médico por ID:
```bash
curl -X GET "http://localhost:8000/medicos/1"
```

#### Atualizar médico:
```bash
curl -X PUT "http://localhost:8000/medicos/1" \
     -H "Content-Type: application/json" \
     -d '{"especialidade": "Cardiologia Intervencionista"}'
```

#### Deletar médico:
```bash
curl -X DELETE "http://localhost:8000/medicos/1"
```

## Teste da API

Execute o script de teste para verificar todos os endpoints:

```bash
python test_api.py
```

## Estrutura do Projeto

```
projeto_teste/
├── main.py              # Aplicação FastAPI principal
├── app/
│   ├── __init__.py
│   ├── database.py      # Configuração do banco SQLite
│   ├── schemas.py       # Schemas Pydantic
│   ├── crud.py          # Operações CRUD
│   └── routers/
│       ├── __init__.py
│       └── medicos.py   # Endpoints de médicos
├── test_api.py          # Script de teste
├── requirements.txt      # Dependências
└── README.md
```

## Banco de Dados

O banco SQLite será criado automaticamente como `database.db` na raiz do projeto na primeira execução da aplicação.

### Tabelas

**medico**
- id (INTEGER PRIMARY KEY)
- nome (TEXT NOT NULL)
- especialidade (TEXT NOT NULL)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**agenda**
- id (INTEGER PRIMARY KEY)
- medico_id (INTEGER FOREIGN KEY)
- data (DATETIME NOT NULL)
- status (TEXT CHECK: 'livre' ou 'ocupado')
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados e serialização
- **SQLite**: Banco de dados leve e embutido
- **Uvicorn**: Servidor ASGI para produção 