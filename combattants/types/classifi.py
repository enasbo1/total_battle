# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:10:25 2022

@author: idugardin
"""

from logging.handlers import RotatingFileHandler
from random import randint
from backwork.direction import*
from combattants.types.actions import Acteur 
from combattants.types.progectile import Fleche
from combattants.types.Statistiques import Stats, Stats_none

class Persoide(Stats):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        self.ecr_x = x
        self.ecr_y = y
        self.putrefaction = 0
        self.hited = 0
        self.avancement = 0
        self.d=unite.d
        self.groupe_up = None
        self.groupe_down = None
        self.x=unite.x+(randint(-500,500)/10)
        self.y=unite.y+(randint(-500,500)/10)
        self.unite = unite
        self.coo_unite = (None, None)
        self.taille = 5
        self.deplacable = True
        self.toile = toile
        self.technique = self.shomen
        self.deplacement = self.no_formation
        self.avancer = self.marcher
        self.quad=quad
        self.cont=quad
        self.quad_alliers = quad_allier
        self.cont_alliers = quad_allier
        self.quad_ennemi = quad_enemis
        self.create_affichage()
    
    def rien(self, pas):
        pass
    
    def create_affichage(self):
        self.tete = self.toile.cnv.create_oval(0,0,0,0, fill=self.unite.color_model)
        self.corp = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
        self.arme = self.toile.cnv.create_line(0,0,0,0, fill=self.unite.color_model, width=3)

        
    def localise(self, cont):
        self.cont = cont
    
    def local1(self, cont):
        self.cont_alliers = cont
    
    def slashed(self, degats, acteur, pas):
        acteur.uncontact = False
        self.posture[0]+=degats*pas
        if randint(0,self.defence[0]+acteur.corp_a_corp[3])>self.defence[0] or abs(dir(self.x, self.y, self.d, acteur.x, acteur.y))>pi/3 or self.stun[0]:
            self.aie(degats*pas)
            return False
        else:
            self.peur[0]+=degats*pas/2
            self.colere[0]+=degats*pas/2
            acteur.posture[0]+=pas*self.posture[3]
            acteur.peur[0]+=degats*pas/3
            acteur.colere[0]+=degats*pas/3
            return True
    
    def shoted(self, item, damage):
        if item.unite.color==self.unite.color:
            damage=damage/2
        self.aie(damage)
        return True
        
    def aie(self, degats):
        self.vie-=degats
        self.unite.dommages+=degats
        self.peur[0]+=degats
        self.colere[0]+=degats
        if self.hited<degats:
            self.hited=degats

    
    def chargee(self, degats, auteur):
        self.x+=avix(auteur.charge[0]*5, auteur.d)
        self.y+=aviy(auteur.charge[0]*5, auteur.d)
        self.posture[0]+=degats
        if randint(0,self.pic[0]+auteur.charge[4])>self.pic[0] or abs(dir(self.x, self.y, self.d, auteur.x, auteur.y))>pi/4 or self.stun[0]:
            self.aie(degats)
            ret = True
        else:
            self.vie-=degats/2
            self.peur[0]+=degats/2
            self.colere[0]+=degats/2
            auteur.posture[0]+=auteur.charge[0]*self.pic[1]
            auteur.aie(auteur.charge[0]*self.pic[1])
            ret = False
        auteur.charge[0]=0
        return ret
    
    def affiche(self, pas):
        X=int(self.x+avix(3, self.d-pi/4))
        Y=int(self.y+aviy(3, self.d-pi/4))
        x1 = self.x + avix(6, self.d+pi/2)
        y1 = self.y + aviy(6, self.d+pi/2)
        x2 = x1 + avix(8, self.d+pi/6)
        y2 = y1 + aviy(8, self.d+pi/6)
        self.toile.coords(self.corp, int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5)
        self.toile.coords(self.tete, int(X)+4.5, int(Y)+4.5, int(X)-4.5, int(Y)-4.5)
        self.toile.coords(self.arme, x1, y1, x2, y2)
        
    def aff_mort(self):
        self.toile.coords(self.corp, self.x+4, self.y+4, self.x-4, self.y-4)
        self.toile.coords(self.tete, self.x+2, self.y+2, self.x-2, self.y-2)
        self.toile.coords(self.arme, self.x+4, self.y-4, self.x+5, self.y+4)
    
    def cache(self):
        self.toile.cnv.coords(self.corp, -1, -1, -1, -1)
        self.toile.cnv.coords(self.tete, -1, -1, -1, -1)
        self.toile.cnv.coords(self.arme, -1, -1, -1, -1)
  
    def tour(self, pas):
        if self.vie>0:
            self.hited-=pas*10*self.regen
            if self.coldown>1:
                self.toile.cnv.itemconfig(self.arme, fill=self.unite.color_model)
            self.recup(pas)
            plproche, dist, direc = self.cont.proche(self, self.vue)
            self.plproche = (plproche, dist, direc)
            self.choisir(pas)
            self.deplacement(pas)
            self.d = lim(0,self.ecr_x,0,self.ecr_y, self.x, self.y, self.d)
            self.x, self.y = limxy(self.x, self.y, 0 ,self.ecr_x, 0, self.ecr_y)
            if plproche!=None:
                dist -= self.taille+plproche.taille+1
                if dist<=0 and plproche.deplacable:
                    plproche.x-=avix(dist, direc)
                    plproche.y-=aviy(dist, direc)
            if self.hited>0:
                self.toile.cnv.itemconfig(self.corp, outline='red')
            elif self.unite.selected:
                self.toile.cnv.itemconfig(self.corp, outline='white')
            else:
                self.toile.cnv.itemconfig(self.corp, outline='black')
            self.affiche(pas)
            return False
        else:
            if self.putrefaction<(self.vie_max**2)/100:
                self.toile.cnv.itemconfig(self.corp, outline = 'black')
                self.aff_mort()
                self.putrefaction+=pas
            else:
                self.cache()
            return True
