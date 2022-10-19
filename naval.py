from random import *
print('test')
alpha = ['A', 'B', 'C', 'D', 'E']
plateauj = [[], [], [], [], []]
plateauo = [[], [], [], [], []]
#Affichage des dimensions du plateau
print(f"Dimensions du plateau: {len(plateauj)}x{len(plateauj)}")
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
  if plateau == plateauo:
    print("\n     A    B    C    D    E\n     [plateau ordinateur]\n")
  else:
    print("     A    B    C    D    E\n       [plateau joueur]\n")
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


remp(plateauj)
remp(plateauo)
makeo(plateauo)
makef(plateauj)
aff(plateauo)
