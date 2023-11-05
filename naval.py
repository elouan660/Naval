# Ce programme appartient à Elouan Deschamps
# Licence (licence.txt) normalement jointe à ce fichier, sinon consultez la à https://www.gnu.org/licenses/gpl-3.0.html
# Projet scolaire de bataille navale NSI TG1 2023-2024 Livet
# Code anglophone, variable et attributs en minuscules, classes et fonctions en CamelCase, méthodes en lowerCamelCase

import random as random
import os as os
import pygame as pygame


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
cross = pygame.transform.scale(pygame.image.load("assets/img/cross.png"), (50,50))
#Bateaux
submarine = pygame.image.load("assets/img/ShipSubMarineHull.png")
patrol = pygame.image.load("assets/img/ShipPatrolHull.png")
carrier = pygame.image.load("assets/img/ShipCarrierHull.png")
#Animations
explosion = [] #Liste contenant les images de l'animation d'explosion
number = 1
for i in range(12):
    explosion.append(pygame.image.load(f"assets/img/explosion-1-d/explosion-d{number}.png"))
    number += 1
number = 0
#Polices
bitstream = pygame.font.SysFont("Bitstream Charter", 30)


pygame.display.set_icon(icon) #Définir l'icone

default_font = pygame.font.Font(None, 50) #Charger la police par défaut de pygame

clock = pygame.time.Clock() #Horloge qui va servir à réguler la rapidité du jeu



