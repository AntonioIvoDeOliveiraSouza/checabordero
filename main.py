from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from scraper import get_campeonato, get_tabelas, get_bordero, extract_bordero
import subprocess
import json

app = FastAPI()

@app.get('/')
def home():
    print("API ChecaBordero v.0.1")
    return {"mensagem":"API ChecaBordero v.0.1"}

@app.get('/competicoes')
def listar_campeonato():
    print(get_campeonato())
    return get_campeonato()
    

@app.get('/tabelas')
def listar_tabelas(idcampeonato:str):
    print(get_tabelas(idcampeonato))
    return get_tabelas(idcampeonato)

@app.get("/partidas")
def listar_partidas(idcampeonato: str, id_fase: str):
    try:
        result = subprocess.run(
            [
                r"C:\Users\Dell master\checabordero\venv_oficial\Scripts\python.exe",  # Caminho completo para o Python do venv
                "coletar_partidas.py",
                idcampeonato,
                id_fase
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",  # <- evita erro de decode
            text=True,
        )
    
        if result.returncode != 0:
            return {
            "erro": "Erro ao executar script externo",
            "detalhes": result.stderr
            }

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "erro": "Erro ao decodificar JSON retornado",
                "stdout": result.stdout,
                "stderr": result.stderr
            }

    except subprocess.CalledProcessError as e:
        return {"erro": "Erro ao executar script externo", "detalhes": e.stderr}
    except json.JSONDecodeError:
        return {"erro": "Erro ao decodificar JSON retornado"}

@app.get('/bordero')
def show_bordero(id_partida:str):
    return get_bordero(id_partida)

@app.get('/extract_bordero', response_class=PlainTextResponse)
def extract_bordero_from_file(id_partida:str):
    return extract_bordero(id_partida)
