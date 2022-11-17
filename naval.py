from random import *
import os as os

#alphabet ci dessous
alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
plateauj = [] #plateau joueur
plateaujo = [] #plateau ordinateur vu par le joueur
plateauo = [] #plateau ordinateur
plateauoj = [] #plateau joueur vu par l'ordinateur
nbrbateau = 0 #Nombre de bateaux par participants
linksj = [] #liste des liens entre les morceaux de bateaux du joueur
linkso = [] #liste des liens entre les morceaux de bateaux de l'ordinateur
rule = "Entrez vos cases au format Lettre-chiffre (ex: a-1)" #Règles affichées en permanence à l'écran
scorej = 0 #score du joueur
scoreo = 0 #score de l'ordinateur
listj = [] #liste des bateaux en service du joueur
listo = [] #liste des bateaux en service de l'ordinateur

listofwinners = []
listofsuperwinner = []
#"dimensions" Définition des dimension du tableau
def dim(dim):
  count = 0
  try:
    if int(dim) >= 3 and int(dim) <= len(alpha):
      for i in range(int(dim)):
        plateauj.append([])
        plateauo.append([])
        plateaujo.append([])
        plateauoj.append([])
      return int(dim)
    else:
      return 1
  except ValueError:
    return -1

#Nettoyage de l'écran
def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

#Création des cases
def remp(plateau):
  count = 0
  for tab in range(len(plateau)):
   for el in range(len(plateau)):
     plateau[count].append("~~~")
   count += 1

#Vérifier si deux cases sont adjacentes
def arenear(case0, case1):
  case0.split('-')
  num0 = int(case0[2]) -1
  lettre0 = alpha.index(case0[0].upper())
  case1.split('-')
  num1 = int(case1[2]) -1
  lettre1 = alpha.index(case1[0].upper())
  #print(f"[{num0-num1}|{lettre0-lettre1}]") #<---test pour débugage
  if num0-num1 in range(-1,2) and lettre0-lettre1 in range(-1,2) and (num0-num1)*(lettre0-lettre1) == 0:
    return True
  else:
    return False


#Placer un bateau de taille 1 sur une case
def placement(case, plateau, listb):
  try:
    case.split('-')
    num = int(case[2]) - 1 #car le compteur commence à 0 contrairement à case[2]
    lettre = alpha.index(case[0].upper())
    if plateau[int(num)][int(lettre)] == "~~~":
      plateau[int(num)][int(lettre)] = "[ ]"
      listb.append(case.upper())
      return 1 #Si tout es bon
    else:
      return 0 #Si un bateau est déja sur la case
  except BaseException:
    return -1 #Si la saisie est incorrecte

#"double placement" placer un bateau de taille 2 sur deux cases
def dbplacement(case0, case1, plateau, link, listb):
  try:
    if arenear(case0, case1) and case0 != case1: #si les deux cases sont proche et ne sont pas les mêmes
      case0.split('-')
      num0 = int(case0[2]) - 1
      lettre0 = alpha.index(case0[0].upper())
      case1.split('-')
      num1 = int(case1[2]) - 1
      lettre1 = alpha.index(case1[0].upper())
      if plateau[int(num0)][int(lettre0)] == "~~~" and plateau[int(num1)][int(lettre1)] == "~~~":
        plateau[int(num0)][int(lettre0)] = "[ ]"
        plateau[int(num1)][int(lettre1)] = "[ ]"
        listb.append(case0.upper())
        listb.append(case1.upper())
        link.append(case0.upper())
        link.append(case1.upper())
        return 2 #Si tout est bon
      else:
        return 0 #Si une ou deux cases sont déja occupées par un autre bateau
    else:
      return 1 #Si les deux cases entrées ne sont pas adjacentes
  except BaseException:
    return -1 #Si la saisie est incorrecte

