from random import choice,randint

def electLeader(a):
    return choice(a)


def initLeaderArray():
    a = []
    for i in range(0,100):
        a.append(0)
    for i in range(0,1):
        a[randint(0,100)] = 1
    return a
