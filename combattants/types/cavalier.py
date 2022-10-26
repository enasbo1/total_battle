from combattants.types.classifi import*

class Cavalier(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.d1 = self.d
        self.reset_statistique()
        
    def reset_statistique(self):
        self.stats_de_base()
        self.vie = 100
        self.vie_max = 75
        self.regen = 0.2
        self.vitesse = 15
        self.magnabilite = 12
        self.corp_a_corp = [1,5,7,4, 4] #degats , portee, agro, precision effective, precision reelle
        self.defence = [2, 2] #effectif, reel
        self.pic = [4, 10, 4, 10] #proba effectif, degats, effectifs, proba reel, degats_reels
        self.charge = [1,10,5,15, 3, 3] #chargement, max, rechargement, x_dégats, precision effective, precision
        self.bouclier = [False, False] #boucier actif, bouclier present
        self.distance = [0,0,0,0,0,0] #etat de chargement, temps de chargement, porte min, porte max, precision,  degats
        self.vue = 1000
        self.visibilite = 1
        self.tournaret = [False, pi/2, pi/2]
        self.peur = [0, 40, 2, 40] #moral, moral max effectif, recup, moral max
        self.colere = [0, 40, 1, 40] #moral, moral max, recup, , moral max
        self.dicipline = 11 # senibilité aux sinergies d'equipe
    
    def create_affichage(self):
        self.arriere = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color_model)
        self.avant = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
        self.corp = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
        self.tete = self.toile.cnv.create_oval(0,0,0,0, fill=self.unite.color_model)
        self.arme = self.toile.cnv.create_line(0,0,0,0, fill=self.unite.color_model, width=3)
    
    def aff_mort(self):
        self.toile.coords(self.avant, self.x+4, self.y+4, self.x-4, self.y-4)
        self.toile.coords(self.arriere, self.x+4, self.y+4, self.x-4, self.y-4)
        self.toile.coords(self.corp, self.x+2, self.y+2, self.x-2, self.y-2)
        self.toile.coords(self.tete, self.x+2, self.y+2, self.x-2, self.y-2)
        self.toile.coords(self.arme, self.x+4, self.y-4, self.x+5, self.y+4)
    
    def cache(self):
        self.toile.cnv.coords(self.corp, -1, -1, -1, -1)
        self.toile.cnv.coords(self.tete, -1, -1, -1, -1)
        self.toile.cnv.coords(self.arme, -1, -1, -1, -1)
        self.toile.cnv.coords(self.avant, -1, -1, -1, -1)
        self.toile.cnv.coords(self.arriere, -1, -1, -1, -1)
    
    def affiche(self,pas):
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
        x1 = self.x + avix(6, self.d+pi/2)
        y1 = self.y + aviy(6, self.d+pi/2)
        x2 = x1 + avix(8, self.d+pi/6)
        y2 = y1 + aviy(8, self.d+pi/6)
        self.toile.coords(self.arriere, xb+4.5, yb+4.5, xb-4.5,yb-4.5)
        self.toile.coords(self.corp, self.x+5, self.y+5, self.x-5, self.y-5)
        self.toile.coords(self.avant, xf+4.5, yf+4.5, xf-4.5,yf-4.5)
        self.toile.coords(self.tete, xt+3, yt+3, xt-3, yt-3)
        self.toile.coords(self.arme, x1, y1, x2, y2)
        if self.charge[0]>=self.charge[1]:
            self.toile.cnv.itemconfig(self.tete, fill='black')
        else:
            self.toile.cnv.itemconfig(self.tete, fill=self.unite.color_model)

class Stats_cavalier(Cavalier):
    def __init__(self):
        self.reset_statistique()