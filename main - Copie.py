import math
import random
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from Object3D import *
from Polynome import *
from solveracine import *
from multiprocessing import *
from matrice import *
from processcalculus import *
from bool1d import *

def topolent(e):
    return e.topolent()

test = [1, 2, 3]

#a tuple à donner en paramètre
#b tuple qui sera modifié

def vtol( tab):
    if 0==len( tab):
        return None
    else:
        l = None
        for i in range( len( tab)-1, -1, -1) :
            l= ( tab[i], l)
        return l

#un rayon mdr
class Rayon(object):
    def __init__(self, source, dir):
        self.source = source
        self.dir = dir
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
        
        return differ(list_inter_a, list_inter_b)
        
        
class Inter():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def intersection(self, rayon):
        ""

class Differ():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def intersection(self, rayon):
        " "
deuxboules = Union( Prim(boule(-0.5,0,0,1), (150,150,150)) , Prim(boule(0.5,0,0,1), (240,150,150)) )

def rendering( cam, contact):
	(rr,vv,bb)= contact.color
	(rr,vv,bb)= (float(rr), float(vv), float(bb))
	(a,b,c,d) = contact.plan
	ps=pscal3(a,b,c, cam.soleil)
	ps = clamp( -1., 1., ps)
	coef= interpole( -1., 0.5, 1., 1., ps)
	return (int(coef*rr), int(coef*vv), int(coef*bb))
    
class Camera(object):
    def __init__(self, o, ox, oy, oz, hsizeworld, hsizewin, soleil, nom):
        self.o = o
        self.ox = ox #vers la droite du spectateur
        self.oy = oy #regard du spectateur
        self.oz = oz #vertical du spectateur
        self.hsizeworld = hsizeworld
        self.hsizewin = hsizewin
        self.soleil = normalize3(soleil)
        self.background = (44, 55, 88)
        self.nom = nom
        
    #???# enfin j'ai compris mais po tout
    def generate_ray(self, x, z):
        (x0, y0, z0)= self.o
            
        kx = interpole( 0., 0., self.hsizewin, self.hsizeworld, float(x))
        kz = interpole( 0., 0., self.hsizewin, self.hsizeworld, float(z))
        
        return Rayon( (x0 + kx*self.ox[0] + kz*self.oz[0], y0 + kx*self.ox[1] + kz*self.oz[1], z0 + kx*self.ox[2] + kz*self.oz[2]), self.oy)

#lancer de rayons de tous les pixels

def raycasting( cam, objet):
    #print("début raycasting", cam.nom)
    img=Image.new("RGB", (2*cam.hsizewin+1, 2*cam.hsizewin+1), (255,255,255))
    for xpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
        for zpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
            rayon= cam.generate_ray(xpix, zpix)
            intervalles=objet.intersection(rayon)
            
            if []==intervalles or intervalles==None:
                (r,v,b)= cam.background
            #elif intervalles[0].a.t > 10:
            #    (r,v,b)= cam.background
            else:
                #(r,v,b)= rendering(cam, intervalles[0].a)
                (r, v, b) = (122,255,122)
               
                
            img.putpixel( (xpix+cam.hsizewin, cam.hsizewin-zpix),(r,v,b)) #what
    
    img.save( cam.nom)
    #print("fin raycasting", cam.nom)
    
oeil = (0.000003,-4.,0.000003)
droite = (1.,0.,0.)
regard = (0.,1.,0.)
vertical = (0.,0.,1.)

camera=Camera( oeil, droite, regard, vertical, 1.5, 50, normalize3((0., -1., 2.)), "zitrus.png")




raycasting( camera, deuxboules)

PI = 3.1415926565
MESURE = PI/180.

def anim_rota_cam_y():
    
    oeil = Point4H(0.000003, -4., 0.000003)
    droite = Vecteur4H(1., 0., 0.)
    regard = Vecteur4H(0.,1.,0.)
    vertical = Vecteur4H(0.,0.,1.)
    
    if __name__ == '__main__':
        for j in range(60):
            processes = []
            for k in range(6):
                n = j*6+k
                NEW_MESURE = MESURE * n
                
                if n < 10:
                    nom = str("image00"+str(n)+".png")
                elif n < 100:
                    nom = str("image0"+str(n)+".png")
                else:
                    nom = str("image"+str(n)+".png")
                
                #calcul nouveau oeil
                trf_oeil = rotaz4H(NEW_MESURE)
                trsf_oeil = trf_oeil.mat_directe*oeil
                
                (ox, oy, oz, ot) = trsf_oeil.toVect()
                
                #transformations
                trf = rotaz4H(NEW_MESURE)
                trf2 = rotaz4H(NEW_MESURE)
                
                trsf_droite = trf2.mat_directe*droite 
                trsf_regard = trf.mat_directe*regard
                trsf_vertical = trf.mat_directe*vertical
                
                (dx, dy, dz, dt) = trsf_droite.toVect()
                (rx, ry, rz, rt) = trsf_regard.toVect()
                (vx, vy, vz, vt) = trsf_vertical.toVect()
                
                camera = Camera((ox, oy, oz), (dx, dy, dz), (rx, ry, rz), (vx, vy, vz), 8, 40, normalize3((0., -1., 2.)), nom)
                
                processes.append(Process(target=raycasting, args=(camera, Prim(boule(0,0,0,1), (150,150,150)))))
            
            for p in processes:
                p.start()

            for p in processes:
                p.join()
