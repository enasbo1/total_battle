from combattants.unites.unite import*
from combattants.types.cavalier import Cavalier, Stats_cavalier
class Unite_cavalier(Unite):
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', nb_model=30, formation = 'Garde'):
        super().__init__(toile, x, y, quad, quad_allie, quad_ennemi, createur, color = color, nb_model=nb_model, color_model = 'brown', Type = Cavalier,Stats=Stats_cavalier, nom='cavalier', formation = formation) 
