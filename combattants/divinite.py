from combattants.types.noeux import*
from backwork.quad import*
from affichage.affiche import*
from combattants.unites.noeux import*
from combattants.rocher import Rocher

class Divin:
    def __init__(self, toile, joueur1, joueur2):
        self.toile=toile
        self.joueurs = [joueur1, joueur2]
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.quad = Quad(None, 0, 0, 0, toile.x_terrain, toile.y_terrain)
        self.quad_1 = Quad(None, 0, 0, 0, toile.x_terrain, toile.y_terrain, donnee=lambda x: x.local1)
        self.quad_2 = Quad(None, 0, 0, 0, toile.x_terrain, toile.y_terrain,  donnee=lambda x: x.local1)
        self.quad_unit_1 =  Quad(None, 0, 0, 0, toile.x_terrain, toile.y_terrain)
        self.quad_unit_2 = Quad(None, 0, 0, 0, toile.x_terrain, toile.y_terrain)
        self.topographie = [Rocher(toile, self.quad, randint(100, self.toile.x_terrain-100), randint(100, self.toile.y_terrain-100), self.toile.x_cam, self.toile.y_cam) for i in range(40)]
        nb = len(joueur1.troupes)/2
        self.unite_equipe_1 = [j(toile, (i-nb)*100+toile.x_terrain/4, -(i-nb)*100+toile.y_terrain/4, self.quad, self.quad_1, self.quad_2, self, color = joueur1.color) for i, j in enumerate(joueur1.troupes)]
        self.equipe_1 = []
        for i in self.unite_equipe_1:
            self.equipe_1=self.equipe_1+i.groupe
        nb = len(joueur2.troupes)/2
        self.unite_equipe_2 = [j(toile, (i-nb)*100+(3*toile.y_terrain/4), -(i-nb)*100+(3*toile.y_terrain/4), self.quad, self.quad_2, self.quad_1, self, color = joueur2.color) for i, j in enumerate(joueur2.troupes)]
        self.equipe_2 = []
        for i in self.unite_equipe_2:
            self.equipe_2=self.equipe_2+i.groupe
        self.unites = self.unite_equipe_1+self.unite_equipe_2
        self.population = self.equipe_1+self.equipe_2+self.topographie
        self.joueur1.init(self, self.quad_unit_1, self.quad_unit_2, self.unite_equipe_1, self.unite_equipe_2)
        self.joueur2.init(self, self.quad_unit_2, self.quad_unit_1, self.unite_equipe_2, self.unite_equipe_1)
        self.decort = []
        
    
    def tour(self, pas):
        for i in self.equipe_1:
            self.quad.insert(i)
            self.quad_1.insert(i)
        for i in self.equipe_2:
            self.quad.insert(i)
            self.quad_2.insert(i)
        for i in self.topographie:
            self.quad.insert(i)
        for i in self.unite_equipe_1:
            self.quad_unit_1.insert(i)
        for i in self.unite_equipe_2:
            self.quad_unit_2.insert(i)
        
        for i in self.topographie:
            i.tour()
        for i in self.joueurs:
            i.tour()
        for i in self.unites:
            i.tour(pas)
        for i in self.decort:
            i.tour(pas)
        self.quad.delete()
        self.quad_1.delete()
        self.quad_2.delete()
        self.quad_unit_1.delete()
        self.quad_unit_2.delete()
    
    def kill(self, item):
        for i,j in enumerate(self.population):
            if j==item:
                del(self.population[i])
        for i,j in enumerate(self.equipe_1):
            if j==item:
                del(self.equipe_1[i])
        for i,j in enumerate(self.equipe_2):
            if j==item:
                del(self.equipe_2[i])
    
    def kill_unite(self, item):
        for i,j in enumerate(self.unites):
            if j==item:
                del(self.unites[i])
        for i,j in enumerate(self.unite_equipe_1):
            if j==item:
                del(self.unite_equipe_1[i])
        for i,j in enumerate(self.unite_equipe_2):
            if j==item:
                del(self.unite_equipe_2[i])
            