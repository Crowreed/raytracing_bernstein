class Polynome():
    def __init__(self, c):
        self.c = c
    
    def len(self):
        return len(self.c)
    
    def coeff(self, i):
        if i < self.len():
            return self.c[i]
        
        else:
            return 0
    
    def vect(self):
        return self.c
    
    def img(self, x):
        for i in range(len(self.c)):
            ""
        
    def __add__(self, Q):
        Z = []
        
        for i in range(max(self.len(), Q.len())):
            Z.append(self.coeff(i) + Q.coeff(i))
            
        return Polynome(Z)
    
    def __mul__(self, Q):
        fl = self.len() + Q.len()
        Z = []
        
        for i in range(fl - 1):
            Z.append(0)
            for j in range (i + 1):
                Z[i] += self.coeff(j) * Q.coeff(i - j)
                
        return Polynome(Z)
    
    def __sub__(self, Q):
        Z = []
        
        for i in range(max(self.len(), Q.len())):
            Z.append(self.coeff(i) - Q.coeff(i))
            
        return Polynome(Z)
    
    def __opp__(self):
        H = []
        
        for i in range(self.len()):
            H.append(-self.coeff(i))
            
        return Polynome(H)