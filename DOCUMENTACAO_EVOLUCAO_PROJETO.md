# Documentacao de Evolucao do Projeto

## Identificacao

- Projeto: Sistema de Gestao Financeira
- Stack principal: Django, Django ORM, SQLite, HTML, CSS, Bootstrap
- Objetivo desta documentacao: registrar de forma detalhada todas as alteracoes e melhorias aplicadas durante a evolucao do projeto, da base academica inicial ate a estrutura atual consolidada nas Fases 1, 2, 3 e 4.

## 1. Visao geral

O repositorio original era um MVP academico de controle financeiro pessoal construindo como um CRUD server-rendered em Django. A base inicial era funcional para demonstracao de disciplina, mas ainda estava muito proxima de um scaffold:

- Um unico app principal centralizando dominio, consultas e camada HTTP.
- Modelagem restrita a `Categoria` e `Transacao`.
- Dashboard com indicadores simples.
- Ausencia de testes automatizados.
- Dependencias infladas e nao aderentes ao codigo real.
- Configuracoes sensiveis versionadas.
- Pouca separacao entre responsabilidades de dominio, consulta e interface.

O trabalho realizado nesta evolucao teve como foco transformar esse MVP em uma base muito mais solida, preparada para continuidade real do produto.

## 2. Objetivos da evolucao

As alteracoes foram guiadas por cinco objetivos principais:

1. Fortalecer a base tecnica e a seguranca do projeto.
2. Ampliar o dominio financeiro para sair do CRUD basico.
3. Organizar melhor a arquitetura interna para permitir crescimento.
4. Adicionar inteligencia de negocio com planejamento e acompanhamento.
5. Deixar o projeto pronto para uma proxima fase de acabamento, automacao e distribuicao.

## 3. Estado inicial do projeto

Antes da evolucao, o projeto tinha as seguintes caracteristicas:

- `SECRET_KEY` exposta no codigo.
- `DEBUG = True` fixo no arquivo de settings.
- Apenas `Categoria` e `Transacao` como entidades de negocio.
- Views concentrando autenticacao, persistencia, consulta e tratamento de formularios.
- Exclusoes sem imposicao forte de metodo HTTP no backend.
- Documentacao divergente da estrutura real do repositorio.
- `requirements.txt` com diversas bibliotecas sem uso no projeto.
- `tests.py` vazio.

Na pratica, isso significava que o sistema funcionava como demonstracao, mas nao tinha base segura nem estrutura suficiente para suportar relatorios, planejamento mensal, metas, filtros ricos ou crescimento de equipe.

## 4. Fase 1 - Endurecimento da base

### 4.1 Objetivo

A Fase 1 foi dedicada a corrigir problemas fundamentais de confiabilidade, configuracao, seguranca e previsibilidade do projeto.

### 4.2 Melhorias implementadas

- Introducao de configuracao por ambiente em `config/settings.py`.
- Leitura de variaveis de ambiente via `.env`.
- Criacao de `.env.example` na raiz.
- Parametrizacao de:
  - `DJANGO_SECRET_KEY`
  - `DJANGO_DEBUG`
  - `DJANGO_ALLOWED_HOSTS`
  - `DJANGO_TIME_ZONE`
- Ajuste de `LANGUAGE_CODE` para `pt-br`.
- Ajustes de seguranca em cookies e cabecalhos.
- Restricao de exclusao a `POST`.
- Remocao de `except:` silencioso em fluxo de categorias.
- Inclusao de mensagens de sucesso e erro no frontend.
- Criacao de testes iniciais cobrindo autenticacao e isolamento de dados.
- Limpeza de dependencias no `requirements.txt`.
- Reescrita do README para refletir o estado real do codigo.

### 4.3 Impacto tecnico

Essa fase nao mudou o produto do ponto de vista funcional, mas mudou radicalmente a confiabilidade da base:

- reduziu risco de configuracao insegura
- tornou o comportamento do sistema mais previsivel
- criou o primeiro colchao de testes
- alinhou documentacao, dependencias e estrutura real

## 5. Fase 2 - Evolucao do dominio financeiro

