from db import conectar
import coleta_api

def menu_admin():
    while True:
        print("\n--- Menu do Administrador ---")
        print("1. Listar reportes da comunidade")
        print("2. Excluir um reporte")
        print("3. Cadastrar novo abrigo")
        print("4. Atualizar abrigo")
        print("5. Deletar abrigo")
        print("6. Ver dados meteorológicos por localidade")
        print("7. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_reportes()
        elif opcao == "2":
            excluir_reporte()
        elif opcao == "3":
            cadastrar_abrigo()
        elif opcao == "4":
            atualizar_abrigo()
        elif opcao == "5":
            deletar_abrigo()
        elif opcao == "6":
            ver_dados_meteorologicos()
        elif opcao == "7":
            break
        else:
            print("Opção inválida!")

# Listar todos os reportes feitos pelos usuários
def listar_reportes():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, tipo_desastre, localizacao, data_reporte FROM ReporteComunidade")
            rows = cursor.fetchall()
            print("\n--- Reportes da Comunidade ---")
            if rows:
                for row in rows:
                    print(f"ID: {row[0]} | Tipo: {row[1]} | Local: {row[2]} | Data: {row[3]}")
            else:
                print("Nenhum reporte encontrado")
        except Exception as e:
            print("Erro ao listar reportes:", e)
        finally:
            conn.close()

# Excluir reportes criados pelos usuários
def excluir_reporte():
    try:
        id_reporte = int(input("Digite o ID do reporte a ser excluído: "))
    except ValueError:
        print("ID inválido! Deve ser um número.")
        return
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ReporteComunidade WHERE id = :1", (id_reporte,))
            conn.commit()
            print("Reporte excluído com sucesso.")
        except Exception as e:
            print("Erro ao excluir reporte:", e)
        finally:
            conn.close()

# Cadastrar abrigos
def cadastrar_abrigo():
    nome = input("Nome do abrigo: ")
    capacidade = input("Capacidade: ")
    endereco = input("Endereço: ")
    status = input("Status (Ativo/Inativo): ").capitalize()

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO AbrigoTemporario (nome, capacidade, endereco, status)
                              VALUES (:1, :2, :3, :4)""", (nome, capacidade, endereco, status))
            conn.commit()
            print("Abrigo cadastrado com sucesso.")
        except Exception as e:
            print("Erro ao cadastrar abrigo:", e)
        finally:
            conn.close()

# Atualizar informações de abrigos
def atualizar_abrigo():
    id_abrigo = input("ID do abrigo que deseja atualizar: ")
    nome = input("Novo nome: ")
    capacidade = input("Nova capacidade: ")
    endereco = input("Novo endereço: ")
    status = input("Novo status (Ativo/Inativo): ").capitalize()

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""UPDATE AbrigoTemporario SET nome = :1, capacidade = :2, endereco = :3, status = :4
                              WHERE id = :5""", (nome, capacidade, endereco, status, id_abrigo))
            conn.commit()
            print(f"Abrigo '{nome}' atualizado com sucesso.")
        except Exception as e:
            print("Erro ao atualizar abrigo:", e)
        finally:
            conn.close()

# Excluir abrigos
def deletar_abrigo():
    id_abrigo = input("ID do abrigo a ser deletado: ")
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM AbrigoTemporario WHERE id = :1", (id_abrigo,))
            conn.commit()
            print("Abrigo deletado com sucesso.")
        except Exception as e:
            print("Erro ao deletar abrigo:", e)
        finally:
            conn.close()

# Ver a temperatura
def ver_dados_meteorologicos():
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
            coleta_api.coletar_e_salvar_dados()
            
            
            cursor.execute("""
                SELECT * FROM (
                    SELECT data_coleta, temperatura, umidade, condicoes_gerais
                    FROM DadosAPIMeteorologia
                    WHERE localidade LIKE :1
                    ORDER BY data_coleta DESC FETCH FIRST 5 ROWS ONLY
                )
                ORDER BY data_coleta ASC
            """, (f"%{localidade}%",)) #Acima, ordena os dados por data_coleta em ordem descrecente, e limita o resultado aos 5 registros mais recentes
            rows = cursor.fetchall()
            if rows:
                print("\n--- Últimos Dados Meteorológicos ---")
                for row in rows:
                    print(f"Data: {row[0]} | Temp: {row[1]}°C | Umidade: {row[2]}% | Condições: {row[3]}")
            else:
                print("Nenhum dado encontrado para essa localidade.")
        except Exception as e:
            print("Erro ao buscar dados:", e)
        finally:
            conn.close()
