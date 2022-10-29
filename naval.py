#Affichage moche à résoudre
from random import *
import os as os
from time import *

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
plateauj = [] #plateau joueur
plateaujo = [] #plateau ordinateur vu par le joueur
plateauo = [] #plateau ordinateur
plateauoj = [] #plateau joueur vu par l'ordinateur
nbrbateau = 0
#Définition des dimension du tableau
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

#Remplisage des colones
def remp(plateau):
  count = 0
  for tab in range(len(plateau)):
   for el in range(len(plateau)):
     plateau[count].append("~~~")
   count += 1

def isnear(case0, case1):




#Modifier la valeur d'une case selon "x-x"
def placement(case, plateau):
  try:
    case.split('-')
    num = int(case[2]) - 1
    lettre = alpha.index(case[0].upper())
    if plateau[int(num)][int(lettre)] == "~~~":
      plateau[int(num)][int(lettre)] = "[ ]"
      return 1
    else:
      return 0
  except BaseException:
    return -1


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
  count = 1
  for el in plateau:
    if count <= 9:
      print(f"{count}  | ", end="")
    else:
      print(f"{count} | ", end="")
    for el1 in el:
      print(f"{el1}  ", end="")
    print("|\n")
    count += 1

#générer une case aléatoirement
def caseo():
  lettre = randint(0,len(plateauo)-1)
  numo = randint(0,len(plateauo)-1)
  case = f"{alpha[lettre]}-{str(numo)}"
  return case

#Placement automatique des bateaux (dépend de "placement()")
def makeo(plateau):
  count = 0
  while count < nbrbateau:
    if placement(caseo(), plateau) == 1:
      count += 1
  
#Placement manuel des bateaux (dépend de "placement()")
def makef(plateau):
  print(f"Placez {nbrbateau} bateaux")
  count = 0
  aff(plateau)
  while count < nbrbateau:
    retourplacement = placement(input("Case où placer un bateau: "), plateau)
    if retourplacement == 1:
      os.system('cls' if os.name == 'nt' else 'clear')
      aff(plateau)
      count += 1
    elif retourplacement == 0:
      print("Vous ne pouvez pas placer 2 bateaux sur la même case")
    else:
      print("saisie incorrecte")

#Tirer sur une case (case en question, plateau sur lequel tirer, plateau sur lequel afficher, variable a modifier)
def boom(case, plateau0, plateau1, nbrbat):
  case.split("-")
  num = int(case[2]) - 1
  lettre = alpha.index(case[0].upper())
  if plateau0 == plateauj:
    user = "[ordinateur]"
  else:
    user = "[joueur]"
  if plateau0[int(num)][int(lettre)] == "~~~":
    plateau1[int(num)][int(lettre)] = "~x~"
    plateau0[int(num)][int(lettre)] = "~x~"
    print(f"\nManqué! (par {user})")
  elif plateau0[int(num)][int(lettre)] == "[ ]":
    plateau1[int(num)][int(lettre)] = "[X]"
    nbrbat -= 1
    print(f"\nCoulé! (par{user})")
  else:
    if user == "[ordinateur]":
      aff(plateau0)
    print(f"\nJe suis débile! ({user})")
  return nbrbat


#Saisie utilisateur dans "dim()"
count = 0
while count != 1:
  retourdim = dim(input("Coté des plateaux: "))
  if retourdim > 1:
    count += 1
    nbrbateau = (retourdim//2)+1
  elif retourdim > 0:
    print(f"Veulliez entrer un nombre compris entre 3 et {len(alpha)+1}")
  else:
    print("saisie incorrecte")

nbrbateauj = nbrbateau #nombre de bateaux du joueur
nbrbateauo = nbrbateau #nombre de bateaux de l'ordinateur
partie = True #indique que la partie est en cour

remp(plateauj)
remp(plateaujo)
remp(plateauo)
remp(plateauoj)
makeo(plateauo)
makef(plateauj)
while partie:
  os.system('cls' if os.name == 'nt' else 'clear')
  nbrbateauo = boom(input("case où tirer: "), plateauo, plateaujo, nbrbateauo)
  aff(plateaujo)
  print(f"nombre de bateau de l'ordinateur restant: {nbrbateauo}")
  if nbrbateauo <= 0:
    winner = "le Joueur"
    partie = False
  nbrbateauj = boom(caseo(), plateauj, plateauoj, nbrbateauj)
  aff(plateauj)
  print(f"nombre de bateaux du joueur restant: {nbrbateauj}")
  if nbrbateauj <= 0:
    winner = "l'Ordinateur"
    partie = False
  input("Tapez entrer pour continuer: ")

print(f"\nEt le gagnant est : {winner}")