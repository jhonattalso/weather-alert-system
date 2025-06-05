import json
import datetime
from db import conectar

def exportar_reportes_comunidade():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, id_usuario, tipo_desastre, localizacao
                FROM ReporteComunidade
            """)
            dados = cursor.fetchall()
            colunas = [desc[0].lower() for desc in cursor.description]

            resultados = [dict(zip(colunas, row)) for row in dados]

            with open("data/reportes.json", "w", encoding="utf-8") as f:
                json.dump(resultados, f, ensure_ascii=False, indent=4)

            print("✔ Exportado: reportes.json")
        except Exception as e:
            print("Erro ao exportar reportes:", e)
        finally:
            conn.close()
            
def exportar_clima_recente():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT localidade FROM DadosAPIMeteorologia")
            locais = [row[0] for row in cursor.fetchall()]

            if not locais:
                print("Nenhuma localidade cadastrada ainda.")
                return

            print("\nEscolha uma localidade:")
            for i, loc in enumerate(locais, 1):
                print(f"{i}. {loc}")

            escolha = int(input("Digite o número correspondente: "))
            localidade = locais[escolha - 1]

            cursor.execute("""
                SELECT data_coleta, temperatura, umidade, condicoes_gerais, localidade
                FROM DadosAPIMeteorologia
                WHERE data_coleta >= (SYSTIMESTAMP - INTERVAL '3' HOUR)
                AND UPPER(localidade) = UPPER(:loc)
                ORDER BY data_coleta DESC
            """, loc = localidade)
            
            dados = cursor.fetchall()
            colunas = [desc[0].lower() for desc in cursor.description]
            resultados = [dict(zip(colunas, row)) for row in dados]

            for item in resultados:
                if isinstance(item["data_coleta"], datetime.datetime):
                    item["data_coleta"] = item["data_coleta"].isoformat()
            
            cidade = localidade.split("/")[-1].lower()
            nome_arquivo = f"data/clima/clima_recente_{cidade}.json"

            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(resultados, f, ensure_ascii=False, indent=4)

            print(f"✔ Exportado: {nome_arquivo}")
        except Exception as e:
            print("Erro ao exportar clima recente:", e)
        finally:
            conn.close()

def exportar_abrigos():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, capacidade, endereco, status
                FROM AbrigoTemporario
            """)
            dados = cursor.fetchall()
            colunas = [desc[0].lower() for desc in cursor.description]

            resultados = [dict(zip(colunas, row)) for row in dados]

            with open("data/abrigos.json", "w", encoding="utf-8") as f:
                json.dump(resultados, f, ensure_ascii=False, indent=4)

            print("✔ Exportado: abrigos.json")
        except Exception as e:
            print("Erro ao exportar abrigos:", e)
        finally:
            conn.close()
            
def menu_json():
    while True:
        print("\n--- Exportação de Dados para JSON ---")
        print("1. Exportar Reportes da Comunidade")
        print("2. Exportar Clima Recente (últimas 3h por localidade)")
        print("3. Exportar Abrigos Temporários")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exportar_reportes_comunidade()
        elif opcao == "2":
            exportar_clima_recente()
        elif opcao == "3":
            exportar_abrigos()
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_json()
