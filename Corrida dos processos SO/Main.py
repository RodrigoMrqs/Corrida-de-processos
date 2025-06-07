# Import das bibliotecas utilizadas
# As bibliotecas Tkinter e Threading foram recomendações de colegas e também descobertas por conversa com IA
import tkinter as tk
from tkinter import ttk
import random
import time
import threading

# Quantum de tempo para Round Robin
QUANTUM = 2 

# Criação dos processdos dentro de uma lista 
PROCESSOS_BASE = [
    {"nome": "Ayrton Senna", "tempo_total": random.randint(5, 10)},
    {"nome": "Michael Schumacher", "tempo_total": random.randint(5, 10)},
    {"nome": "Lewis Hamilton", "tempo_total": random.randint(5, 10)},
    {"nome": "Max Verstappen", "tempo_total": random.randint(5, 10)},
    {"nome": "Alain Prost", "tempo_total": random.randint(5, 10)},
]

# Classe que carregar toda a interface gráfica do programa
class CorridaGUI:

    # Construtor para o menu
    def __init__(self, root):
        self.root = root
        self.root.title("Corrida dos Processos 🧠🏁")
        self.root.geometry("600x500")
        self.processos = []
        self.progressos = []
        self.labels = []
        self.politica = tk.StringVar(value="FIFO")
        self.criar_interface()

    # Método para criar a interface do jogo
    def criar_interface(self):

        # Gera a primeira parte onde o jogador pode escolher o tipo de escalonamento que será executado
        tk.Label(self.root, text="Escolha a política de escalonamento:", font=("Arial", 12)).pack(pady=10)
        tk.Radiobutton(self.root, text="FIFO", variable=self.politica, value="FIFO").pack()
        tk.Radiobutton(self.root, text="Round Robin", variable=self.politica, value="RR").pack()

        # Botão para iniciar o jogo
        self.btn_iniciar = tk.Button(self.root, text="Iniciar Corrida", command=self.iniciar_corrida)
        self.btn_iniciar.pack(pady=10)

        # Barra de progresso dos processos
        self.frame_corrida = tk.Frame(self.root)
        self.frame_corrida.pack(pady=10)

        # Ao fim da corrida, anuncia qual processo foi mais rápido
        self.resultado_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.resultado_label.pack(pady=10)

        # Botão para reiniciar a corrida
        self.btn_reiniciar = tk.Button(self.root, text="Reiniciar", command=self.reiniciar, state="disabled")
        self.btn_reiniciar.pack(pady=5)

    # Método para ajustar os processos e a barra de progreção 
    def setup_corrida(self):

        # Realiza a limpeza da corrida anterior para criara  nova corrida
        self.processos.clear()
        for widget in self.frame_corrida.winfo_children():
            widget.destroy()
        self.progressos.clear()
        self.labels.clear()

        # Recarrega os processos com seus novos tempos de execução
        for p in PROCESSOS_BASE:
            processo = {
                "nome": p["nome"],
                "tempo_total": p["tempo_total"],
                "executado": 0,
                "concluido": False
            }

            # Gera a barra de progresso da corrida
            # A barra de progressão foi feita com ajuda do ChatGPT
            self.processos.append(processo)

            label = tk.Label(self.frame_corrida, text=f"{p['nome']} (0/{p['tempo_total']})")
            label.pack()
            self.labels.append(label)

            pb = ttk.Progressbar(self.frame_corrida, maximum=p["tempo_total"], length=400)
            pb.pack(pady=2)
            self.progressos.append(pb)

    # Método para atualizar a interface conforme a corrida ocorre
    def atualizar_interface(self):
        for i, processo in enumerate(self.processos):
            self.labels[i].config(text=f"{processo['nome']} ({processo['executado']}/{processo['tempo_total']})")
            self.progressos[i]["value"] = processo["executado"]

    # Métood para iniciar a corrida quando o botão é pressionado 
    def iniciar_corrida(self):
        self.resultado_label.config(text="")
        self.btn_iniciar.config(state="disabled")
        self.btn_reiniciar.config(state="disabled")
        self.setup_corrida()
        threading.Thread(target=self.executar_corrida).start()

    # Define de que forma a corrida vai ocorrer de acordo com o tipo de escalonamento selecionado
    def executar_corrida(self):
        if self.politica.get() == "FIFO":
            self.executar_fifo()
        elif self.politica.get() == "RR":
            self.executar_round_robin()

        # Ao fim da corrida, exibe o vencedor
        vencedor = min(self.processos, key=lambda p: p["executado"])
        self.resultado_label.config(text=f"🏆 Vencedor: {vencedor['nome']} com {vencedor['executado']} unidades de CPU!")
        self.btn_reiniciar.config(state="normal")

    # Método para execução do FIFO
    def executar_fifo(self):
        for processo in self.processos:
            while processo["executado"] < processo["tempo_total"]:
                processo["executado"] += 1
                self.atualizar_interface()
                time.sleep(0.2)
            processo["concluido"] = True

    # Método para o round robin dos processos
    def executar_round_robin(self):
        while any(not p["concluido"] for p in self.processos):
            for processo in self.processos:
                if processo["concluido"]:
                    continue
                for _ in range(QUANTUM):
                    if processo["executado"] < processo["tempo_total"]:
                        processo["executado"] += 1
                        self.atualizar_interface()
                        time.sleep(0.2)
                if processo["executado"] >= processo["tempo_total"]:
                    processo["concluido"] = True

    # Botão reiniciar no fim da tela para realizar outras corridas
    def reiniciar(self):
        # Sorteio de novos tempos para os processos
        for i, p in enumerate(PROCESSOS_BASE):
            p["tempo_total"] = random.randint(5, 10)
        self.resultado_label.config(text="")
        self.iniciar_corrida()


# Local onde o jogo é iniciado, urando a biblioteca tkinter dentro da classe CorridaGUI

# root é utilizado para criar a janela com o tkinter
root = tk.Tk()
# Cria a janela do jogo passando a root como parametro para usar as funções da biblioteca
app = CorridaGUI(root)
# Loop para manter o jogo funcionando e permitir interação do usuário
root.mainloop()
