# 🖼️ TP 2 — Segmentation d'image par détection des vallées

> **Licence 3ème Année — SPI | Traitement & Analyse d'images**
> Université de Nouvelle-Calédonie — Auteur du sujet : Nazha SELMAOUI

---

## 📌 Présentation du projet

Ce projet implémente une méthode de **segmentation d'image en niveaux de gris par seuillage automatique**, basée sur la détection des vallées dans l'histogramme.

L'idée centrale est simple : une image contenant plusieurs objets distincts produit un histogramme **multimodal** — plusieurs pics séparés par des creux. Ces creux, appelés **vallées**, constituent des frontières naturelles entre classes de pixels. Détecter ces vallées permet de placer automatiquement des seuils et de segmenter l'image sans intervention manuelle.

### Pipeline de l'algorithme

```
Image (niveaux de gris)
        │
        ▼
  Histogramme (256 bins)
        │
        ▼
  P0 — Tous les maxima locaux
        │
        ▼
  P1 — Maxima des maxima
        │
        ▼
  P2 — Filtrage : suppression des petits pics (< 5% du max)
        │
        ▼
  P3 — Fusion des pics trop proches (distance < 15 niveaux)
        │
        ▼
  P4 — Test de profondeur de vallée (havg / hmean > 0.75)
        │
        ▼
  Seuils ← minima entre chaque paire de pics retenus
        │
        ▼
  Image segmentée (étiquetée par région)
```

---

## 📁 Structure du projet

```
TP2_Segmentation/
│
├── main.py              # Script principal — détection + segmentation + boucle interactive
├── tools.py             # Module utilitaire — PlotWorker, welcome()
├── requirements.txt     # Dépendances Python
├── README.md            # Ce fichier
│
└── img_test/            # Dossier d'images de test (à créer)
    ├── lena.png
    ├── trafic_voiture.jpg
    └── ...
```

---

## ⚙️ Prérequis

- **Python** `>= 3.9`
- **pip** (gestionnaire de paquets Python)
- Un système avec interface graphique (requis pour `tkinter` — la fenêtre de sélection de fichier)

---

## 🚀 Installation

### 1. Cloner ou télécharger le projet

```bash
git clone https://github.com/votre-utilisateur/tp2-segmentation.git
cd tp2-segmentation
```

Ou décompresser l'archive ZIP si fournie.

### 2. Créer un environnement virtuel (recommandé)

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (cmd)**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 📦 Dépendances (`requirements.txt`)

```
numpy>=1.24.0
opencv-python>=4.8.0
matplotlib>=3.7.0
```

| Package | Version min | Rôle dans le projet |
|---|---|---|
| `numpy` | 1.24.0 | Calculs vectoriels, histogramme, masques booléens |
| `opencv-python` | 4.8.0 | Lecture d'image, conversion BGR → niveaux de gris |
| `matplotlib` | 3.7.0 | Affichage des images, histogrammes et seuils superposés |

> `tkinter` est inclus nativement dans Python — aucune installation supplémentaire n'est nécessaire.
> Si toutefois il est absent sur votre système Linux, installez-le via :
> ```bash
> sudo apt install python3-tk
> ```

---

## ▶️ Lancement

```bash
python main.py
```

Le script démarre en boucle interactive :

1. Une fenêtre de sélection s'ouvre — choisissez une image `.png` ou `.jpg`
2. L'image est convertie en niveaux de gris si elle est en couleur
3. Les seuils sont détectés automatiquement
4. Les résultats s'affichent dans une figure à trois panneaux :

| Panneau | Contenu |
|---|---|
| Image originale | Niveaux de gris avant traitement |
| Histogramme + seuils | Distribution des intensités avec les seuils en rouge |
| Image segmentée | Régions étiquetées (colormap `viridis`) |

5. À la fermeture de la figure, le script propose de traiter une autre image ou de quitter.

---

## 🔧 Paramètres ajustables

Dans `main.py`, deux critères de filtrage peuvent être modifiés selon les images traitées :

```python
# Seuil d'amplitude — pics inférieurs à X% du maximum supprimés (défaut : 0.5%)
seuil_hist = 0.005 * maxhist

# Distance minimale entre deux pics pour les considérer distincts (défaut : 15 niveaux)
if (P2[j] - p) < 15:

# Critère de profondeur de vallée (défaut : 0.75)
if Havg / Hmean > 0.75:
```

> **Conseil :** pour des images très contrastées, abaisser le seuil d'amplitude à `0.002`. Pour des images uniformes, augmenter le critère de profondeur à `0.85`.

---

## 🐛 Problèmes fréquents

**`ModuleNotFoundError: No module named 'cv2'`**
```bash
pip install opencv-python
```

**`ModuleNotFoundError: No module named 'tkinter'`**
```bash
# Linux (Debian/Ubuntu)
sudo apt install python3-tk

# macOS (si Python installé via Homebrew)
brew install python-tk
```

**La fenêtre de sélection ne s'ouvre pas**
Vérifier que le script est lancé depuis un terminal avec accès à l'interface graphique (ne pas utiliser SSH sans redirection X11).

**L'image segmentée est entièrement noire ou uniforme**
L'histogramme de l'image est probablement trop uniforme pour que des vallées soient détectées. Essayer avec une image plus contrastée ou abaisser le seuil `seuil_hist`.
