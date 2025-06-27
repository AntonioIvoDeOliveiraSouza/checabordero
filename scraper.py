import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError
import sys
import json

URL_BASE = "https://ffp-pi.com.br/competicoes"
URL_COMPETICOES_MA = "https://www.futebolmaranhense.com.br/competicoes/" #URL Federação Maranhense - Permitir que eu busque mais de uma

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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    r = requests.get(URL_TABELA,headers=headers)
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

def get_bordero(id_partida:str):
    URL_BORDERO = f"https://conteudo.cbf.com.br/federacoes/10/borderos/2025/{id_partida}b.pdf"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(URL_BORDERO,headers=headers,timeout=10)
        if response.status_code == 200:
            nome_arquivo = f"bordero_{id_partida}.pdf"
            with open(nome_arquivo, "wb") as f:
                f.write(response.content)
                print(f"✅ PDF salvo como: {nome_arquivo}")
            return URL_BORDERO
        else:
            print(f"❌ Borderô não encontrado para o jogo {id_partida} (Status: {response.status_code})")
            return None
    except SSLError as e:
        print(f"❌ Erro SSL ao tentar baixar borderô: {e}")
        return {"erro": "Erro SSL ao tentar acessar o PDF", "detalhes": str(e)}
    except Exception as e:
        print(f"❌ Erro inesperado ao tentar baixar o borderô: {e}")
        return {"erro": "Erro inesperado", "detalhes": str(e)}
    
if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("API ChecaBordero v.0.1\nLink para Github:https://github.com/AntonioIvoDeOliveiraSouza/checabordero\n\nPara iniciar, digite:\npython scraper.py get_campeonato")
    elif len(sys.argv) >= 2:
        comando = sys.argv[1]
        if comando == "get_campeonato":
            campeonatos = get_campeonato()
            print(json.dumps(campeonatos, indent=2, ensure_ascii=False))
        elif comando == "get_tabelas":
            if len(sys.argv) != 3:
                print("Uso para get_tabelas: python scraper.py get_tabelas <idcampeonato>")

            else:
                idcampeonato = sys.argv[2]
                tabelas = get_tabelas(idcampeonato)
                print(json.dumps(tabelas,indent=2,ensure_ascii=False))
        elif comando == "get_partidas":
            if len(sys.argv) !=3:
                print("Uso: python coletar_partidas.py <idcampeonato> <id_fase>")
        elif comando == "get_bordero":
            if len(sys.argv) !=3:
                print("Uso para get_bordero: python scraper.py get_bordero <id_partida>")
            
            else:
                id_partida = sys.argv[2]
                bordero = get_bordero(id_partida)
        else:
            print("❌ Comando desconhecido.")
        
