
<div align="center">

  <h1>Bicicletário API</h1>
  
  <p>
    API para gestão de bicicletários utilizando FastAPI 🚴‍♀️<br>
  </p>
  
<!-- Badges -->

</div>

---

## 📌 Sobre o Projeto

API para gerenciamento de bicicletários, permitindo controle de acessos, relatórios, estatísticas e muito mais. Construída com **FastAPI** para alta performance, utilizando boas práticas de desenvolvimento e testes automatizados com **Pytest**.

---

## ⚙️ Tecnologias e Dependências

| Ferramenta      | Finalidade                            |
|-----------------|----------------------------------------|
| Python 3.9+     | Linguagem principal                    |
| FastAPI         | Framework Web para APIs                |
| Uvicorn         | Servidor ASGI para rodar o FastAPI     |
| Pandas          | Manipulação e análise de dados         |
| Pytest          | Testes automatizados                   |


### 📦 Instaladas via `pyproject.toml`:

```toml
[tool.poetry.dependencies]
python = ">=3.9,<3.13"
fastapi = ">=0.115.12,<0.116.0"
uvicorn = ">=0.34.3,<0.35.0"
pandas = ">=2.2.3,<3.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.4.0"
```

---

## ☁️ Hospedagem na Nuvem (AWS)

A aplicação está hospedada em uma instância EC2 da Amazon Web Services (AWS), permitindo o acesso remoto da API em produção.

🔗 Acesse a documentação da API via Swagger:  
👉 [http://3.138.108.109:8000/docs](http://3.138.108.109:8000/docs)

---

## 🔎 Revisão de Código

Este projeto utiliza o [**SonarCloud**](https://sonarcloud.io/) para análise estática de código, garantindo qualidade, cobertura de testes e boas práticas.

🔍 **Dashboard do SonarCloud:**  
👉 [SonarCloud - bicicletario-api](https://sonarcloud.io/project/overview?id=evellynfreitas_bicicletario-api)

---

## 🧪 Testes Automatizados

Utilizamos `pytest` para validar o comportamento da aplicação com testes automatizados.

📁 O arquivo de testes de exemplo está localizado em:

```
tests/test_hello.py
```

### ▶️ Executar testes:

Com o ambiente virtual ativado, execute:

```bash
pytest -s
```

---

## 🛠️ Como Rodar o Projeto Localmente

### 📋 Pré-requisitos

- Python >=3.9
- Git

### 📦 Instalar e executar:

```bash
# Clonar o repositório
git clone https://github.com/evellynfreitas/bicicletario-api.git
cd bicicletario-api

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
venv\scripts\activate

# Instalar dependências
pip install -r requirements.txt

```

---

## 👥 Contribuidores

<a href="https://github.com/evellynfreitas/bicicletario-api/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=evellynfreitas/bicicletario-api" />
</a>

---

## ⚖️ Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](https://github.com/evellynfreitas/bicicletario-api/blob/main/LICENSE) para mais detalhes.
