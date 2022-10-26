from combattants.unites.unite import*
from combattants.types.heros import Heros, Stats_heros

class Unite_heros(Unite):
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', nb_model=1, formation = 'Groupe'):
        super().__init__(toile, x, y, quad, quad_allie, quad_ennemi, createur, color = color, nb_model=nb_model, color_model = 'darkslategrey', Type = Heros, Stats=Stats_heros, nom='heros', formation = formation) 
