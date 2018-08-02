# MSC_pli

Un pli composite est constitué de l'assemblage d'un renfort et d'une matrice.
Les propriétés mécaniques du pli peuvent être calculées par des méthodes d'homogénéisations,
à partir des propriétés des constituants de départ.
L’homogénéisation consiste au passage d’une structure hétérogène (multi-matériaux) 
à une structure homogène (création d’un matériau équivalent).

Ce script python ce propose de faire se travail.


## Pour commencer

Récupérer les fichiers :
- main_mecanique_pli.py
- homogeneisation_mecanique_pli.py
- renfort_matrice.xlsx


```
Pré-requis :
- Posséder un tableur type Excel
- Posséder les packages : numpy, pandas, matplotlib, time
```


## Fonctionnement

* Renseigner dans "renfort_matrice.xlsx" les propriétés du renfort et de la matrice.
* [option] Indiquer le nombre de chaine et de trame dans le cas d'un tissu. Sinon laisser à 1.
* Excécuter "main_mecanique_pli.py"

```
Excécution par l'invite de commande dans le dossier de travail :
python main_mecanique_pli.py
```



### Résultats

Après excécution du fichier "main_mecanique_pli.py", un fichier texte est généré dans le dossier de travail.
Ce fichier contient les valeurs homogénéisées du pli dans le cas d'un UD, d'un mat et d'un tissu.
Une figure est également générée et présente l'évolution des propriétés du pli en fonction de son orientation.

