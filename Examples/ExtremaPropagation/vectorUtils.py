from random import expovariate

def initializeVector(k):
    list_init = []
    while (len(list_init) < k):
        x = expovariate(1.0)
        #if (x in list_init) == False:
        list_init.append(x)
    return list_init

def pointWiseMinimum(a,b):
    list_pwm = []
    for i in range(0,len(a)):
        if a[i] < b[i]:
            list_pwm.append(a[i])
        else:
            list_pwm.append(b[i])
    return list_pwm