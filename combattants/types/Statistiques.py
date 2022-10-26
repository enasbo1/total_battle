from math import*
from combattants.types.actions import Acteur

class Stats(Acteur):
    def __init__(self):
        pass
    
    def rien(self, pas):
        pass
    
    def stats_de_base(self):
        self.competence = []
        self.taille = 5
        self.vie = 175
        self.vie_max = 120
        self.regen = 0.3
        self.vitesse = 5
        self.magnabilite = 10
        self.stun = [False,0]
        self.posture = [0,20, 2, 1] #domages, max, regen, contre
        self.animation = self.rien
        self.coldown = 0
        self.corp_a_corp = [1.7,5,7,5, 5] #degat5s , portee, agro, precision effective, precision reelle
        self.defence = [12, 12] #effectif, reel
        self.pic = [5, 5, 5, 5] #proba effectif, degats, effectifs, proba reel, degats_reels
        self.charge = [1,1,0.5,5, 5, 5] #chargement, max, rechargement, x_dégats, precision effective, precision
        self.bouclier = [False, False] #boucier actif, bouclier present
        self.distance = [0,0,0,0,0,0] #etat de chargement, temps de chargement, porte min, porte max, precision,  degats
        self.carquoi = [0,0] # nb de fleche restance, nb de fleches au depart 
        self.vue = 1000
        self.visibilite = 1
        self.tournaret = [True, pi/2, pi/2]
        self.uncontact = True
        self.peur = [0, 60, 2, 60] #moral, moral max effectif, recup, moral max reel
        self.colere = [0, 60, 1, 60] #moral, moral max effectif recup, , moral max reel
        self.dicipline = 15 # senibilité aux sinergies d'equipe
        self.choix = {'Groupe': self.groupea, 'Garde': self.grouped, 'Dispertion': self.disperse, 'Regroupe': self.disperse}
        self.formation = {'Groupe': self.no_formation, 'Garde': self.garde, 'Dispertion': self.dispertion, 'Regroupe': self.regroupe}
        self.vitesses = {'Arret': self.arret, 'Marche': self.marcher, 'Course':self.courir}
    
    def recup(self, pas):
        self.defence[0] = self.defence[1]
        self.charge[4] = self.charge[5]
        self.pic[0]=self.pic[2]
        self.pic[1]=self.pic[3]
        self.peur[1]=self.peur[3]
        self.colere[1]=self.colere[3]
        self.corp_a_corp[3] = self.corp_a_corp[4]
        if self.posture[0]>=self.posture[1]:
            self.stun[0]=True
            self.charge[0]=0
            self.stun[1]=2.5
            self.posture[0]=self.posture[1]
        if self.coldown<=0:
            if self.vie<self.vie_max:
                if self.vie+(pas*self.regen)<self.vie_max:
                    self.vie+=pas*self.regen
                else:
                    self.vie=self.vie_max
        if self.posture[0]-(pas*self.posture[2])>0:
            self.posture[0]-=pas*self.posture[2]
        else:
            self.posture[0]=0
        if self.peur[0]-(pas*self.peur[2])>0:
            self.peur[0]-=pas*self.peur[2]
        else:
            self.peur[0]=0
        if self.colere[0]-(pas*self.colere[2])>0:
            self.colere[0]-=pas*self.colere[2]
        else:
            self.colere[0]=0
        if self.coldown<=0:
            if self.charge[0]+(pas*self.charge[2]/20)<self.charge[1]:
                self.charge[0]+=pas*self.charge[2]/20
            else:
                self.charge[0]=self.charge[1]
        if self.stun[0]:
            self.stun[1]-=pas
            if self.stun[1]<=0:
                self.stun[0]=False
        self.coldown -= pas
        self.distance[0] -= pas
        self.uncontact = True

class Stats_none(Stats):
    def __init__(self):
        self.stats_de_base()