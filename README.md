# Aplicativo de Controle Financeiro Pessoal

Projeto academico em Django para gestao financeira pessoal. Esta versao inclui a Fase 4 de evolucao de produto: planejamento financeiro com orcamentos mensais, metas, indicadores do mes e historico consolidado no dashboard.

## Stack atual

- Python
- Django
- Django ORM
- SQLite para desenvolvimento
- HTML, CSS e Bootstrap 5

## Estrutura real do projeto

```text
sistema_gestao_financeira/
|-- config/
|-- financeiro/
|-- static/
|-- templates/
|-- manage.py
|-- requirements.txt
`-- README.md
```

## Melhorias da Fase 4

- Configuracao sensivel movida para variaveis de ambiente.
- `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS` e fuso configuraveis.
- Exclusoes protegidas por `POST`.
- Feedback de sucesso e erro com mensagens no frontend.
- Validacao amigavel para categoria duplicada.
- Modelagem de `Conta` com tipo, saldo inicial e status.
- `Transacao` agora suporta conta, observacao e recorrencia.
- Dashboard com patrimonio total e resumo por conta.
- Consultas extraidas para `selectors.py` e operacoes para `services.py`.
- Orcamento mensal por categoria.
- Metas financeiras com valor alvo, valor atual e status.
- Dashboard com receitas/despesas do mes, historico e resumos de planejamento.
- Filtros de conta, tipo, recorrencia e busca textual na listagem de transacoes.
- Paginacao da listagem de transacoes.
- Testes cobrindo autenticacao, isolamento de dados, seletores, paginacao e planejamento.
- `requirements.txt` reduzido ao que o projeto realmente usa.

## Configuracao do ambiente

Crie um arquivo `.env` na raiz do projeto com algo como:

```env
DJANGO_SECRET_KEY=troque-esta-chave-em-producao
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_TIME_ZONE=America/Sao_Paulo
```

## Como rodar

1. Crie e ative um ambiente virtual.
2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Gere e aplique as migracoes:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Execute os testes:

```bash
python manage.py test
```

5. Suba o servidor:

```bash
python manage.py runserver
```

## Proxima etapa

A Fase 5 deve atacar acabamento de produto e distribuicao: UX melhor, automacoes de recorrencia, importacao, exportacao e preparacao para deploy.
