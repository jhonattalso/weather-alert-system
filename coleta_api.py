import requests
import datetime
from db import conectar

API_KEY = "0f9e04d27069c5dafbc255ad81086a2e"

# Cidades que podem ser consultadas
localidades = [
    {"nome": "São Paulo", "uf": "SP"},
    {"nome": "Rio de Janeiro", "uf": "RJ"},
    {"nome": "Belo Horizonte", "uf": "MG"}
]

def coletar_e_salvar_dados():
    for local in localidades:
        cidade = local["nome"].strip()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade},BR&appid={API_KEY}&units=metric&lang=pt_br"

        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                dados = resposta.json()
                temperatura = dados["main"]["temp"]
                umidade = dados["main"]["humidity"]
                condicoes = dados["weather"][0]["description"]
                data_coleta = datetime.datetime.now()
                localidade = f"{cidade}/{local['uf']}"

                # Inserir no banco
                salvar_no_banco(data_coleta, temperatura, umidade, condicoes, localidade)

            else:
                print(f"Erro ao buscar dados de {cidade}: {resposta.status_code}")

        except Exception as e:
            print(f"Erro de conexão com API para {cidade}: {e}")

def salvar_no_banco(data_coleta, temperatura, umidade, condicoes, localidade):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO DadosAPIMeteorologia (data_coleta, temperatura, umidade, condicoes_gerais, localidade)
                VALUES (:1, :2, :3, :4, :5)
            """, (data_coleta, temperatura, umidade, condicoes, localidade))
            conn.commit()
            # print(f"Dados salvos para {localidade} com sucesso.")
        except Exception as e:
            print("Erro ao salvar no banco:", e)
        finally:
            conn.close()

if __name__ == "__main__":
    coletar_e_salvar_dados()
