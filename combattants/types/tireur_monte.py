from combattants.types.classifi import*
from tkinter import ARC

class Tireur_monte(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.d1 = self.d
        self.reset_statistique()
        
    def reset_statistique(self):
        self.stats_de_base()
        self.competence.append('tir_en_mouvement')
        self.vie = 100
        self.vie_max = 75
        self.regen = 0.2
        self.vitesse = 15
        self.magnabilite = 14
        self.corp_a_corp = [1,4,5,2, 2] #degats , portee, agro, precision effective, precision reelle
        self.defence = [2, 2] #effectif, reel
        self.pic = [4, 10, 4, 10] #proba effectif, degats, effectifs, proba reel, degats_reels
        self.charge = [1,10,5,15, 3, 3] #chargement, max, rechargement, x_dégats, precision effective, precision
        self.bouclier = [False, False] #boucier actif, bouclier present
        self.distance = [0,20,50,300,12,75] #etat de chargement, temps de chargement, porte min, porte max, precision,  degats
        self.carquoi = [5,5] # nb de fleche restance, nb de fleches au depart 
        self.vue = 1000
        self.visibilite = 1
        self.tournaret = [False, pi/3, pi/2]
        self.peur = [0, 50, 2, 50] #moral, moral max effectif, recup, moral max
        self.colere = [0, 50, 2, 50] #moral, moral max, recup, , moral max
        self.dicipline = 11 # senibilité aux sinergies d'equipe
        self.choix = {'Cible': self.grouped, 'Groupe':self.groupea, 'Garde': self.grouped, 'Dispertion': self.disperse, 'Regroupe': self.disperse}
        self.formation = {'Cible': self.cibler,'Groupe':self.no_formation, 'Garde': self.garde, 'Dispertion': self.dispertion, 'Regroupe': self.regroupe}
        self.vitesses = {'Arret': self.arret, 'Marche': self.marcher, 'Course':self.courir}
    
    def create_affichage(self):
        self.arriere = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color_model)
        self.avant = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
        self.corp = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
        self.arme = self.toile.cnv.create_arc(0,0,0,0, outline=self.unite.color_model, style=ARC, width=3)
        self.fleche = Fleche(self.toile, self, self.quad)
        self.tete = self.toile.cnv.create_oval(0,0,0,0, fill=self.unite.color_model)
        self.main = self.toile.cnv.create_oval(0,0,0,0, fill=self.unite.color_model)
        xf1 = self.x + avix(5, self.d+pi/3)
        yf1 = self.y + aviy(5, self.d+pi/3)
        xf2 = xf1 + avix(10, self.d+pi/3)
        yf2 = yf1 + aviy(10, self.d+pi/3)
        self.fleche.place(xf1, yf1, xf2, yf2)
    
    def aff_mort(self):
        self.toile.coords(self.avant, self.x+4, self.y+4, self.x-4, self.y-4)
        self.toile.coords(self.arriere, self.x+4, self.y+4, self.x-4, self.y-4)
        self.toile.coords(self.corp, self.x+2, self.y+2, self.x-2, self.y-2)
        self.toile.coords(self.arme, self.x+4, self.y-4, self.x+5, self.y+4)
        self.toile.coords(self.tete, self.x+2, self.y+2, self.x-2, self.y-2)
        self.toile.coords(self.main, self.x+2, self.y+2, self.x-2, self.y-2)
        self.fleche.cache()

    
    def cache(self):
        self.toile.cnv.coords(self.corp, -1, -1, -1, -1)
        self.toile.cnv.coords(self.tete, -1, -1, -1, -1)
        self.toile.cnv.coords(self.main, -1, -1, -1, -1)
        self.toile.cnv.coords(self.arme, -1, -1, -1, -1)
        self.toile.cnv.coords(self.avant, -1, -1, -1, -1)
        self.toile.cnv.coords(self.arriere, -1, -1, -1, -1)
        self.fleche.cache()
    
    def affiche(self,pas):
        #arc
        d = self.degres()
        xm=self.x+avix(7, self.d+pi/3)
        ym=self.y+aviy(7, self.d+pi/3)
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
            xm=self.x+avix(7, self.d)
            ym=self.y+aviy(7, self.d)
        if self.carquoi[0]>0:  #WIP
            self.fleche.aff()
        else:
            self.fleche.cache()
        self.toile.coords(self.main, xm+2, ym+2, xm-2, ym-2)
        self.toile.cnv.itemconfig(self.arme, start=d-120, extent=120)
        self.toile.coords(self.arme, x1, y1, x2, y2)
        # cheval
        d = rot(-self.d1, self.d)
        if pas!=0:
            d = d*self.magnabilite/(pas*25)
            df = rot(d, self.d)
            dt = rot(d, df)
        else:
            df = self.d
            dt = self.d
        self.d1 = self.d
        xb = self.x-avix(4.5, self.d)
        yb = self.y-aviy(4.5, self.d)
        xf=self.x+avix(4.5, df)
        yf=self.y+aviy(4.5, df)
        xt=xf+avix(4, dt)
        yt=yf+aviy(4, dt)
        self.toile.coords(self.arriere, xb+4.5, yb+4.5, xb-4.5,yb-4.5)
        self.toile.coords(self.corp, self.x+5, self.y+5, self.x-5, self.y-5)
        self.toile.coords(self.avant, xf+4.5, yf+4.5, xf-4.5,yf-4.5)
        self.toile.coords(self.tete, xt+3, yt+3, xt-3, yt-3)
    
    def cibler(self, pas):
        plproche, dist, direc = self.quad_ennemi.close(self, self.vue)
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            if dist<self.corp_a_corp[2]:
                self.ennemi = (plproche, dist, direc)
                self.combat(pas)
            else:
                if self.distance[5]>0  and self.carquoi[0]>0:
                    plproche, dist, direc = self.quad_ennemi.close(self.unite.pointeur, self.unite.r+50)
                    if plproche!=None:
                        direc = dir(self.x, self.y, 0, plproche.x, plproche.y)
                        dist = dis(self.x, self.y, plproche.x, plproche.y)-self.taille+plproche.taille+1
                        self.tir(direc, dist, pas)
                self.au_pas(pas)
        else:
            self.au_pas(pas)
    
    def garde(self, pas):
        plproche, dist, direc = self.quad_ennemi.close(self, self.vue)
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            if dist<self.corp_a_corp[2]:
                self.ennemi = (plproche, dist, direc)
                self.combat(pas)
            elif self.portee(dist):
                self.tir(direc, dist, pas)
            else:
                if self.distance[5]>0 and self.carquoi[0]>0:
                    plproche, dist, direc = self.quad_ennemi.close(self.unite.pointeur, self.unite.r+50)
                    if plproche!=None:
                        dist = dis(self.x, self.y, plproche.x, plproche.y)-self.taille+plproche.taille+1
                        if self.move_portee(dist):
                            direc = dir(self.x, self.y, 0, plproche.x, plproche.y)
                            self.tir(direc, dist, pas)
                            self.avancer(pas)
                        else:
                            self.au_pas(pas)
                    else:
                        di = self.unite.d
                        e = 1
                        self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
                        self.avancer(pas)
                else:
                    self.au_pas(pas)
        else:
            self.au_pas(pas)
    
    def degres(self):
        return(-self.d*180/pi)

class Stats_monte(Tireur_monte):
    def __init__(self):
        self.reset_statistique()