from tkinter import PhotoImage
from backwork.contact import hitbox
from combattants.unites.unite import Unite

class Produit:
    def __init__(self,vendeur, toile, x, y, statistique, nom='None', prix=50):
        self.x = x
        self.y = y
        self.statistique = statistique
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
        if self.vendeur.argent>=self.prix:
            if hitbox(self.box, souris_box):
                self.vendeur.argent-=self.prix
                self.vendeur.ajoute(self)
        if self.vendeur.argent<self.prix:
            self.toile.cnv.itemconfig(self.cadre, fill = 'white')
            
    def tour(self):
        if self.vendeur.argent>=self.prix:
             self.toile.cnv.itemconfig(self.cadre, fill = 'grey')