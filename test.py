alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def arenear(case0, case1):
  case0.split('-')
  num0 = int(case0[2]) -1
  lettre0 = alpha.index(case0[0].upper())
  case1.split('-')
  num1 = int(case1[2]) -1
  lettre1 = alpha.index(case1[0].upper())
  print(f"[{num0-num1}|{lettre0-lettre1}]")
  if num0-num1 in range(-1,2) and lettre0-lettre1 in range(-1,2):
    return True
  else:
    return False

print(arenear('b-4','d-4'))