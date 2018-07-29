# -*- coding: utf-8 -*-
"""
Cree par    : Jean COLLOMB
Societe     : CT1 - groupe Compose
Laboratoire : SYMME - Polytech Annecy-Chambéry - Université Savoie Mont Blanc
Date        : janvier 2017

Ce programme a pour objectif d'estimer les proprietes mecaniques
d'un pli composite a l'aide des proprietes de la matrice et du renfort.

Le fonctionnement est le suivant :
    Etape 1 : Recuperation des informations stockees dans le document Excel
    Etape 2 : Calculs des proprietes homogeneisees
    Etape 3 : Stockage des resultats dans un fichier texte
    Etape 4 : Stockage des courbes dans un fichier pdf
"""

#------------------------ Importation des Modules
import time
import pandas as pd
from homogeneisation_mecanique_pli import Homogeneisation_Mecanique_Pli



#------------------------ Extraction des informations

temps_depart_extraction = time.time()
informations = pd.read_excel('renfort_matrice.xlsx')


"""
Stockage de chaque propriete dans des listes.
"""
liste_El = informations['El'].tolist()
liste_Et = informations['Et'].tolist()
liste_Glt = informations['Glt'].tolist()
liste_Nult = informations['Nult'].tolist()
liste_Rho = informations['Rho'].tolist()
liste_Msf = informations['Msf'].tolist()
Vf = informations['Vf'][0]
liste_n = informations['Tissu'].tolist()
temps_fin_extraction = time.time()


#------------------------ Realisation des calculs

"""
Realisation du calcul a l'aide de la Class Homogeneisation_Mecanique_Pli
presente dans le fichier homogeneisation_mecanique_pli.py
Calculs des proprietes homogeneisees du pli.
"""
temps_depart_calculs = time.time()
#--- Creation de l'objet Calcul
Calcul = Homogeneisation_Mecanique_Pli(liste_El, liste_Et, liste_Glt, liste_Nult, liste_Rho, liste_Msf, Vf, liste_n)

#--- Calculs des resultats pour un UD
El_UD = Calcul.LM_auto_coherent()[0]
Et_UD = Calcul.LM_auto_coherent()[1]
Glt_UD = Calcul.LM_auto_coherent()[2] 
Gtt_UD = Calcul.LM_auto_coherent()[3]
Nult_UD = Calcul.LM_auto_coherent()[4] 
Nutl_UD = Calcul.LM_auto_coherent()[5]
Nutt_UD = Calcul.LM_auto_coherent()[6]

#--- Calculs des resultats pour un mat
E_mat = Calcul.LM_mat()[0]
G_mat = Calcul.LM_mat()[1]
Nu_mat = Calcul.LM_mat()[2]

#--- Calculs des resultats pour un tissu
El_tissu = Calcul.LM_tissu()[0]
Et_tissu = Calcul.LM_tissu()[1]
Glt_tissu = Calcul.LM_tissu()[2]
Nult_tissu = Calcul.LM_tissu()[3]

#--- Creation des tableaux de resultats
resultats_UD = {'El': round(El_UD,1), 'Et': round(Et_UD,1), 'Glt':round(Glt_UD,1) , 'Gtt':round(Gtt_UD,1) , 'Nult':round(Nult_UD,3) , 'Nutl':round(Nutl_UD,3) , 'Nutt':round(Nutt_UD,3)}
resultats_UD_df = pd.DataFrame(data=resultats_UD, index=['Resultats UD'])

resultats_mat = {'E': round(E_mat,1), 'G': round(G_mat,1), 'Nu':round(Nu_mat,3)}
resultats_mat_df = pd.DataFrame(data=resultats_mat, index=['Resultats Mat'])

resultats_tissu = {'El': round(El_tissu,1),'Et':round(Et_tissu,1) , 'Glt':round(Glt_tissu,1) , 'Nult':round(Nult_tissu,3)}
resultats_tissu_df = pd.DataFrame(data=resultats_tissu, index=['Resultats Tissu'])

temps_fin_calculs = time.time()


#------------------------ Exportation des resultats

#--- Graphiques PDF
temps_depart_graphique = time.time()
Calcul.graphiques_proprietes_UD()
temps_fin_graphique = time.time()

#--- Fichier texte
temps_depart_ecriture = time.time()
resultats_txt = open("resultats.txt", "w")

resultats_txt.write("----------------------")
resultats_txt.write("\n")
resultats_txt.write("-------------RESULTATS")
resultats_txt.write("\n")
resultats_txt.write("----------------------")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("Ci-après, les resultats obtenus pour l'homogénéisation des propriétés mécaniques du pli")
resultats_txt.write("\n")
resultats_txt.write("Les calculs MSC permettent d'estimer les proprietes mecaniques finales du pli composite \n")
resultats_txt.write("en se basant sur les proprietes mecaniques de chaque composant. \n")

resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("-----Donnees d'entrees\n")
resultats_txt.write("----------------------\n")
resultats_txt.write("\n")
resultats_txt.write("Le taux volumique de fibres est de : " + str(round(Calcul.Vf * 100)) + " %")
resultats_txt.write("\n")
resultats_txt.write("\n")
informations.set_index('Composant', inplace = True)
resultats_txt.write(str(informations[['El', 'Et', 'Glt', 'Nult', 'Rho', 'Msf']]))

resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("-----Donnees de sorties")
resultats_txt.write("\n")
resultats_txt.write("-----------------------")
resultats_txt.write("\n")
resultats_txt.write("L'epaisseur du pli est de : " + str(round(Calcul.epaisseur_pli(),3)) + " mm")
resultats_txt.write("\n")
resultats_txt.write("Le pli est constitué de : " + str(round(Calcul.masses()[0],3)) + " grammes de fibres")
resultats_txt.write("\n")
resultats_txt.write("Le pli est constitué de : " + str(round(Calcul.masses()[1],1)) + " grammes de résine")
resultats_txt.write("\n")
resultats_txt.write("La masse volumique du pli est de : " + str(round(Calcul.masse_volumique(),1)) + " kg/m3")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("--> Homogeneisation UD \n")
resultats_txt.write(str(resultats_UD_df))
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("--> Homogeneisation mat \n")
resultats_txt.write(str(resultats_mat_df))
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("--> Homogeneisation tissu \n")
informations.set_index('Equilibrage', inplace = True)
informations.rename_axis(None)
resultats_txt.write(str(informations[['Tissu']]))
resultats_txt.write("\n")
resultats_txt.write(str(resultats_tissu_df))

resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("\n")
resultats_txt.write("-----Information")
resultats_txt.write("\n")
resultats_txt.write("-----------------------")
resultats_txt.write("\n")
temps_fin_ecriture = time.time()
resultats_txt.write("\n")
resultats_txt.write("temps d'extraction des donnees : " + str(round(temps_fin_extraction - temps_depart_extraction, 3)) + " secondes")
resultats_txt.write("\n")
resultats_txt.write("temps de calculs               : " + str(round(temps_fin_calculs - temps_depart_calculs, 3)) + " secondes")
resultats_txt.write("\n")
resultats_txt.write("temps tracer graphiques        : " + str(round(temps_fin_graphique - temps_depart_graphique, 3)) + " secondes")
resultats_txt.write("\n")
resultats_txt.write("temps d'ecriture               : " + str(round(temps_fin_ecriture - temps_depart_ecriture, 3)) + " secondes")
resultats_txt.write("\n")
resultats_txt.write("temps total                    : " + str(round(temps_fin_ecriture - temps_depart_extraction, 3)) + " secondes")

resultats_txt.close()







