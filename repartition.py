#!/usr/bin/env python3

import csv
import collections
from pathlib import Path
import random


class Dossier():
    def __init__(self, code, site):
        self.code = code
        self.site = site

class Medecin():
    def __init__(self, code, site, max_dossiers):
        self.code = code
        self.site = site
        self.max_dossiers = int(max_dossiers)
        self.dossiers = []

    # Retourne a prefered site associated with this medecin or None
    def get_associated_with_site(self):
        dossier_sites = [d.site for d in self.dossiers]
        if len(set(dossier_sites)) == 1:
            return dossier_sites[0]


def load_file(file_name):
    my_file = Path(file_name)
    data = csv.reader(my_file.open())
    # J'ignore la première ligne car elle contient le nom des colonnes.
    next(data)
    return data


dossiers = []
for row in load_file("code_dossier.csv"):
    dossiers.append(Dossier(row[0], row[1]))

medecins = []
for row in load_file("mds.csv"):
    # Si la ligne n'a pas de code médecin, on l'ignore
    if not row[0]:
        continue
    medecins.append(Medecin(row[1], row[0], row[2]))



print(f"{len(medecins)} médecins chargés")
print(f"{len(dossiers)} dossiers chargés")

# On mélange les médecins
random.shuffle(medecins)

for d in dossiers:
    for m in medecins:
        if len(m.dossiers) >= m.max_dossiers:
            # On ne peut plus donner de travail à ce medecin
            continue
        if m.site == d.site:
            # Les sites sont les même. On ignore aussi
            continue

        medecin_potentiel = m
        # Ce médecin est bon, mais on continu la recherche pour regrouper
        if d.site == m.get_associated_with_site():
            # La le site du dossier correspond avec des dossiers
            # existants du médecin
            break

    if not medecin_potentiel:
        print(f"Nous n'avons pas de médecin pour le dossier {d.code}")
        exit(1)

    # On ajoute le dossier sélectionné au médecin.
    medecin_potentiel.dossiers.append(d)



print("Résultats")
for m in medecins:
    print(f"médecin {m.code} du site {m.site}")
    for d in m.dossiers:
        print(f"  - {d.code} du site {d.site}")

print()
print("Bilan par CHSLD")
chslds = collections.defaultdict(int)
for m in medecins:
    for d in m.dossiers:
        chslds[d.site] += 1

for chsld in sorted(chslds):
    print(f"  {chsld}: {chslds[chsld]} dossier(s)")
