import tkinter as tk
from tkinter import messagebox, ttk
import random
import math

# Dados da roleta
numeros_roleta = [str(i) for i in range(0, 37)]

# Cores fixas: 0=branco, ímpares=vermelho, pares=preto
def obter_cor(numero):
    if numero == "0":
        return "white"
    elif int(numero) % 2 == 1:  # ímpar
        return "red"
    else:  # par
        return "black"

cores = {str(i): obter_cor(str(i)) for i in range(37)}

class RoletaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 ROLETA PREMIUM CASINO 🎰")
        self.root.geometry("800x900")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a0a0a")

        self.saldo = 100
        self.angulo_atual = 0
        self.velocidade = 0
        self.animando = False
        self.setores = len(numeros_roleta)
        self.brilho = 0
        self.confetes = []
        self.luzes_piscando = False
        self.numero_vencedor = None
        self.historico = []
        self.vitorias = 0
        self.derrotas = 0
        self.maior_ganho = 0

        # Título
        title_frame = tk.Frame(root, bg="#0a0a0a")
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="🎰 ROLETA PREMIUM 🎰", font=("Arial", 24, "bold"), 
                fg="#FFD700", bg="#0a0a0a").pack()

        # Canvas com borda dourada
        canvas_frame = tk.Frame(root, bg="#FFD700", relief="raised", bd=3)
        canvas_frame.pack(pady=20)
        self.canvas = tk.Canvas(canvas_frame, width=500, height=500, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)
        self.raio = 230
        self.centro = (250, 250)

        # Painel de controles
        control_frame = tk.Frame(root, bg="#1a1a1a", relief="raised", bd=2)
        control_frame.pack(pady=20, padx=50, fill="x")

        # Saldo
        saldo_frame = tk.Frame(control_frame, bg="#1a1a1a")
        saldo_frame.pack(pady=10)
        self.label_saldo = tk.Label(saldo_frame, text=f"💰 SALDO: R${self.saldo}", 
                                   font=("Arial", 18, "bold"), fg="#00FF00", bg="#1a1a1a")
        self.label_saldo.pack()

        # Valor da aposta
        valor_frame = tk.Frame(control_frame, bg="#1a1a1a")
        valor_frame.pack(pady=10)
        tk.Label(valor_frame, text="💵 Valor da Aposta:", font=("Arial", 12, "bold"), 
                fg="#FFFFFF", bg="#1a1a1a").pack()
        self.entry_valor = tk.Entry(valor_frame, font=("Arial", 14), width=10, justify="center",
                                   bg="#2a2a2a", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.entry_valor.insert(0, "10")
        self.entry_valor.pack(pady=5)

        # Tipo de aposta
        tipo_frame = tk.Frame(control_frame, bg="#1a1a1a")
        tipo_frame.pack(pady=15)
        tk.Label(tipo_frame, text="🎯 Tipo de Aposta:", font=("Arial", 12, "bold"), 
                fg="#FFFFFF", bg="#1a1a1a").pack()
        
        self.tipo_var = tk.StringVar(value="numero")
        radio_frame = tk.Frame(tipo_frame, bg="#1a1a1a")
        radio_frame.pack(pady=5)
        
        tk.Radiobutton(radio_frame, text="🔢 Número", variable=self.tipo_var, value="numero", 
                      command=self.desenhar_roleta, font=("Arial", 11), fg="#FFD700", 
                      bg="#1a1a1a", selectcolor="#2a2a2a").pack(side="left", padx=10)
        tk.Radiobutton(radio_frame, text="⚖️ Par/Ímpar", variable=self.tipo_var, value="par_impar", 
                      command=self.desenhar_roleta, font=("Arial", 11), fg="#FFD700", 
                      bg="#1a1a1a", selectcolor="#2a2a2a").pack(side="left", padx=10)
        tk.Radiobutton(radio_frame, text="🎨 Cor", variable=self.tipo_var, value="cor", 
                      command=self.desenhar_roleta, font=("Arial", 11), fg="#FFD700", 
                      bg="#1a1a1a", selectcolor="#2a2a2a").pack(side="left", padx=10)

        # Aposta
        aposta_frame = tk.Frame(control_frame, bg="#1a1a1a")
        aposta_frame.pack(pady=10)
        tk.Label(aposta_frame, text="🎲 Sua Aposta:", font=("Arial", 12, "bold"), 
                fg="#FFFFFF", bg="#1a1a1a").pack()
        
        # Frame para entrada e dica
        entrada_frame = tk.Frame(aposta_frame, bg="#1a1a1a")
        entrada_frame.pack()
        
        self.entry_aposta = tk.Entry(entrada_frame, font=("Arial", 14), width=20, justify="center",
                                    bg="#2a2a2a", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.entry_aposta.pack(pady=5)
        
        # Dica para apostas múltiplas
        tk.Label(entrada_frame, text="💡 Múltiplos números: 1,7,13,25", font=("Arial", 9), 
                fg="#888888", bg="#1a1a1a").pack()

        # Botão girar
        self.btn_girar = tk.Button(control_frame, text="🎯 GIRAR ROLETA 🎯", command=self.iniciar_giro,
                                  font=("Arial", 16, "bold"), bg="#FF4500", fg="#FFFFFF",
                                  relief="raised", bd=3, padx=30, pady=10,
                                  activebackground="#FF6500", activeforeground="#FFFFFF")
        self.btn_girar.pack(pady=20)

        # Botões extras
        extra_frame = tk.Frame(control_frame, bg="#1a1a1a")
        extra_frame.pack(pady=10)
        
        tk.Button(extra_frame, text="📊 Estatísticas", command=self.mostrar_stats,
                 font=("Arial", 10), bg="#4CAF50", fg="#FFFFFF", padx=15).pack(side="left", padx=5)
        tk.Button(extra_frame, text="📜 Histórico", command=self.mostrar_historico,
                 font=("Arial", 10), bg="#2196F3", fg="#FFFFFF", padx=15).pack(side="left", padx=5)
        tk.Button(extra_frame, text="💰 Reset Saldo", command=self.reset_saldo,
                 font=("Arial", 10), bg="#FF9800", fg="#FFFFFF", padx=15).pack(side="left", padx=5)

        # Resultado
        self.resultado_label = tk.Label(root, text="🎲 Faça sua aposta e gire a roleta! 🎲", 
                                       font=("Arial", 16, "bold"), fg="#FFD700", bg="#0a0a0a")
        self.resultado_label.pack(pady=20)

        self.desenhar_roleta()

    def desenhar_roleta(self):
        self.canvas.delete("all")
        
        # Fundo com efeito de luzes piscando
        borda_cor = "#FFFF00" if self.luzes_piscando else "#FFD700"
        self.canvas.create_oval(20, 20, 480, 480, fill="#2a2a2a", outline=borda_cor, width=5)
        
        angulo_por_setor = 360 / self.setores
        for i, numero in enumerate(numeros_roleta):
            inicio = self.angulo_atual + i * angulo_por_setor
            cor_base = cores.get(numero, "gray")
            
            # Destacar número vencedor
            is_vencedor = self.numero_vencedor == numero and not self.animando
            
            # Cores mais vibrantes
            if cor_base == "red":
                cor = "#FF0040" if is_vencedor else "#FF1744"
            elif cor_base == "black":
                cor = "#444444" if is_vencedor else "#212121"
            elif cor_base == "white":
                cor = "#FFFFFF" if is_vencedor else "#F0F0F0"
            else:  # green
                cor = "#00FF40" if is_vencedor else "#00C853"
            
            # Setor com borda especial para vencedor
            borda_setor = "#FFFF00" if is_vencedor else "#FFD700"
            largura_borda = 4 if is_vencedor else 2
            
            self.canvas.create_arc(
                self.centro[0] - self.raio, self.centro[1] - self.raio,
                self.centro[0] + self.raio, self.centro[1] + self.raio,
                start=inicio, extent=angulo_por_setor,
                fill=cor, outline=borda_setor, width=largura_borda
            )
            
            # Efeito de brilho nos setores
            if self.brilho > 0 or is_vencedor:
                brilho_extra = 50 if is_vencedor else self.brilho
                brilho_cor = f"#{min(255, int(cor[1:3], 16) + brilho_extra):02x}{min(255, int(cor[3:5], 16) + brilho_extra):02x}{min(255, int(cor[5:7], 16) + brilho_extra):02x}"
                self.canvas.create_arc(
                    self.centro[0] - self.raio + 10, self.centro[1] - self.raio + 10,
                    self.centro[0] + self.raio - 10, self.centro[1] + self.raio - 10,
                    start=inicio, extent=angulo_por_setor,
                    fill=brilho_cor, outline="", stipple="gray25"
                )

            # Números sempre visíveis com melhor contraste
            angulo_meio = math.radians(inicio + angulo_por_setor/2)
            raio_texto = self.raio * 0.8
            x = self.centro[0] + raio_texto * math.cos(angulo_meio)
            y = self.centro[1] + raio_texto * math.sin(angulo_meio)
            
            fonte_size = 16 if is_vencedor else 12
            # Cor do texto baseada no fundo para máximo contraste
            if cor_base == "red":
                cor_texto = "#FFFFFF"
            elif cor_base == "black":
                cor_texto = "#FFFFFF"
            elif cor_base == "white":
                cor_texto = "#000000"
            else:  # green
                cor_texto = "#FFFFFF"
            
            if is_vencedor:
                cor_texto = "#FFFF00"
            
            # Sombra preta forte para contraste
            self.canvas.create_text(x+1, y+1, text=numero, fill="#000000", font=("Arial", fonte_size, "bold"))
            self.canvas.create_text(x-1, y-1, text=numero, fill="#000000", font=("Arial", fonte_size, "bold"))
            # Texto principal
            self.canvas.create_text(x, y, text=numero, fill=cor_texto, font=("Arial", fonte_size, "bold"))

        # Centro da roleta com efeito especial
        centro_cor = "#FFFF00" if self.luzes_piscando else "#FFD700"
        for r in range(40, 0, -2):
            intensity = int(255 * (40-r) / 40)
            if self.luzes_piscando:
                cor_centro = f"#{intensity:02x}{intensity:02x}00"
            else:
                cor_centro = f"#{intensity:02x}{intensity//2:02x}00"
            self.canvas.create_oval(
                self.centro[0] - r, self.centro[1] - r,
                self.centro[0] + r, self.centro[1] + r,
                fill=cor_centro, outline=""
            )
        
        # Botão central interativo
        if not self.animando:
            # Círculo do botão com gradiente
            for r in range(35, 25, -1):
                alpha = (35-r) / 10
                cor_btn = f"#{int(255*alpha):02x}{int(200*alpha):02x}00"
                self.canvas.create_oval(
                    self.centro[0] - r, self.centro[1] - r,
                    self.centro[0] + r, self.centro[1] + r,
                    fill=cor_btn, outline="", tags="botao_central"
                )
            
            # Texto do botão
            logo = "💰" if self.luzes_piscando else "🎰"
            self.canvas.create_text(self.centro[0], self.centro[1]-5, text=logo, 
                                  font=("Arial", 16), tags="botao_central")
            self.canvas.create_text(self.centro[0], self.centro[1]+10, text="GIRAR", 
                                  font=("Arial", 8, "bold"), fill="#FFFFFF", tags="botao_central")
            
            # Bind do clique no botão
            self.canvas.tag_bind("botao_central", "<Button-1>", self.giro_rapido)
            self.canvas.tag_bind("botao_central", "<Enter>", self.hover_botao)
            self.canvas.tag_bind("botao_central", "<Leave>", self.leave_botao)
        else:
            # Durante animação, mostrar apenas logo
            logo = "💰" if self.luzes_piscando else "🎰"
            self.canvas.create_text(self.centro[0], self.centro[1], text=logo, font=("Arial", 20))

        # Ponteiro 3D com efeito
        ponteiro_cor = "#FFFF00" if self.luzes_piscando else "#FFD700"
        self.canvas.create_polygon(250, 30, 240, 60, 260, 60, fill=ponteiro_cor, outline="#B8860B", width=2)
        self.canvas.create_polygon(250, 30, 245, 50, 255, 50, fill="#FFFF00")
        
        # Marcadores externos piscando
        for i in range(8):
            angulo = i * 45
            x1 = self.centro[0] + 240 * math.cos(math.radians(angulo))
            y1 = self.centro[1] + 240 * math.sin(math.radians(angulo))
            x2 = self.centro[0] + 250 * math.cos(math.radians(angulo))
            y2 = self.centro[1] + 250 * math.sin(math.radians(angulo))
            cor_marcador = "#FFFF00" if self.luzes_piscando else "#FFD700"
            self.canvas.create_line(x1, y1, x2, y2, fill=cor_marcador, width=4)
            
        # Desenhar confetes
        self.desenhar_confetes()
        
    def desenhar_confetes(self):
        for confete in self.confetes:
            x, y, cor, tamanho = confete
            self.canvas.create_oval(x-tamanho, y-tamanho, x+tamanho, y+tamanho, fill=cor, outline="")
            
    def criar_confetes(self):
        self.confetes = []
        cores_confete = ["#FF0040", "#00FF40", "#0040FF", "#FFFF00", "#FF8000", "#8000FF"]
        for _ in range(50):
            x = random.randint(50, 450)
            y = random.randint(50, 450)
            cor = random.choice(cores_confete)
            tamanho = random.randint(3, 8)
            self.confetes.append([x, y, cor, tamanho])
            
    def animar_confetes(self, contador=0):
        if contador < 30:  # 30 frames de animação
            for confete in self.confetes:
                confete[1] += random.randint(2, 5)  # cair
                confete[0] += random.randint(-2, 2)  # balançar
                if confete[1] > 500:
                    confete[1] = random.randint(-20, 0)
                    confete[0] = random.randint(50, 450)
            self.desenhar_roleta()
            self.root.after(100, lambda: self.animar_confetes(contador + 1))
        else:
            self.confetes = []
            self.desenhar_roleta()
            
    def piscar_luzes(self, contador=0):
        if contador < 20:  # 20 piscadas
            self.luzes_piscando = not self.luzes_piscando
            self.desenhar_roleta()
            self.root.after(150, lambda: self.piscar_luzes(contador + 1))
        else:
            self.luzes_piscando = False
            self.numero_vencedor = None
            self.desenhar_roleta()
            
    def hover_botao(self, event):
        if not self.animando:
            self.canvas.config(cursor="hand2")
            
    def leave_botao(self, event):
        self.canvas.config(cursor="")
        
    def giro_rapido(self, event):
        if self.animando:
            return
            
        # Giro rápido com valor fixo de 10
        if self.saldo < 10:
            messagebox.showerror("❌ Saldo Insuficiente", "💰 Você precisa de pelo menos R$10 para girar!")
            return
            
        # Aposta automática nos números da sorte
        self.aposta_valor = 10
        self.aposta_tipo = "numero"
        self.aposta = "7,17,27"  # Múltiplos números da sorte
        
        # Feedback visual
        self.resultado_label.config(text="🎲 Giro rápido! Apostando R$10 nos números da sorte! 🎲")
        
        # Iniciar giro
        self.velocidade = random.uniform(15, 20)  # Giro mais rápido
        self.animando = True
        self.girar()

    def iniciar_giro(self):
        if self.animando:
            return

        try:
            valor = int(self.entry_valor.get())
            if valor <= 0 or valor > self.saldo:
                raise ValueError
        except ValueError:
            messagebox.showerror("❌ Erro", "💰 Digite um valor de aposta válido!")
            return
            
        aposta = self.entry_aposta.get().strip().lower()
        if not aposta:
            messagebox.showerror("❌ Erro", "🎯 Digite sua aposta!")
            return
            
        # Validar aposta baseada no tipo
        if not self.validar_aposta(aposta):
            return

        self.aposta_valor = valor
        self.aposta_tipo = self.tipo_var.get()
        self.aposta = aposta
        
        # Desabilitar botão durante o giro
        self.btn_girar.config(state="disabled", text="🌀 GIRANDO... 🌀")
        self.resultado_label.config(text="🎲 A roleta está girando... 🎲")

        self.velocidade = random.uniform(12, 18)
        self.animando = True
        self.girar()
        
        # Reabilitar botão após o giro
        self.root.after(6000, lambda: self.btn_girar.config(state="normal", text="🎯 GIRAR ROLETA 🎯"))

    def girar(self):
        if self.velocidade > 0.1:
            self.angulo_atual = (self.angulo_atual + self.velocidade) % 360
            # Efeito de brilho durante o giro
            self.brilho = int(20 * self.velocidade / 15)
            self.desenhar_roleta()
            self.velocidade *= 0.98  # desaceleração mais suave
            self.root.after(20, self.girar)  # animação mais fluida
        else:
            self.brilho = 0
            self.animando = False
            self.sortear_resultado()

    def sortear_resultado(self):
        escolhido = random.choice(numeros_roleta)
        cor = cores.get(escolhido, "gray")
        
        # Destacar número vencedor
        self.numero_vencedor = escolhido
        
        # Efeito visual no resultado
        cor_display = "🔴 VERMELHO" if cor == "red" else "⚫ PRETO" if cor == "black" else "⚪ BRANCO"
        self.resultado_label.config(text=f"🎯 RESULTADO: {escolhido} ({cor_display}) 🎯")

        ganhou = False
        ganho = 0

        if self.aposta_tipo == "numero":
            # Verificar apostas múltiplas
            numeros_apostados = [n.strip() for n in self.aposta.split(',')]
            if escolhido in numeros_apostados:
                ganhou = True
                # Pagamento ajustado para apostas múltiplas
                multiplicador = 35 // len(numeros_apostados) if len(numeros_apostados) > 1 else 35
                ganho = self.aposta_valor * multiplicador
        elif self.aposta_tipo == "par_impar":
            if escolhido == "0":
                ganhou = False
            else:
                numero = int(escolhido)
                if (numero % 2 == 0 and self.aposta == "par") or (numero % 2 == 1 and self.aposta in ["ímpar", "impar"]):
                    ganhou = True
                    ganho = self.aposta_valor * 2
        elif self.aposta_tipo == "cor":
            cor_nome = "vermelho" if cor == "red" else "preto" if cor == "black" else "branco"
            if self.aposta in [cor, cor_nome]:
                ganhou = True
                ganho = self.aposta_valor * 2

        # Atualizar estatísticas
        self.historico.append({
            'numero': escolhido,
            'cor': cor_display,
            'aposta': self.aposta,
            'tipo': self.aposta_tipo,
            'valor': self.aposta_valor,
            'ganhou': ganhou,
            'ganho': ganho if ganhou else -self.aposta_valor
        })
        
        if ganhou:
            self.saldo += ganho
            self.vitorias += 1
            if ganho > self.maior_ganho:
                self.maior_ganho = ganho
            self.label_saldo.config(fg="#00FF00")
            
            # EFEITOS DE VITÓRIA ESPETACULARES!
            self.criar_confetes()
            self.animar_confetes()
            self.piscar_luzes()
            
            # Som visual de vitória
            self.root.bell()
            
            # Mensagem de vitória com delay para mostrar efeitos
            self.root.after(1000, lambda: messagebox.showinfo("🎉 JACKPOT! 🎉", 
                f"🏆🎊 INCRÍVEL! Você ganhou R${ganho}! 🎊🏆\n💎 Que sorte fantástica! 💎"))
        else:
            self.saldo -= self.aposta_valor
            self.derrotas += 1
            self.label_saldo.config(fg="#FF4444")
            messagebox.showinfo("😔 Que pena!", f"💸 Você perdeu R${self.aposta_valor}\n🍀 Tente novamente!")

        self.label_saldo.config(text=f"💰 SALDO: R${self.saldo}")
        
        # Restaurar cor do saldo após 3 segundos
        self.root.after(3000, lambda: self.label_saldo.config(fg="#00FF00" if self.saldo > 0 else "#FF4444"))

        if self.saldo <= 0:
            messagebox.showinfo("🎮 FIM DE JOGO", "💔 Você perdeu todo o saldo! Tente novamente!")
            self.root.destroy()

    def validar_aposta(self, aposta):
        if self.aposta_tipo == "numero":
            numeros = aposta.split(',')
            for num in numeros:
                num = num.strip()
                if num not in [str(i) for i in range(37)]:
                    messagebox.showerror("❌ Erro", f"🔢 Número '{num}' inválido! Use 0-36")
                    return False
        elif self.aposta_tipo == "par_impar":
            if aposta not in ["par", "impar", "ímpar"]:
                messagebox.showerror("❌ Erro", "⚖️ Digite 'par' ou 'impar'!")
                return False
        elif self.aposta_tipo == "cor":
            if aposta not in ["red", "black", "white", "vermelho", "preto", "branco"]:
                messagebox.showerror("❌ Erro", "🎨 Digite 'vermelho', 'preto' ou 'branco'!")
                return False
        return True
        
    def mostrar_stats(self):
        total_jogos = len(self.historico)
        if total_jogos == 0:
            messagebox.showinfo("📊 Estatísticas", "🎲 Nenhum jogo realizado ainda!")
            return
            
        taxa_vitoria = (self.vitorias / total_jogos) * 100
        lucro_total = sum(h['ganho'] for h in self.historico)
        
        stats = f"""📊 ESTATÍSTICAS DO CASSINO 📊
        
🎮 Total de Jogos: {total_jogos}
🏆 Vitórias: {self.vitorias}
😔 Derrotas: {self.derrotas}
📈 Taxa de Vitória: {taxa_vitoria:.1f}%
💰 Lucro/Prejuízo Total: R${lucro_total}
🎯 Maior Ganho: R${self.maior_ganho}
💳 Saldo Atual: R${self.saldo}"""
        
        messagebox.showinfo("📊 Estatísticas", stats)
        
    def mostrar_historico(self):
        if not self.historico:
            messagebox.showinfo("📜 Histórico", "🎲 Nenhum jogo realizado ainda!")
            return
            
        # Mostrar últimos 10 jogos
        ultimos = self.historico[-10:]
        historico_text = "📜 ÚLTIMOS 10 JOGOS 📜\n\n"
        
        for i, jogo in enumerate(reversed(ultimos), 1):
            resultado = "🏆" if jogo['ganhou'] else "😔"
            historico_text += f"{i}. {resultado} {jogo['numero']} {jogo['cor']} - R${jogo['ganho']:+}\n"
            
        messagebox.showinfo("📜 Histórico", historico_text)
        
    def reset_saldo(self):
        resposta = messagebox.askyesno("💰 Reset Saldo", 
            "🔄 Deseja resetar seu saldo para R$100?\n⚠️ Isso apagará seu histórico!")
        if resposta:
            self.saldo = 100
            self.historico = []
            self.vitorias = 0
            self.derrotas = 0
            self.maior_ganho = 0
            self.label_saldo.config(text=f"💰 SALDO: R${self.saldo}", fg="#00FF00")
            self.resultado_label.config(text="🎲 Saldo resetado! Boa sorte! 🎲")
            messagebox.showinfo("✅ Sucesso", "💰 Saldo resetado com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    # Ícone da janela
    try:
        root.iconbitmap(default="casino.ico")
    except:
        pass
    app = RoletaApp(root)
    root.mainloop()
