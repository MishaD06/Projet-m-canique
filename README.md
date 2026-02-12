# Projet Mécanique - Fast & Furious Circuit Simulation

Simulation numérique et analyse physique d'un circuit automobile. Ce projet utilise Python pour modéliser et résoudre les équations du mouvement d'une voiture sur un circuit complexe.

## 📋 Description du Projet

Dans le contexte du film Fast & Furious, Dom Toretto doit remporter une course sur un circuit extrême comprenant :
- Une **piste d'élan** : hauteur 2m, longueur 31m
- Un **looping** : rayon 6m
- Un **saut au-dessus d'un ravin** : largeur 9m, dénivelé -1m
- Une **piste horizontale** : 10m jusqu'à l'arrivée

**Objectif** : Temps cible < 8 secondes

L'équipe doit analyser différents modèles de voitures pour sélectionner celle qui réussira le circuit sans dommages.

## 🎯 Concepts Physiques Étudiés

- **Cinématique** : vecteurs position, vitesse, accélération
- **Dynamique** : Lois de Newton, forces appliquées (gravité, frottements sol/air, portance)
- **Énergétique** : énergie cinétique, potentielle, mécanique, travail des forces
- **Mathématiques** : calcul intégral, trigonométrie, résolution d'équations différentielles

## 📁 Structure du Projet

```
Projet-mécanique/
├── Livrable 1/           # Repères et référentiels
│   ├── schemas/          # Schémas des forces et repères
│   └── rapport_L1.pdf    # Justification des choix de repères
│
├── Livrable 2/           # Modèles mathématiques
│   ├── equations/        # Équations du mouvement pour chaque portion
│   └── rapport_L2.pdf    # Modélisation complète avec hypothèses
│
├── Livrable 3/           # Simulation numérique Python
│   ├── simulation.py     # Code principal de simulation
│   ├── voitures.py       # Classe et paramètres des voitures
│   ├── circuits.py       # Modélisation de chaque portion du circuit
│   ├── analyse.py        # Analyse des résultats et comparaisons
│   ├── visualisation.py  # Graphiques et tracés
│   ├── requirements.txt  # Dépendances Python
│   └── rapport_L3.pdf    # Rapport final avec résultats
│
└── Ressources/
    ├── caracteristiques_voitures.xlsx
    ├── mesures_circuit.xlsx
    └── references/        # Documentation technique
```

## 🐍 Utilisation de Python dans le Projet

### Pourquoi Python ?

Python est utilisé pour **résoudre numériquement les équations différentielles du mouvement** qui sont trop complexes pour être résolues analytiquement. Le projet nécessite :

1. **Résolution d'équations différentielles** : équations du mouvement de Newton
2. **Calculs vectoriels** : position, vitesse, accélération en coordonnées multiples
3. **Intégration numérique** : calcul de trajectoires et énergies
4. **Visualisation** : graphiques de vitesse, trajectoire, énergies
5. **Analyse comparative** : tests de plusieurs modèles de voitures

### Bibliothèques Python Utilisées

```python
# Calcul numérique et algèbre linéaire
numpy          # Manipulation de vecteurs et matrices, calculs mathématiques

# Résolution d'équations différentielles
scipy          # solve_ivp pour résoudre les équations du mouvement

# Visualisation graphique
matplotlib     # Tracés de vitesse, trajectoire, énergies au cours du temps

# Traitement de données
pandas         # Importation et analyse des mesures sur circuit (Excel)

# Calculs d'incertitudes (optionnel)
uncertainties  # Propagation des incertitudes de mesure
```

### Architecture du Code

#### 1. **Classe Voiture** (`voitures.py`)
```python
class Voiture:
    def __init__(self, nom, masse, cx, surface, puissance):
        """
        Paramètres physiques de la voiture
        - masse : kg
        - cx : coefficient de traînée aérodynamique
        - surface : surface frontale (m²)
        - puissance : chevaux
        """
```

