from combattants.unites.unite import*
from combattants.types.soldat import Soldat, Stats_soldat

class Unite_soldats(Unite):
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', nb_model=40, formation = 'Garde'):
        super().__init__(toile, x, y, quad, quad_allie, quad_ennemi, createur, color = color, Type=Soldat,Stats=Stats_soldat, nb_model=nb_model, color_model = 'black', formation = formation)