### 5.1 Objetivo

A Fase 2 teve como foco tirar o projeto do nivel "categorias + lancamentos" e introduzir um dominio financeiro mais realista.

### 5.2 Novas capacidades

Foi criada a entidade `Conta`, permitindo ao usuario separar movimentacoes por origem financeira:

- conta corrente
- poupanca
- carteira
- investimento

Tambem foram acrescentados novos dados em `Transacao`:

- `conta`
- `observacao`
- `recorrente`
- timestamps de criacao e atualizacao

### 5.3 Melhorias no produto

- CRUD de contas.
- Dashboard com patrimonio total.
- Soma de saldo inicial com movimentacao financeira.
- Listagem de transacoes com filtro por conta.
- Bloqueio de cadastro de transacao sem conta ativa.

### 5.4 Impacto tecnico

Essa fase foi o primeiro salto de modelagem de negocio. O sistema deixou de representar apenas um conjunto solto de entradas e passou a refletir a estrutura minima de uma vida financeira real.

## 6. Fase 3 - Organizacao arquitetural

### 6.1 Objetivo

A Fase 3 buscou reduzir acoplamento e preparar o sistema para crescer sem transformar `views.py` em um gargalo.

### 6.2 Camadas introduzidas

Foram criados dois novos modulos:

- `financeiro/selectors.py`
- `financeiro/services.py`

#### Selectors

Os selectors passaram a concentrar:

- consultas filtradas por usuario
- agregacoes do dashboard
- paginação
- filtros de transacoes

#### Services

Os services passaram a concentrar:

- criacao de conta
- criacao de categoria
- criacao de transacao
- verificacao de conta ativa
- remocao de recursos por usuario

### 6.3 Ganhos obtidos

- Views mais simples e legiveis.
- Melhor separacao entre consulta, regra operacional e resposta HTTP.
- Menor duplicacao de logica.
- Maior facilidade para criar APIs no futuro.
- Melhor testabilidade da camada de negocio.

### 6.4 Melhorias funcionais adicionais

- Paginacao da lista de transacoes.
- Busca textual por descricao e observacao.
- Filtro por conta.
- Filtro por tipo.
- Filtro por recorrencia.

## 7. Fase 4 - Planejamento financeiro e inteligencia de negocio

### 7.1 Objetivo

A Fase 4 transformou o sistema de registro financeiro em um sistema de acompanhamento e planejamento.

### 7.2 Novas entidades

Foram adicionadas duas entidades centrais:

#### OrcamentoMensal

Representa o limite financeiro planejado para uma categoria em um determinado mes e ano.

Campos principais:

- `usuario`
- `categoria`
- `ano`
- `mes`
- `limite`
- `observacao`

Restricao importante:

- unicidade por usuario, categoria, ano e mes

#### MetaFinanceira

Representa objetivos financeiros do usuario, como reserva, viagem, equipamento, emergencia ou investimento.

Campos principais:

- `nome`
- `valor_alvo`
- `valor_atual`
- `prazo`
- `status`

### 7.3 Novas telas e fluxos

Foram criadas novas areas funcionais:

- Gerenciamento de orcamentos mensais
- Gerenciamento de metas financeiras
- Dashboard expandido com indicadores do mes
- Historico consolidado por mes
- Resumo de consumo de orcamento
- Resumo de progresso de metas

### 7.4 Novos indicadores

O dashboard agora exibe:

- patrimonio atual
- receitas do mes
- despesas do mes
- saldo do mes
- resumo por conta
- historico mensal consolidado
- progresso de orcamentos
- progresso de metas

### 7.5 Valor de produto

Essa fase e importante porque muda a natureza do sistema:

- antes o sistema registrava fatos
- agora o sistema tambem ajuda a planejar, comparar e acompanhar metas

Isso aproxima o projeto de um produto real de gestao financeira pessoal.

## 8. Arquitetura atual

Atualmente o projeto esta organizado, de forma simplificada, da seguinte maneira:

- `config/`
  - configuracao global do Django
- `financeiro/models.py`
  - entidades de dominio
