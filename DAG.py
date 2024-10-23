from Polynome import *

class M(object):
    def __init__(self):
        "  "
    
    def __add__(self, b):
        return Plus(self, b)
    
    def __mul__(self, b):
        return Mult(self, b)
    
    def __sub__(self, b):
        return Plus(self, Opp(b))
    
class Opp(M):
    def __init__(self, a):
        self.a = a
    
    def eval(self, dico):
        return -self.a.eval(dico)
    
    def evalsymb(self, dico):
        return Nb(0.) - self.a.evalsymb(dico)
    
    def derivee(self, nom):
        return Nb(0.) - self.a.derivee(nom)
    
    def topolent(self):
        return Polynome([0]) - self.a.topolent()
    
    def toString(self):
        return "(-" + self.a.toString() + ")"
    
class Plus(M):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def eval(self, dico):
        return self.a.eval(dico) + self.b.eval(dico)
    
    def evalsymb(self, dico):
        return self.a.evalsymb(dico) + self.b.evalsymb(dico)
    
    def derivee(self, nom):
        return self.a.derivee(nom) + self.b.derivee(nom)
    
    def topolent(self):
        return self.a.topolent() + self.b.topolent()
    
    def toString(self):
        return "(" + self.a.toString() + "+" + self.b.toString() + ")"

class Mult(M):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def eval(self, dico):
        return self.a.eval(dico) * self.b.eval(dico)
    
    def evalsymb(self, dico):
        return self.a.evalsymb(dico) * self.b.evalsymb(dico)
    
    def derivee(self, nom):
        return self.a.derivee(nom) * self.b + self.a * self.b.derivee(nom)
    
    def topolent(self):
        return self.a.topolent() * self.b.topolent()
    
    def toString(self):
        return "(" + self.a.toString() + "*" + self.b.toString() + ")"

class Nb(M):
    def __init__(self, n):
        self.nb = n
    
    def eval(self, dico):
        return self.nb
    
    def evalsymb(self, dico):
        return self
    
    def derivee(self, nom):
        return Nb(0.)
    
    def topolent(self):
        return Polynome([self.nb])
    
    def toString(self):
        return str(self.nb)

class Var(M):
    def __init__(self, nom):
        self.nom = nom
    
    def eval(self, dico):
        if self.nom in dico:
            return dico.get(self.nom)
        
        else:
            return Var(self.nom)
    
    def evalsymb(self, dico):
        if self.nom in dico:
            return dico.get(self.nom)
        
        else:
            return self
        
    def derivee(self, nom):
        if (self.nom==nom):
            return Nb(1.)
        
        else:
            return self
        
    def topolent(self):
        if self.nom=="t":
            return Polynome([0.,1.])
    
    def toString(self):
        return self.nom