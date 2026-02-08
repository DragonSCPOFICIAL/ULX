import tkinter as tk
from tkinter import ttk

class ULXVisualEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("ULX Visual Editor - Drag & Drop Design")
        self.root.geometry("1200x800")
        
        # Layout Principal
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        # Barra de Ferramentas (Esquerda)
        self.toolbar = ttk.Frame(self.paned, width=200, relief=tk.SUNKEN)
        self.paned.add(self.toolbar)
        
        ttk.Label(self.toolbar, text="Componentes", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        components = ["Botão", "Texto", "Imagem", "Campo de Entrada", "Sprite de Jogo"]
        for comp in components:
            btn = ttk.Button(self.toolbar, text=comp, command=lambda c=comp: self.add_component(c))
            btn.pack(fill=tk.X, padx=5, pady=2)
            
        # Área de Design (Centro)
        self.canvas = tk.Canvas(self.paned, bg="white", width=800, height=600)
        self.paned.add(self.canvas)
        
        # Propriedades (Direita)
        self.props = ttk.Frame(self.paned, width=200, relief=tk.SUNKEN)
        self.paned.add(self.props)
        ttk.Label(self.props, text="Propriedades", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        # Botão de Exportar
        ttk.Button(self.props, text="Gerar Código ULX", command=self.generate_code).pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    def add_component(self, name):
        # Simulação de adicionar componente visual
        x, y = 100, 100
        if name == "Botão":
            self.canvas.create_rectangle(x, y, x+100, y+40, fill="#ddd", outline="black", tags="comp")
            self.canvas.create_text(x+50, y+20, text="Botão")
        elif name == "Texto":
            self.canvas.create_text(x+50, y+20, text="Texto de Exemplo", font=("Helvetica", 10))
        print(f"[EDITOR] Adicionado: {name}")

    def generate_code(self):
        code = """
func main() {
    ulx_init("Meu App Visual", 800, 600)
    // Código gerado automaticamente pelo Visual Editor
    ui_label("Olá do Editor Visual!", {100, 100}, 20)
    ulx_render()
}
"""
        print("--- CÓDIGO ULX GERADO ---")
        print(code)
        tk.messagebox.showinfo("Sucesso", "Código ULX gerado com sucesso! Pronto para compilar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ULXVisualEditor(root)
    root.mainloop()
