Aplicativo de Controle Financeiro Pessoal (MVP)
Este é um projeto acadêmico de um aplicativo web full-stack para controle financeiro pessoal. Foi desenvolvido como parte da disciplina de [Nome da sua Disciplina] do 4º semestre do curso de Análise e Desenvolvimento de Sistemas.

O objetivo é fornecer uma ferramenta simples, segura e intuitiva para que os usuários possam gerenciar suas receitas e despesas. O pilar central do projeto é a privacidade de dados: a arquitetura é multi-tenant, garantindo que cada usuário tenha acesso única e exclusivamente aos seus próprios dados.

🏛️ Contexto Acadêmico e Social
Este projeto foi desenvolvido para cumprir os requisitos de extensão da [Nome da sua Universidade/Faculdade], conectando o aprendizado acadêmico com a comunidade.

Ele está alinhado ao ODS 8 (Trabalho Decente e Crescimento Econômico) da ONU, atuando como uma ferramenta de empoderamento e alfabetização financeira. Ao fornecer um meio acessível para a gestão de finanças pessoais, o projeto visa dar estabilidade a jovens trabalhadores e microempreendedores, ajudando-os a tomar decisões baseadas em dados e a construir um futuro financeiro mais sólido.

✨ Funcionalidades Principais
Autenticação Segura: Sistema completo de Registro, Login e Logout de usuários.

Privacidade Total: Usuários só podem ver e gerenciar os dados que eles mesmos criaram.

Dashboard Dinâmico: Uma visão geral e instantânea do saldo atual, total de receitas e total de despesas.

Gestão de Categorias: CRUD (Criar, Ler, Deletar) completo para categorias de gastos/receitas personalizadas.

Gestão de Transações: CRUD (Criar, Ler, Editar, Deletar) completo para todas as transações financeiras.

Formulário Inteligente: O formulário de transação filtra dinamicamente, mostrando apenas as categorias que o usuário logado criou.

Interface Responsiva: O design utiliza Bootstrap 5, adaptando-se a desktops, tablets e celulares.

💻 Tecnologias Utilizadas
Back-End:

Python: Linguagem principal da lógica de negócios.

Django: Framework web full-stack para o desenvolvimento rápido e seguro.

Django ORM: Para interação com o banco de dados de forma segura (prevenindo SQL Injection).

SQLite: Banco de dados relacional leve utilizado para desenvolvimento.

Front-End:

HTML5

CSS3

Bootstrap 5: Framework CSS para estilização e responsividade.

Django Template Language (DTL): Para renderizar os dados do back-end no HTML.

Segurança:

Sistema de Autenticação nativo do Django (criptografia de senhas e gerenciamento de sessões).

Proteção contra CSRF (Cross-Site Request Forgery) em todos os formulários.

Lógica de filter(usuario=request.user) para garantir o isolamento de dados.

🚀 Como Executar o Projeto (Setup)
Siga os passos abaixo para executar o projeto localmente:

1. Clonar o Repositório:

Bash

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
2. Criar e Ativar o Ambiente Virtual (Venv):

Bash

# Criar o ambiente
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no Mac/Linux
source venv/bin/activate
3. Instalar as Dependências: (Este passo usa o requirements.txt que você acabou de criar)

Bash

pip install -r requirements.txt
4. Aplicar as Migrações do Banco: (Isso irá criar o arquivo db.sqlite3 com todas as tabelas)

Bash

python manage.py migrate
5. Criar um Superusuário (Admin): (Siga as instruções para criar seu usuário de administrador)

Bash

python manage.py createsuperuser
6. Executar o Servidor:

Bash

python manage.py runserver
7. Acessar o App: Abra seu navegador e acesse: http://127.0.0.1:8000/

Para acessar o painel de admin: http://127.0.0.1:8000/admin/

👨‍💻 Autores
Danilo Oliveira
Marina Kleinschmitt
André Araújo