#Afficher un plateau
def aff(plateau):
  #detection de l'utilisateur
  if plateau == plateauo or plateau == plateaujo:
    user = "ordinateur"
  elif plateau == plateauj or plateau == plateauoj:
    user = "joueur"

  #Affichage des lettres
  count = 0
  print(f"  [vue du plateau {user}]\n      ", end="")
  for i in plateauj:
    print(f"{alpha[count]}    ", end="")
    count += 1
  print("\n")

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

#"case ordinateur" générer et renvoyer une case aléatoirement
def caseo():
  lettre = randint(0,len(plateauo)-1)
  numo = randint(1,len(plateauo)-1)
  case = f"{alpha[lettre]}-{str(numo)}"
  return case

#"make ordinateur" Placement automatique des bateaux (dépend de "placement()" et "dbplacement()")
def makeo(plateau):
  count = 0
  while count < nbrbateau-1:
    if placement(caseo(), plateau, listo) == 1:
      count += 1
  count = 0
  while count < 1:
    caseo0 = caseo()
    caseo1 = caseo()
    if dbplacement(caseo0, caseo1, plateau, linkso, listo) == 2:
      count += 1
  
#"make joueur" Placement manuel des bateaux (dépend de "placement()" et "dbplacement()")
def makej(plateau):
  nbrbatoplace = nbrbateau #nombre de bateau à placer restant
  count = 0
  aff(plateau)
  #placement des baeaux de taille 1
  while count < nbrbateau-1:
    print(f"Placez {nbrbatoplace} bateaux")
    retourplacement = placement(input("Case où placer un bateau de taille 1: "), plateau, listj)
    if retourplacement == 1:
      clear()
      print(rule)
      aff(plateau)
      count += 1
      nbrbatoplace -= 1
    elif retourplacement == 0:
      print("Vous ne pouvez pas placer 2 bateaux sur la même case")
    else:
      print("saisie incorrecte")
  count = 0
  #placement des bateaux de taille 2
  while count < 1:
    print(f"Placez {nbrbatoplace} bateaux")
    dbretourplacement = dbplacement(input("Case où placer la 1/2 part d'un bateau de taille 2: "),input("Case où placer la 2/2 part d'un bateau de taille 2: "), plateau, linksj, listj)
    if dbretourplacement == 2:
      clear()
      print(rule)
      aff(plateau)
      count += 1
      nbrbatoplace -= 1
    elif dbretourplacement == 0:
      print("Vous ne pouvez pas placer 2 bateaux sur la même case")
    elif dbretourplacement == 1:
      print("Les cases ne sont pas à proximité")
    else:
      print("saisie incorrecte")
  

#Tirer sur une case (case en question, plateau sur lequel tirer, plateau sur lequel afficher, variable à baisser en cas de touche)
def boom(case, plateau0, plateau1, nbrbat, link, listb):
  global scoreo
  global scorej
  try:
    case2 = case
    case.split("-")
    num = int(case[2]) - 1
    lettre = alpha.index(case[0].upper())
    if plateau0 == plateauj:
      user = "[ordinateur]"
    else:
      user = "[joueur]"
    #Si cette case est touchée pour la première fois et qu'il n'y a rien sur celle-ci
    if plateau0[int(num)][int(lettre)] == "~~~":
        plateau1[int(num)][int(lettre)] = "~x~"
        plateau0[int(num)][int(lettre)] = "~x~"
        print(f"\nManqué! (par {user})")
    #Si cette case est touchée pour la première fois et qu'il y a un bateau de taille 2 sur celle-ci    
    elif plateau0[int(num)][int(lettre)] == "[ ]" and case2.upper() in link:
      if len(link) == 2:
        link.remove(str(case2.upper()))
        listb.remove(str(case2.upper()))
        plateau1[int(num)][int(lettre)] = "[X]"
        plateau0[int(num)][int(lettre)] = "[x]"
        print(f"\nTouché! (par{user})")
      elif len(link) == 1:
        link.remove(str(case2.upper()))
        listb.remove(str(case2.upper()))
        plateau1[int(num)][int(lettre)] = "[X]"
        plateau0[int(num)][int(lettre)] = "[x]"
        nbrbat -= 1
        print(f"\nCoulé! (par{user})")
        #augmenter de 8 le score en cas de coulage
        if user == "[ordinateur]":
          scoreo += 8
        else:
          scorej += 8
    #Si cette case est touchée pour la première fois et qu'il y a un bateau de taille 1 sur celle-ci    
    elif plateau0[int(num)][int(lettre)] == "[ ]":
      listb.remove(str(case2.upper()))
      plateau1[int(num)][int(lettre)] = "[X]"
      plateau0[int(num)][int(lettre)] = "[x]"
      nbrbat -= 1
      print(f"\nCoulé! (par{user})")
      #augmenter de 8 le score en cas de coulage
      if user == "[ordinateur]":
        scoreo += 8
      else:
        scorej += 8
    #Si cette case avait déja été touchée
    else:
      print(f"\nJe suis débile! ({user})")
    #augmenter le score de 1 si le tir à manqué de peu un bateau
    for element in listb:
      if arenear(case, element):
        if user == "[ordinateur]":
          scoreo += 1
        else:
          scorej += 1
    return nbrbat #nombre de bateau sur le plateau0 après le tir
  except BaseException:
    return -1
