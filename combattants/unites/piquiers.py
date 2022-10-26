from combattants.unites.unite import*
from combattants.types.piquiers import Piquiers, Stats_piquier


class Unite_piquier(Unite):
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', nb_model=40, formation = 'Garde'):
        super().__init__(toile, x, y, quad, quad_allie, quad_ennemi, createur, color = color, nb_model=nb_model,Type = Piquiers, Stats=Stats_piquier, color_model = 'yellow4', nom='piquiers', formation=formation)