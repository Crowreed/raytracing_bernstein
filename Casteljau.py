def vecteurdesmilieux(v):
    l = len(v)
    vm = []
    
    for k in range(l-1):
        vm.append((v[k]+v[k+1])/2.)
    return vm

def Casteljau(v):
    l = len(v)
    pv, dv, sv = [], [], []
    
    sv.append(v)
    
    for k in range (1, l):
        sv.append(vecteurdesmilieux(sv[k-1]))
        
    for k in range(l):
        pv.append(sv[k][0])
        dv.append(sv[l-1-k][-1])
        
    return (pv, dv)
