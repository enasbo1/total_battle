from combattants.types.soldat import Stats_soldat
from magasin.produit import *
import magasin.carte as mag
from combattants.unites.noeux import*
from combattants.types.noeux import*


class Marchant:
    def __init__(self, toile):
        self.toile = toile
        self.souris = self.toile.souris
        self.argent = 300
        self.choix = {'aspirant':(25, Unite_aspirants, Stats_aspirants),'soldats':(50,Unite_soldats, Stats_soldat()), 'cavalier':(50,Unite_cavalier, Stats_cavalier()), 'piquiers':(50,Unite_piquier, Stats_piquier()), 'archet':(50,Unite_Archet, Stats_archets()),'elite':(50,Unite_elite, Stats_elite()), 'heros':(75,Unite_heros, Stats_heros()), 'tireur_monte':(75,Unite_tireur_monte, Stats_monte())}
        self.image = PhotoImage(file = 'images\gold.png')
        self.img_table = PhotoImage(file = "images\Table.png")
        self.table = self.toile.cnv.create_image(toile.x_cam/2, 260, image=self.img_table)
        self.tableau = self.toile.cnv.create_rectangle((self.toile.x_cam-800)/2, self.toile.y_cam-130, (self.toile.x_cam+800)/2, self.toile.y_cam-5, fill ='gold')
        self.barre = self.toile.cnv.create_image(50,30, image=self.image)
        self.money = self.toile.cnv.create_text(40,30, text=self.argent)
        if (len(self.choix)//((toile.x_cam-20)/50))>=1:
                    x = 155
        else:
            x = int((toile.x_cam-100*(len(self.choix)%((toile.x_cam-20)/50)))/2)+50
        self.articles = [Produit(self, toile, x+100*(i%((toile.x_cam-20)/50)), 255+140*(i//((toile.x_cam-20)/50)), self.choix[j][2], nom = j, prix = self.choix[j][0]) for i,j in enumerate(self.choix)]
        self.unite = []
        self.carte_unite = []
    
    def tour(self):
        self.toile.cnv.itemconfig(self.money, text=self.argent)
        X=int((self.toile.x_cam/2)-(len(self.unite)*25))
        Y=int(self.toile.y_cam-90)
        for i, carte in enumerate(self.carte_unite):
            carte.tour(X+(i*50),Y,i)
        if self.toile.stats:
            self.toile.stats = False
            souris_box = ['point', self.souris.x_ecrant, self.souris.y_ecrant]
            for i in self.articles:
                i.buy(souris_box)
            for i in self.carte_unite:
                i.buy(souris_box)
    
    def retire(self, i):
        del self.unite[i]
        del self.carte_unite[i]
        X=int((self.toile.x_cam/2)-(len(self.unite)*25))
        Y=int(self.toile.y_cam-90)
        for i, carte in enumerate(self.carte_unite):
            carte.tour(X+(i*50),Y,i)
        for i in self.articles:
            i.tour()
        
    def ajoute(self, produit):
        X=int((self.toile.x_cam/2)-((len(self.carte_unite)+1)*25))
        Y=int(self.toile.y_cam-90)
        i = len(self.carte_unite)
        self.carte_unite.append(mag.Carte(self, self.toile, X+(i*50),Y,i, nom = produit.nom, prix=produit.prix))
        self.unite.append(self.choix[produit.nom][1])