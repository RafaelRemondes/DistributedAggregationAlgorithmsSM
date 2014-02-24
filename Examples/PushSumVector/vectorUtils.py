class vectorUtils():
	
    def sum(self, a, b):
       list_sum = {}
       for i in range(0,len(a)-1):
          list_sum[i] = a[i]+b[i]
       return list_sum

    def mul(self, a, x):
      list_mul = {}      
      for i in range(0,len(a)-1):        
        list_mul[i] = a[i]*x    
      return list_mul

    def initVector(self,lenght, pos):      
      list_init = {}      
      for i in range(0,lenght-1):        
        list_init[i] = 0   
      list_init[pos] = 1 
      return list_init
    
    def initZeros(self,lenght):
      list_init = {}
      for i in range(0,lenght-1):
        list_init[i] = 0
      return list_init

    def sumElems(self, list):
      sum = 0
      for i in range(0,len(list)-1):
        sum+=list[i]
      return sum