#### 2. **Simulation de la Pente** (`circuits.py`)
```python
def simuler_pente(voiture, hauteur=2, longueur=31):
    """
    Résout les équations du mouvement sur la pente avec :
    - Force de gravité
    - Force de frottement du sol (coefficient μ)
    - Force de traînée aérodynamique (proportionnelle à v²)
    
    Retourne : vitesse finale en bas de pente
    """
```

**Équation résolue numériquement** :
```
m * dv/dt = m*g*sin(θ) - μ*m*g*cos(θ) - 0.5*ρ*Cx*S*v²
```

#### 3. **Simulation du Looping** (`circuits.py`)
```python
def simuler_looping(voiture, rayon=6, vitesse_entree):
    """
    Résout le mouvement circulaire avec :
    - Force centripète nécessaire (m*v²/r)
    - Condition de non-décollement : N ≥ 0
    
    Calcule :
    - Vitesse minimale d'entrée
    - Vitesse de sortie
    - Trajectoire complète
    """
```

**Condition critique** :
```python
v_min = sqrt(g * rayon)  # Vitesse minimale au sommet du looping
```

#### 4. **Simulation du Saut** (`circuits.py`)
```python
def simuler_saut(voiture, largeur=9, denivele=-1, vitesse_entree):
    """
    Résout le mouvement parabolique (projectile) avec :
    - Gravité
    - Traînée aérodynamique
    
    Vérifie : la voiture franchit-elle les 9m ?
    """
```

**Équations résolues** :
```python
# Équations différentielles du projectile
dx/dt = vx
dy/dt = vy
dvx/dt = -0.5*ρ*Cx*S*vx*v/m
dvy/dt = -g - 0.5*ρ*Cx*S*vy*v/m
```

#### 5. **Intégration Numérique** (exemple avec `scipy`)
```python
from scipy.integrate import solve_ivp

def equations_mouvement(t, y, voiture, forces):
    """
    y = [x, y, vx, vy] : état du système
    Retourne : [vx, vy, ax, ay]
    """
    x, y_pos, vx, vy = y
    
    # Calcul des forces
    F_gravite = voiture.masse * 9.81
    F_frottement = calcul_frottement(vx, vy, voiture)
    F_trainee = calcul_trainee(vx, vy, voiture)
    
    # Accélérations (2ème loi de Newton)
    ax = (F_x_totale) / voiture.masse
    ay = (F_y_totale) / voiture.masse
    
    return [vx, vy, ax, ay]

# Résolution
solution = solve_ivp(
    equations_mouvement, 
    t_span=(0, t_final), 
    y0=[x0, y0, vx0, vy0],
    args=(voiture, forces)
)
```

#### 6. **Visualisation** (`visualisation.py`)
```python
import matplotlib.pyplot as plt

def tracer_vitesse(temps, vitesses):
    """Graphique de vitesse en fonction du temps"""
    plt.plot(temps, vitesses)
    plt.xlabel('Temps (s)')
    plt.ylabel('Vitesse (m/s)')
    plt.title('Évolution de la vitesse sur le circuit')
    plt.grid(True)
    plt.show()

def tracer_trajectoire(x, y):
    """Tracé de la trajectoire de la voiture"""
    plt.plot(x, y)
    plt.xlabel('Distance (m)')
    plt.ylabel('Hauteur (m)')
    plt.title('Trajectoire dans le ravin')
    plt.axhline(y=-1, color='r', linestyle='--', label='Sol')
    plt.legend()
    plt.show()
```

