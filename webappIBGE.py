import re                  # módulo para trabalhar com expressões regulares (usado para extrair o ano do período)
import unicodedata         # módulo para manipular caracteres e remover acentos
import requests            # para fazer requisições HTTP (consultar a API do IBGE)
import pandas as pd        # para manipulação e organização dos dados em tabelas
import streamlit as st     # para criar a interface web do app

# URL base da API de nomes do IBGE
API_BASE = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/"

# Função para normalizar o nome
def _normalize_name(name: str) -> str:
    """
    Coloca o nome em minúsculas, remove espaços extras no início/fim
    e tira acentos para evitar problemas com a API.
    """
    nfkd = unicodedata.normalize("NFKD", name.strip().lower())
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

# Função para extrair o ano inicial de um período retornado pela API
def _period_to_int(period: str) -> int:
    """
    A API retorna períodos no formato '1930[', '2000[', ou '2000[)'.
    Aqui, usamos regex para extrair o ano (quatro dígitos) e
    converter para inteiro.
    """
    m = re.search(r"(\d{4})", period or "")
    return int(m.group(1)) if m else 0

# Função genérica para fazer requisição GET e retornar JSON
def fazer_request(url, params=None):
    """
    Faz uma requisição GET para a URL especificada.
    Retorna o JSON da resposta ou levanta erro em caso de falha.
    """
    r = requests.get(url, params=params, timeout=10)  # timeout de 10s para evitar travar
    r.raise_for_status()  # se status != 200, levanta exceção
    return r.json()

# Função principal para buscar dados do nome na API e processar
@st.cache_data(ttl=3600)  # guarda o resultado em cache por 1 hora para evitar repetir requisição
def pegar_nome_por_decada(nome: str) -> pd.DataFrame | None:
    """
    Consulta a API do IBGE para o nome informado e retorna
    um DataFrame com a frequência por década.
    """
    url = f"{API_BASE}{_normalize_name(nome)}"  # normaliza o nome e monta a URL
    try:
        payload = fazer_request(url)  # busca os dados na API
    except Exception:
        return None  # em caso de erro de requisição, retorna None

    if not payload:
        return None  # se a API não retornar nada, sai

    # Monta uma lista de dicionários com ano inicial da década e frequência
    rows = []
    for item in payload[0].get("res", []):
        decade_start = _period_to_int(item.get("periodo"))  # extrai o ano da década
        rows.append({
            "decade_start": decade_start,
            "frequencia": item.get("frequencia", 0)
        })

    if not rows:
        return None  # sem dados, sai

    # Cria DataFrame ordenado pela década
    df = pd.DataFrame(rows).sort_values("decade_start")

    # Cria coluna 'Década' no formato '1930s', '2000s', etc.
    df["Década"] = df["decade_start"].astype(int).astype(str) + "s"

    # Mantém apenas as colunas desejadas e renomeia 'frequencia' para 'Frequência'
    df = df[["Década", "frequencia"]].rename(columns={"frequencia": "Frequência"})

    return df  # retorna o DataFrame

# Função que monta a interface Streamlit
def main():
    # Configuração da página (título, ícone)
    st.set_page_config(page_title="Popularidade de Nomes (IBGE)", page_icon="📊")

    # Título e legenda do app
    st.title("📊 Popularidade de Nomes no Brasil (IBGE)")
    st.caption("Fonte: IBGE – API de Nomes • https://servicodados.ibge.gov.br/api/docs/nomes?versao=2")

    # Campo para digitar o nome
    nome = st.text_input("Consulte um nome:", placeholder="Ex.: Maria, João, Filipe")
    if not nome:  # se não digitou nada, mostra instrução e para
        st.info("Digite um nome para começar.")
        st.stop()

    # Mostra spinner enquanto consulta a API
    with st.spinner("Consultando o IBGE..."):
        df = pegar_nome_por_decada(nome)

    # Caso não encontre dados para o nome
    if df is None or df.empty:
        st.warning(f'Nenhum dado encontrado para "{nome}". Tente outro nome.')
        st.stop()

    # Layout: duas colunas (tabela à esquerda, gráfico à direita)
    col1, col2 = st.columns([0.35, 0.65])

    with col1:
        st.subheader("Frequência por década")
        # Exibe tabela sem índice, ocupando largura total
        st.dataframe(df, hide_index=True, use_container_width=True)

    with col2:
        st.subheader("Evolução no tempo")
        # Exibe gráfico de linha com 'Década' no eixo X e 'Frequência' no Y
        st.line_chart(df.set_index("Década")["Frequência"])

    # Texto final de dica
    st.caption("Dica: tente variações do nome (acentuação, apelidos).")

# Ponto de entrada do app
if __name__ == "__main__":
    main()
