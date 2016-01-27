import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as mbox


"""
Legenda za ustvarjanje levelov:
    ' ' ... prazno polje
    'O' ... igralec
    '#' ... zid
    '*' ... blokec (ki se ga lahko premika)
    'X' ... tocka za zmago
    'A' ... igralec na tocki za zmago
    'R' ... blokec na tocki za zmago
"""


class Sokoban:
    kocka = 50

    def __init__(self):
        self.datoteka = self.izberi_level()
        self.polje = self.preberi_level(self.datoteka)
        self.igralec = self.moja_lokacija()

        self.visina_polja = len(self.polje)
        self.sirina_polja = len(self.polje[0])

        self.sirina_okna = self.sirina_polja * self.kocka
        self.visina_okna = self.visina_polja * self.kocka

        self.okno = tk.Tk()
        self.okno.title("Sokoban")
        self.okno.focus_force()
        self.canvas = tk.Canvas(self.okno, width=self.sirina_okna,
                                height=self.visina_okna)
        self.canvas.pack()
        self.narisi_polje()

        self.okno.bind_all("<Escape>", self.okno.quit)
        self.okno.bind_all("<Key>", self.preberi_tipke)

    def ponovi_level(self):
        self.polje = self.preberi_level(self.datoteka)
        self.igralec = self.moja_lokacija()

    def izberi_level(self):
        okno_izbire = tk.Tk()
        okno_izbire.withdraw()
        level = askopenfilename(
            title="Choose the level you want to play", initialdir="level",
            filetypes=[('Level files', '.lvl'), ('All files', '.*')])
        okno_izbire.destroy()
        return level

    def preberi_level(self, datoteka):
        polje = []
        with open(datoteka, 'r') as f:
            for vrstica in f:
                vrstica = vrstica.strip()
                polje.append(list(vrstica))
        return polje

    def moja_lokacija(self):
        for i, vrstica in enumerate(self.polje):
            for j, znak in enumerate(vrstica):
                if znak in "OA":
                    return [j, i]

    def sem_zmagal(self):
        for vrstica in self.polje:
            if "A" in vrstica:
                return False
            if "X" in vrstica:
                return False
        return True

    def odmik(self, x, y):
        if(self.polje[y][x] == 'O'):
            self.polje[y][x] = ' '
        if(self.polje[y][x] == 'A'):
            self.polje[y][x] = 'X'

    def primik(self, x, y):
        if(self.polje[y][x] == 'X'):
            self.polje[y][x] = 'A'
        if(self.polje[y][x] == ' '):
            self.polje[y][x] = 'O'

    def odmik_stvar(self, x, y):
        if(self.polje[y][x] == '*'):
            self.polje[y][x] = ' '
        if(self.polje[y][x] == 'R'):
            self.polje[y][x] = 'X'

    def primik_stvar(self, x, y):
        if(self.polje[y][x] == ' '):
            self.polje[y][x] = '*'
        if(self.polje[y][x] == 'X'):
            self.polje[y][x] = 'R'

    def premakni_se(self, dx, dy):
        novo = [self.igralec[0] + dx, self.igralec[1] + dy]
        if self.polje[novo[1]][novo[0]] in "X ":
            self.odmik(*self.igralec)
            self.igralec = novo
            self.primik(*self.igralec)
        if self.polje[novo[1]][novo[0]] in "*R":
            if self.polje[novo[1]+dy][novo[0]+dx] in "X ":
                self.odmik(*self.igralec)
                self.odmik_stvar(*novo)
                self.primik(*novo)
                self.primik_stvar(novo[0] + dx, novo[1] + dy)
                self.igralec = novo

    def preberi_tipke(self, event):
        if event.char == 'r':
            self.ponovi_level()
        tipka = event.keysym
        if(tipka == 'Up'):
            self.premakni_se(0, -1)

        elif(tipka == 'Down'):
            self.premakni_se(0, 1)

        elif(tipka == 'Left'):
            self.premakni_se(-1, 0)

        elif(tipka == 'Right'):
            self.premakni_se(1, 0)

        self.narisi_polje()
        if self.sem_zmagal():
            mbox.showinfo("Zmagal si!", "Cestitam, zmagal si!")
            self.okno.quit()

    # ========== Risanje ==============
    def narisi_kvadrat(self, x, y, barva):
        self.canvas.create_rectangle(x, y, x+self.kocka, y+self.kocka,
                                     fill=barva)

    def narisi_krog(self, x, y, barva):
        self.canvas.create_oval(x, y, x+self.kocka, y+self.kocka, fill=barva)

    def narisi_polje(self):
        self.canvas.delete("all")
        for i in range(self.kocka, self.sirina_okna, self.kocka):
            self.canvas.create_line(i, 0, i, self.visina_okna)

        for i in range(self.kocka, self.visina_okna, self.kocka):
            self.canvas.create_line(0, i, self.sirina_okna, i)

        for i in range(self.sirina_polja):
            for j in range(self.visina_polja):
                if(self.polje[j][i] == '#'):
                    self.narisi_kvadrat(i*self.kocka, j*self.kocka, "#252525")
                if(self.polje[j][i] == 'O'):
                    self.narisi_krog(i*self.kocka, j*self.kocka, "red")
                if(self.polje[j][i] == '*'):
                    self.narisi_kvadrat(i*self.kocka, j*self.kocka, "blue")
                if(self.polje[j][i] == 'X'):
                    self.narisi_kvadrat(i*self.kocka, j*self.kocka, "yellow")
                if(self.polje[j][i] == 'A'):
                    self.narisi_kvadrat(i*self.kocka, j*self.kocka, "yellow")
                    self.narisi_krog(i*self.kocka, j*self.kocka, "red")
                if(self.polje[j][i] == 'R'):
                    self.narisi_kvadrat(i*self.kocka, j*self.kocka, "pink")


igra = Sokoban()
igra.okno.mainloop()