#### 7. **Analyse Comparative** (`analyse.py`)
```python
import pandas as pd

def comparer_voitures(voitures):
    """
    Compare les performances de différents modèles
    Retourne : DataFrame avec temps, vitesses, succès/échec
    """
    resultats = []
    
    for voiture in voitures:
        temps_total = simuler_circuit_complet(voiture)
        resultats.append({
            'Voiture': voiture.nom,
            'Temps total (s)': temps_total,
            'Passe looping': verifier_looping(voiture),
            'Passe ravin': verifier_ravin(voiture)
        })
    
    return pd.DataFrame(resultats)

def comparer_mesures_theorique(mesures_excel, resultats_simulation):
    """
    Importe les mesures réelles et compare avec la théorie
    Calcule les écarts et incertitudes
    """
    mesures = pd.read_excel('mesures_circuit.xlsx')
    
    for index, row in mesures.iterrows():
        ecart = abs(row['vitesse_mesuree'] - resultats_simulation[index])
        incertitude = 5  # km/h
        print(f"Écart : {ecart:.2f} km/h (incertitude : ±{incertitude} km/h)")
```

## 🚀 Installation et Utilisation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/MishaD06/Projet-m-canique.git
cd Projet-m-canique/Livrable\ 3

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Fichier `requirements.txt`
```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
pandas>=1.3.0
openpyxl>=3.0.0
uncertainties>=3.1.0
```

### Exécution

```bash
# Simulation complète du circuit
python simulation.py

# Comparaison de tous les modèles de voitures
python analyse.py --mode comparaison

# Simulation d'une voiture spécifique
python simulation.py --voiture dodge --modifications turbo

# Génération des graphiques uniquement
python visualisation.py --resultats resultats.json
```

### Exemple d'Utilisation du Code

```python
from voitures import Voiture
from circuits import simuler_circuit_complet
from visualisation import tracer_resultats

# Définir la voiture de Dom (Dodge)
dodge = Voiture(
    nom="Dodge Charger",
    masse=1800,  # kg
    cx=0.35,
    surface=2.5,  # m²
    puissance=500  # ch
)

# Simuler le circuit complet
resultats = simuler_circuit_complet(dodge)

# Afficher les résultats
print(f"Temps total : {resultats['temps_total']:.2f} s")
print(f"Passe le looping : {'Oui' if resultats['looping_ok'] else 'Non'}")
print(f"Passe le ravin : {'Oui' if resultats['ravin_ok'] else 'Non'}")

# Générer les graphiques
tracer_resultats(resultats)
```

## 📊 Résultats Attendus

Le code Python doit produire pour chaque voiture :

### 1. Pente
- Vitesse de sortie en m/s et km/h
- Graphique vitesse vs temps

### 2. Looping
- Vitesse minimale d'entrée (théorique)
- Vitesse réelle de sortie
- Tracé de la vitesse angulaire
- **Validation** : comparaison vitesse sortie pente vs vitesse minimale requise

### 3. Saut du Ravin
- Trajectoire parabolique (graphique x-y)
- Distance horizontale atteinte
- Vitesse minimale requise
- **Validation** : comparaison vitesse sortie looping vs vitesse minimale requise

### 4. Temps Total
- Temps pour chaque portion
- Temps total du circuit
- Comparaison avec l'objectif (< 8s)

### 5. Comparaison Théorie/Mesures
```python
# Exemple de sortie
Voiture: Dodge Charger
-----------------------------------
Vitesse sortie pente (théorie): 18.5 m/s
Vitesse sortie pente (mesure):  19.2 m/s ± 1.4 m/s
Écart: 0.7 m/s (dans l'incertitude ✓)
```

## 🎓 Compétences Développées

### Physique
- Mécanique newtonienne
- Dynamique du point matériel
- Énergétique
- Analyse de forces

### Mathématiques
- Équations différentielles
- Intégration numérique
- Trigonométrie
- Algèbre vectorielle

### Programmation Python
- POO (Programmation Orientée Objet)
- Résolution numérique avec `scipy`
- Visualisation avec `matplotlib`
- Traitement de données avec `pandas`
- Gestion d'incertitudes
- Paramétrage et modularité du code

## 📈 Soutenance Finale

Présentation de 15 minutes à Dom Toretto incluant :
1. Contexte et hypothèses
2. Modèles physiques
3. Résultats de simulation
4. Comparaison mesures/théorie (avec incertitudes ±5 km/h)
5. **Recommandation de voiture + modifications**
6. Temps estimé
7. Critique des résultats
