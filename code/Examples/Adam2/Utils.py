def merge(hp,hq,a):
   h = []
   if hq == []:
      return hp
   else:
      if hp == []:
         for i in range(0,len(hq)):
            if a<=hq[i][0]:
               h.append((hq[i][0],1))
            else:
               h.append((hq[i][0],0))
      else:
         for i in range(0,len(hp)):
            h.append((hp[i][0], (hq[i][1]+hp[i][1])/2))
      return h

def findN(h):
    maxN  = 0
    n = 0
    for i in range(1,len(h)):
        if (h[i][1]-h[i-1][1]) > maxN :
            maxN = (h[i][1]-h[i-1][1])
            n = i
    return n

def findM(h):
    minM  = 3380
    m = 0
    for i in range(1,len(h)-1):
        if (h[i+1][1]-h[i-1][1]) < minM :
            maxN = (h[i][1]-h[i-1][1])
            m = i
    return m


def minMax(h_old):
    h = h_old
    while 1:
        n = findN(h)
        m = findM(h)
        if (h[n][1]-h[n-1][1]) > (h[m+1][1]-h[m-1][1]):
            (tm,fm) = h[m]
            h.remove((tm,fm))
            h.append(  (h[n][0]+h[n-1][0])/2,h[n][1]+h[n-1][1])/2)
        else:
            return h





