import cx_Oracle

def conectar():
    try:
        dsn = cx_Oracle.makedsn("oracle.fiap.com.br", 1521, service_name="ORCL")  # personalize
        conexao = cx_Oracle.connect(user="RM560277", password="070505", dsn=dsn)
        return conexao
    except cx_Oracle.Error as erro:
        print("Erro ao conectar ao banco:", erro)
        return None
