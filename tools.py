import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy as np

import tkinter
from tkinter import filedialog


#=====================================================#
# Welcome Manager
#=====================================================#
def welcome() :
    
    print('Welcome in tp-01 : Segmentation d une image par seuillage ! \n\n\n It s recommended to run this script in a terminal (Control + T)\n\n\n # Please select file ...\n')
    
    #- condition
    selecter = None
    while not selecter :
        try :
            selecter = True
            root = tkinter.Tk()
            root.withdraw()
            Ipath = filedialog.askopenfilename(
                title = 'Choisisez une image :)',
                filetype = [("Images",  "*.png *.jpg *.jpeg")])
        except Exception as e :
            print('Erreur de selection réessayez :: ',e, '\n',type(e))
            selecter = False
    return Ipath


#=====================================================#
# Plot Class — Synchrone
#=====================================================#
class PlotWorker:
    """
    Gestionnaire d'affichage matplotlib synchrone.
    Accumule les commandes (imshow, hist, plot) dans une grille
    dynamique et affiche tout d'un coup à l'appel de stop().
    """

    def __init__(self, cols: int = 3):
        self.cols      = cols
        self.queue     = []          #> stock commands FIFO

    # ── API publique ──────────────────────────────────────────────────────────

    def plot(self, x, y, label=None):
        self.queue.append({'cmd': 'plot', 'x': x, 'y': y, 'label': label})

    def imshow(self, img, title='', cmap='gray'):
        self.queue.append({'cmd': 'imshow', 'img': img, 'title': title, 'cmap': cmap})

    def histshow(self, data, bins=256, range=None, vlines=None, xlabel='', ylabel='', title='Histogramme') :
        data_flat = np.asarray(data).ravel()
        
        self.queue.append({
            'cmd'   : 'hist',
            'data'  : data_flat,
            'bins'  : bins,
            'range' : range,
            'vlines': vlines or [],
            'xlabel': xlabel,
            'ylabel': ylabel,
            'title' : title,
        })

    def hist(self, data, bins=256, range=None):
        #- init data
        data_flat = np.asarray(data).ravel()
        hist_values, bin_edges = np.histogram(data_flat, bins=bins, range=range)	#> Extract values

        return hist_values, bin_edges
    
    
    def show(self):
        """Construit et affiche la figure complète."""
        n     = len(self.queue)
        if n == 0:
            return
        #-
        cols  = min(self.cols, n)
        rows  = (n + cols - 1) // cols

        fig = plt.figure(figsize=(5 * cols, 4 * rows))
        gs  = gridspec.GridSpec(rows, cols, figure=fig, hspace=0.5, wspace=0.3)

        for idx, item in enumerate(self.queue):
            row = idx // cols
            col = idx % cols
            ax  = fig.add_subplot(gs[row, col])
            cmd = item['cmd']

            # ── IMAGE ────────────────────────────────────────────────────────
            if cmd == 'imshow':
                ax.imshow(item['img'], cmap=item.get('cmap'))
                ax.set_title(item.get('title', 'Image'))
                ax.axis('off')

            # ── HISTOGRAMME ──────────────────────────────────────────────────
            elif cmd == 'hist':
                ax.hist(
                    item['data'].ravel(),
                    bins=item.get('bins', 256),
                    range=item.get('range'),
                    color='steelblue'
                )
                for vl in item.get('vlines', []):
                    ax.axvline(
                        x=vl['x'],
                        color=vl.get('color', 'red'),
                        linestyle=vl.get('linestyle', '--'),
                        linewidth=vl.get('linewidth', 1.5),
                        label=vl.get('label')
                    )
                ax.set_title(item.get('title', 'Histogramme'))
                ax.set_xlabel(item.get('xlabel', ''))
                ax.set_ylabel(item.get('ylabel', ''))
                if any(vl.get('label') for vl in item.get('vlines', [])):
                    ax.legend()

            # ── COURBE ───────────────────────────────────────────────────────
            elif cmd == 'plot':
                ax.plot(item['x'], item['y'], label=item.get('label'))
                ax.set_title('Courbe')
                if item.get('label'):
                    ax.legend()

        plt.tight_layout()
        plt.show()
