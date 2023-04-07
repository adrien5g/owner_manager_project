# Controle de carros e proprietários

Este é um sistema de gerenciamento, permitindo a adição e remoção de carros e proprietários, bem como a visualização dos dados armazenados no sistema.

## Funcionalidades

O sistema conta com as seguintes funcionalidades:

- Login com usuário e senha
- Criação de proprietários
- Registro de carros para proprietários
- Remoção de carro de proprietários
- Remoção de proprietários, com remoção automática dos carros associados
- Listagem de todos os proprietários cadastrados
- Busca de um proprietário específico

## Tecnologias Utilizadas

O sistema foi desenvolvido utilizando as seguintes tecnologias:

- Flask: utilizado na parte da API
- Redoc: utilizado para documentação de API
- Pydantic: utilizado para transformação de dados internamente
- SQLModel: utilizado para interagir com o banco de dados
- Svelte: utilizado no frontend
- Pytest: utilizando para testes automatizados
- Docker: utilizado para facilitar a execução do projeto

## Sobre o desenvolvimento

Algumas funcionalidades extras foram desenvolvidas para tornar o sistema mais completo e facilitar sua usabilidade:

- Documentação de todos os endpoints, disponível na URL `http://localhost:5000/apidoc/redoc`
- Frontend interativo com Svelte, para facilitar a usabilidade da API
- Endpoints de controle para tornar a API mais completa
- Utilização de containers separados para frontend e backend, facilitando a execução do projeto
- Padronização de código, visando facilitar a compreensão e a manutenção por parte de outros desenvolvedores

## Como Executar

### Com Docker

Para executar o projeto com Docker, basta rodar o seguinte comando:

```bash
docker-compose up -d
```

Ao executar o comando acima, o frontend estará disponível na URL `http://localhost:8080` e a API estará disponível na URL `http://localhost:5000`. 

É possível acessar o sistema com o usuário padrão `admin` e senha `admin`.

Para acessar a documentação dos endpoints acesse `http://localhost:5000/apidoc/redoc`

### Sem Docker

#### Preparando ambiente

Para executar o projeto sem Docker, é necessário primeiro instalar as dependências do projeto. Para isso, você pode executar os seguintes comandos:

- Usando Poetry:

    Instale as dependências com o comando
    ```bash
    poetry install
    ```

    Ative o ambiente virtual
    ```bash
    poetry shell
    ```

- Usando Pip:

    **(Opcional)** Crie um ambiente de desenvolvimento e depois ative
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    Instale as dependências
    ```bash
    pip3 install -r requirements-back.txt
    pip3 install -r requirements-front.txt
    ```
#### Executando projeto

Para executar o **frontend**, execute o seguinte comando:
```bash
streamlit run www/index.py
```
Para executar o **backend**, execute o seguinte comando:
```bash
python3 backend/main.py
```

Caso esteja executando o frontend e o backend em máquinas diferentes, é necessário configurar a variável de ambiente API_URL no frontend. Essa variável deve apontar para a URL do backend. Por padrão, a URL é http://localhost:5000.