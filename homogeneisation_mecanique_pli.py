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
import numpy as np
import matplotlib.pyplot as plt


#------------- Creation de la Class Homogeneisation_Mecanique
class Homogeneisation_Mecanique_Pli():
    """
    Cette Class a pour objectif de permettre l'estimation des proprietes homogeneisees
    d'un pli composite a l'aide des proprietes de la matrice et du renfort.
    -----
    Donnees d'entrees :
        liste_El [list]
        liste_Et [list]
        liste_Glt [list]
        liste_Nult [list]
        liste_Rho [list]
        liste_Msf [list]
        Vf [float]
        liste_n [list]
    -----
    Les donnees en position [0] correspondent aux proprietes de la matrice.
    Les donnees en position [1] correspondent aux proprietes du renfort.
    -----
    Exemple :
        liste_El = [3450, 72000]
        liste_Et = [0, 72000]
        liste_Glt = [1300, 29508]
        liste_Nult = [0.4, 0.22]
        liste_Rho = [1200, 2550]
        liste_Msf = [0, 300]
        liste_n  = [1, 1]
        Vf = 50
        test_1 = Homogeneisation_Mecanique_Pli(liste_El, liste_Et, liste_Glt, liste_Nult, liste_Rho, liste_Msf, Vf, liste_n)
    """
    
    def __init__ (self, liste_El, liste_Et, liste_Glt, liste_Nult, liste_Rho, liste_Msf, Vf, liste_n) :
        """
        Fonction d'initialisation de la Class
        Donnees d'entrees : proprietes materiaux.
        Les donnees d'entrees sont sous forme de listes.
        La position 0 dans la liste correspond aux proprietes Matrice.
        La position 1 dans la liste correspond aux proprietes Rendort.
        """
        self.liste_El = liste_El
        self.liste_Et = liste_Et
        self.liste_Glt = liste_Glt
        self.liste_Nult = liste_Nult
        self.liste_Rho = liste_Rho
        self.liste_Msf = liste_Msf
        self.Vf = Vf / 100
        self.Vm = 1 - self.Vf
        self.liste_n = liste_n
        self.liste_k = self.k()
        
    def k (self):
        """
        Module d'elasticite isostatique
        """
        k_matrice = self.liste_El[0] / (2 * (1 - 2 * self.liste_Nult[0]) * (1 + self.liste_Nult[0]))
        k_renfort = self.liste_El[1] / (2 * (1 - 2 * self.liste_Nult[1]) * (1 + self.liste_Nult[1]))
        liste_k = [k_matrice, k_renfort]
        return liste_k
    
    def masse_volumique (self):
        """
        Masse volumique du pli composite.
        Calcul base sur la loi des melanges.
        """
        rho_pli = self.liste_Rho[1] * self.Vf + self.liste_Rho[0] * self.Vm
        return rho_pli
    
    def masses (self, surface = 1):
        """
        Calcul de la masse de chaque constituant pour le Vf donne.
        Le calcul des masses peut etre utile pour une aide a la preparation
        a l'atelier.
        -----
        Les resultats sont en grammes.
        -----
        Les resultats sont valables pour un pli de 1m² par defaut.
        """
        masse_fibre = self.liste_Msf[1] * surface
        masse_resine = self.taux_massiques()[2] * masse_fibre
        return masse_fibre, masse_resine
    
    def epaisseur_pli (self):
        """
        Calcul de l'epaisseur du pli composite pour le Vf donne.
        """
        epaisseur = self.liste_Msf[1] / (self.liste_Rho[1] * self.Vf)
        return epaisseur
    
    def taux_massiques (self):
        """
        Calcul des taux massiques de fibres et de resine en fonction du Vf donne.
        """
        Mf = (self.Vf * self.liste_Rho[1]) / (self.Vf * self.liste_Rho[1] + self.Vm * self.liste_Rho[0])
        Mm = 1 - Mf
        coefficient_impregnation = Mm / Mf
        return Mf, Mm, coefficient_impregnation
    
    def LM_auto_coherent (self):
        """
        Cette fonction permet d'estimer les proprietes mecaniques du pli composite
        a partir des proprietes des constituants (matrice et fibre).
        -----
        Les calculs d'homogeneisation sont realises a l'aide du
        Bilan Auto-coherent.
        """
        El_pli = self.Vf * self.liste_El[1] + self.Vm * self.liste_El[0]
        k = ((self.liste_k[1] + self.liste_Glt[0]) * self.liste_k[0] +              \
             (self.liste_k[1] - self.liste_k[0]) * self.liste_Glt[0] * self.Vf) /   \
             (self.liste_k[1] + self.liste_Glt[0] - (self.liste_k[1] - self.liste_k[0]) * self.Vf)
        Gtt_pli = self.liste_Glt[0] * (self.liste_k[0] * (self.liste_Glt[1] + self.liste_Glt[0]) + 2 * self.liste_Glt[1] * self.liste_Glt[0] + self.liste_k[0] * (self.liste_Glt[1] - self.liste_Glt[0]) * self.Vf) / (self.liste_k[0] * (self.liste_Glt[0] + self.liste_Glt[1]) + 2 * self.liste_Glt[0] * self.liste_Glt[1] - (self.liste_k[0] + 2 * self.liste_Glt[0]) * (self.liste_Glt[1] - self.liste_Glt[0]) * self.Vf)
        Nult_pli = self.liste_Nult[1] * self.Vf + self.liste_Nult[0] * self.Vm
        Et_pli = 1 / ((1 / (4 * k)) + (1 / (4 * Gtt_pli)) + (Nult_pli**2 / El_pli))
        Glt_pli = self.liste_Glt[0] * (((1 - self.Vf) * self.liste_Glt[0] + (1 + self.Vf) * self.liste_Glt[1])) / ((1 - self.Vf) * self.liste_Glt[1] + (1 + self.Vf) * self.liste_Glt[0])
        Nutl_pli = Nult_pli * Et_pli / El_pli
        Nutt_pli = (2 * El_pli * k - El_pli * Et_pli - 4 * Nult_pli**2 * k * Et_pli) / (2 * El_pli * k)
        return El_pli, Et_pli, Glt_pli, Gtt_pli, Nult_pli, Nutl_pli, Nutt_pli
    
    def LM_mat (self):
        """
        Estimation des proprietes mecaniques d'un mat.
        Calculs bases sur la loi des melanges.
        """
        E_mat = (3/8) * self.LM_auto_coherent()[0] + (5/8) * self.LM_auto_coherent()[1]
        G_mat = (1/8) * self.LM_auto_coherent()[0] + (1/4) * self.LM_auto_coherent()[1] 
        Nu_mat = E_mat / (2 * G_mat) - 1
        return E_mat, G_mat, Nu_mat
    
    def LM_tissu (self):
        """
        Estimation des proprietes mecaniques d'un tissu.
        Calculs bases sur la loi des melanges.
        """
        k = self.liste_n[0] / (self.liste_n[0] + self.liste_n[1])
        El_tissu = k * self.LM_auto_coherent()[0] + (1 - k) * self.LM_auto_coherent()[1]
        Et_tissu = k * self.LM_auto_coherent()[1] + (1 - k) * self.LM_auto_coherent()[0]
        Glt_tissu = self.LM_auto_coherent()[2]
        Nult_tissu = self.LM_auto_coherent()[4] / (k + (1 - k) * (self.LM_auto_coherent()[0] / self.LM_auto_coherent()[1]))
        return El_tissu, Et_tissu, Glt_tissu, Nult_tissu
    
    def J (self, angle):
        """
        Fonction permettant le calcul de  :
            la matrice de changement de repere
            l'inverse de la matrice de changement de repere
            la transposee de la matrice de changement de repere
            la transposee de l'inverse de la matrice de changement de repere
        ------
        Entree : angle [float]
        """
        angle = np.radians(float(angle))
        J11 = np.cos(angle)**2
        J12 = np.sin(angle)**2
        J13 = 2 * np.cos(angle) * np.sin(angle)
        J21 = np.sin(angle)**2
        J22 = np.cos(angle)**2
        J23 = -2 * np.cos(angle) * np.sin(angle)
        J31 = -1 * np.cos(angle) * np.sin(angle)
        J32 = np.cos(angle) * np.sin(angle)
        J33 = np.cos(angle)**2 - np.sin(angle)**2
        matrice_J = np.array([[J11, J12, J13],[J21, J22, J23],[J31, J32, J33]])
        matrice_J_inv = np.linalg.inv(matrice_J)
        matrice_J_trans = matrice_J.transpose()
        matrice_J_trans_inv = np.linalg.inv(matrice_J_trans)
        return matrice_J, matrice_J_inv, matrice_J_trans, matrice_J_trans_inv
    
    def Q0 (self, El, Et, Glt, Nult):
        """
        Fonction permettant le calcul de la matrice de rigidite du pli
        dans le repere local L, T.
        -------
        Entrees : 
            El [float]
            Et [float]
            Glt [float]
            Nult [float]
        """
        El = float(El)
        Et = float(Et)
        Glt = float(Glt)
        Nult = float(Nult)
        Nutl = float(Nult * Et / El)
        Q11 = El / (1 - Nult * Nutl)
        Q12 = (Nult * Et) / (1 - Nult * Nutl)
        Q13 = 0
        Q21 = (Nutl * El) / (1 - Nult * Nutl)
        Q22 = Et / (1 - Nult * Nutl)
        Q23 = 0
        Q31 = 0
        Q32 = 0
        Q33 = Glt
        matrice_Q0 = np.array([[Q11, Q12, Q13],[Q21, Q22, Q23],[Q31, Q32, Q33]])
        return matrice_Q0
    
    def Qx (self, matrice_J_inv, matrice_J_trans_inv, matrice_Q0):
        """
        Fonction permettant le calcul de la matrice de rigidite du pli
        dans le repere global x, y.
        -------
        Entrees :
            matrice_J_trans [array]
            matrice_J [array]
            matrice_Q0 [array]
        """
        matrice_Qx = np.dot(np.dot(matrice_J_inv, matrice_Q0), matrice_J_trans_inv)
        return matrice_Qx
    
    def graphiques_proprietes_UD(self):
        """
        Fonction permettant de tracer l'evolution des proprietes mecaniques du
        pli en fonction de l'angle.
        """
        liste_Ex_UD = []
        liste_Ey_UD = []
        liste_Gxy_UD = []
        liste_Nuxy_UD = []
        liste_angle = []
        
        El = self.LM_auto_coherent()[0]
        Et = self.LM_auto_coherent()[1]
        Glt = self.LM_auto_coherent()[2]
        Nult = self.LM_auto_coherent()[4]
        Q0 = self.Q0(El, Et, Glt, Nult)
        
        for angle in range(-90, 90, 1):
            matrice_J, matrice_J_inv, matrice_J_trans, matrice_J_trans_inv = self.J(angle)
            Qx = self.Qx(matrice_J_inv, matrice_J_trans_inv, Q0)
            Sx = np.linalg.inv(Qx)
            liste_Ex_UD.append(1/Sx[0][0])
            liste_Ey_UD.append(1/Sx[1][1])
            liste_Gxy_UD.append(1/Sx[2][2])
            liste_Nuxy_UD.append(-1 * Sx[0][1] / Sx[0][0])
            liste_angle.append(angle)
        
        #stockage resultats
        plt.clf()
        plt.figure(figsize=(18,8), dpi=80)
        
        graph = plt.subplot(221)
        graph.plot(liste_angle,liste_Ex_UD,markersize=3.0, markeredgewidth=0.1, linewidth=0.5)    # Tracer de y en fonction de x
        plt.xlabel("angle (°)")                     # Légende de l'axe x
        plt.ylabel("Ex (MPa)")                      # Légende de l'axe y
        plt.grid(True)
        plt.xlim((-90,90))                      # Borne l'axe des y  
        plt.xticks( [-90, -45, 0, 45, 90])
        
        graph = plt.subplot(222)
        graph.plot(liste_angle,liste_Ey_UD,markersize=3.0, markeredgewidth=0.1, linewidth=0.5)    # Tracer de y en fonction de x
        plt.xlabel("angle (°)")                     # Légende de l'axe x
        plt.ylabel("Ey (MPa)")                      # Légende de l'axe y
        plt.grid(True)
        plt.xlim((-90,90))                      # Borne l'axe des y 
        plt.xticks( [-90, -45, 0, 45, 90])
        
        graph = plt.subplot(223)
        graph.plot(liste_angle,liste_Gxy_UD,markersize=3.0, markeredgewidth=0.1, linewidth=0.5)    # Tracer de y en fonction de x
        plt.xlabel("angle (°)")                     # Légende de l'axe x
        plt.ylabel("Gxy (MPa)")                     # Légende de l'axe y
        plt.grid(True)
        plt.xlim((-90,90))                      # Borne l'axe des y 
        plt.xticks( [-90, -45, 0, 45, 90])
        
        graph = plt.subplot(224)
        graph.plot(liste_angle,liste_Nuxy_UD,markersize=3.0, markeredgewidth=0.1, linewidth=0.5)    # Tracer de y en fonction de x
        plt.xlabel("angle (°)")                     # Légende de l'axe x
        plt.ylabel("Nuxy")                     # Légende de l'axe y
        plt.grid(True)
        plt.xlim((-90,90))                      # Borne l'axe des y 
        plt.xticks( [-90, -45, 0, 45, 90])
        
        plt.suptitle('Variation des Propriétés du pli en fonction de l angle')                                # Affiche le graphique
        plt.savefig("proprietes.pdf")
    
    
    

#liste_El = [3450, 72000]
#liste_Et = [0, 72000]
#liste_Glt = [1300, 29508]
#liste_Nult = [0.4, 0.22]
#liste_Rho = [1200, 2550]
#liste_Msf = [0, 300]
#liste_n  = [1, 1]
#Vf = 50
#
#test_1 = Homogeneisation_Mecanique_Pli(liste_El, liste_Et, liste_Glt, liste_Nult, liste_Rho, liste_Msf, Vf, liste_n)
