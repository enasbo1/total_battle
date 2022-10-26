from combattants.unites.unite import*
from combattants.types.aspirants import Aspirant, Stats_aspirants

class Unite_aspirants(Unite):
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', nb_model=25, formation = 'Garde'):
        super().__init__(toile, x, y, quad, quad_allie, quad_ennemi, createur, color = color, Type=Aspirant,Stats=Stats_aspirants, nb_model=nb_model, nom="aspirant", color_model = 'grey20', formation = formation)
