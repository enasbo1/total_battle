from combattants.types.classifi import*
from tkinter import ARC
   
class Archet(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.reset_statistique()
        
    def reset_statistique(self):
        self.stats_de_base()
        self.vie = 50
        self.vie_max = 40
        self.regen = 0.1
        self.vitesse = 6
        self.magnabilite = 12
        self.corp_a_corp = [1,4,5,2, 2] #degats , portee, agro, precision effective, precision reelle
        self.defence = [2, 2] #effectif, reel
        self.pic = [0, 0, 0, 0] #proba effectif, degats, effectifs, proba reel, degats_reels
        self.charge = [0,1,1,0, 0, 0] #chargement, max, rechargement, x_dégats, precision effective, precision
        self.bouclier = [False, False] #boucier actif, bouclier present
        self.distance = [5,5,50,400,10,15] #etat de chargement, temps de chargement, porte min, porte max, precision,  degats
        self.carquoi = [40,40] # nb de fleche restance, nb de fleches au depart 
        self.vue = 1000
        self.visibilite = 1
        self.tournaret = [True, pi/3, pi/2]
        self.peur = [0, 20, 1, 20] #moral, moral max effectif, recup, moral max
        self.colere = [0, 40, 1, 40] #moral, moral max, recup, , moral max
        self.dicipline = 11 # senibilité aux sinergies d'equipe
        self.choix = {'Cible': self.groupea, 'Garde': self.grouped, 'Dispertion': self.disperse, 'Regroupe': self.disperse}
        self.formation = {'Cible': self.cibler, 'Garde': self.garde, 'Dispertion': self.dispertion, 'Regroupe': self.regroupe}
        self.vitesses = {'Arret': self.arret, 'Marche': self.marcher, 'Course':self.courir}
    
    def create_affichage(self):
        self.corp = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
        self.arme = self.toile.cnv.create_arc(0,0,0,0, outline=self.unite.color_model, style=ARC, width=3)
        self.fleche = Fleche(self.toile, self, self.quad)
        self.tete = self.toile.cnv.create_oval(0,0,0,0, fill=self.unite.color_model)
        xf1 = self.x + avix(5, self.d+pi/3)
        yf1 = self.y + aviy(5, self.d+pi/3)
        xf2 = xf1 + avix(10, self.d+pi/3)
        yf2 = yf1 + aviy(10, self.d+pi/3)
        self.fleche.place(xf1, yf1, xf2, yf2)
    
    def aff_mort(self):
        self.toile.coords(self.corp, self.x+2, self.y+2, self.x-2, self.y-2)
        self.toile.coords(self.arme, self.x+4, self.y-4, self.x+5, self.y+4)
        self.toile.coords(self.tete, self.x+2, self.y+2, self.x-2, self.y-2)
        self.fleche.cache()

    
    def cache(self):
        self.toile.cnv.coords(self.corp, -1, -1, -1, -1)
        self.toile.cnv.coords(self.tete, -1, -1, -1, -1)
        self.toile.cnv.coords(self.arme, -1, -1, -1, -1)
        self.fleche.cache()
    
    def affiche(self,pas):
        d = self.degres()
        xt=self.x+avix(7, self.d+pi/3)
        yt=self.y+aviy(7, self.d+pi/3)
        x1 = self.x + avix(-2.5, self.d+pi/3)+9
        y1 = self.y + aviy(-2.5, self.d+pi/3)+9
        x2 = x1-18
        y2 = y1-18

        if self.distance[0]<self.distance[1]-2:
            if self.distance[0]<0:
                    self.fleche.color('black')
            else:
                self.fleche.color(self.unite.color_model)
            xf1 = self.x + avix(5, self.d+pi/3)
            yf1 = self.y + aviy(5, self.d+pi/3)
            xf2 = xf1 + avix(10, self.d+pi/3)
            yf2 = yf1 + aviy(10, self.d+pi/3)
            self.fleche.place(xf1, yf1, xf2, yf2)
        else:
            d+=60
            xt=self.x+avix(7, self.d)
            yt=self.y+aviy(7, self.d)
        if self.carquoi[0]>0:  #WIP
            self.fleche.aff()
        else:
            self.fleche.cache()
        self.toile.coords(self.corp, self.x+5, self.y+5, self.x-5, self.y-5)
        self.toile.coords(self.tete, xt+2, yt+2, xt-2, yt-2)
        self.toile.cnv.itemconfig(self.arme, start=d-120, extent=120)
        self.toile.coords(self.arme, x1, y1, x2, y2)
    
    def cibler(self, pas):
        plproche, dist, direc = self.quad_ennemi.close(self, self.vue)
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            if dist<self.corp_a_corp[2]:
                self.ennemi = (plproche, dist, direc)
                self.combat(pas)
            else:
                plproche, dist, direc = self.quad_ennemi.close(self.unite.pointeur, self.unite.r+50)
                if plproche!=None:
                    direc = dir(self.x, self.y, 0, plproche.x, plproche.y)
                    dist = dis(self.x, self.y, plproche.x, plproche.y)-self.taille+plproche.taille+1
                    if self.portee(dist):
                        self.tir(direc, dist, pas)
                    else:
                        self.au_pas(pas)
                else:
                    self.au_pas(pas)
        else:
            self.au_pas(pas)
    
    def degres(self):
        return(-self.d*180/pi)

class Stats_archets(Archet):
    def __init__(self):
        self.reset_statistique()