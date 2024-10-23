def puissancerecursif(a, b):
    if(b==0):
        return 1
    else:
        return a*puissancerecursif(a, b-1)

def factrecursif(n):
    if(n==0):
        return 1
    else:
        return n*factrecursif(n-1)
    
def coeffbin(k, n):
    if k> n:
        return 0
    else:
        return (factrecursif(n))/((factrecursif(k)*factrecursif(n-k)))


def tobernstein(b):
    l=len(b)
    pol = [0]*l
    for k in range(l):
        for i in range(l):
            pol[k] = pol[k] + b[i]*(coeffbin(i,k)/coeffbin(i,l-1))
    return pol
