from combattants.unites.unite import*
from combattants.types.elite import Elite, Stats_elite

class Unite_elite(Unite):
    def __init__(self,toile, x, y, quad, quad_allie, quad_ennemi, createur, color = 'white', nb_model=7, formation = 'Garde'):
        super().__init__(toile, x, y, quad, quad_allie, quad_ennemi, createur, color = color, nb_model=nb_model, color_model = 'magenta4', Type = Elite, Stats=Stats_elite, nom='elite', formation = formation) 
