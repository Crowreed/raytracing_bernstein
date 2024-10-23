from DAG import *
from solveracine import *
from util import *
from bool1d import *
from matrice import *
#un rayon mdr

#???#
class Obj(object): 
    def __init__( self):
        " "
#???#        " "
class Prim(Obj):
    def __init__(self, fonc_xyz, color):
        self.fonc = fonc_xyz
        self.color = color
        
    def creer_contact(self, rayon, t): #t est une racine
        (sx, sy, sz) = rayon.source
        (dx, dy, dz) = rayon.dir
        
        x = sx + dx*t
        y = sy + dy*t
        z = sz + dz*t
        pt = (x, y, z)
        
        (a, b, c) = self.normale(x, y, z)
        
        d = a*x+b*y+c*z
        
        plan = (a, b, c, d)
        
        color = (255, 255, 255)
        
        return Contact(t, pt, plan, color)

    def intersection( self, rayon):
        dico = { "x": Nb(rayon.source[0]) + Nb(rayon.dir[0])*Var("t"),"y": Nb(rayon.source[1]) + Nb(rayon.dir[1])*Var("t"),"z": Nb(rayon.source[2]) + Nb(rayon.dir[2])*Var("t")}
        expression_en_t = self.fonc.evalsymb(dico)
        
        pol_t = expression_en_t.topolent()
        
        contacts = []
        roots = racine(pol_t.vect())
        
        intervalles = []
        
        #on va créer les intervalles
        if(roots != []):
            for i in range (0, len(roots), 2): #calcul d'intervalles conne à revoir le plus rapidement possible
                intervalles.append(Intervalle(self.creer_contact(rayon, roots[i]), self.creer_contact(rayon, roots[i+1])))
                
        return (intervalles) 
    
    def normale(self, x, y, z):
        fx = self.fonc.derivee("x")
        fy = self.fonc.derivee("y")
        fz = self.fonc.derivee("z")
        dico = {"x":x, "y":y, "z":z}
        (a,b,c) = (fx.eval(dico), fy.eval(dico), fz.eval(dico))
        return normalize3((a, b, c))

#Intervalle prenant deux contacts
class Intervalle():
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def toTuple():
        return(a, b)
   
class Objet_transfo(Obj):
    def __init__(self, objet, transfo):
        self.objet = objet
        self.transfo = transfo
    
    def intersection(self, rayon):
        trf_inverse_rayon = transformation_rayon4H(rayon, translation4H(0.5,0.5,0.5))
        
        (source, direction) = trf_inverse_rayon
        trf_rayon = Rayon(source, direction)
        dico = { "x": Nb(trf_rayon.source[0]) + Nb(trf_rayon.dir[0])*Var("t"),
                 "y": Nb(trf_rayon.source[1]) + Nb(trf_rayon.dir[1])*Var("t"),
                 "z": Nb(trf_rayon.source[2]) + Nb(trf_rayon.dir[2])*Var("t")}
        expression_en_t = self.objet.fonc.evalsymb(dico)
        pol_t = expression_en_t.topolent()
        contacts = []
        roots = racine(pol_t.vect())
       
        for i in range(len(roots)):
            contacts.append(self.objet.creer_contact(rayon, roots[i]))
            
        return contacts 
        
    def normale(self, x, y, z):
        fx = self.objet.fonc.derivee("x")
        fy = self.objet.fonc.derivee("y")
        fz = self.objet.fonc.derivee("z")
        dico = {"x":x, "y":y, "z":z}
        (a,b,c) = (fx.eval(dico), fy.eval(dico), fz.eval(dico))
        return normalize3((a, b, c))

class Union():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def intersection(self, rayon):
        intersection_a = self.a.intersection(rayon)
        intersection_b = self.b.intersection(rayon)
    
        list_inter_a = vtol(intersection_a)
        list_inter_b = vtol(intersection_b)
        
        return union(list_inter_a, list_inter_b)
        
        
class Inter():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def intersection(self, rayon):
        intersection_a = self.a.intersection(rayon)
        intersection_b = self.b.intersection(rayon)
    
        list_inter_a = vtol(intersection_a)
        list_inter_b = vtol(intersection_b)
        
        return inter(list_inter_a, list_inter_b)

class Differ():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def intersection(self, rayon):
        intersection_a = self.a.intersection(rayon)
        intersection_b = self.b.intersection(rayon)
    
        list_inter_a = vtol(intersection_a)
        list_inter_b = vtol(intersection_b)
        
        return differ(list_inter_a, list_inter_b)
    