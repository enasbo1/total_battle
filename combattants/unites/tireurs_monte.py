from combattants.unites.unite import*
from combattants.types.tireur_monte import Stats_monte, Tireur_monte
class Unite_tireur_monte(Unite):
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', nb_model=30, formation = 'Garde'):
        super().__init__(toile, x, y, quad, quad_allie, quad_ennemi, createur, color = color, nb_model=nb_model, color_model = 'RoyalBlue1', Type = Tireur_monte, Stats=Stats_monte, nom='tireur_monte', formation = formation) 
        self.strategies = ['Groupe','Cible', 'Garde', 'Dispertion', 'Regroupe']
        self.formations = {'Groupe':self.groupee, 'Cible': self.portee, 'Garde': self.groupee, 'Dispertion': self.disperse, 'Regroupe': self.disperse}
    
    def portee(self):
        distance = self.groupe[0].distance[3]**2
        di = disrap(self.x, self.y, self.pointeur.x, self.pointeur.y)
        
        if di<distance:
            self.deplacement = False
            self.vitesse = self.deplacements[0]
        if self.deplacement:
            X=0
            Y=0
            for i in self.groupe:
                X+=i.x
                Y+=i.y
            self.x=X/self.taille
            self.y=Y/self.taille