- `financeiro/forms.py`
  - validacoes e formularios
- `financeiro/selectors.py`
  - consultas, filtros e agregacoes
- `financeiro/services.py`
  - operacoes de negocio
- `financeiro/views.py`
  - camada HTTP
- `financeiro/urls.py`
  - roteamento do app
- `templates/financeiro/`
  - interfaces do produto
- `financeiro/tests.py`
  - testes automatizados

Essa estrutura continua simples, mas agora ja possui uma divisao clara de responsabilidades, o que facilita a manutencao e novas entregas.

## 9. Modelagem atual do dominio

### Conta

Responsavel por representar onde o dinheiro existe ou transita.

Uso no produto:

- separacao de patrimonio por origem
- saldo inicial por conta
- base para futuros recursos de transferencia e conciliacao

### Categoria

Responsavel por agrupar classificacoes de receitas e despesas.

Uso no produto:

- relatorios por classificacao
- orcamento mensal por categoria

### Transacao

Responsavel por registrar eventos financeiros.

Uso no produto:

- receitas e despesas
- ligacao com conta e categoria
- filtros, historico e relatorios

### OrcamentoMensal

Responsavel por registrar o limite planejado por categoria e periodo.

Uso no produto:

- controle de gasto por categoria
- comparacao entre planejado e realizado

### MetaFinanceira

Responsavel por acompanhar objetivos financeiros do usuario.

Uso no produto:

- reserva de emergencia
- objetivos de compra
- poupanca orientada por meta

## 10. Qualidade e testes

Durante a evolucao foram adicionados testes para validar:

- necessidade de login no dashboard
- isolamento de dados entre usuarios
- validacao de categoria duplicada
- validacao de conta duplicada
- filtros em transacoes
- paginação
- consultas do dashboard
- visao de planejamento financeiro
- redirecionamento quando nao ha conta ativa

Mesmo sem executar os testes neste ambiente, a base de testes ja foi incorporada ao projeto para permitir regressao controlada no ambiente local do usuario.

## 11. Ganhos concretos do trabalho realizado

Ao final das quatro fases, os ganhos podem ser resumidos em quatro grupos:

### Base tecnica

- configuracao segura e flexivel
- dependencias mais limpas
- documentacao alinhada
- maior previsibilidade de ambiente

### Dominio

- contas financeiras
- transacoes mais ricas
- planejamento por orcamento
- metas financeiras

### Arquitetura

- extracao de consultas para selectors
- extracao de operacoes para services
- views mais simples
- menor acoplamento

### Produto

- dashboard mais inteligente
- filtros mais ricos
- historico mensal
- acompanhamento de planejamento financeiro

## 12. Limites atuais

Mesmo com a evolucao, alguns pontos continuam abertos para etapas futuras:

- recorrencia automatica ainda nao gera lancamentos sozinha
- nao existe importacao de CSV ou OFX
- nao existe exportacao de dados
- nao existe API REST
- nao existe fluxo de deploy automatizado
- nao existe observabilidade ou logs operacionais estruturados
- nao existe permissao granular ou multiempresa

Esses pontos nao sao falhas do trabalho feito, mas o backlog natural de um produto que saiu do nivel academico e entrou em nivel de evolucao estruturada.

## 13. Proposta para a Fase 5

A proxima fase recomendada e de acabamento e distribuicao. Os focos mais coerentes sao:

1. UX e interface final.
2. Automacao de recorrencia.
3. Importacao e exportacao de dados.
4. Preparacao para deploy.
5. Melhorias de administracao e operacao.

## 14. Conclusao

O projeto deixou de ser apenas um CRUD academico simples e passou a ser uma base consistente para um sistema de gestao financeira pessoal com:

- configuracao profissional minima
- modelagem mais realista
- separacao arquitetural melhor definida
- indicadores de acompanhamento
- planejamento por orcamento
- metas financeiras
- testes iniciais relevantes

Em resumo, o sistema ainda nao e um produto final, mas ja nao e mais um MVP fragil. Agora ele possui estrutura suficiente para continuar evoluindo de forma muito mais segura e organizada.
