# Ce programme appartient à Elouan Deschamps
# Licence (licence.txt) normalement jointe à ce fichier, sinon consultez la à https://www.gnu.org/licenses/gpl-3.0.html
# Projet scolaire de bataille navale NSI TG1 2023-2024 Livet
# Code anglophone, variable et attributs en minuscules, classes en CamelCase, fonctions et méthodes en lowerCamelCase
# Todo: Penser à inclure des piles et des files

from random import *
import os as os
import pygame as pygame


#Initialisation
alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#Initialiser pygame
pygame.init() 

width = 800 #Largeur de la fenêtre
height = 900 #Hauteur de la fenêtre
screen = pygame.display.set_mode((width,height)) #Créer une fenêtre
pygame.display.set_caption(f"naval660 - {os.getlogin()}") #Définir le titre de la fenêtre
icon = 

clock = pygame.time.Clock() #Horloge qui va servir à réguler la rapidité du jeu

background = pygame.Surface((width, height))
background.fill("White")


#Classe permettant la génération de plateaux de Jeu
class Board:

    def __init__(self, width, user):
        self.width = width #Largeur en case du plateau
        self.user = user 
        self.cells_list = [] #Contenu du plateau
        self.makeBoard() #remplir le plateau de cases

    # Classe permettant la génération de cellules
    class Cell():
        def __init__(self, x, y, boat_state):
            self.x = x #Position en x de la case
            self.y = y #Position en y de la case
            self.boat_state = boat_state # 0 -> absence de bateau, 1 -> bateau vivant, 2 -> bateau coulé
            self.links = [] # Liste des liens avec d'autres cases (bateaux multi-cases)
        def __repr__(self): #retourner les coordonnées en cas de print
            return f"({self.x};{self.y})"
        def getBoatState(self): # Obtenir l'état du bateau
            return self.boat_state
        def getCoord(self): # Obtenir les coordonées de la case
            return (self.x, self.y)
        def getTextCell(self): #Obtenir une représentation de l'état du bateau
            if self.boat_state == 0:
                self.text_cell = "~~~"
            elif self.boat_state == 1:
                self.text_cell = "[ ]"
            elif self.boat_state == 2:
                self.text_cell = "[X]"
            else:
                self.text_cell = -1 #En cas d'erreur
            return self.text_cell
    
    def makeBoard(self): #Créer les cases et les ranger dans le plateau
        self.x_count = 0 #Colonne courante
        self.y_count = 0 #Ligne courante
        for i in range(self.width): #Pour chaque ligne
            self.cells_list.append([])
            for i in range(self.width): #Pour chaque cellule dans la ligne
                self.cells_list[self.y_count].append(self.Cell(self.x_count, self.y_count, 0)) #Ajouter dans la ligne
                self.x_count += 1 #passer à la colonne
            self.y_count += 1 #Passer à la ligne suivante
            self.x_count = 0 #Revenir à colonne

    def showBoard(self):

        #Affichage des lettres
        self.count = 0
        print(f"  [vue du plateau {self.user}]\n      ", end="") #Afficher le nom du plateau
        for i in range(self.width): #Afficher autant de lettres que le coté du plateau
            print(f"{alpha[self.count]}    ", end="")
            self.count += 1 #Passer à la lettre suivante
        print("\n")

        self.current_x = 0 #Colonne courante
        self.current_y = 0 #Ligne courante
        for cell in self.cells_list:
            print(f"\n{self.current_y}  | ", end="")
            self.current_y += 1
            if cell.getCoord()[0] == self.current_x:
                print(f"{cell.getTextCell()}  ", end="")
                
def gameLoop():
    running = True #Indique que le Jeu est en cours
    print("Jeu en cours")
    while running:
        for event in pygame.event.get(): #Vérifier chaque évenement "extérieur"
            if event.type == pygame.QUIT: #Si le joueur veut quitter le jeu (il clique la croix de la fenêtre)
                running = False #Arrêter le Jeu


        screen.blit(background, (0,0))
        clock.tick(60) #Ne pas dépasser 60 images par seconde
        pygame.display.update() #Rafraichir l'écran
    pygame.quit()
    print("Jeu fermé ")





player_board = Board(3, "elouan")
#player_board.showBoard()
for line in player_board.cells_list:
    print(line)

gameLoop()



