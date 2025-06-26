# 📊 ChecaBordero API

Uma API desenvolvida com FastAPI para consultar e baixar os borderôs (boletim financeiro) dos jogos da Federação de Futebol do Piauí (FFP), sem precisar acessar manualmente o site oficial.

---

## 🚀 Propósito

Facilitar o acesso aos dados de competições organizadas pela FFP, como:

- Lista de competições
- Tabelas e fases
- Partidas (com data, placar, times)
- Download do borderô em PDF
- Extração de informações do PDF (em breve)

---

## 🔧 Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Playwright](https://playwright.dev/python/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://pypi.org/project/requests/)

---

## 📂 Estrutura dos Arquivos

- `main.py` → Arquivo principal da API (endpoints)
- `scraper.py` → Módulo que faz o scraping de dados e baixa PDFs
- `coletar_partidas.py` → Script auxiliar que coleta partidas via Playwright
- `requirements.txt` → Dependências do projeto

---

## 📌 Endpoints Disponíveis

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Verifica se a API está ativa |
| `/competicoes` | GET | Lista os campeonatos disponíveis |
| `/tabelas?idcampeonato=...` | GET | Mostra as fases da competição |
| `/partidas?idcampeonato=...&id_fase=...` | GET | Lista as partidas da fase |
| `/bordero?id_partida=...` | GET | Baixa o PDF do borderô da partida |

---

## ⚙️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/AntonioIvoDeOliveiraSouza/checa-bordero.git
   cd checa-bordero
   ```

2. Crie e ative um ambiente virtual:
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  .\venv\Scripts\activate   # Windows
   ```

3. Instale as dependências:
  ```bash
  pip install -r requirements.txt
  ```

4. Execute a API:
  ```bash
  uvicorn main:app --reload
   ```

5. Acesse a documentação interativa:
  ```bash
  http://localhost:8000/docs
  ```
