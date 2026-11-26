# Pharmacy Management System

Sistema de gestão de farmácia. Este repositório está a receber uma primeira implementação de backend em Python, com foco inicial no catálogo de medicamentos e controlo de stock por lote.

## Tecnologias

- Python 3.10+
- FastAPI
- SQLAlchemy 2
- SQLite (desenvolvimento)
- Pydantic

A estrutura segue o padrão de API com sessões de base de dados por pedido. O FastAPI permite usar diferentes bases de dados relacionais; SQLite foi escolhido nesta fase inicial por ser simples de executar localmente. Para produção, deverá ser avaliada uma base de dados servidor, como PostgreSQL. [Documentação oficial](https://fastapi.tiangolo.com/tutorial/sql-databases/).

## Funcionalidades implementadas nesta primeira versão

- Registo de medicamentos com SKU, nome, princípio ativo, categoria e código de barras opcional.
- Consulta e listagem de medicamentos.
- Registo de lotes por medicamento.
- Armazenamento de validade, preço de compra, preço de venda e quantidade por lote.
- Resumo de stock: medicamentos, lotes, unidades, stock baixo e lotes expirados.
- Endpoints de estado da API.

## Estrutura

```text
app/
  database.py
  models.py
  schemas.py
  main.py
  routers/
    medicines.py
    batches.py
    dashboard.py
tests/
  test_api.py
requirements.txt
requirements-dev.txt
```

## Executar localmente

1. Criar e ativar um ambiente virtual:

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# Linux/macOS
source .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Iniciar a API:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`. A documentação interativa fica em `http://127.0.0.1:8000/docs`.

## Endpoints iniciais

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/health` | Estado da API |
| POST | `/api/v1/medicines/` | Registar medicamento |
| GET | `/api/v1/medicines/` | Listar medicamentos |
| GET | `/api/v1/medicines/{id}` | Consultar medicamento |
| POST | `/api/v1/medicines/{id}/batches` | Registar lote |
| GET | `/api/v1/medicines/{id}/batches` | Consultar lotes |
| GET | `/api/v1/dashboard/stock` | Resumo do stock |

## Testes

```bash
pytest
```

## Próximas etapas

- [ ] Validar a implementação e ampliar os testes automatizados.
- [ ] Criar movimentos de entrada, saída e ajuste de stock com histórico auditável.
- [ ] Implementar vendas e linhas de venda.
- [ ] Implementar fornecedores e compras.
- [ ] Implementar autenticação, perfis e permissões.
- [ ] Criar alertas de stock mínimo e validade próxima.
- [ ] Criar interface web para utilizadores da farmácia.
- [ ] Preparar migrações de base de dados e configuração de produção.

## Estado e limitações

**Versão inicial de desenvolvimento (0.1.0).** Ainda não é um sistema pronto para utilização comercial. Não inclui autenticação, vendas, faturação fiscal, integração com sistemas externos ou validação de requisitos regulamentares. Não deve ser usado para gerir uma farmácia em produção sem revisão, testes, segurança e validação dos requisitos aplicáveis.

O código original do projeto anteriormente mencionado não estava disponível neste repositório vazio; esta primeira estrutura é uma nova base de desenvolvimento e deve ser conciliada com o projeto original caso os seus ficheiros sejam recuperados.
