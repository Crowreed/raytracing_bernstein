from DAG import *

def boule(cx, cy, cz, r):
    x = Var("x")
    y = Var("y")
    z = Var("z")
    
    return (x - Nb(cx)) * (x - Nb(cx)) + (y - Nb(cy)) * (y - Nb(cy)) + (z - Nb(cz)) * (z - Nb(cz)) - Nb(r) * Nb(r)

def tore(r, R):
    x=Var("x")
    y=Var("y")
    z=Var("z")
    
    tmp = x * x + y * y + z * z + Nb(R * R - r * r)
    
    return tmp * tmp - Nb(4. * R * R) * (x * x + z * z)

def steiner2():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    
    return (x * x * y * y - x * x * z * z + y * y * z * z - x * y * z)

def steiner4():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    
    return y * y - Nb(2.) * x * y * y - x * z * z + x * x * y * y + x * x * z * z - z * z * z * z

def hyperboloide_2nappes():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    
    return Nb(0.) - (z * z - (x * x + y * y + Nb(0.1)))

def hyperboloide_1nappe():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    
    return Nb(0.) - (z * z - (x * x + y * y - Nb(0.1)))

def roman():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    
    return (x * x * y * y + x * x * z * z + y * y * z * z - Nb(2.) * x * y * z)