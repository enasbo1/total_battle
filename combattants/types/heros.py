from combattants.types.classifi import*

class Heros(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.reset_statistique()
        
    def reset_statistique(self):
        self.stats_de_base()
        self.competence.append('claivoyance')
        self.competence.append('prescient')
        self.competence.append('bouclier')
        self.competence.append('telekinesie')
        self.vie = 450
        self.vie_max = 300
        self.regen = 1
        self.vitesse = 10
        self.taille = 7
        self.magnabilite = 20
        self.posture = [0,200, 20, 4] #domages, max, regen, contre
        self.corp_a_corp = [40 ,10, 15, 8, 8] #degats , portee, agro, precision effective, precision reelle
        self.defence = [15, 15] #effectif, reel
        self.pic = [15, 25, 15, 25] #proba effectif, degats, effectifs, proba reel, degats_reels
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
        self.arme = self.toile.cnv.create_line(0,0,0,0, fill=self.unite.color_model, width=4)
        self.tete = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color_model)
            
    def aff_mort(self):
        self.toile.coords(self.corp, self.x+4, self.y+4, self.x-4, self.y-4)
        self.toile.coords(self.tete, self.x+2, self.y+2, self.x-2, self.y-2)
        self.toile.coords(self.arme, self.x+4, self.y-4, self.x+5, self.y+4)
    
    def affiche(self,pas):
        if self.stun[0]:
            xt=self.x+avix(11, self.d)+avix(7, self.d+2*pi/3)
            yt=self.y+aviy(11, self.d)+aviy(7, self.d+2*pi/3)
            x1 = xt - avix(2, self.d+5*pi/6)
            y1 = yt - aviy(2, self.d+5*pi/6)
            x2 = x1 + avix(17, self.d+5*pi/6)
            y2 = y1 + aviy(17, self.d+5*pi/6)

        else:
            xt=self.x+avix(11, self.d)+avix(7, self.d+2*pi/3)
            yt=self.y+aviy(11, self.d)+aviy(7, self.d+2*pi/3)
            x1 = self.x + avix(11, self.d) + avix(9, self.d+2*pi/3)
            y1 = self.y + aviy(11, self.d) + aviy(9, self.d+2*pi/3)
            x2 = x1 - avix(20, self.d+2*pi/3)
            y2 = y1 - aviy(20, self.d+2*pi/3)
        self.toile.coords(self.corp, self.x+7, self.y+7, self.x-7, self.y-7)
        self.toile.coords(self.tete, xt+3, yt+3, xt-3, yt-3)
        self.toile.coords(self.arme, x1, y1, x2, y2)
    
    def slashed(self, degats, acteur, pas):
        acteur.uncontact = False
        self.posture[0]+=degats*pas
        if self.stun[0]:
            self.aie(pas*degats)
            return False
        else:
            self.peur[0]+=degats*pas/2
            self.colere[0]+=degats*pas/2
            acteur.peur[0]+=degats*pas/3
            acteur.colere[0]+=degats*pas/3
            return True
    
    def shomen(self, cible):
        plproche, dist, direc = cible
        if self.coldown<=0:
            if dist<self.corp_a_corp[1] and abs(rot(-self.d, direc))<pi/3:
                pare = plproche.slashed(self.corp_a_corp[0], self, 2)
                self.coldown = 2
                if pare:
                    self.toile.cnv.itemconfig(self.arme, fill = 'grey')
                else:
                    self.toile.cnv.itemconfig(self.arme, fill = 'red')
                    self.x+=avix(20, direc)
                    self.y+=aviy(20, direc)
                    proche = self.quad_ennemi.proxi(self, 20)
                    for i in proche:
                        direc = dir(self.x, self.y, 0, i.x, i.y)
                        i.x+=avix(5, self.d)+avix(5, direc)
                        i.y+=aviy(5, self.d)+aviy(5, direc)
                        i.slashed(self.corp_a_corp[0], self, 0.5)
                    plproche.x=self.x+avix(10, self.d)
                    plproche.y=self.y+aviy(10, self.d)
    
    def chargee(self, degats, auteur):
        self.x+=avix(auteur.charge[0]*5, auteur.d)
        self.y+=aviy(auteur.charge[0]*5, auteur.d)
        self.posture[0]+=degats
        if self.stun[0]:
            self.aie(degats)
            return False
        else:
            self.aie(degats/4)
            auteur.posture[0]+=auteur.charge[0]*self.pic[1]
            auteur.aie(auteur.charge[0]*self.pic[1])
        auteur.charge[0]=0
    
    def shoted(self, item, damage):
        if self.uncontact:
            if self.stun[0] or randint(0,2)==0:
                if item.unite.color==self.unite.color:
                    damage=damage/2
                self.aie(damage)
                return True
            else:
                self.posture[0]-=damage
                return False
        else:
            if item.unite.color==self.unite.color:
                damage=damage/2
            self.aie(damage)
            return True

class Stats_heros(Heros):
    def __init__(self):
        self.reset_statistique()