# Ce programme appartient à Elouan Deschamps
# Licence d'utilisation: https://www.gnu.org/licenses/gpl-3.0.html
# Projet scolaire de bataille navale NSI TG1 2023-2024 Livet

from random import *
import os as os
import pygame as pg

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


#Classe permettant la génération de plateaux de Jeu
class Board:

    def __init__(self, width, user):
        self.width = width #Largeur en case du plateau
        self.user = user
        self.cells_list = []
        self.makeBoard()

    # Classe permettant la génération de cellules
    class Cell():
        def __init__(self, x, y, boat_state):
            self.x = x #Position en x de la case
            self.y = y #Position en y de la case
            self.boat_state = boat_state # 0 -> absence de bateau, 1 -> bateau vivant, 2 -> bateau coulé
        def getBoatState(self): # Obtenir l'état du bateau
            return self.boat_state
        def getCoord(self): # Obtenir les coordonées de la case
            return (self.x, self.y)
        def getTextCell(self):
            if self.boat_state == 0:
                return "~~~"
            elif self.boat_state == 1:
                return "[ ]"
            elif self.boat_state == 2:
                return "[X]"
            else:
                return -1
    
    def makeBoard(self):
        self.x_count = 0
        self.y_count = 0
        for i in range(self.width):
            for i in range(self.width):
                self.cells_list.append(self.Cell(self.x_count, self.y_count, 0))
                self.y_count += 1
            self.x_count += 1
            self.y_count = 0

    def showBoard(self):

        #Affichage des lettres
        self.count = 0
        print(f"  [vue du plateau {self.user}]\n      ", end="")
        for i in range(self.width):
            print(f"{alpha[self.count]}    ", end="")
            self.count += 1
        print("\n")

        self.current_x = 0
        self.current_y = 0
        for cell in self.cells_list:
            print(f"{self.current_y}  | ", end="")
            self.current_y += 1
            if cell.getCoord()[0] == self.current_x:
                print(f"{cell.getBoatText()}  ", end="")
                





        



        """
        #Affichage des nombres et des cases
        count = 1 #et non 0 car l'affichage commence a 1
        for el in plateau:
            if count <= 9:
                print(f"{count}  | ", end="")
            else:
                print(f"{count} | ", end="")
            for el1 in el:
                print(f"{el1}  ", end="")
            print("|\n")
            count += 1
        """

player_board = Board(3, "elouan")
player_board.showBoard()
for cell in player_board.cells_list:
    print(str(player_board.Cell.getCoord(cell)))





