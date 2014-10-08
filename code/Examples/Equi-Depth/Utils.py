from random import randint

def initArray(k):
    a = []
    for i in range(0,k):
        x = randint(1,100)
        a.append((x,1))
    return a

def merge(a,b):
    x = []
    print "A %d"%len(a)
    print "B %d"%len(b)
    for i in range(0,len(a)):
        c = (a[i],b[i])
        j =  randint(0,1)
        x.append(c[j])
    return x
