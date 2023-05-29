import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import random
from playsound import playsound
import threading as th
import json


class App:

    def __init__(self):
        self.rangeValues = ["5", "6", "7", "8", "9", "10", "15", "20",
                            "25"]  # Valores disponibilizados para seleção de range
        self.dados = dict()
        self.recuperaDados()
        self.labelHighscore = None
        self.pontos = 0
        self.conta = None
        self.resultadoConta = None
        self.labelPontos = None
        self.timer = None
        self.boxRange = None

        self.menu = tk.Tk()
        self.menu.title("Jogo de multiplicar")
        self.menu.resizable(False, False)
        self.jogar = None
        self.inicializaMenu()

    def checaHighscore(self):
        rangeAtual = self.dados['range']
        if self.pontos > self.dados[str(rangeAtual)]:
            self.dados[str(rangeAtual)] = self.pontos
            self.salvaDados()
            tk.messagebox.showinfo('Novo record!', "Parabéns!! Você conseguiu fazer um novo record!\nVocê "
                                                   "acertou {} contas seguidas!!".format(self.pontos))
            self.labelHighscore.configure(text="Maior pontuação: {}".format(self.dados[str(self.dados['range'])]))

    def recuperaDados(self):
        try:
            file = open("data.json", "r")
            self.dados = json.loads(file.read())
            file.close()
        except (FileNotFoundError, ValueError, IndexError):
            self.dados['range'] = int(self.rangeValues[0])
            for i in self.rangeValues:
                self.dados[i] = 0

    def salvaDados(self):
        file = open("data.json", "w")
        file.write(json.dumps(self.dados))
        file.close()

    def rangeSelecionada(self):
        newRange = int(self.boxRange.get())
        if self.dados['range'] != newRange:
            self.dados['range'] = newRange
            self.labelHighscore.configure(text="Maior pontuação: {}".format(self.dados[str(self.dados['range'])]))
            self.salvaDados()

    def inicializaMenu(self):
        # linha 0
        labelTitulo = tk.Label(self.menu, text="Jogo de multiplicar", font=("Arial", 30, "bold"))
        labelTitulo.grid(row=0, column=1, columnspan=1, pady=(0, 20), padx=(30, 30), sticky="WE")

        # linha 1
        self.labelHighscore = tk.Label(self.menu, text="Maior pontuação: {}"
                                       .format(self.dados[str(self.dados['range'])]),
                                       font=("Times New Roman", 16, "bold"))
        self.labelHighscore.grid(row=1, column=1, columnspan=1, pady=(0, 30), sticky="WE")

        # linha 2
        labelRange = tk.Label(self.menu, text="Selecione abaixo o maior número que possa aparecer nas continhas:")
        labelRange.grid(row=2, column=1, columnspan=1, sticky="WE")

        # linha 3
        txtVariable = tk.StringVar()
        txtVariable.set(str(self.dados['range']))
        self.boxRange = ttk.Combobox(self.menu, textvariable=txtVariable, justify=tk.CENTER,
                                     width=5, values=tuple(self.rangeValues),
                                     state="readonly")
        self.boxRange.grid(row=3, column=1, columnspan=1, pady=(0, 30))
        self.boxRange.bind("<<ComboboxSelected>>", lambda e: self.rangeSelecionada())

        # linha 4
        buttonJogar = tk.Button(self.menu, text="JOGAR!", font=("Tahoma", 12, "bold"), command=self.iniciaJogo)
        buttonJogar.grid(row=4, column=1, pady=(0, 20))

        # linha 5
        labelAssinatura = tk.Label(self.menu, text="Criado com ♡ para Miguel", font=("Sylfaen", 12, "bold"))
        labelAssinatura.grid(row=5, column=1, sticky="E")

        self.menu.update_idletasks()  # Garante que o método winfo_width saiba o tamanho correto da janela
        self.centraliza(self.menu)
        self.menu.mainloop()

    def iniciaJogo(self):
        self.menu.withdraw()
        self.jogar = tk.Toplevel(self.menu)
        self.jogar.title("Jogo de multiplicar")
        self.jogar.resizable(False, False)
        self.gerarConta()

        def validaResposta():
            if not entryResposta.get():
                return None

            respostaInserida = int(entryResposta.get())

            if respostaInserida == self.resultadoConta:
                self.acertou()
                self.gerarConta()
                labelConta.configure(text="{} x {} = ?".format(self.conta[0], self.conta[1]))
                self.labelPontos.configure(text="Pontos: {}".format(self.pontos))
                entryResposta.delete(0, tk.END)
            else:
                tk.messagebox.showerror('Fim de jogo', "Você errou!\nA resposta correta era: {}\nVocê conseguiu"
                                                       " fazer {} ponto(s).".format(self.resultadoConta, self.pontos))
                self.jogar.destroy()
                self.menu.deiconify()
                self.checaHighscore()
                self.pontos = 0
                self.gerarConta()

        def onClosing():
            tk.messagebox.showinfo('Fim de jogo',
                                   "Você desistiu!\nVocê acertou {} contas seguidas!".format(self.pontos))
            self.checaHighscore()
            self.pontos = 0
            self.jogar.destroy()
            self.menu.deiconify()

        # linha 0
        labelDescricao = tk.Label(self.jogar, text="Você sabe resolver essa continha?",
                                  font=("Sans Serif Comic", 15, "italic"))
        labelDescricao.grid(row=0, column=0, columnspan=1, padx=5, pady=(5, 30), sticky="WE")

        # linha 1
        labelConta = tk.Label(self.jogar, text="{} x {} = ?".format(self.conta[0], self.conta[1]),
                              font=("Tahoma", 20, "bold"))
        labelConta.grid(row=1, column=0, columnspan=1, sticky="WE")

        # linha 2
        entryResposta = tk.Entry(self.jogar, width=5, justify="center", font=("Tahoma", 18, "bold"))
        entryResposta.grid(row=2, column=0, columnspan=1, pady=5)
        entryResposta.focus()
        entryResposta.focus_force()

        # linha 3
        buttonResposta = tk.Button(self.jogar, text="Responder!", font=("Tahoma", 10, "bold"), command=validaResposta)
        buttonResposta.grid(row=3, column=0, columnspan=1, pady=5)

        # linha 4
        self.labelPontos = tk.Label(self.jogar, text="Pontos: {}".format(self.pontos), font=("Sans Serif", 15, "bold"),
                                    background="SystemButtonFace")
        self.labelPontos.grid(row=4, column=0, columnspan=1, pady=(30, 5), sticky="WE")

        # binds
        entryResposta.bind("<Return>", lambda event: buttonResposta.invoke())
        self.jogar.protocol("WM_DELETE_WINDOW", onClosing)

        # validações
        entryResposta.config(validate="key", validatecommand=(self.jogar.register(App.validarNumero), "%P"))

        self.jogar.update_idletasks()  # Garante que o método winfo_width saiba o tamanho correto da janela
        self.centraliza(self.jogar)

    def gerarConta(self):
        x = random.randint(0, self.dados['range'])
        y = random.randint(0, self.dados['range'])
        self.conta = (x, y)
        self.resultadoConta = x * y

    def acertou(self):
        playsound('https://github.com/bruamado/jogoMultiplicar/raw/main/sucess.mp3', False)
        if self.timer:
            self.timer.cancel()
            del self.timer
        self.timer = th.Timer(0.5, self.descolorir)
        self.timer.start()
        self.pontos += 1
        self.labelPontos.configure(background="green")

    def descolorir(self):
        self.labelPontos.configure(background="SystemButtonFace")

    @staticmethod
    def centraliza(tela):
        larguraTela = tela.winfo_screenwidth()
        alturaTela = tela.winfo_screenheight()
        larguraJanela = tela.winfo_width()
        alturaJanela = tela.winfo_height()

        largura = larguraTela / 2 - larguraJanela / 2
        altura = alturaTela / 2 - alturaJanela / 2

        altura -= alturaTela * 0.04  # Incrementa 4% da tela na altura (afim de desconsiderar a taskbar do windows)
        tela.geometry("+{}+{}".format(int(largura), int(altura)))

    @staticmethod
    def validarNumero(entrada):
        if entrada == "":
            return True
        try:
            int(entrada)
            return True
        except ValueError:
            return False


app = App()
