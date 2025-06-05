from funcoes_usuario import menu_usuario
from funcoes_admin import menu_admin
import exportar_json

def autenticar_admin():
    tentativas = 3
    while tentativas > 0:
        user = input("Usuário admin: ").strip()
        senha = input("Senha: ").strip()
        if user == "admin" and senha == "admin":
            print("\n✅ Login de administrador bem-sucedido.\n")
            return True
        else:
            tentativas -= 1
            print(f"\n❌ Usuário ou senha incorretos! Tentativas restantes: {tentativas}")
    print("\n⛔ Acesso negado. Voltando ao menu principal.\n")
    return False

def menu_principal():
    while True:
        print("\n=== Bem-vindo ao Echo Report ===")
        print("1. Acessar como Usuário")
        print("2. Acessar como Administrador")
        print("3. Exportarções para JSON")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_usuario()

        elif opcao == "2":
            if autenticar_admin():
                menu_admin()
                
        elif opcao == "3":
            exportar_json.menu_json()
            
        elif opcao == "4":
            print("👋 Saindo do sistema. Até logo!")
            break

        else:
            print("⚠️ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu_principal()
