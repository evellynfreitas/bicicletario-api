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

Este projeto é dividido em **três APIs independentes**, organizadas em microsserviços:

- 🔧 `equipamento` – gestão de bicicletas e equipamentos;
- 👤 `aluguel` – controle de usuários e empréstimos;
- 🌐 `externo` – integração e funcionalidades públicas.

---

## ⚙️ Tecnologias e Dependências

| Ferramenta      | Finalidade                            |
|-----------------|----------------------------------------|
| Python 3.9+     | Linguagem principal                    |
| FastAPI         | Framework Web para APIs                |
| Uvicorn         | Servidor ASGI para rodar o FastAPI     |
| Pandas          | Manipulação e análise de dados         |
| Pytest          | Testes automatizados                   |

As dependências estão listadas no arquivo `requirements.txt`.

---

## ☁️ Hospedagem na Nuvem (Render)

A aplicação está hospedada na plataforma **[Render](https://render.com/)**, permitindo o acesso remoto das APIs em produção.

🔗 Acesse a documentação da API via Swagger:  
👉 [API Externa](https://bicicletario-api.onrender.com/docs)
👉 [API Aluguel](https://bicicletario-api-aluguel.onrender.com/docs)
👉 [API Equipamentos](https://bicicletario-api-equipamento.onrender.com/docs)
---

## 🔎 Revisão de Código

Este projeto utiliza o [**SonarCloud**](https://sonarcloud.io/) para análise estática de código, garantindo qualidade, cobertura de testes e boas práticas.

🔍 **Dashboard do SonarCloud:**  
👉 [SonarCloud - bicicletario-api](https://sonarcloud.io/project/overview?id=evellynfreitas_bicicletario-api)


---

## 🧪 Testes Automatizados

Utilizamos `pytest` para validar o comportamento da aplicação com testes automatizados.

📁 Os arquivo de testes estão dentro das pastas "tests" em cada API

---

### ▶️ Executar testes:

Com o ambiente virtual ativado e dentro de alguma API, execute:

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



---

## ⚖️ Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](https://github.com/evellynfreitas/bicicletario-api/blob/main/LICENSE) para mais detalhes.
