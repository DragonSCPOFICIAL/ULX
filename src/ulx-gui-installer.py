import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import shutil

def install_package(pkg_path):
    # Simulação de instalação nativa
    app_name = os.path.basename(pkg_path).replace(".ulx", "")
    install_path = f"/opt/ulx-apps/{app_name}"
    
    try:
        if not os.path.exists("/opt/ulx-apps"):
            os.makedirs("/opt/ulx-apps")
        
        # Simula a cópia e integração
        print(f"Instalando {app_name} em {install_path}...")
        # shutil.copy(pkg_path, install_path) # Seria o comando real
        
        messagebox.showinfo("Sucesso", f"O aplicativo '{app_name}' foi instalado com sucesso e já está disponível no seu menu!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao instalar: {str(e)}")

def run_gui():
    global root
    root = tk.Tk()
    root.title("Instalador de Aplicativos ULX")
    root.geometry("400x250")
    root.resizable(False, False)

    if len(sys.argv) < 2:
        messagebox.showwarning("Aviso", "Nenhum pacote .ulx selecionado.")
        sys.exit(1)

    pkg_path = sys.argv[1]
    app_name = os.path.basename(pkg_path).replace(".ulx", "")

    # Estilo
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10))
    style.configure("TLabel", font=("Helvetica", 11))

    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    lbl_title = ttk.Label(frame, text=f"Deseja instalar o aplicativo?", font=("Helvetica", 12, "bold"))
    lbl_title.pack(pady=10)

    lbl_name = ttk.Label(frame, text=f"Nome: {app_name}", foreground="blue")
    lbl_name.pack(pady=5)

    lbl_info = ttk.Label(frame, text="Este aplicativo será instalado nativamente no seu sistema.", wraplength=350)
    lbl_info.pack(pady=10)

    btn_install = ttk.Button(frame, text="Instalar Agora", command=lambda: install_package(pkg_path))
    btn_install.pack(side=tk.LEFT, padx=20, pady=20)

    btn_cancel = ttk.Button(frame, text="Cancelar", command=root.destroy)
    btn_cancel.pack(side=tk.RIGHT, padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
