import numpy as np
import cv2 as cv

from tools import *


def detect_valley(Ig: np.ndarray)-> list:
    """
    Détecte automatiquement les seuils de segmentation d'une image en niveaux de gris
    par analyse de l'histogramme (maxima locaux → filtrage → vallées).

    Paramètres
    ----------
    Ig : np.ndarray
        Image 2D en niveaux de gris (dtype uint8, valeurs 0-255).

    Retour
    ------
    seuils : list[int]
        Liste triée des indices de niveaux de gris correspondant aux vallées
        (seuils de segmentation).
    """
    
    #- init maxima filtering steps
    P0, P1, P2, P3, P4 = ([] for _ in range(5))
    #- init histogram vars
    hist = plt.hist(Ig.ravel(), bins=256, range=(0,255))	#> all data
    hist = hist[0]											#> i data
    maxhist = max(hist)										#> max hist
    seuil_hist = 0.005 * maxhist							#> seuil level
    
    # ── Maxima local X2 +  Clean small pic ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    
    for i in range(1, len(hist) - 1):
        if hist[i] > hist[i-1] and hist[i] > hist[i+1]:
            P0.append(i)   												#> stock P0
            
    for i in range(1, len(P0) -1) :
        if hist[P0[i]] > hist[P0[i-1]] and hist[P0[i]] > hist[P0[i+1]] :
            P1.append(P0[i])											#> stock P1
            
    for i in P1 :
        if hist[i] >= seuil_hist:
           P2.append(i)													#> stock P2
    
    # ── Clean close pic ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

    i = 0
    while i < len(P2):
        #-0t
        p = P2[i]

        # Regarder les pics suivants tant qu'ils sont trop proches
        j = i + 1
        while j < len(P2) and (P2[j] - p) < 15:
            # On garde le plus haut
            if hist[P2[j]] > hist[p]:
                p = P2[j]
            j += 1
        P3.append(p)													#> stock P3
        #- next group
        i = j
    
    for i in range(len(P3) - 1):
        p1 = P3[i]
        p2 = P3[i+1]

    # ── Depth valley filtering ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        
        #- init current average
        Havg = sum(hist[p1:p2+1]) / (p2 - p1 + 1)	#> Havg : moyen p1-p2
        Hmean = (hist[p1] + hist[p2]) / 2			#> Hmean : moyen h pic

        #- valley not deep enough (Havg / Hmean > 0.75)
        if Havg / Hmean > 0.75:
            #- keep taller pic
            if hist[p1] >= hist[p2]:
                if p1 not in P4:
                    P4.append(p1)										#> stock P4
            else:
                if p2 not in P4:
                    P4.append(p2)
        #- valley (p1,p2) ok -> keep all
        else:
            if p1 not in P4:
                P4.append(p1)
            if p2 not in P4:
                P4.append(p2)
                
    #- clean double & sort
    P4 = sorted(set(P4))

    # ── Recover seuils ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    
    #- init res
    seuils = []
    for i in range(len(P4) - 1):
        #- current pic
        p1 = P4[i]
        p2 = P4[i+1]

        #- get min-valley p1-p2
        sous_hist = hist[p1:p2+1]
        idx_min_local = np.argmin(sous_hist)	#> i min-valley
        idx_min_global = p1 + idx_min_local		#> global i min-valley

        seuils.append(idx_min_global)									#> stock seuils

    print("Seuils = ", seuils)

    return seuils
 
def segment_img(Ig: np.array, seuils: list)-> np.array:
    """
    Segmente une image en niveaux de gris en régions distinctes par seuillage.
 
    
    Paramètres
    ----------
    Ig : np.ndarray
        Image 2D en niveaux de gris (dtype uint8, valeurs 0-255).
    seuils : list[int]
        Liste des seuils de segmentation (niveaux de gris, valeurs dans [0, 255]).
        N'a pas besoin d'être triée — le tri est appliqué automatiquement.
        Exemple : [60, 130, 200] produit 4 régions.

    Retour
    ------
    Iseg : np.ndarray
        Image 2D segmentée (même shape que Ig, dtype uint8).
    """

    #- sort by size
    seuils = sorted(seuils)

    #- init img res
    Iseg = np.zeros_like(Ig, dtype=np.uint8)

    #- apply seuillage
    Iseg[Ig < seuils[0]] = 0		#> 1st class

    for k in range(len(seuils) - 1):
        bas = seuils[k]
        haut = seuils[k+1]
        Iseg[(Ig >= bas) & (Ig < haut)] = (k+1) * (255 // (len(seuils)+1))	#> k-1 class

    Iseg[Ig >= seuils[-1]] = 255	#> Last class

    return Iseg




if __name__ == "__main__":
    
    while True :
            
        #- welcome get file
        Ipath = welcome()
        
        plt = PlotWorker(cols=3)
        
        #- init img -> gray
        I = cv.imread(Ipath)
        Ig = cv.cvtColor(I, cv.COLOR_BGR2GRAY); print('init img to gray')
        
        #- traitement
        seuils = detect_valley(Ig)			#> get filtred seuils
        Iseg = segment_img(Ig, seuils)			#> get segmented img

        #- display all
        plt.imshow(Ig)
        plt.histshow(
                data   = Ig,
                bins   = 256,
                range  = (0, 255),
                title  = 'Histogramme + Seuils',
                vlines = [{'x': s, 'color': 'red', 'label': f'seuil={s}'} for s in seuils]
                )
        plt.imshow(Iseg, cmap='viridis')
                
        #print("H0 - index values : \n\n",hist[0], 'card(hist)=',len(hist))
        #print("H1 - volume : \n\n", hist[1])
        
        plt.show()
        try :
            if int(input('\n\n\nSelect next image | (0) \nQuit script       | (1)\n#?> ')) :
                continue
            break
        except Exception as e :
            print('Error :: ',e)
            
    
