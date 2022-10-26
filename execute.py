# -*- coding: utf-8 -*-

from combattants.divinite import *
from time import*
from combattants.joueur import *
from combattants.bot import *
from magasin.menu import menu
from magasin.produit import Produit

x_terrain=2000
y_terrain=2000
x_cam = 1522
y_cam = 850
vitesse = 4
toile = Toile(x_cam, y_cam, title='boid')
troupes1, troupes2 = menu(toile)
toile.charge(x_terrain, y_terrain)
joueur = Joueur(toile, troupes1, color = 'grey80')
bot = Bot(toile,troupes2, color="white")
divinite = Divin(toile, joueur, bot)

fps=toile.cnv.create_text(x_cam/2, 20, text='0')
temps = 0
unlance= True
t=time()
while toile.cont:
    T=time()
    if (T-t)>(0.1)*vitesse:
        temps = 0.1
        pas = temps*vitesse
        toile.cnv.itemconfig(fps, text='OOO')
    elif T-t>0.01:
        temps = (T-t)
        pas = temps*vitesse
        toile.cnv.itemconfig(fps, text=str((100//(T-t))/100))
    else:
        sleep(0.01-(T-t))
        temps = 0.01
        pas = temps*vitesse
        toile.cnv.itemconfig(fps, text='+++')
    if unlance:
        pas=0
        if is_pressed('l'):
            unlance=False
    t=time()
    toile.moove(temps)
    divinite.tour(pas)
    toile.update()
toile.cnv.update()
toile.fenetre.destroy()