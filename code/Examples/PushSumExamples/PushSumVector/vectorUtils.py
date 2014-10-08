def sum(a, b):
  list_sum = []
  for i in range(0,len(a)):
       list_sum.append(a[i]+b[i])
  return list_sum

def mul(a, x):
  list_mul = {}  
  for i in range(0,len(a)):
    list_mul[i] = a[i]*x
  return list_mul

def mulVector(a,b):
  list_mul = []
  for i in range(0,len(a)):
       list_mul.append(a[i]*b[i])
  return list_mul

def initVector(lenght, pos):  
  list_init = {}  
  for i in range(0,lenght):
     list_init[i] = 0   
     list_init[pos] = 1 
  return list_init

def initZeros(lenght):
  list_init = []
  for i in range(0,lenght):
    list_init.append(0)
  return list_init

def sumElems(list):
  sum = 0
  for i in range(0,len(list)):
     sum+=list[i]
  return sum