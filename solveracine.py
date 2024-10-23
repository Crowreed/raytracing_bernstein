from bernstein import *
from Casteljau import *
from Polynome import *

def solve(epsilon, tab, t1, t2, solutions):

    
    if 0.< min(tab) or 0. > max(tab):
       
        return solutions
    else:
        dt = t2-t1
       
        if dt < epsilon:
            if solutions != []:
                return [((t1+t2)/2.), solutions]
            else:
                return [(t1+t2)/2.]
        else:
            (tab1, tab2) = Casteljau(tab)
            tm = (t1+t2)/2.
            return solve(epsilon, tab1, t1, tm, solve(epsilon, tab2, tm, t2, solutions))
   

def mymap(f, tab):
    for i in range (len(tab)):
        if type(tab[i]) != list:
            tab[i] = f(tab[i])
        else:
            return mymap(f, tab[i])
    return tab

def hd():
    return

def reverse(tab):
    tr = []
    for i in range (len(tab)):
        tr.append(tab[-i-1])
    return tr

def racine(tab):
    tab=reverse(tab)
    polebernstein = tobernstein(tab)
    roots=solve(1e-10, polebernstein, 0., 1., [])
    
    roots2 = []
    net(roots, roots2)
    
    
    return (reverse(mymap(lambda x: 1./x,roots2)))


def net(tab, newtab): #nettoye le tableau des sous tableaux
    for i in range (len(tab)):
        if type(tab[i]) != list:
            newtab.append(tab[i])
        else:
            net(tab[i], newtab)

