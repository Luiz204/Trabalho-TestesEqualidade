# QA Automation Project

Projeto de automacao de testes com Python, cobrindo API REST (Petstore Swagger) e Web E2E (SauceDemo), com CI/CD via GitHub Actions.

---

## Estrutura do Projeto

    qa-automation-project/
    .github/workflows/ci.yml
    api_tests/tests/test_pet.py
    api_tests/tests/test_store.py
    api_tests/tests/test_user.py
    api_tests/utils/api_client.py
    api_tests/utils/data_factory.py
    web_tests/pages/base_page.py
    web_tests/pages/login_page.py
    web_tests/pages/inventory_page.py
    web_tests/pages/cart_page.py
    web_tests/pages/checkout_page.py
    web_tests/tests/test_saucedemo.py
    web_tests/conftest.py
    requirements.txt

---

## Tecnologias Utilizadas

- Python 3.11
- pytest
- requests
- Selenium 4.x
- pytest-html
- GitHub Actions

---

## Instalacao e Configuracao

1. Clone o repositorio:
   git clone https://github.com/seu-usuario/qa-automation-project.git

2. Ative o ambiente virtual:
   .venv\Scripts\activate

3. Instale as dependencias:
   pip install -r requirements.txt

---

## Executando os Testes

Todos os testes:
   pytest

Somente API:
   pytest api_tests/

Somente Web:
   pytest web_tests/

Com relatorio HTML:
   pytest --html=reports/report.html --self-contained-html

---

## Cobertura dos Testes

### API - Petstore Swagger
Base URL: https://petstore.swagger.io/v2

- Pet: criar, buscar por ID, atualizar, buscar por status, deletar
- Store: inventario, realizar pedido, buscar pedido, deletar pedido
- User: criar, login, buscar, atualizar, deletar

### Web - SauceDemo
URL: https://www.saucedemo.com/

- Login valido
- Login invalido
- Fluxo E2E: Login, Produtos, Carrinho, Checkout, Confirmacao

---

## Pipeline CI/CD - GitHub Actions

Acionada em push para main e develop e em Pull Requests.

Etapas:
1. Checkout do codigo
2. Setup Python 3.11
3. Instalacao das dependencias
4. Testes de API
5. Testes Web (Chrome headless)
6. Upload do relatorio HTML

---

## Design Patterns

- Page Object Model (POM): cada tela tem sua propria classe
- Factory Pattern: data_factory.py centraliza criacao de dados
- Base Page: metodos comuns reutilizados por todos os Page Objects
- Fixtures: setup e teardown do WebDriver via conftest.py

---

## Autor

Luiz Guilherme Aguiar de Almeida
Trabalho QA
