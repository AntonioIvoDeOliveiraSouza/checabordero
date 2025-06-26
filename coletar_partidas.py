from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sys
import json

def get_partidas(idcampeonato: str, id_fase: str):
    URL_FASE = f"https://ffp-pi.com.br/competicoes/tabela/{idcampeonato}/{id_fase}"
    jogos = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            extra_http_headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
        )
        page.goto(URL_FASE, timeout=60000)
        page.wait_for_selector("#jogos", timeout=10000)
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    jogos_div = soup.select_one("#jogos")

    if not jogos_div:
        print("⚠️ Nenhum conteúdo encontrado na seção de jogos.")
        return []

    for rodada in jogos_div.select("ul.uk-slider-items li"):
        for partida in rodada.select("ul.uk-list > li"):
            data_partida = partida.select_one("p.uk-text-center, p.uk-text-small.uk-text-center")
            times = partida.select("div[uk-grid] div")

            if len(times) < 3 or not data_partida:
                continue
            
            #manipulação dos dados obtidos
            resultado = times[0].get_text(strip=True)

            time_casa = times[1].get_text(strip=True)
            time_fora = resultado[8:]
            placar = times[2].get_text(strip=True)

            resultado = f"{time_casa} {placar} {time_fora}"

            link = partida.select_one("a[href*='/competicoes//jogo/']")
            id_partida = None
            if link and "href" in link.attrs:
                href = link["href"]
                id_partida = href.strip("/").split("/")[-1]

            jogos.append({
                "id_partida": id_partida,
                "data": data_partida.text.strip(),
                "resultado": resultado,
                "time_casa": time_casa,
                "time_fora": time_fora,
                "placar": placar,
                "url_partida": f"https://ffp-pi.com.br{href}" if id_partida else None
            })
    return jogos

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python coletar_partidas.py <idcampeonato> <id_fase>")
        sys.exit(1)

    idcampeonato = sys.argv[1]
    id_fase = sys.argv[2]
    partidas = get_partidas(idcampeonato, id_fase)
    print(json.dumps(partidas, ensure_ascii=False, indent=2))