#Classe permettant la génération de plateaux de Jeu
class Board:
    #Les coordonnées des cellules seront données aux méthodes et fonctions sous la forme de tuple (x,y)
    def __init__(self, width, user, position):
        self.width = width #Largeur en case du plateau
        self.life = 3 #Points de vie
        self.user = user 
        self.score = 0
        self.position = position #En haut ou en bas
        self.cells_list = [] #Contenu du plateau
        self.makeBoard() #remplir le plateau de cases

    # Classe permettant la génération de cellules
    class Cell():
        def __init__(self, x, y, boat_state, boat_size=0):
            self.x = x #Position en x de la case
            self.y = y #Position en y de la case
            self.boat_state = boat_state # 0 -> absence de bateau, 1 -> bateau vivant, 2 -> bateau coulé
            self.boat_size = boat_size #taille du bateau présent sur la case racine, utile pour l'affichage graphique
            self.links = [] # Liste des liens avec d'autres cases (bateaux multi-cases)
        def __repr__(self): #retourner les coordonnées en cas de print
            return f"({self.x};{self.y});{self.boat_state}"
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
        linkable = True #Indique que jusqu'à présent il n'y a aucun problème pour la liaison entre les cases
        if boatcell_y + boatsize <= self.width and boatcell_x <= self.width: #Vérifier que le bateau ne dépassera pas du plateau
            count = 0
            for i in range(boatsize):
                if len(self.cells_list[boatcell_y+count][boatcell_x].links) == 0 and self.cells_list[boatcell_y+count][boatcell_x].boat_state == 0: #Si un bateau n'est pas déjà sur cette case
                    linked_cells.append((boatcell_x, boatcell_y+count))
                else:
                    linkable = False
                    print("placeBoat: Le bateau en chevauche un autre!")
                count += 1
            if linkable:
                self.cells_list[boatcell_y][boatcell_x].boat_state = 1 #permet d'indiquer qu'un bateau prend racine sur cette case
                self.cells_list[boatcell_y][boatcell_x].boat_size = boatsize
                self.makeLink(linked_cells)
                return 1 #Si le bateau a bien pu être placé
            else:
                return -1 #Si une erreur s'est produite
        else:
            print("placeBoat: Le bateau dépasse du plateau!")
            return -1
    
    def detectCellWithCos(self, mousecos): #permet de réu
        cellsize = (width-300)//self.width
        if self.position == top:
            gap = 0
        else:
            gap = 5
        return (mousecos[0]//cellsize, ((mousecos[1])//cellsize)-gap)

    def detectCosWithCell(self, cellcos): #Retrouver en multipliant les coordonnées plateau par les coordonnées réelles les corrdonnées du centre d'une case
        cellsize = (width-300)//self.width
        if self.position == top: #Corrections relatives à la position du plateau
            gap = 0
            gap2 = 100
        else:
            gap = 5
            gap2 = 600
        return (((cellcos[0]*cellsize)-cellsize//2)+100, ((((cellcos[1])*cellsize)+gap)-cellsize//2)+gap2) 

    def destroyBoat(self, selected_cell):
        try:
            cells_to_destroy = []
            size_of_boat = len(self.cells_list[selected_cell[1]][selected_cell[0]].links)
            score = 0 #score gagné par l'adversaire lors de cette attaque
            if size_of_boat != 0 or self.cells_list[selected_cell[1]][selected_cell[0]].boat_state == 1: #si un bateau se trouve sur cette case
                if self.cells_list[selected_cell[1]][selected_cell[0]].boat_state != 2: #Si le bateau n'a pas déjà été détruit
                    self.life -= 1 #Se retirer une vie
                    if size_of_boat == 0:
                        score += 1
                        self.score -= 1
                    elif size_of_boat == 1:
                        score += 2
                        self.score -= 2
                    elif size_of_boat == 2:
                        score += 3
                        self.score -=3
                cells_to_destroy.append(selected_cell)
                for cell in self.cells_list[selected_cell[1]][selected_cell[0]].links:
                    cells_to_destroy.append(cell)
            #print(cells_to_destroy)
            for cell in cells_to_destroy:
                self.cells_list[cell[1]][cell[0]].boat_state = 2
            return score  #indique que tout s'est bien passé
        except IndexError:
            return -1 #Indique qu'une erreur a empêché le bon fonctionnement de la méthode
        


    def graphShowBoard(self, visible=True):
        self.top_jump = 0 #Décalage en hauteur
        self.left_jump = 0 #Décalage en largeur
        self.color = "Red"
        if self.position == height/2:
            #self.top_jump = 20
            self.color = "Blue"
        #elif position == 0:
            #self.top_jump = 20
        self.bord_width = width-300

        self.water = pygame.transform.scale(water, (self.bord_width, self.bord_width)) #Redimensionner l'image
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
                if cell.boat_state == 1 and visible:
                    nb_cases_linked = len(cell.links)
                    #print(f"{cell} - {nb_cases_linked}")
                    if nb_cases_linked == 0:
                        self.board_background.blit(patrol, (current_x-3, current_y-30)) #Petits ajustements pour centrer l'image comme on le souhaite
                    elif nb_cases_linked == 1:
                        self.board_background.blit(submarine, (current_x-15, current_y-20))
                    elif nb_cases_linked == 2:
                        self.board_background.blit(carrier, (current_x-20, current_y))
                if cell.boat_state == 2:
                    self.board_background.blit(cross, (current_x-25, current_y-25))

                current_x += int(self.bord_width/self.width)
            current_x = int(self.bord_width/self.width)/2
            current_y += int(self.bord_width/self.width)

        screen.blit(self.board_background, (0, self.position)) #Afficher le plateau en haut ou en bas


def DisplayInformations(board):
     #Affichage des informations joueur
    diplayed_player = bitstream.render(board.user, True, (0,0,0), "white")
    center_player = diplayed_player.get_rect()
    center_player.center = (width-150, (board.position)+12)
    screen.blit(diplayed_player, center_player)
      #Score
    player_score = bitstream.render(f"score: {board.score}", True, (0,0,0))
    player_score_rect = player_score.get_rect()
    player_score_rect.x = (width-300)+50
    player_score_rect.y = board.position+50
    screen.blit(player_score, player_score_rect)
      #vies
    player_life = bitstream.render(f"vies: {board.life}", True, (0,0,0))
    player_life_rect = player_life.get_rect()
    player_life_rect.x = (width-300)+50
    player_life_rect.y = board.position+70
    screen.blit(player_life, player_life_rect)    

def DisplayFinal(winner, loser):
    #Créer un rectangle blanc centré
    pygame.draw.rect(screen, (255,255,255), pygame.Rect((width//2)-150,(height//2)-150, 300, 300))
    #Afficher le gagnant en haut de ce rectangle
    display_winner = bitstream.render(f"Gagnant: {winner.user}", True, (0,0,0))
    display_winner_rect = display_winner.get_rect()
    display_winner_rect.center = ((width//2),(height//2)-130)
    screen.blit(display_winner, display_winner_rect)

    winner_score = bitstream.render(f"score: {winner.score}", True, (0,0,0))
    winner_score_rect = winner_score.get_rect()
    winner_score_rect.x = (width//2)-130
    winner_score_rect.y = (height//2)-110
    screen.blit(winner_score, winner_score_rect) 

    display_loser = bitstream.render(f"Perdant: {loser.user}", True, (0,0,0))
    display_loser_rect = display_loser.get_rect()
    display_loser_rect.center = ((width//2),(height//2)+20)
    screen.blit(display_loser, display_loser_rect)

    loser_score = bitstream.render(f"score: {loser.score}", True, (0,0,0))
    loser_score_rect = loser_score.get_rect()
    loser_score_rect.x = (width//2)-130
    loser_score_rect.y = (height//2)+40
    screen.blit(loser_score, loser_score_rect) 
    

#Afficher le plateau en globalité
def ShowGlobalBoard(board_0, board_1, phase, user, pos="center"):
    board_0.graphShowBoard()
    board_1.graphShowBoard(False)
    pygame.draw.line(screen, "black", (0, int(height/2)), (width, int(height/2)), 3)
    #Afficher des informations concernant le tour
     #Affichage du tour courant
    diplayed_phase = bitstream.render(phase, True, (0,0,0), "white") #Texte noir sur fond blanc
    center_phase = diplayed_phase.get_rect()
    center_phase.center = ((width-300)//2, height//2) #centrer le texte entre les deux plateaux
    screen.blit(diplayed_phase, center_phase)

    DisplayInformations(board_0)
    DisplayInformations(board_1)

    #Rafraichir l'écran
    clock.tick(20)
    pygame.display.update()


#Premier tour du joueur
def FirstPlayerTurn(myboard, otherboard):
    selected = 1
    exit_signal = 1 #Indique que tout s'est bien déroulé
    while selected <= 3: #Tant que trois bateaux n'ont pas été placés
        for event in pygame.event.get(): #Vérifier chaque évenement "extérieur", indispensable pour l'interactivité souris
            if event.type == pygame.QUIT: #Si le joueur veut quitter le jeu (il clique la croix de la fenêtre)
                exit_signal = 2 #Indique une interruption de la part de l'utilisateur
                print("FirstplayerTurn: Signal d'arrêt envoyé")
                selected = 4
        ShowGlobalBoard(myboard, otherboard, "Placement des bateaux", os.getlogin())
        mouse_position = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            #print("detected")
            selected_case = myboard.detectCellWithCos(mouse_position) #Convertir les coordonnées de la souris en case
            #print(selected_case)
            if myboard.placeBoat(selected_case, selected) == 1:
                selected += 1
                #print(selected)
    return exit_signal

#Permettre à l'utilisateur d'attaquer l'adversaire
def PlayerAttack(myboard, otherboard):
    selected = 0
    exit_signal = 1 #Indique que tout s'est bien déroulé
    while selected != 1:
        for event in pygame.event.get(): #Vérifier chaque évenement "extérieur", indispensable pour l'interactivité souris
            if event.type == pygame.QUIT: #Si le joueur veut quitter le jeu (il clique la croix de la fenêtre)
                exit_signal = 2 #Indique une interruption de la part de l'utilisateur
                print("Player: Signal d'arrêt envoyé")
                selected = 1
        ShowGlobalBoard(myboard, otherboard, "À l'attaque!", os.getlogin())
        mouse_position = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            #print("detected")
            selected_case = otherboard.detectCellWithCos(mouse_position) #Convertir les coordonnées de la souris en case
            #print(selected_case)
            score = otherboard.destroyBoat(selected_case)
            #print(score)
            if score != -1: #Si le bateau a bien pu être détruit
                myboard.score += score
                selected = 1
    return exit_signal

def ComputerAttack(itsboard, otherboard):
    if itsboard.life != 0: #Pour eviter qu'il n'attaque après sa mort
        score = otherboard.destroyBoat((random.randrange(0, 4, 1), random.randrange(0, 4, 1)))
        itsboard.score += score



def FirstcomputerTurn(itsboard):
    selected = 1
    while selected <= 3: #Tant que trois bateaux n'ont pas été placés, usage d'une 
        selected_case = (random.randrange(0, 4, 1), random.randrange(0, 4, 1))
        if itsboard.placeBoat(selected_case, selected) == 1: #Si le bateau a bien pu être placé
            selected += 1
   

                
def GameLoop(board_0, board_1): #board_0: joueur, board_1: Ordinateur
    running = True #Indique que le Jeu est en cours
    isfirst = True
    print("GameLoop: Jeu en cours")
    while running:
        if isfirst: #Si c'est le premier Tour
            exit_signal = FirstPlayerTurn(board_0, board_1) #En cas d'interruption volontaire de la part de l'utilisateur
            FirstcomputerTurn(board_1)
        if isfirst == False:
            exit_signal = PlayerAttack(board_0, board_1)
            ComputerAttack(board_1, board_0)
            for line in board_1.cells_list:
                print(line)
            print("\n")
        changeTurn = False
        #if board_0 
        isfirst = False #Puisque ce qui était à faire seulement au premier tour est passé
        if exit_signal == 2:
            running = False
        while changeTurn == False:
            ShowGlobalBoard(board_0, board_1, "Appuyez sur espace pour continuer", board_0.user)
            for event in pygame.event.get(): #Vérifier chaque évenement "extérieur", indispensable pour l'interactivité souris
                if event.type == pygame.QUIT: #Si le joueur veut quitter le jeu (il clique la croix de la fenêtre)
                    #running = False
                    changeTurn = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        changeTurn = True
        if board_0.life == 0 or board_1.life == 0:
            if board_0.life > board_1.life:
                DisplayFinal(board_0, board_1)
            else:
                DisplayFinal(board_1, board_0)
            quit_game = False
            while quit_game == False:
                clock.tick(20)
                pygame.display.update()
                for event in pygame.event.get(): #Vérifier chaque évenement "extérieur", indispensable pour l'interactivité souris
                    if event.type == pygame.QUIT: #Si le joueur veut quitter le jeu (il clique la croix de la fenêtre)
                        quit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            quit_game = True
            running = False
    pygame.quit()
    print("GameLoop: Jeu fermé ")



player_board = Board(5, os.getlogin(), bottom)
computer_board = Board(5, "Ordinateur", top)
GameLoop(player_board, computer_board)
