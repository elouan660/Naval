from random import *

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O']
plateauj = []
plateauo = []
def dim(dim):
  for i in range(int(dim)):
    plateauj.append([])
    plateauo.append([])

#création des cases
def remp(plateau):
  count = 0
  for tab in range(len(plateau)):
   for el in range(len(plateau)):
     plateau[count].append("~~~")
   count += 1


#Modifier la valeur d'une case selon "Lettre-nombre"
def placement(case, plateau):
  case.split("-")
  num = int(case[2]) - 1
  lettre = alpha.index(case[0].upper())
  if plateau[int(num)][int(lettre)] == "~~~":
    plateau[int(num)][int(lettre)] = "[ ]"
    return 0
  else:
    return -1


#Afficher le plateau
def aff(plateau):
  count = 0
  print("     ", end="")
  if plateau == plateauo:
    user = "ordinateur"
  else:
    user = "joueur"

  print(f"\n    [plateau {user}]\n     ", end="")
  for i in plateauj:
    print(f"{alpha[count]}    ", end="")
    count += 1
  print("\n")

  count = 1
  for el in plateau:
    print(f"{count} | ", end="")
    for el1 in el:
      print(f"{el1}  ", end="")
    print("|\n")
    count += 1


def makeo(plateau):
  count = 0
  while count < 3:
    lettre = randint(0,4)
    numo = randint(0,4)
    case = f"{alpha[lettre]}-{str(numo)}"
    if placement(case, plateau) == 0:
      count += 1
  

def makef(plateau):
  print("Placez 3 bateaux")
  count = 0
  while count < 3:
    if placement(input("case: "), plateau) == 0:
      aff(plateau)
      count += 1

dim(input("Coté du plateau de jeu: "))
remp(plateauj)
remp(plateauo)
makeo(plateauo)
makef(plateauj)
aff(plateauo)
