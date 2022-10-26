from magasin.produit import Produit
from magasin.vendeur import Marchant
from combattants.divinite import *
from combattants.joueur import *
from combattants.bot import *
from time import*

def menu(toile):
    marchant = Marchant(toile)
    while not is_pressed(' ') and toile.cont:
        marchant.tour()
        toile.update()
    return marchant.unite, [Unite_cavalier, Unite_soldats, Unite_piquier, Unite_elite, Unite_heros, Unite_Archet, Unite_cavalier]
#[Unite_tour][Unite_cavalier, Unite_soldats, Unite_piquier, Unite_elite, Unite_heros, Unite_Archet, Unite_cavalier]
