from tkinter import PhotoImage
from backwork.contact import hitbox
from combattants.unites.unite import Unite

class Carte:
    def __init__(self,vendeur, toile, x, y, i, nom='None', prix=50):
        self.i = i
        self.toile = toile
        self.vendeur = vendeur
        self.nom = nom
        self.image = PhotoImage(file = "images/"+self.nom+".png")
        self.money  = PhotoImage(file = "images/money.png")
        self.prix = prix
        self.box = ['rect', x-20, y-29, x+20, y+29]
        self.cadre = self.toile.cnv.create_rectangle(x-20, y-29, x+20, y+29,fill='grey')
        self.apparence = self.toile.cnv.create_image(x, y,image=self.image)
        self.solde = self.toile.cnv.create_image(x, y+20,image=self.money)
        self.nombre = self.toile.cnv.create_text(x-3, y+20,text=str(self.prix))
    
    def buy(self, souris_box):
        if hitbox(self.box, souris_box):
            self.vendeur.argent+=self.prix
            self.cache()
            self.vendeur.retire(self.i)
    
    def tour(self, x, y, i):
        self.i = i
        self.box[1]=x-20
        self.box[2]=y-29
        self.box[3]=x+20
        self.box[4]=y+29
        self.toile.cnv.coords(self.cadre, x-20, y-29, x+20, y+29)
        self.toile.cnv.coords(self.apparence, x, y)
        self.toile.cnv.coords(self.solde, x , y+20)
        self.toile.cnv.coords(self.nombre, x-3, y+20)
        
    def cache(self):
        self.toile.cnv.delete(self.cadre)
        self.toile.cnv.delete(self.apparence)
        self.toile.cnv.delete(self.solde)
        self.toile.cnv.delete(self.nombre)

        