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

width = 900 #Largeur de la fenêtre, Ne doit pas être inférieur à 900
height = 900 #Hauteur de la fenêtre

top = 0 #Pour placer des éléments dans la partie supérieure du plateau
bottom = height/2 #Pour placer des éléments dans la partie inférieure du plateau

screen = pygame.display.set_mode((width,height)) #Créer une fenêtre
#screen.fill("White")

pygame.display.set_caption(f"naval660 - {os.getlogin()}") #Définir le titre de la fenêtre
icon = pygame.image.load("assets/img/cruise.png") #Charger l'image qui servira d'icone
pygame.display.set_icon(icon) #Définir l'icone

default_font = pygame.font.Font(None, 50) #Charger la police par défaut de pygame

clock = pygame.time.Clock() #Horloge qui va servir à réguler la rapidité du jeu



#Classe permettant la génération de plateaux de Jeu
class Board:

    def __init__(self, width, user, position=0):
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
    
    def graphShowBoard(self, position):
        self.top_jump = 0 #Décalage en hauteur
        self.left_jump = 0 #Décalage en largeur
        self.color = "White"
        if position == height/2:
            #self.top_jump = 20
            self.color = "Blue"
        #elif position == 0:
            #self.top_jump = 20
        self.bord_width = width-300
        self.bord_height = (height/2)-self.top_jump

        self.water = pygame.image.load("assets/img/water.png") #charger le fond du plateau courant
        self.water = pygame.transform.scale(self.water, (self.bord_width, self.bord_height)) #Redimensionner l'image
        self.board_background = pygame.Surface((width, (height/2))) 
        self.board_background.fill(self.color)
        self.board_background.blit(self.water, pygame.Rect(self.left_jump, self.top_jump, 0, 0)) #Afficher l'image

        gap = int(self.bord_width/self.width)-15
        for i in range(self.width):
            pygame.draw.line(self.board_background, "black", (0, gap), (self.bord_width, gap), 3)
            gap += int(self.bord_width/self.width)
        gap = int(self.bord_width/self.width)
        for i in range(self.width-1):
            pygame.draw.line(self.board_background, "black", (gap, 0), (gap, self.bord_width), 3)
            gap += int(self.bord_width/self.width)
        screen.blit(self.board_background, (0, position)) #Afficher le plateau en haut ou en bas

        

                
def gameLoop(board_0, board_1): #board_0: joueur, board_1: Ordinateur
    running = True #Indique que le Jeu est en cours
    print("Jeu en cours")
    while running:
        for event in pygame.event.get(): #Vérifier chaque évenement "extérieur"
            if event.type == pygame.QUIT: #Si le joueur veut quitter le jeu (il clique la croix de la fenêtre)
                running = False #Arrêter le Jeu

        board_1.graphShowBoard(top)
        board_0.graphShowBoard(bottom)
        pygame.draw.line(screen, "black", (0, int(height/2)), (width, int(height/2)), 1)
        clock.tick(20) #FPS bas mais stables pour ménager le processeur
        pygame.display.update() #Rafraichir l'écran
    pygame.quit()
    print("Jeu fermé ")





player_board = Board(5, "elouan")
computer_board = Board(5, "computer")
#player_board.showBoard()
for line in player_board.cells_list:
    print(line)

gameLoop(player_board, computer_board)
