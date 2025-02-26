import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Configurações do backend
BACKEND_URL = "http://127.0.0.1:5000"

def fazer_login():
    nome_user = entry_nome_user.get()
    senha = entry_senha.get()

    try:
        response = requests.post(f"{BACKEND_URL}/login", json={"nome_user": nome_user, "senha": senha})
        response.raise_for_status()
        data = response.json()
        messagebox.showinfo("Sucesso", data['message'])
        abrir_interface(data['perfil'], data['id_user'])
    except requests.exceptions.HTTPError:
        messagebox.showerror("Erro", "Credenciais inválidas!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def abrir_interface(perfil, id_user):
    login_window.destroy()
    
    window = tk.Tk()
    window.title(f"Área do {perfil.capitalize()}")

    tk.Label(window, text=f"Bem-vindo, {perfil.capitalize()}!", font=("Arial", 14)).pack(pady=10)

    if perfil in ['Administrador', 'Gerente', 'Operador']:
        tk.Button(window, text="Ver Itens", command=lambda: ver_tabela("itens", perfil)).pack(pady=5)
        tk.Button(window, text="Ver Locais", command=lambda: ver_tabela("locais", perfil)).pack(pady=5)

    if perfil in ['Administrador', 'Gerente']:
        tk.Button(window, text="Ver Logs de Auditoria", command=lambda: ver_tabela("logs", perfil)).pack(pady=5)
        tk.Button(window, text="Ver Movimentações", command=lambda: ver_tabela("movimentacoes", perfil)).pack(pady=5)

    if perfil == 'Administrador':
        tk.Button(window, text="Ver Usuários", command=lambda: ver_tabela("usuarios", perfil)).pack(pady=5)

    if perfil in ['Administrador', 'Gerente']:
        tk.Button(window, text="Adicionar Item", command=adicionar_item).pack(pady=5)
        tk.Button(window, text="Remover Item", command=remover_item).pack(pady=5)
        tk.Button(window, text="Mover Item", command=mover_item).pack(pady=5)

    window.mainloop()

def ver_tabela(tabela, perfil):
    try:
        response = requests.get(f"{BACKEND_URL}/{tabela}", headers={"Perfil": perfil})
        response.raise_for_status()
        dados = response.json()
        exibir_tabela(tabela, dados)
    except requests.exceptions.HTTPError:
        messagebox.showerror("Erro", "Não foi possível carregar os dados da tabela.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def exibir_tabela(nome_tabela, dados):
    tabela_window = tk.Toplevel()
    tabela_window.title(f"Tabela {nome_tabela.capitalize()}")

    colunas = list(dados[0].keys()) if dados else []
    tree = ttk.Treeview(tabela_window, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for item in dados:
        tree.insert("", "end", values=tuple(item.values()))

    tree.pack(expand=True, fill="both")
    tabela_window.mainloop()

def adicionar_item():
    def enviar():
        nome = entry_nome.get()
        descricao = entry_desc.get()
        local = entry_local.get()

        try:
            response = requests.post(f"{BACKEND_URL}/itens", json={"nome": nome, "descricao": descricao, "local": local})
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Item adicionado com sucesso!")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    add_window = tk.Toplevel()
    add_window.title("Adicionar Item")

    tk.Label(add_window, text="Nome:").pack()
    entry_nome = tk.Entry(add_window)
    entry_nome.pack()

    tk.Label(add_window, text="Descrição:").pack()
    entry_desc = tk.Entry(add_window)
    entry_desc.pack()

    tk.Label(add_window, text="Local:").pack()
    entry_local = tk.Entry(add_window)
    entry_local.pack()

    tk.Button(add_window, text="Adicionar", command=enviar).pack(pady=5)

def remover_item():
    def carregar_itens():
        try:
            response = requests.get(f"{BACKEND_URL}/itens")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return []

    def deletar():
        item_id = lista_itens.get(tk.ACTIVE).split(" - ")[0]
        try:
            response = requests.delete(f"{BACKEND_URL}/itens/{item_id}")
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Item removido com sucesso!")
            remove_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    itens = carregar_itens()

    remove_window = tk.Toplevel()
    remove_window.title("Remover Item")

    lista_itens = tk.Listbox(remove_window)
    for item in itens:
        lista_itens.insert(tk.END, f"{item['id']} - {item['nome']}")
    lista_itens.pack()

    tk.Button(remove_window, text="Remover", command=deletar).pack(pady=5)

def mover_item():
    def carregar_dados():
        try:
            itens = requests.get(f"{BACKEND_URL}/itens").json()
            locais = requests.get(f"{BACKEND_URL}/locais").json()
            return itens, locais
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return [], []

    def transferir():
        item_id = lista_itens.get(tk.ACTIVE).split(" - ")[0]
        novo_local = lista_locais.get(tk.ACTIVE).split(" - ")[0]

        try:
            response = requests.put(f"{BACKEND_URL}/itens/{item_id}/mover", json={"novo_local": novo_local})
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Item movido com sucesso!")
            mover_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    itens, locais = carregar_dados()

    mover_window = tk.Toplevel()
    mover_window.title("Mover Item")

    tk.Label(mover_window, text="Selecione um Item:").pack()
    lista_itens = tk.Listbox(mover_window)
    for item in itens:
        lista_itens.insert(tk.END, f"{item['id']} - {item['nome']}")
    lista_itens.pack()

    tk.Label(mover_window, text="Novo Local:").pack()
    lista_locais = tk.Listbox(mover_window)
    for local in locais:
        lista_locais.insert(tk.END, f"{local['id']} - {local['nome']}")
    lista_locais.pack()

    tk.Button(mover_window, text="Mover", command=transferir).pack(pady=5)

# Interface de login
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Nome de Usuário:").grid(row=0, column=0)
entry_nome_user = tk.Entry(login_window)
entry_nome_user.grid(row=0, column=1)

tk.Label(login_window, text="Senha:").grid(row=1, column=0)
entry_senha = tk.Entry(login_window, show="*")
entry_senha.grid(row=1, column=1)

tk.Button(login_window, text="Login", command=fazer_login).grid(row=2, column=0, columnspan=2)

# Inicia o loop principal
login_window.mainloop()
