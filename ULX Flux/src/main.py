import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import subprocess
import utils

class ULXFluxUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ULX Flux v1.0 - Camada de Tradução Nativa (Performance Mode)")
        
        # Configuração de Janela (Seguindo o estilo compacto e funcional)
        window_width, window_height = 800, 500
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f0f")
        
        # Cores do Projeto ULX
        self.colors = {
            "bg": "#0f0f0f",
            "sidebar": "#050505",
            "accent": "#00D4FF", # Azul Flux
            "text": "#ffffff",
            "success": "#50fa7b"
        }
        
        # Inicializar Modo Performance
        print("[ULX FLUX] Ativando Modo Prime...")
        utils.enable_performance_mode()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=200)
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="ULX FLUX", font=("Segoe UI", 16, "bold"), 
                 bg=self.colors["sidebar"], fg=self.colors["accent"]).pack(pady=30)
        
        self.create_nav_btn("Tradução", self.show_translator)
        self.create_nav_btn("Configurações", self.show_settings)
        self.create_nav_btn("Sobre", self.show_about)
        
        # Área de Conteúdo Principal
        self.main_content = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.show_translator()

    def create_nav_btn(self, text, cmd):
        btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 10), bg=self.colors["sidebar"], 
                        fg="white", bd=0, activebackground=self.colors["accent"], 
                        cursor="hand2", anchor="w", padx=20, command=cmd)
        btn.pack(fill="x", pady=5)

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_translator(self):
        self.clear_content()
        tk.Label(self.main_content, text="Motor de Tradução ULX", font=("Segoe UI", 14, "bold"), 
                 bg=self.colors["bg"], fg="white").pack(anchor="w")
        
        tk.Label(self.main_content, text="Selecione um binário ou script para traduzir para o ecossistema ULX:", 
                 bg=self.colors["bg"], fg="#888", font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 20))
        
        self.file_path = tk.StringVar()
        file_frame = tk.Frame(self.main_content, bg=self.colors["bg"])
        file_frame.pack(fill="x")
        
        tk.Entry(file_frame, textvariable=self.file_path, bg="#1a1a1a", fg="white", 
                 insertbackground="white", bd=0, font=("Consolas", 10)).pack(side="left", fill="x", expand=True, ipady=8)
        
        tk.Button(file_frame, text="Procurar", bg=self.colors["accent"], fg="black", 
                  font=("Segoe UI", 9, "bold"), bd=0, padx=15, cursor="hand2", 
                  command=self.browse_file).pack(side="right", padx=10)
        
        self.btn_translate = tk.Button(self.main_content, text="INICIAR TRADUÇÃO FLUX", 
                                       bg=self.colors["accent"], fg="black", font=("Segoe UI", 12, "bold"), 
                                       bd=0, pady=15, cursor="hand2", command=self.start_translation)
        self.btn_translate.pack(fill="x", pady=30)
        
        self.log_area = tk.Text(self.main_content, bg="#050505", fg=self.colors["success"], 
                                font=("Consolas", 9), bd=0, state="disabled")
        self.log_area.pack(fill="both", expand=True)

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.set(path)

    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert("end", f"> {message}\n")
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def start_translation(self):
        path = self.file_path.get()
        if not path:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro!")
            return
        
        self.btn_translate.config(state="disabled", text="TRADUZINDO...")
        threading.Thread(target=self.run_engine, args=(path,), daemon=True).start()

    def run_engine(self, path):
        self.log(f"Iniciando tradução de: {os.path.basename(path)}")
        
        # Integração com a arquitetura ULX -> CLX -> LNX
        success = utils.translate_to_ulx(path, self.log)
        
        if success:
            self.log("Tradução concluída com sucesso!")
            self.log(f"Saída gerada: {path}.ulx")
            self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Tradução para ULX finalizada!"))
        else:
            self.log("Erro durante a tradução.")
            
        self.root.after(0, lambda: self.btn_translate.config(state="normal", text="INICIAR TRADUÇÃO FLUX"))

    def show_settings(self):
        self.clear_content()
        tk.Label(self.main_content, text="Configurações do Flux", font=("Segoe UI", 14, "bold"), 
                 bg=self.colors["bg"], fg="white").pack(anchor="w")
        
        # Opções de otimização
        tk.Checkbutton(self.main_content, text="Otimização Extrema de CPU", bg=self.colors["bg"], 
                       fg="white", selectcolor="#1a1a1a", activebackground=self.colors["bg"]).pack(anchor="w", pady=10)
        tk.Checkbutton(self.main_content, text="Tradução em Tempo Real (JIT)", bg=self.colors["bg"], 
                       fg="white", selectcolor="#1a1a1a", activebackground=self.colors["bg"]).pack(anchor="w", pady=10)

        # Seção de Gerenciamento do Sistema
        tk.Label(self.main_content, text="Gerenciamento do Sistema", font=("Segoe UI", 11, "bold"), 
                 bg=self.colors["bg"], fg="#888").pack(anchor="w", pady=(30, 10))
        
        tk.Button(self.main_content, text="DESINSTALAR ULX FLUX COMPLETAMENTE", 
                  bg="#B43D3D", fg="white", font=("Segoe UI", 9, "bold"), 
                  bd=0, pady=10, padx=20, cursor="hand2", command=self.confirm_uninstall).pack(anchor="w")

    def confirm_uninstall(self):
        if messagebox.askyesno("Desinstalar", "Isso removerá o ULX Flux e todos os seus componentes do sistema. Continuar?"):
            self.run_uninstall()

    def run_uninstall(self):
        try:
            # Comando para remover tudo (precisa de sudo para /opt e /usr/bin)
            # Como o app roda como usuário, usamos pkexec ou sudo via shell
            cmd = "sudo rm -f /usr/bin/ulxflux && sudo rm -f /usr/share/applications/ulxflux.desktop && sudo rm -rf /opt/ulxflux"
            subprocess.run(['sh', '-c', cmd], check=True)
            messagebox.showinfo("Sucesso", "ULX Flux foi removido. O aplicativo será fechado.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao desinstalar: {e}")

    def show_about(self):
        self.clear_content()
        tk.Label(self.main_content, text="Sobre o ULX Flux", font=("Segoe UI", 14, "bold"), 
                 bg=self.colors["bg"], fg="white").pack(anchor="w")
        tk.Label(self.main_content, text="Desenvolvido por: DragonSCPOFICIAL\nVersão: 1.0-ULTRA\n\nUma camada de tradução nativa para o ecossistema ULX.", 
                 bg=self.colors["bg"], fg="#ccc", justify="left").pack(anchor="w", pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ULXFluxUI(root)
    root.mainloop()
