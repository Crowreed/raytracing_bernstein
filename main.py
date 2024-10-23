import os
import sys
from PIL import Image, ImageDraw, ImageFont
from Object3D import *
from util import *
from rayon import *
from Object import *

deuxboules = Union( Prim(boule(-0.5,0,0,0.5), (150,150,150)) , Prim(boule(1,-1,0,1), (240,150,150)) )

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
        print(xpix)
        for zpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
            rayon= cam.generate_ray(xpix, zpix)
            intervalles=objet.intersection(rayon)
            
            if []==intervalles or intervalles==None:
                (r,v,b)= cam.background
            #elif intervalles[0].a.t > 10:
            #    (r,v,b)= cam.background
            else:
                
                (r,v,b)= rendering(cam, hd(intervalles).a)
                 
            img.putpixel( (xpix+cam.hsizewin, cam.hsizewin-zpix),(r,v,b)) #what
    
    img.save( cam.nom)
    #print("fin raycasting", cam.nom)
    
oeil = (0.000003,-4.,0.000003)
droite = (1.,0.,0.)
regard = (0.,1.,0.)
vertical = (0.,0.,1.)

camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)), "zitrus1.png")

raycasting( camera, deuxboules)
