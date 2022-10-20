#À résoudre: 
# x>9 en num est mal pris en charge
# Faire varier la quantité de bateaux
# Prise en charge des mauvaises saisies pour "dim"
from random import *

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
plateauj = []
plateauo = []
#Définition des dimension du tableau
def dim(dim):
  count = 0
  try:
    for i in range(int(dim)):
      plateauj.append([])
      plateauo.append([])
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
  if plateau == plateauo:
    user = "ordinateur"
  else:
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
  while count < 3:
    lettre = randint(0,4)
    numo = randint(0,4)
    case = f"{alpha[lettre]}-{str(numo)}"
    if placement(case, plateau) == 1:
      count += 1
  
#Placement manuel des bateaux (dépend de "placement()")
def makef(plateau):
  print("Placez 3 bateaux")
  count = 0
  while count < 3:
    retourplacement = placement(input("case: "), plateau)
    if retourplacement == 1:
      aff(plateau)
      count += 1
    elif retourplacement == 0:
      print("Vous ne pouvez pas placer 2 bateaux sur la même case")
    else:
      print("saisie incorrecte")

    

#Saisie utilisateur dans "dim()"
count = 0
while count < 1:
  if dim(input("Coté des plateaux: ")) == 1:
    count += 1
  else:
    print("saisie incorrecte")

remp(plateauj)
remp(plateauo)
makeo(plateauo)
makef(plateauj)
aff(plateauo)
