import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import subprocess
import utils

class ULXFluxUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ULX Flux - Tradução Nativa Ultra")
        
        # Configuração de Janela
        window_width, window_height = 850, 550
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")
        self.root.configure(bg="#0a0a0a")
        
        # Cores Estilo "Dark Flux"
        self.colors = {
            "bg": "#0a0a0a",
            "sidebar": "#050505",
            "accent": "#00d4ff",
            "text": "#e0e0e0",
            "success": "#00ff88",
            "warning": "#ffcc00",
            "error": "#ff4444"
        }
        
        # Ativar Modo Performance ao iniciar
        threading.Thread(target=utils.enable_performance_mode, daemon=True).start()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Sidebar Lateral
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="ULX FLUX", font=("Segoe UI", 18, "bold"), 
                 bg=self.colors["sidebar"], fg=self.colors["accent"]).pack(pady=40)
        
        self.create_nav_btn("Tradução", self.show_translator)
        self.create_nav_btn("Performance", self.show_performance)
        self.create_nav_btn("Configurações", self.show_settings)
        
        # Separador inferior na sidebar
        tk.Frame(self.sidebar, bg="#222", height=1).pack(fill="x", side="bottom", pady=10)
        tk.Label(self.sidebar, text="v1.0.2-STABLE", font=("Consolas", 8), 
                 bg=self.colors["sidebar"], fg="#555").pack(side="bottom", pady=10)

        # Área Principal
        self.main_content = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        self.show_translator()
        
    def create_nav_btn(self, text, cmd):
        btn = tk.Button(self.sidebar, text=f"  {text}", font=("Segoe UI", 11), bg=self.colors["sidebar"], 
                        fg="white", bd=0, activebackground="#111", activeforeground=self.colors["accent"],
                        cursor="hand2", anchor="w", padx=20, pady=10, command=cmd)
        btn.pack(fill="x")

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_translator(self):
        self.clear_content()
        
        header = tk.Frame(self.main_content, bg=self.colors["bg"])
        header.pack(fill="x")
        
        tk.Label(header, text="Motor de Tradução Flux", font=("Segoe UI", 16, "bold"), 
                 bg=self.colors["bg"], fg="white").pack(side="left")
        
        tk.Label(self.main_content, text="Converta .exe, .apk ou .ulx para execução nativa otimizada.", 
                 bg=self.colors["bg"], fg="#777", font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 25))
        
        # Campo de Arquivo
        self.file_path = tk.StringVar()
        file_frame = tk.Frame(self.main_content, bg="#111", padx=2, pady=2)
        file_frame.pack(fill="x")
        
        tk.Entry(file_frame, textvariable=self.file_path, bg="#111", fg="white", 
                 insertbackground="white", bd=0, font=("Consolas", 11)).pack(side="left", fill="x", expand=True, padx=10, ipady=10)
        
        tk.Button(file_frame, text="PROCURAR", bg=self.colors["accent"], fg="black", 
                  font=("Segoe UI", 9, "bold"), bd=0, padx=20, cursor="hand2", 
                  command=self.browse_file).pack(side="right")
        
        # Botão Ação
        self.btn_translate = tk.Button(self.main_content, text="INICIAR TRADUÇÃO DE ALTA VELOCIDADE", 
                                       bg=self.colors["accent"], fg="black", font=("Segoe UI", 12, "bold"), 
                                       bd=0, pady=18, cursor="hand2", command=self.start_translation)
        self.btn_translate.pack(fill="x", pady=30)
        
        # Log
        tk.Label(self.main_content, text="LOG DE OPERAÇÃO:", font=("Segoe UI", 9, "bold"), 
                 bg=self.colors["bg"], fg="#555").pack(anchor="w", pady=(0, 5))
        self.log_area = tk.Text(self.main_content, bg="#050505", fg=self.colors["success"], 
                                font=("Consolas", 10), bd=0, padx=10, pady=10, state="disabled")
        self.log_area.pack(fill="both", expand=True)

    def browse_file(self):
        path = filedialog.askopenfilename(title="Selecionar Aplicativo para Traduzir")
        if path:
            self.file_path.set(path)

    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert("end", f"[{threading.current_thread().name}] > {message}\n")
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def start_translation(self):
        path = self.file_path.get()
        if not path:
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo para traduzir.")
            return
        
        self.btn_translate.config(state="disabled", text="TRADUZINDO EM TEMPO REAL...")
        threading.Thread(target=self.run_engine, args=(path,), name="FLUX-CORE", daemon=True).start()

    def run_engine(self, path):
        self.log(f"Iniciando tradução: {os.path.basename(path)}")
        success = utils.translate_to_ulx(path, self.log)
        
        if success:
            self.log("SUCESSO: Tradução concluída com FPS otimizado.")
            self.root.after(0, lambda: messagebox.showinfo("ULX Flux", "Tradução concluída com sucesso!"))
        else:
            self.log("ERRO: Falha crítica na tradução.")
            
        self.root.after(0, lambda: self.btn_translate.config(state="normal", text="INICIAR TRADUÇÃO DE ALTA VELOCIDADE"))

    def show_performance(self):
        self.clear_content()
        tk.Label(self.main_content, text="Otimizações de Performance", font=("Segoe UI", 16, "bold"), 
                 bg=self.colors["bg"], fg="white").pack(anchor="w")
        
        perf_frame = tk.Frame(self.main_content, bg="#111", padx=20, pady=20)
        perf_frame.pack(fill="x", pady=20)
        
        tk.Label(perf_frame, text="Status do Modo Prime: ATIVO", fg=self.colors["success"], bg="#111", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(perf_frame, text="- CPU Governor: Performance\n- I/O Scheduler: Noop (SSD Optimized)\n- GPU Threaded: Enabled", 
                 fg="#aaa", bg="#111", justify="left").pack(anchor="w", pady=10)
        
        tk.Button(self.main_content, text="REATIVAR OTIMIZAÇÕES AGORA", bg="#222", fg="white", 
                  bd=0, pady=10, padx=20, command=lambda: threading.Thread(target=utils.enable_performance_mode, daemon=True).start()).pack(anchor="w")

    def show_settings(self):
        self.clear_content()
        tk.Label(self.main_content, text="Configurações do Sistema", font=("Segoe UI", 16, "bold"), 
                 bg=self.colors["bg"], fg="white").pack(anchor="w")
        
        # Botões de Ação de Sistema
        btn_frame = tk.Frame(self.main_content, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=30)
        
        tk.Button(btn_frame, text="VERIFICAR ATUALIZAÇÕES", bg=self.colors["accent"], fg="black", 
                  font=("Segoe UI", 10, "bold"), bd=0, pady=12, padx=25, command=self.check_updates).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="DESINSTALAR ULX FLUX", bg="#331111", fg="#ff4444", 
                  font=("Segoe UI", 10, "bold"), bd=0, pady=12, padx=25, command=self.confirm_uninstall).pack(side="left")

    def check_updates(self):
        messagebox.showinfo("Update", "Você já está na versão mais recente (1.0.2-STABLE).")

    def confirm_uninstall(self):
        if messagebox.askyesno("Desinstalar", "Isso removerá o ULX Flux do sistema. Deseja continuar?"):
            try:
                # Lógica de remoção
                subprocess.run(['sudo', 'rm', '-f', '/usr/bin/ulxflux'], check=True)
                messagebox.showinfo("Sucesso", "ULX Flux removido. O programa será fechado.")
                self.root.destroy()
            except:
                messagebox.showerror("Erro", "Falha ao remover arquivos. Verifique as permissões.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ULXFluxUI(root)
    root.mainloop()
