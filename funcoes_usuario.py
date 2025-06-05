from db import conectar
from datetime import datetime

def menu_usuario():
    while True:
        print("\n--- Menu do Usuário ---")
        print("1. Reportar desastre")
        print("2. Ver reportes da comunidade")
        print("3. Listar abrigos disponíveis")
        print("4. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            reportar_desastre()
        elif opcao == "2":
            listar_reportes()
        elif opcao == "3":
            listar_abrigos()
        elif opcao == "4":
            break
        else:
            print("Opção inválida!")

def reportar_desastre():
    tipo = input("Tipo de desastre (Enchente, Deslizamento, Seca, Incêndio Florestal): ").title()
    local = input("Localização: ")
    descricao = input("Descrição do ocorrido: ")

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO ReporteComunidade (tipo_desastre, localizacao, descricao, data_reporte)
                     VALUES (:1, :2, :3, :4)"""
            cursor.execute(sql, (tipo, local, descricao, datetime.now()))
            conn.commit()
            print("Desastre reportado com sucesso!")
        except Exception as e:
            print("Erro ao reportar desastre:", e)
        finally:
            conn.close()

def listar_reportes():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, tipo_desastre, localizacao, data_reporte FROM ReporteComunidade")
            rows = cursor.fetchall()
            print("\n--- Reportes da Comunidade ---")
            for row in rows:
                print(f"ID: {row[0]}, Tipo: {row[1]}, Local: {row[2]}, Data: {row[3]}")
        except Exception as e:
            print("Erro ao buscar reportes:", e)
        finally:
            conn.close()

def listar_abrigos():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, capacidade, endereco FROM AbrigoTemporario WHERE status = 'Ativo'")
            rows = cursor.fetchall()
            print("\n--- Abrigos Disponíveis ---")
            for row in rows:
                print(f"ID: {row[0]}, Nome: {row[1]}, Capacidade: {row[2]}, Endereço: {row[3]}\n")
        except Exception as e:
            print("Erro ao buscar abrigos:", e)
        finally:
            conn.close()
