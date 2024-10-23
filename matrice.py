import math

class Contact(object):
    def __init__( self, t, pt, plan, color):
        self.t = t
        self.pt = pt
        self.plan = plan
        self.color = color

class Matrice():
    def __init__(self, tab):
        self.mat = tab
    
    def nb_ligne(self):
        return len(self.mat)
    
    def nb_colonne(self):
         return len(self.mat[0])
    
    def get(self, i, j): #ième ligne, jème colonne
        return self.mat[i][j]
        
    def __str__(self):
        return str(self.mat)
    
    def __add__(self, a):
        if self.nb_colonne()==a.nb_colonne() and self.nb_ligne() == a.nb_ligne():
            sum = []
            for i in range (self.nb_ligne()):
                tmpligne = []
                for j in range (self.nb_colonne()):
                    tmpligne.append(self.get(i, j)+a.get(i, j))
                
                sum.append(tmpligne)
            return sum  
                    
    def __mul__(self, b):
       
        nb_ligne_a = len(self.mat)
        nb_colonne_a = len(self.mat[0])
        
        nb_ligne_b = len(b.mat)
        nb_colonne_b = len(b.mat[0])
        
   
        mul = []
        if (nb_colonne_a == nb_ligne_b or nb_colonne_b == nb_ligne_a):
 
            for i in range(nb_ligne_a):
                mul.append([])
                for j in range(nb_colonne_b):
                    s = 0
                    for k in range (nb_colonne_a):
                        s+=self.get(i, k)*b.get(k, j)
                    mul[i].append(s)
            
            return Matrice(mul)
        else:
            return Matrice([[]])
        
    def __sub__(self, a):
         if self.nb_colonne()==a.nb_colonne() and self.nb_ligne() == a.nb_ligne():
            sum = []
            for i in range (self.nb_ligne()):
                tmpligne = []
                for j in range (self.nb_colonne()):
                    tmpligne.append(self.get(i, j)-a.get(i, j))
                    
                sum.append(tmpligne)
            return sum
        
    def toVect(self):
        vect = []
        for i in range(self.nb_ligne()):
            for j in range(self.nb_colonne()):
                vect.append(self.get(i, j))
        return vect

class Point4H(Matrice):
    def __init__(self, x, y, z):
        
        self.mat = [[x], [y], [z], [1]]

class Vecteur4H(Matrice):
    def __init__(self, x, y, z):
        
        self.mat = [[x], [y], [z], [0]]
        
class Transformation():
    def __init__(self, mat_directe, mat_inverse):
        self.mat_directe = Matrice(mat_directe)
        self.mat_inverse = Matrice(mat_inverse)
        
    def __mul__(self, a):
        return Transformation(self.mat_directe*a.mat_directe, self.mat_inverse*a.mat_inverse)
        
        
def inverse_trf(trf):
    return Transformation(trf.mat_inverse, trf.mat_directe)

def translation4H(tx, ty, tz):
    mat_directe = [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]]
    mat_inverse = [[1, 0, 0, -tx], [0, 1, 0, -ty], [0, 0, 1, -tz], [0, 0, 0, 1]]
    
    return Transformation(mat_directe, mat_inverse)

def rotax4H(theta):
    mat_directe = [[1, 0, 0, 0], [0, math.cos(theta), -math.sin(theta), 0], [0, math.sin(theta), math.cos(theta), 0], [0, 0, 0, 1]]
    mat_inverse = [[1, 0, 0, 0], [0, math.cos(-theta), -math.sin(-theta), 0], [0, math.sin(-theta), math.cos(-theta), 0], [0, 0, 0, 1]]

    return Transformation(mat_directe, mat_inverse)

def rotay4H(theta):
    mat_directe = [[math.cos(theta), 0, math.sin(theta), 0], [0, 1, 0, 0], [-math.sin(theta), 0, math.cos(theta), 0], [0, 0, 0, 1]]
    mat_inverse = [[math.cos(-theta), 0, math.sin(-theta), 0], [0, 1, 0, 0], [-math.sin(-theta), 0, math.cos(-theta), 0], [0, 0, 0, 1]]
    
    return Transformation(mat_directe, mat_inverse)

def rotaz4H(theta):
    
    mat_directe = [[math.cos(theta), -math.sin(theta), 0, 0], [math.sin(theta), math.cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    mat_inverse = [[math.cos(-theta), -math.sin(-theta), 0, 0], [math.sin(-theta), math.cos(-theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    
    return Transformation(mat_directe, mat_inverse)

def affinite4H(a, b, c):
    mat_directe = [[a,0,0,0],[0,b,0,0],[0,0,c,0],[0,0,0,1]]
    mat_inverse = [[1/a,0,0,0],[0,1/b,0,0],[0,0,1/c,0],[0,0,0,1]]
    
    return Transformation(mat_directe, mat_inverse)


#def transformation_camera(camera, transformation_point, transformation_repere):
    
def transformation_rayon4H(rayon, transformation):
   
    (x, y, z) = rayon.source
    smat = Point4H(x,y,z)
   
    (dx, dy, dz) = rayon.dir 
    dmat = Vecteur4H(dx,dy,dz)
     
    transfosmat = transformation.mat_directe*smat
    transfodmat = transformation.mat_directe*dmat
   
    tsx = transfosmat.get(0,0) 
    tsy = transfosmat.get(1,0)
    tsz = transfosmat.get(2,0)
    
    tdx = transfodmat.get(0,0)
    tdy = transfodmat.get(1,0)
    tdz = transfodmat.get(2,0)
    
    trfsource = (tsx, tsy, tsz)
    trfdir = (tdx, tdy, tdz)
      
    return trfsource, trfdir
    
def transformation_contact(contact, transformation):
    pt = contact.pt
    plan = contact.plan
    
    (x, y, z) = pt
    vpt = (x, y, z, 1)
    [a, b, c, d] = plan
    vplan = [a, b, c, d]
    
    matvpt = Matrice(vpt)
    matvplan = Matrice(vplan)
    
    transfomatvpt = transformation.mat_directe*matvpt
    transfomatvplan = transformation.mat_inverse*matvplan
    
    trf_pt = (transfomatvpt.get(0,0),transfomatvpt.get(0,1),transfomatvpt.get(0,2))
    trf_contact = (transfomatvplan.get(0,0),transfomatvplan.get(0,1),transfomatvplan.get(0,2), transfomatvplan.get(0,3))
    return Contact(contact.t, trf_pt, trf_plan, contact.color)


# faire le produit scalaire pour des matrices
# phase 3= operation bouleenes entre objets.
#  intersection, union, difference
#  - soit la transformation (translation, homothétie ou affinité, rotation, symétrie, etc) d'un objet solide.
#Les transformations pourront être représentées par des matrices 4x4.
#- soit la réunion, l'intersection ou la différence entre deux objets solides. Cette représentation
#arborescente est appelée CSG, Constructive Solid Geometry
