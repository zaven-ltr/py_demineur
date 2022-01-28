from cgitb import text
from functools import partial
import tkinter as tk
from random import seed
from random import randint
from tkinter import font
import os


def show_px(n, m, px):
        for i in range(n):
            for j in range(m):
                print(px[i][j], end=" ")
            print("")

class Grid():

    def new_grid2(n, m):
        TT = []

        for j in range(m):
            TT.extend([j])

        return TT

    def new_grid(n, m):
        T = []

        for i in range(n):
            T.append(Grid.new_grid2(n, m))
        
        return T
    
    def init_grid(n, m, grid):
        for i in range(n):
            for j in range(m):
                grid[i][j] = 0
    
    def bombe_grid(n, m, grid):
        seed()
        for i in range(n):
            for j in range(m):
                if 2 > randint(0, 20):
                    grid[i][j] = 1
                else:
                    grid[i][j] = 0

    def how_bombe(n, m, p2, p3):
        c = 0
        for i in range(n):
            for j in range(m):
                for k in range(-1, 2, 1):
                    for h in range(-1, 2, 1):
                        try:
                            if (p2[i+k][j+h] == 1) and (i+k >= 0) and (j+h >= 0) and ((k != 0) or (h != 0)):
                                c = c + 1
                        except IndexError:
                            pass
                p3[i][j] = c
                c = 0

class Plateau():
    def __init__(self, n, m):
        self.n = n
        self.m = m

        self.all_grid()
        self.all_init_grid()

    def all_grid(self):
        self.p1 = Grid.new_grid(self.n, self.m)
        self.p2 = Grid.new_grid(self.n, self.m)
        self.p3 = Grid.new_grid(self.n, self.m)
        self.p4 = Grid.new_grid(self.n, self.m)
    
    def all_init_grid(self):
        Grid.init_grid(self.n, self.m, self.p1)
        Grid.bombe_grid(self.n, self.m, self.p2)
        Grid.how_bombe(self.n, self.m, self.p2, self.p3)
        Grid.init_grid(self.n, self.m, self.p4)

class Game():

    def creuser(i, j, P, A):
        P.p4[i][j] = 1
        if P.p2[i][j] == 1:
            A.pt[i][j] = tk.Button(A.plateau, width=5, height=1, text="BOUM", bg="red", command = partial(Game.is_mine, i, j, P, A))
            A.pt[i][j].grid(row=i, column=j)

        elif (P.p2[i][j] == 0) and (P.p3[i][j] != 0):
            A.pt[i][j] = tk.Button(A.plateau, width=5, height=1, text=P.p3[i][j], bg="blue", command = partial(Game.is_mine, i, j, P, A))
            A.pt[i][j].grid(row=i, column=j)
        
        elif (P.p2[i][j] == 0) and (P.p3[i][j] == 0):
            A.pt[i][j] = tk.Button(A.plateau, width=5, height=1, text="", bg="gray", command = partial(Game.is_mine, i, j, P, A))
            A.pt[i][j].grid(row=i, column=j)

    def recur(i, j, P, A):
        if P.p2[i][j] == 0: #si pas de mine sur ij
            Game.creuser(i, j, P, A) #on creuse ij
            for k in range(-1, 2, 1):
                for h in range(-1, 2, 1):
                    try:
                        if (P.p4[i+k][j+h] == 0) and (P.p3[i+k][j+h] == 0) and (i+k >= 0) and (j+h >= 0) and ((k != 0) or (h != 0)): #si pas creuser et si pas de mines autour
                            try:
                                Game.recur(i+k, j+h, P, A) #on relance 
                            except:
                                pass
                    except IndexError:
                        pass
                    try:
                        if (P.p3[i+k][j+h] != 0): #si mine autour
                            try:
                                Game.creuser(i+k, j+h, P, A)
                            except:
                                pass
                    except IndexError:
                        pass

    def is_mine(i, j, P, A):
        Game.creuser(i, j, P, A)

        if P.p3[i][j] == 0:
            Game.recur(i, j, P, A)
        
        if P.p2[i][j] == 1: #si mine
            A.life.configure(text='GAME OVER')

    def replay(x, P, A):
        os.system('cls')
        show_px(P.n, P.m, P.p2)
        A.all_supp()
        P.all_init_grid()
        A.Fen_2(x, P)
        A.Fen_3(x, P)


class App():
    def __init__(self, x, P):

        self.Fen_Set()

        self.Fen_1()
        self.Fen_2(x, P)
        self.Fen_3(x, P)

        self.fen.mainloop()

    def Fen_Set(self):
        self.fen = tk.Tk()
        self.fen.title('demineur')
        self.fen.geometry('1000x1000')

    def Fen_1(self):
        self.content = tk.Frame(self.fen, width=1000, height=1000) #contient tout les groupes de widgets
        self.plateau = tk.Frame(self.content, width=500, height=500) #groupe widgets des grilles
        self.info = tk.Frame(self.content) #groupe widgets des scores vies ...

        self.content.place(x=0, y=0)
        self.plateau.place(x=150, y=200)
        self.info.place(x=0, y=0)

    def Fen_2(self, x, P):
        self.pt = Grid.new_grid(x, x)
        for i in range(x):
            for j in range(x):
                self.pt[i][j] = tk.Button(self.plateau, width=5, height=1, text="", command = partial(Game.is_mine, i, j, P, self))
                self.pt[i][j].grid(row=i, column=j)

    def Fen_3(self, x, P):
        self.life = tk.Label(text="GAME")
        self.replay = tk.Button(text="Rejouer", command=lambda: Game.replay(x, P, self))

        self.life.place(x=10, y=10)
        self.replay.place(x=10, y=30)

    def all_supp(self):
        self.life.destroy()

x = 15
P = Plateau(x, x)
show_px(x, x, P.p2)
A = App(x, P)
