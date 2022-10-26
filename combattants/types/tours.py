from combattants.types.classifi import*

class Tour(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.reset_statistique()
    
    def reset_statistique(self):
        self.stats_de_base()
        self.vie = 1000
        self.vie_max = 1000
        self.regen = 2
        self.vitesse = 1
        self.taille = 10
        self.magnabilite = 3
        self.posture = [0,0, 0, 0] #domages, max, regen, contre
        self.corp_a_corp = [0 ,0, 0, 0, 0] #degats , portee, agro, precision effective, precision reelle
        self.defence = [0, 0] #effectif, reel
        self.pic = [0, 0, 0, 0] #proba effectif, degats, effectifs, proba reel, degats_reels
        self.charge = [0,0,0,0, 0, 0] #chargement, max, rechargement, x_dégats, precision effective, precision
        self.bouclier = [False, False] #boucier actif, bouclier present
        self.distance = [0,0,0,0,0,0] #etat de chargement, temps de chargement, porte min, porte max, precision,  degats
        self.vue = 1000
        self.visibilite = 1
        self.tournaret = [True, pi/2, pi/2]
        self.peur = [0, 1000, 10, 200] #moral, moral max effectif, recup, moral max
        self.colere = [0, 700, 10, 150] #moral, moral max, recup, , moral max
        self.dicipline = 20 # sensibilité aux sinergies d'equipe
    
    def create_affichage(self):
        self.corp = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
            
    def aff_mort(self):
        self.toile.coords(self.corp, self.x+4, self.y+4, self.x-4, self.y-4)
    
    def affiche(self,pas):
        self.toile.coords(self.corp, self.x+10, self.y+10, self.x-10, self.y-10)

class Stats_Tour(Tour):
    def __init__(self):
        self.reset_statistique()