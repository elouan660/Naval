#À résoudre: 
# x>9 en num est mal pris en charge
from random import *

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
    for i in range(int(dim)):
      plateauj.append([])
      plateauo.append([])
      plateaujo.append([])
      plateauoj.append([])
    return int(dim)
  except ValueError:
    return -1

#Remplisage des colones
def remp(plateau):
  count = 0
  for tab in range(len(plateau)):
   for el in range(len(plateau)):
     plateau[count].append("~~~")
   count += 1


#Modifier la valeur d'une case selon "x-x"
def placement(case, plateau):
  try:
    case.split("-")
    num = int(case[2]) - 1
    lettre = alpha.index(case[0].upper())
    if plateau[int(num)][int(lettre)] == "~~~":
      plateau[int(num)][int(lettre)] = "[ ]"
      return 1
    else:
      return 0
  except ValueError:
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
  print(f"     \n    [plateau {user}]\n     ", end="")
  for i in plateauj:
    print(f"{alpha[count]}    ", end="")
    count += 1
  print("\n")

  #Affichage des nombres et des cases
  count = 1
  for el in plateau:
    print(f"{count} | ", end="")
    for el1 in el:
      print(f"{el1}  ", end="")
    print("|\n")
    count += 1

#Placement automatique des bateaux (dépend de "placement()")
def makeo(plateau):
  count = 0
  while count < nbrbateau:
    lettre = randint(0,4)
    numo = randint(0,4)
    case = f"{alpha[lettre]}-{str(numo)}"
    if placement(case, plateau) == 1:
      count += 1
  
#Placement manuel des bateaux (dépend de "placement()")
def makef(plateau):
  print(f"Placez {nbrbateau} bateaux")
  count = 0
  while count < nbrbateau:
    retourplacement = placement(input("case: "), plateau)
    if retourplacement == 1:
      aff(plateau)
      count += 1
    elif retourplacement == 0:
      print("Vous ne pouvez pas placer 2 bateaux sur la même case")
    else:
      print("saisie incorrecte")

def boom(case, plateau0, plateau1):
  case.split("-")
  num = int(case[2]) - 1
  lettre = alpha.index(case[0].upper())
  if plateau0[int(num)][int(lettre)] == "~~~":
    plateau1[int(num)][int(lettre)] = "~x~"
    plateau0[int(num)][int(lettre)] = "~x~"
    aff(plateau1)
    print("Manqué!")
  elif plateau0[int(num)][int(lettre)] == "[ ]":
    plateau1[int(num)][int(lettre)] = "[X]"
    aff(plateau1)
    print("Coulé!")
  else:
    print("?")


    
  

    

#Saisie utilisateur dans "dim()"

count = 0
while count != 1:
  retourdim = dim(input("Coté des plateaux: "))
  if retourdim >= 3 and retourdim <= 26:
    count += 1
    nbrbateau = (retourdim//2)+1
  elif retourdim > 0:
    print("Veulliez entrer un nombre compris entre 3 et 26")
  else:
    print("saisie incorrecte")

remp(plateauj)
remp(plateaujo)
remp(plateauo)
remp(plateauoj)
makeo(plateauo)
makef(plateauj)

boom(input("case: "), plateauo, plateaujo)
