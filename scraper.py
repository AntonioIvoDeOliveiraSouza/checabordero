import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL_BASE = "https://ffp-pi.com.br/competicoes"

def get_campeonato(): #função de buscar competições
    r = requests.get(URL_BASE) #pega a url
    soup = BeautifulSoup(r.text, "html.parser") #destrincha o html
    lista = [] #lista a ser usada adiante

    for link in soup.select("a[href^='/competicoes/']"): #para os links que estiverem em:
        nome = link.text.strip() #nome será o título do link
        href = link["href"] #o link que vai levar
        if nome and "/competicoes/" in href: #se há nome e competição:
            lista.append({
                "idcampeonato": href.strip("/").split("/")[-1],  # slug como ID
                "nome_competicao": nome,
                "url_competicao": "https://ffp-pi.com.br" + href
            })

    return lista #lista de competições registradas



def get_tabelas(idcampeonato:str): #função de pegar partidas dentro das competições

    URL_TABELA = f"https://ffp-pi.com.br/competicoes/tabela/{idcampeonato}"

    r = requests.get(URL_TABELA)
    soup = BeautifulSoup(r.text, 'html.parser')
    fases = []
    #print(soup.prettify())

    for item in soup.select("ul.uk-subnav li a"):
        nome_fase = item.text.strip()
        href = item.get("href", "")

        if not href.startswith("/competicoes/tabela/"):
            continue

        fase = href.strip("/").split("/")[-1]
        fases.append({
            "fase": fase,
            "nome_fase": nome_fase,
            "url_fase": "https://ffp-pi.com.br" + href
        })
    
    return fases

def baixar_bordero(id_partida:str):

    URL_BORDERO = f"https://conteudo.cbf.com.br/federacoes/10/borderos/2025/{id_partida}b.pdf"
    response = requests.get(URL_BORDERO)

    if response.status_code == 200:
        nome_arquivo = f"bordero_{id_partida}.pdf"
        with open(nome_arquivo, "wb") as f:
            f.write(response.content)
        print(f"✅ PDF salvo como: {nome_arquivo}")
        return URL_BORDERO
    else:
        print(f"❌ Borderô não encontrado para o jogo {id_partida}")
        return None