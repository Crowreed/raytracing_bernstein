from multiprocessing import *
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
