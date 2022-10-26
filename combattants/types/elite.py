from combattants.types.classifi import*

class Elite(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.reset_statistique()
        
    def reset_statistique(self):
        self.stats_de_base()
        self.competence.append('6e sens')
        self.vie = 250
        self.vie_max = 200
        self.regen = 0.3
        self.vitesse = 5
        self.magnabilite = 15
        self.posture = [0,150, 5, 1] #domages, max, regen, contre
        self.corp_a_corp = [5 ,10, 15, 12, 12] #degats , portee, agro, precision effective, precision reelle
        self.defence = [15, 15] #effectif, reel
        self.pic = [15, 20, 15, 20] #proba effectif, degats, effectifs, proba reel, degats_reels
        self.charge = [1,6,2,30, 10, 10] #chargement, max, rechargement, x_dégats, precision effective, precision
        self.bouclier = [False, False] #boucier actif, bouclier present
        self.distance = [0,0,0,0,0,0] #etat de chargement, temps de chargement, porte min, porte max, precision,  degats
        self.vue = 1000
        self.visibilite = 1
        self.tournaret = [True, pi/2, pi/2]
        self.peur = [0, 200, 10, 200] #moral, moral max effectif, recup, moral max
        self.colere = [0, 150, 10, 150] #moral, moral max, recup, , moral max
        self.dicipline = 20 # sensibilité aux sinergies d'equipe
    
    def create_affichage(self):
        self.corp = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
        self.arme = self.toile.cnv.create_line(0,0,0,0, fill=self.unite.color_model, width=3)
        self.tete = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color_model)
            
    def aff_mort(self):
        self.toile.coords(self.corp, self.x+4, self.y+4, self.x-4, self.y-4)
        self.toile.coords(self.tete, self.x+2, self.y+2, self.x-2, self.y-2)
        self.toile.coords(self.arme, self.x+4, self.y-4, self.x+5, self.y+4)
    
    def affiche(self,pas):
        if self.stun[0]:
            xt=self.x+avix(7, self.d)+avix(4, self.d+2*pi/3)
            yt=self.y+aviy(7, self.d)+aviy(4, self.d+2*pi/3)
            x1 = xt - avix(2, self.d+5*pi/6)
            y1 = yt - aviy(2, self.d+5*pi/6)
            x2 = x1 + avix(17, self.d+5*pi/6)
            y2 = y1 + aviy(17, self.d+5*pi/6)
            self.toile.coords(self.corp, self.x+5, self.y+5, self.x-5, self.y-5)
            self.toile.coords(self.tete, xt+2, yt+2, xt-2, yt-2)
            self.toile.coords(self.arme, x1, y1, x2, y2)
        else:
            xt=self.x+avix(7, self.d)+avix(4, self.d+2*pi/3)
            yt=self.y+aviy(7, self.d)+aviy(4, self.d+2*pi/3)
            x1 = self.x + avix(6, self.d) + avix(5, self.d+2*pi/3)
            y1 = self.y + aviy(6, self.d) + aviy(5, self.d+2*pi/3)
            x2 = x1 - avix(17, self.d+2*pi/3)
            y2 = y1 - aviy(17, self.d+2*pi/3)
            self.toile.coords(self.corp, self.x+5, self.y+5, self.x-5, self.y-5)
            self.toile.coords(self.tete, xt+2, yt+2, xt-2, yt-2)
            self.toile.coords(self.arme, x1, y1, x2, y2)
    
    def slashed(self, degats, acteur, pas):
        acteur.uncontact = False
        self.posture[0]+=degats*pas
        if randint(0,self.defence[0]+acteur.corp_a_corp[3])>self.defence[0] or self.stun[0]:
            self.aie(pas*degats)
            return False
        else:
            self.peur[0]+=degats*pas/2
            self.colere[0]+=degats*pas/2
            acteur.peur[0]+=degats*pas/3
            acteur.colere[0]+=degats*pas/3
            return True

class Stats_elite(Elite):
    def __init__(self):
        self.reset_statistique()