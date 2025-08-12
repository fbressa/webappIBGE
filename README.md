# 📊 Popularidade de Nomes no Brasil (IBGE)

Aplicação web interativa em **Streamlit** que consulta a API de Nomes do **IBGE** e exibe a frequência de um nome ao longo das décadas, com tabela e gráfico.

[![Deploy Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fbressa-webappibge-webappibge-mynuph.streamlit.app/)

---

## 🔍 Problema

A API de Nomes do IBGE disponibiliza dados sobre a popularidade de nomes no Brasil, mas de forma bruta e pouco amigável para usuários não técnicos.

---

## ✅ Solução

Este projeto oferece:
- Busca interativa por nome.
- Consulta direta à API do IBGE.
- Organização dos resultados por década.
- Visualização em **tabela** e **gráfico**.
- Dicas para variações do nome (acentuação, apelidos).

---

## 🧰 Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://requests.readthedocs.io/)
- [API de Nomes do IBGE](https://servicodados.ibge.gov.br/api/docs/nomes?versao=2)

---

## 📂 Estrutura do Projeto

├── webappIBGE.py # Código principal do Streamlit
├── requirements.txt # Dependências para rodar o app
└── README.md # Documentação do projeto

## ▶️ Como Rodar Localmente

1. **Clone este repositório**
   ```bash
   git clone https://github.com/fbressa/webappIBGE.git
   cd webappIBGE
