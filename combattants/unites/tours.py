from combattants.unites.unite import*
from combattants.types.tours import Tour

class Unite_tour(Unite):
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', nb_model=1, formation = 'Garde'):
        super().__init__(toile, x, y, quad, quad_allie, quad_ennemi, createur, color = color, nb_model=nb_model, color_model = 'red', Type = Tour, nom='heros', formation = formation) 
