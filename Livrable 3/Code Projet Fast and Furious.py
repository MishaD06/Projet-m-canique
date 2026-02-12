# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:46:32 2024

@author: Misha
"""

# Importation des bibliothèques nécessaires au calcul
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Données des voitures
dodge = [1760, 5.1, 5.28, 1.95, 1.35, 0.38, 0.3, 0.1]
supra = [1615, 5, 4.51, 1.81, 1.27, 0.29, 0.3, 0.1]
camaro = [1498, 5.3, 4.72, 1.88, 1.30, 0.35, 0.3, 0.1]
rx_7 = [1385, 5.2, 4.3, 1.75, 1.23, 0.28, 0.3, 0.1]
skyline = [1540, 5.8, 4.6, 1.79, 1.36, 0.34, 0.3, 0.1]
lancer = [1600, 5, 4.51, 1.81, 1.48, 0.28, 0.3, 0.1]

# Association des noms de voitures avec leurs données
voitures = {
    "dodge": dodge,
    "supra": supra,
    "camaro": camaro,
    "rx_7": rx_7,
    "skyline": skyline,
    "lancer": lancer,
}

# Liste des noms disponibles
liste_voiture = list(voitures.keys())

voitures_selectionnees = []
while True:
    choix = input(f"Quelles voitures choisissez-vous ? (séparées par des virgules parmi {', '.join(liste_voiture)}) ").strip().lower()
    choix_liste = [v.strip() for v in choix.split(",")]
    if all(v in voitures for v in choix_liste):
        voitures_selectionnees = {v: voitures[v] for v in choix_liste}
        print(f"Vous avez choisi : {', '.join(v.capitalize() for v in choix_liste)}")
        break
    else:
        print("Une ou plusieurs voitures sont invalides. Veuillez choisir parmi la liste suivante :")
        print(", ".join(liste_voiture))

# Déclaration des conditions initiales
xoA = 0
vx0A = 0
S_initA = [xoA, vx0A]
pas = 1000
t0 = 0
tfinal = 3.7
t = np.linspace(t0, tfinal, pas)

# Demande d'utilisation du nitro à l'utilisateur
nosA = 1
nosB = 1
nosC = 1
nosD = 1

nos = input("Sur quelle portion activer le boost (A, B, C, D ou N pour aucun) ? ").strip().lower()
if nos == 'a':
    nosA = 1.3
elif nos == 'b':
    nosB = 1.3
elif nos == 'c':
    nosC = 1.3
elif nos == 'd':
    nosD = 1.3
elif nos == 'n':
    nosA = 1
    nosB = 1
    nosC = 1
    nosD = 1
else:
    print("Choix invalide. Le boost ne sera pas activé.")
    nosA = 1
    nosB = 1
    nosC = 1
    nosD = 1

psup = 0
kz = 1
kx = 1
Sz = 0

ailes = input("Voulez-vous monter les ailes sur le bolide ? (oui/non) ").strip().lower()
if ailes == "oui":
    kz = 1.1
    Sz = 0.8
    psup += 30
elif ailes == "non" or ailes == "":
    print("Pas d'ailes ajoutées.")
else:
    print("Choix invalide. Pas d'ailes ajoutées.")

jupe = input("Voulez-vous monter la jupe sur le bolide ? (oui/non) ").strip().lower()
if jupe == "oui":
    psup += 15
    kx = 0.95
elif jupe == "non" or jupe == "":
    print("Pas de jupe ajoutée.")
else:
    print("Choix invalide. Pas de jupe ajoutée.")

# Déclaration des constantes
Alpha = np.arcsin(2 / 31)
vx0 = 0
vy0 = 0
g = 9.81
mv = 1.225
air = 1.225
finA = 31

# Déclaration de l'équation différentielle générale
def equation_a(s, t, m, am, l, h, cx, mu):
    sp_a = [s[1], g * np.sin(Alpha) - mu * g * np.cos(Alpha) + (1 / (2 * m)) * air * (h * l) * (s[1] ** 2) * cx + am]
    return sp_a

# Résolution pour chaque voiture sélectionnée
resultats = {}
for nom, donnees in voitures_selectionnees.items():
    m, am, L, l, h, cx, cz, mu = donnees

    # Résolution avec odeint
    solution = odeint(equation_a, S_initA, t, args=(m + psup, am * nosA, l, h, cx * kx, mu))
    resultats[nom] = solution

    # Affichage des résultats
    for i in range(0, pas):
        if resultats[nom][i][0] >= finA:
            voitures[nom].append(t[i])  # position 8 = temps de fin
            voitures[nom].append(resultats[nom][i][0])  # position 9 = position de fin
            voitures[nom].append(resultats[nom][i][1])  # position 10 = vitesse de fin
            break

    print(f"\nRésultats pour {nom.capitalize()} :")
    print(f"Temps final : {voitures[nom][8]} s")
    print(f"Position finale : x = {voitures[nom][9]} m")
    print(f"Vitesse finale : vx = {voitures[nom][10]} m/s")

# Création des sous-graphiques
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Affichage des résultats sous forme graphique pour l'étape 1
for nom, solution in resultats.items():
    positions = solution[:, 0]
    temps = t[:len(positions)]
    axs[0, 0].plot(positions, temps, label=f"{nom.capitalize()} (t vs x)")
axs[0, 0].set_ylabel("Temps (s)")
axs[0, 0].set_xlabel("Position (m)")
axs[0, 0].legend()
axs[0, 0].set_title("Étape 1: Position des voitures au cours du temps")
axs[0, 0].grid()

# Étape 2
print("")
print("-------------Etape-2--------------")
print("")

r = 6
finB = (2 * np.pi)

# Déclaration de l'équation différentielle générale
def equation_b(s, t, m, am, sx, cx, mu):
    sp_b = [s[1], (s[1] ** 2) * (-mu - ((cx * sx * air * r) / (2 * m))) - ((np.sin(s[0]) + np.cos(s[0])) * (g * (1 + mu))) / r + (am) / r]
    return sp_b

# Résolution pour chaque voiture sélectionnée
resultats = {}
for nom, donnees in voitures_selectionnees.items():
    m, am, L, l, h, cx, cz, mu, tempsFinal, x0B, v0B = donnees
    S_initB = (0, v0B / r)
    solution = odeint(equation_b, S_initB, t, args=(m + psup, am * nosB, l * h, cx * kx, mu))
    resultats[nom] = solution

    for i in range(0, pas):
        if resultats[nom][i][0] >= finB:
            voitures[nom][8] += t[i]
            voitures[nom][9] = resultats[nom][i][0] * r
            voitures[nom][10] = resultats[nom][i][1] * r
            break

    print(f"\nRésultats pour {nom.capitalize()} :")
    print(f"Temps final : {voitures[nom][8]} s")
    print(f"Position finale : x = {voitures[nom][9]} m")
    print(f"Vitesse finale : vx = {voitures[nom][10]} m/s")

# Affichage des résultats sous forme graphique pour l'étape 2
for nom, solution in resultats.items():
    positions = solution[:, 0]
    temps = t[:len(positions)]
    axs[0, 1].plot(positions, temps, label=f"{nom.capitalize()} (t vs x)")
axs[0, 1].set_ylabel("Temps (s)")
axs[0, 1].set_xlabel("Position (m)")
axs[0, 1].legend()
axs[0, 1].set_title("Étape 2: Position des voitures au cours du temps")
axs[0, 1].grid()

# Étape 3
print("")
print("-------------Etape-3--------------")
print("")

finC = 0

# Déclaration de l'équation différentielle générale
def equation_c(s, t, m, am, sx, cx, sz, cz, mu):
    sp_c = [s[2], s[3], (-air * sx * cx * (np.sqrt(s[2] ** 2 + s[3] ** 2) * s[2]) - air * sz * cz * (np.sqrt(s[2] ** 2 + s[3] ** 2) * s[3])) / (2 * m), -g + ((air * (-sx) * cx * (np.sqrt(s[2] ** 2 + s[3] ** 2) * s[3]) + air * sz * cz * (np.sqrt(s[2] ** 2 + s[3] ** 2) * s[2])) / (2 * m))]
    return sp_c

# Résolution pour chaque voiture sélectionnée
resultats = {}
for nom, donnees in voitures_selectionnees.items():
    m, am, L, l, h, cx, cz, mu, tempsFinal, x0C, v0C = donnees
    S_initC = (-9, 1, v0C, 0)
    solution = odeint(equation_c, S_initC, t, args=(m + psup, am * nosC, l * h, cx * kx, (l * L) + Sz, cz * kz, mu))
    resultats[nom] = solution

    for i in range(0, pas):
        if resultats[nom][i][1] <= finC:
            voitures[nom][8] += t[i]
            voitures[nom][9] = resultats[nom][i][0]
            voitures[nom][10] = resultats[nom][i][2]
            break

    print(f"\nRésultats pour {nom.capitalize()} :")
    print(f"Temps final : {voitures[nom][8]} s")
    print(f"Position finale : x = {voitures[nom][9]} m")
    print(f"Vitesse finale : vx = {voitures[nom][10]} m/s")

# Affichage des résultats sous forme graphique pour l'étape 3
for nom, solution in resultats.items():
    positions = solution[:, 0]
    temps = t[:len(positions)]
    axs[1, 0].plot(positions, temps, label=f"{nom.capitalize()} (t vs x)")
axs[1, 0].set_ylabel("Temps (s)")
axs[1, 0].set_xlabel("Position (m)")
axs[1, 0].legend()
axs[1, 0].set_title("Étape 3: Position des voitures au cours du temps")
axs[1, 0].grid()

# Étape 4
print("")
print("-------------Etape-4--------------")
print("")

finD = 10

# Déclaration de l'équation différentielle générale
def equation_d(s, t, m, am, sx, cx, mu):
    sp_d = [s[1], am + (1 / (2 * m)) * air * sx * (s[1] ** 2) * cx - mu * g]
    return sp_d

# Résolution pour chaque voiture sélectionnée
resultats = {}
for nom, donnees in voitures_selectionnees.items():
    m, am, L, l, h, cx, cz, mu, tempsFinal, x0D, v0D = donnees
    S_initD = (x0D, v0D)
    solution = odeint(equation_d, S_initD, t, args=(m + psup, am * nosD, l * h, cx * kx, mu))
    resultats[nom] = solution

    for i in range(0, pas):
        if resultats[nom][i][0] >= finD:
            voitures[nom][8] += t[i]
            voitures[nom][9] = resultats[nom][i][0]
            voitures[nom][10] = resultats[nom][i][1]
            break

    print(f"\nRésultats pour {nom.capitalize()} :")
    print(f"Temps final : {voitures[nom][8]} s")
    print(f"Position finale : x = {voitures[nom][9]} m")
    print(f"Vitesse finale : vx = {voitures[nom][10]} m/s")

# Affichage des résultats sous forme graphique pour l'étape 4
for nom, solution in resultats.items():
    positions = solution[:, 0]
    temps = t[:len(positions)]
    axs[1, 1].plot(positions, temps, label=f"{nom.capitalize()} (t vs x)")
axs[1, 1].set_ylabel("Temps (s)")
axs[1, 1].set_xlabel("Position (m)")
axs[1, 1].legend()
axs[1, 1].set_title("Étape 4: Position des voitures au cours du temps")
axs[1, 1].grid()

# Affichage de tous les graphiques dans une seule fenêtre
plt.tight_layout()
plt.show()