clear()

#Saisie utilisateur dans "dim()", permettant de choisir les dimensions du plateau de jeu
count = 0
while count != 1:
  cotéplateau = input("Coté des plateaux: ")
  retourdim = dim(cotéplateau)
  if retourdim > 1:
    count += 1
    nbrbateau = (retourdim//2)+1
  elif retourdim > 0:
    print(f"Veulliez entrer un nombre compris entre 3 et {len(alpha)+1}")
  else:
    print("saisie incorrecte")
clear()
 




#Lancement et déroulement de la partie
def jouer_une_partie():
  global cotéplateau
  #Si le joueur n'est pas le premier de la partie
  if j != 0:
    dim(cotéplateau)
  #Composition des plateaux
  remp(plateauj)
  remp(plateaujo)
  remp(plateauo)
  remp(plateauoj)
  makeo(plateauo)
  print(rule)
  makej(plateauj)
  nbrbateauj = nbrbateau #nombre de bateaux du joueur
  nbrbateauo = nbrbateau #nombre de bateaux de l'ordinateur

  username = input("Nom utilisateur: ")
  partie = True #indique que la partie est en cours
  while partie:
    clear()
    print(f"Partie n°{partieplay+1}, Joueur: {username}")
    #print(f"{listj}-{listo}") #<---test pour débugage
    print(rule)
    test = False
    #boucle permettant de 
    while test == False:
      bat1 = boom(input("case où tirer: "), plateauo, plateaujo, nbrbateauo, linkso, listo)
      if bat1 != -1:
        nbrbateauo = bat1
        test = True
      else:
        print("saisie incorrecte")
    aff(plateaujo)
    print(f"nombre de bateau de l'ordinateur restant: {nbrbateauo}")
    if nbrbateauo <= 0:
      winner = username
      partie = False #arreter la partie
    nbrbateauj = boom(caseo(), plateauj, plateauoj, nbrbateauj, linksj, listj)
    aff(plateauj)
    print(f"nombre de bateaux du joueur restant: {nbrbateauj}")
    if nbrbateauj <= 0:
      winner = "l'Ordinateur"
      partie = False #arreter la partie
    print(f"\nscore joueur: {scorej}\nscore ordinateur: {scoreo}")
    input("[Tapez entrer pour continuer]")
  listofwinners[partieplay].append([username, winner, scorej, scoreo])
  return winner



j = 0 #numéro du joueur
partieplay = 0 #numéro de la partie en cours
rejouer = True #si le joueur désire jouer
listofwinners.append([]) #liste contenant les premiers résultats de la partie
while rejouer:
  winner = jouer_une_partie()
  print(f"\nEt le gagnant est : {winner}")
  if input("Passer au joueur suivant? (y/n)").upper() == "Y":
    j += 1
    #reinitialiser le jeu
    plateauj = [] #plateau joueur
    plateaujo = [] #plateau ordinateur vu par le joueur
    plateauo = [] #plateau ordinateur
    plateauoj = [] #plateau joueur vu par l'ordinateur
    linksj = [] #liste des liens entre les morceaux de bateaux du joueur
    linkso = [] #liste des liens entre les morceaux de bateaux de l'ordinateur
    scorej = 0 #score du joueur
    scoreo = 0 #score de l'ordinateur
    listj = [] #liste des bateaux en service du joueur
    listo = [] #liste des bateaux en service de l'ordinateur
    clear()
  else:
    #si cette partie s'arrête ici, afficher les résultats de celle-ci
    print("\n")
    count = 0
    highscore = 0
    print(f"\n*****************party n°{partieplay+1}*****************")
    for thing in listofwinners[partieplay]:
      result = f"joueur: {listofwinners[partieplay][count][0]}  gagnant: {listofwinners[partieplay][count][1]}  score joueur: {listofwinners[partieplay][count][2]}  score ordinateur: {listofwinners[partieplay][count][3]}"
      print(result)
      if listofwinners[partieplay][count][2] >= highscore:
        highscore = listofwinners[partieplay][count][2]
        bestplayer = listofwinners[partieplay][count][1]
      count += 1
    print("********************************************")
    print(f"Et le meilleur joueur de cette partie est: {bestplayer} avec {highscore} de score\n")

    newparty = input(f"Refaire une partie? (y/n)")
    if newparty.upper() != "Y":
      #Si le jeu s'arrête ici, afficher les résultats
      clear()
      print("\n######################-Résultats finaux-###########################\n")
      suphighscore = 0 #meilleur score inter-partie
      supbestplayer = 0 #meilleur joueur inter-partie
      partycount = 0 #comptage des parties
      for party in listofwinners:
        print(f"\n  *****************party n°{partycount+1}*****************")
        highscore = 0 #meilleur score de la partie
        bestplayer = 0 #meilleur joueur de la partie
        playercount = 0 #comptage des joueurs dans la partie
        for player in listofwinners[partycount]:
          result = f"  joueur: {listofwinners[partycount][playercount][0]}  gagnant: {listofwinners[partycount][playercount][1]}  score joueur: {listofwinners[partycount][playercount][2]}  score ordinateur: {listofwinners[partycount][playercount][3]}"
          print(result)

          #Si le joueur s'avère avoir un meilleur score que les précédents de la partie
          if listofwinners[partycount][playercount][2] >= highscore:
            highscore = listofwinners[partycount][playercount][2]
            bestplayer = listofwinners[partycount][playercount][1]
          
          #Si le joueur s'avère avoir un meilleur score que tout les précédents inter-partie
          if listofwinners[partycount][playercount][2] >= suphighscore:
            if listofwinners[partycount][playercount][1] == supbestplayer:
              suphighscore += listofwinners[partycount][playercount][2]
            else:
              suphighscore = listofwinners[partycount][playercount][2]
              supbestplayer = listofwinners[partycount][playercount][1]

          playercount += 1
        print("  ********************************************")
        print(f"  Meilleur joueur de la party: {bestplayer} avec {highscore} de score\n")
        partycount += 1
      print("\n###################################################################")
      print(f"Meilleur joueur inter-party: {supbestplayer} avec {suphighscore} de score")
      rejouer = False
    else:
      j = 0
      listofwinners.append([])
      partieplay += 1
      #reinitialiser le jeu
      plateauj = [] #plateau joueur
      plateaujo = [] #plateau ordinateur vu par le joueur
      plateauo = [] #plateau ordinateur
      plateauoj = [] #plateau joueur vu par l'ordinateur
      linksj = [] #liste des liens entre les morceaux de bateaux du joueur
      linkso = [] #liste des liens entre les morceaux de bateaux de l'ordinateur
      scorej = 0 #score du joueur
      scoreo = 0 #score de l'ordinateur
      listj = [] #liste des bateaux en service du joueur
      listo = [] #liste des bateaux en service de l'ordinateur
      dim(cotéplateau)
      clear()
      #revient au début de la boucle eet relance une partie