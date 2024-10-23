def hd(A):
    (h, t) = A
    return h

def tl(A):
    (h, t) = A
    return t
    
def tof(a):
    return a.t

def union(A, B):
    if None == A:
        return B
    
    elif None == B:
        return A
    
    else:
        (ta, qa) = (hd(A), tl(A))
        (tb, qb) = (hd(B), tl(B))
        (a1, a2) = (tof(ta.a), tof(ta.b))
        (b1, b2) = (tof(tb.a), tof(tb.b))
        
        assert(a1 <= a2)
        assert(b1 <= b2)
        
        if a1 > b1:
            return union(B, A)
        
        elif a2 < b1:
            return (ta,(union(tl(A), B)))
        
        elif b2 <= a2:
            return union((ta, tl(A)), tl(B))
        
        else:
            return union(union((a1, b2), tl(A)) , tl(B))

def differ(A, B):
    if None == A:
        return None
    
    elif None == B:
        return A
    
    else:
        (ta, qa) = (hd(A), tl(A))
        (tb, qb) =  (hd(B), tl(B))
        (a1, a2) = (ta.a.t, ta.b.t)
        (b1, b2) = (tb.a.t, tb.b.t)
        
        assert(a1 <= a2)
        assert(b1 <= b2)
        
        if b2 <= a1:
            return differ(A, tl(B))
        
        elif a2 <= b1:
            return ta, differ(tl(A), B)
        
        elif b1 <= a1:
            if b2 <= a2:
                return differ(((b2, a2), tl(A)), tl(B) )
        
            else:
                return differ(tl(A), B)
            
        elif a2 <= b2:
            return ((a1, b1), differ(tl(A), B))
        
        else:
            return ((a1, b1), differ(((b2, a2),tl(A)), tl(B)))

def inter(A, B):
    if None == a or None == b:
        return None
    else:
        (ta, qa) = (hd(A), tl(A))
        (tb, qb) =  (hd(B), tl(B))
        (a1, a2) = (ta.a.t, ta.b.t)
        (b1, b2) = (tb.a.t, tb.b.t)
        
        assert(a1 <= a2)
        assert(b1 <= b2)
        
        if a1 > b1:
            return inter(b, a)
        
        elif a2 < b1:
            return inter(qa, b)
        
        elif b2 <= a2:
            return ((b1, b2), inter(a, qb))
        
        else:
            return ((b1, a2), inter(qa, b))