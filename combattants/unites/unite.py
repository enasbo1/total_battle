from backwork.direction import *
from combattants.types.classifi import*
from combattants.unites.pointeur import Pointeur
class Unite:
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', color_model = 'white', Type=Persoide, Stats=Stats_none, nb_model=40, nom = 'soldats', formation = 'Garde'):
        self.x = x
        self.y = y
        self.groupe_up = None
        self.groupe_down = None
        self.nom = nom
        self.createur = createur
        self.d = dir(self.x, self.y,0, toile.x_terrain/2, toile.y_terrain/2)
        self.color = color
        self.color_model = color_model
        self.toile = toile
        self.stats = Stats()
        self.pointeur = Pointeur(self.toile, self)
        self.cible = self.pointeur
        self.groupe = [Type(toile, quad, quad_allie, quad_ennemi, toile.x_terrain, toile.y_terrain, unite = self)for i in range(nb_model)]
        self.corp = toile.cnv.create_oval(0,0,0,0, width = 2, outline= self.color_model)
        self.tete = toile.cnv.create_oval(0,0,0,0, width = 2, outline= color)
        self.taille = nb_model
        racine=sqrt(self.taille)
        self.selected = False
        self.strats = []
        self.r = racine*7
        self.zone = self.taille*100
        self.etat = None
        self.dommages = 0
        self.strategies = ['Groupe', 'Garde', 'Dispertion', 'Regroupe']
        self.formations = {'Groupe': self.groupee, 'Garde': self.groupee, 'Dispertion': self.disperse, 'Regroupe': self.disperse}
        self.deplacements = ['Arret','Marche', 'Course']
        self.vitesse = self.deplacements[2]
        self.retardataire = False
        self.formation = formation

    
    def localise(self, cont):
        pass
    
    def cible(self, cible):
        self.cible = cible
        
    def groupee(self):
        if self.deplacement:
            X=0
            Y=0
            for i in self.groupe:
                X+=i.x
                Y+=i.y
            self.x=X/self.taille
            self.y=Y/self.taille
    
    def disperse(self):
        X=0
        Y=0
        for i in self.groupe:
            X+=i.x
            Y+=i.y
        X=X/self.taille
        Y=Y/self.taille
        self.d = dir(self.x, self.y, 0, X, Y)
        self.x=X
        self.y=Y
    
    def tour(self, pas):
        if self.taille>0:
            self.alerte(pas)
            self.deplacement = True
            if self.retardataire:
                self.vitesse = self.deplacements[1]
                self.retardataire = False
            else:
                self.vitesse = self.deplacements[2]
            if self.cible==self.pointeur:
                if disrap(self.x, self.y, self.cible.x, self.cible.y)<(((self.taille+10)/2)**2):
                    self.vitesse = self.deplacements[0]
                    if self.cible.oriente:
                        self.d = self.cible.d
                    self.deplacement = False
                else:
                    self.d = dir(self.x, self.y, 0,self.cible.x, self.cible.y)
            else:
                if disrap(self.x, self.y, self.cible.x, self.cible.y)<((self.taille/2)**2):
                    self.vitesse = self.deplacements[0]
                    self.deplacement = False
                self.d = dir(self.x, self.y, 0,self.cible.x, self.cible.y)
            self.pointeur.tour()
            kill = []
            self.formations[self.formation]()
            for j,i in enumerate(self.groupe):
                if i.tour(pas):
                    kill.append(j)
            for i in kill:
                self.kill(i)
            n = 0
            for i in kill:
                del(self.groupe[i-n])
                n+=1
            if n!=0:
                self.taille = len(self.groupe)
                racine=sqrt(self.taille)
                self.r = racine*7
                self.zone = self.taille*100

            self.affiche()
        else:
            self.toile.cnv.coords(self.corp, -1, -1 , -1 ,-1)
            self.toile.cnv.coords(self.tete, -1, -1 , -1 ,-1)
            self.pointeur.visible=False
            self.pointeur.tour()
            self.etat = "grey"
            self.selected = False
            self.createur.kill_unite(self)
    
    def alerte(self, pas):
        if self.dommages>pas*(self.stats.regen+0.01)*self.taille*10:
            self.dommages-=pas*(self.stats.regen+0.1)*self.taille*10
        else:
            self.dommages=0
        unalerte=True
        if self.dommages>=self.taille*self.stats.vie_max/3:
            unalerte=False
            self.dommages-=pas*(self.stats.regen+0.1)*self.taille*20
            self.etat="red"
        if self.taille==0:
            unalerte=False
            self.etat="grey"
        if unalerte:
            self.etat = "white"
    
    def kill(self,i):
        self.createur.decort.append(self.groupe[i])
        self.createur.kill(self.groupe[i])

        
    def affiche(self):
        if self.toile.masqued[0]:
            self.toile.coords(self.corp, -1, -1, -1, -1)
            self.toile.coords(self.tete, -1, -1, -1, -1)
        else:
            self.toile.coords(self.corp, self.x+self.r, self.y+self.r, self.x-self.r, self.y-self.r)
            X = self.x+avix(self.r, self.d)
            Y = self.y+aviy(self.r, self.d)
            self.toile.coords(self.tete, X+(self.r*0.6), Y+(self.r*0.6), X-(self.r*0.6), Y-(self.r*0.6))
        if self.selected:
            r=(self.r*10/7)+self.stats.taille
            self.toile.coords(self.corp, self.x+r, self.y+r, self.x-r, self.y-r)