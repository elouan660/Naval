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

width = 800 #Largeur de la fenêtre, Ne doit pas être inférieur à 900
height = 1000 #Hauteur de la fenêtre

top = 0 #Pour placer des éléments dans la partie supérieure du plateau
bottom = height/2 #Pour placer des éléments dans la partie inférieure du plateau

screen = pygame.display.set_mode((width,height)) #Créer une fenêtre
#screen.fill("White")

pygame.display.set_caption(f"naval660 - {os.getlogin()}") #Définir le titre de la fenêtre

#Charger des assets
icon = pygame.image.load("assets/img/cruise.png") #Charger l'image qui servira d'icone
water = pygame.image.load("assets/img/water.png")
#Bateaux
submarine = pygame.image.load("assets/img/ShipSubMarineHull.png")
patrol = pygame.image.load("assets/img/ShipPatrolHull.png")
carrier = pygame.image.load("assets/img/ShipCarrierHull.png")
#Animations
explosion = [] #Liste contenant les images de l'animation d'explosion
d = 1
for i in range(12):
    explosion.append(pygame.image.load(f"assets/img/explosion-1-d/explosion-d{d}.png"))
    d += 1
d = 0


pygame.display.set_icon(icon) #Définir l'icone

default_font = pygame.font.Font(None, 50) #Charger la police par défaut de pygame

clock = pygame.time.Clock() #Horloge qui va servir à réguler la rapidité du jeu



#Classe permettant la génération de plateaux de Jeu
class Board:
    #Les coordonnées des cellules seront données aux méthodes et fonctions sous la forme de tuple (x,y)
    def __init__(self, width, user, position=0):
        self.width = width #Largeur en case du plateau
        self.user = user 
        self.cells_list = [] #Contenu du plateau
        self.makeBoard() #remplir le plateau de cases

    # Classe permettant la génération de cellules
    class Cell():
        def __init__(self, x, y, boat_state, boat_size=0):
            self.x = x #Position en x de la case
            self.y = y #Position en y de la case
            self.boat_state = boat_state # 0 -> absence de bateau, 1 -> bateau vivant, 2 -> bateau coulé
            self.boat_size = boat_size
            self.links = [] # Liste des liens avec d'autres cases (bateaux multi-cases)
        def __repr__(self): #retourner les coordonnées en cas de print
            return f"({self.x};{self.y});{self.links}"
        def getBoatState(self): # Obtenir l'état du bateau
            return self.boat_state
        def getCoord(self): # Obtenir les coordonées de la case
            return (self.x, self.y)
    
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

    def makeLink(self, celltab): #Permet de lier des cellules entre elles
        for cell0 in celltab:
            for cell1 in celltab:
                if cell1 != cell0: #Rien ne sert qu'une cellule soit liée à elle-même
                    self.cells_list[cell0[1]][cell0[0]].links.append(cell1) #puisque dans cells_list chaque tableau correspond à y
    def placeBoat(self, boatcell, boatsize):
        linked_cells = [] #Liste des cellules à lier
        boatcell_x = boatcell[0] #permet de séparer le tuple
        boatcell_y = boatcell[1]
        linkable = True
        """
        self.cells_list[boatcell_y][boatcell_x].boat_state = 1 #permet d'indiquer qu'un bateau prend racine sur cette case
        self.cells_list[boatcell_y][boatcell_x].boat_size = boatsize
        """
        if boatcell_y + boatsize <= self.width and boatcell_x <= self.width: #Vérifier que le bateau ne dépassera pas du plateau
            count = 0
            for i in range(boatsize):
                if len(self.cells_list[boatcell_y+count][boatcell_x].links) == 0:
                    linked_cells.append((boatcell_x, boatcell_y+count))
                else:
                    linkable = False
                    print("Le bateau en chevauche un autre!")
                count += 1
            if linkable:
                self.cells_list[boatcell_y][boatcell_x].boat_state = 1 #permet d'indiquer qu'un bateau prend racine sur cette case
                self.cells_list[boatcell_y][boatcell_x].boat_size = boatsize
                self.makeLink(linked_cells)
        else:
            print("Le bateau dépasse du plateau!")
    

    def graphShowBoard(self, position):
        self.top_jump = 0 #Décalage en hauteur
        self.left_jump = 0 #Décalage en largeur
        self.color = "Red"
        if position == height/2:
            #self.top_jump = 20
            self.color = "Blue"
        #elif position == 0:
            #self.top_jump = 20
        self.bord_width = width-300
        self.bord_height = width-300

        self.water = pygame.transform.scale(water, (self.bord_width, self.bord_height)) #Redimensionner l'image
        self.board_background = pygame.Surface((width, (height/2))) 
        self.board_background.fill(self.color)
        self.board_background.blit(self.water, (0,0)) #pygame.Rect(self.left_jump, self.top_jump, 0, 0)) #Afficher l'image

        #Dessiner des lignes de gauche à droite
        gap = int(self.bord_width/self.width) #Anomalie constatée quand au 
        for i in range(self.width-1): #Rien ne sert de faire une ligne en dehors de l'écran
            pygame.draw.line(self.board_background, "black", (0, gap), (self.bord_width, gap), 2)
            gap += int(self.bord_width/self.width)
        #Dessiner des lignes de haut en bas
        gap = int(self.bord_width/self.width)
        for i in range(self.width): #Pas de -1 pour séparer le plateau de la zone d'information
            pygame.draw.line(self.board_background, "black", (gap, 0), (gap, self.bord_width), 2)
            gap += int(self.bord_width/self.width)
        
        #Afficher un bateau
        current_x = int(self.bord_width/self.width)/2
        current_y = int(self.bord_width/self.width)/2
        for tab in self.cells_list:
            for cell in tab:
                if cell.boat_state == 1:
                    nb_cases_linked = len(cell.links)
                    #print(f"{cell} - {nb_cases_linked}")
                    if nb_cases_linked == 0:
                        self.board_background.blit(patrol, (current_x-3, current_y-30)) #Petits ajustements pour centrer l'image comme on le souhaite
                    elif nb_cases_linked == 1:
                        self.board_background.blit(submarine, (current_x-15, current_y-20))
                    elif nb_cases_linked == 2:
                        self.board_background.blit(carrier, (current_x-20, current_y))

                    #elif nb_cases_linked == 2:
                     #   self.board_background.blit(self.)


                current_x += int(self.bord_width/self.width)
            current_x = int(self.bord_width/self.width)/2
            current_y += int(self.bord_width/self.width)





        #essai technique
        #self.board_background.blit(self.submarine, (90,0))
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
        pygame.draw.line(screen, "black", (0, int(height/2)), (width, int(height/2)), 3)
        clock.tick(20) #FPS bas mais stables pour ménager le processeur
        pygame.display.update() #Rafraichir l'écran
    pygame.quit()
    print("Jeu fermé ")





player_board = Board(5, "elouan")
computer_board = Board(5, "computer")
#player_board.showBoard()
#player_board.makeLink([(0,0),(1,1),(3,4)])
#player_board.placeBoat((0,2), 3)
player_board.placeBoat((1,0), 3)
player_board.placeBoat((0,1), 2)
computer_board.placeBoat((0,2),1)
for line in player_board.cells_list:
    print(line)

gameLoop(player_board, computer_board)
