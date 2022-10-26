from combattants.types.classifi import*

class Piquiers(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.reset_statistique()
        
    def reset_statistique(self):
        self.stats_de_base()
        self.competence.append('push')
        self.competence.append('mur')
        self.vie = 150
        self.vie_max = 100
        self.regen = 0.2
        self.vitesse = 5
        self.magnabilite = 9
        self.posture = [0,20, 2, 1] #domages, max, regen, contre
        self.corp_a_corp = [1.7,7,10,5, 5] #degats , portee, agro, precision effective, precision reelle
        self.defence = [6, 6] #effectif, reel
        self.pic = [15, 20, 15, 20] #proba effectif, degats, effectifs, proba reel, degats_reels
        self.charge = [1,5,1,5, 15, 15] #chargement, max, rechargement, x_dégats, precision effective, precision
        self.bouclier = [False, False] #boucier actif, bouclier present
        self.distance = [0,0,0,0,0,0] #etat de chargement, temps de chargement, porte min, porte max, precision,  degats
        self.vue = 1000
        self.visibilite = 1
        self.tournaret = [True, pi/2, pi/2]
        self.peur = [0, 60, 2, 60] #moral, moral max effectif, recup, moral max
        self.colere = [0, 60, 1, 60] #moral, moral max, recup, , moral max
        self.dicipline = 15 # senibilité aux sinergies d'equipe
    
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
            xt=self.x+avix(7, self.d+pi/3)
            yt=self.y+aviy(7, self.d+pi/3)
            x1 = xt - avix(4, self.d+pi/2)
            y1 = yt - aviy(4, self.d+pi/2)
            x2 = x1 + avix(15, self.d+pi/2)
            y2 = y1 + aviy(15, self.d+pi/2)
            self.toile.coords(self.corp, self.x+5, self.y+5, self.x-5, self.y-5)
            self.toile.coords(self.tete, xt+2, yt+2, xt-2, yt-2)
            self.toile.coords(self.arme, x1, y1, x2, y2)
        else:
            xt=self.x+avix(7, self.d+pi/3)
            yt=self.y+aviy(7, self.d+pi/3)
            x1 = self.x + avix(-1, self.d) + avix(6.5, self.d+pi/2)
            y1 = self.y + aviy(-1, self.d) + aviy(6.5, self.d+pi/2)
            x2 = x1 + avix(15, self.d-pi/12)
            y2 = y1 + aviy(15, self.d-pi/12)
            self.toile.coords(self.corp, self.x+5, self.y+5, self.x-5, self.y-5)
            self.toile.coords(self.tete, xt+2, yt+2, xt-2, yt-2)
            self.toile.coords(self.arme, x1, y1, x2, y2)
    
    def shomen(self, cible):
        plproche, dist, direc = cible
        if self.coldown<=0:
            if dist<self.corp_a_corp[1] and abs(rot(-self.d, direc))<pi/3:
                plproche.x+=avix(1, self.unite.d)
                plproche.y+=aviy(1, self.unite.d)
                pare = plproche.slashed(self.corp_a_corp[0], self, 2)
                self.coldown = 2
                if pare:
                    self.toile.cnv.itemconfig(self.arme, fill = 'grey')
                else:
                    self.toile.cnv.itemconfig(self.arme, fill = 'red')
    
    def chargee(self, degats, auteur):
        self.x+=avix(auteur.charge[0]*5, auteur.d)
        self.y+=aviy(auteur.charge[0]*5, auteur.d)
        if randint(0,self.pic[0]+auteur.charge[4])>self.pic[0] or abs(dir(self.x, self.y, self.d, auteur.x, auteur.y))>pi/4 or self.stun[0]:
            self.posture[0]+=degats
            self.aie(degats)
            ret = True
        else:
            self.posture[0]+=degats/10
            self.vie-=degats/2
            self.peur[0]+=degats/2
            self.colere[0]+=degats/2
            auteur.posture[0]+=auteur.charge[0]*self.pic[1]
            auteur.aie(auteur.charge[0]*self.pic[1])
            ret = False
        auteur.charge[0]=0
        return ret

class Stats_piquier(Piquiers):
    def __init__(self):
        self.reset_statistique()