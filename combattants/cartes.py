from turtle import width

class Carte:
    def __init__(self, toile, x, y, unite, image='None'):
        self.x = x
        self.y = y
        self.toile = toile
        self.unite = unite
        self.unite.carte = self
        self.select = False
        self.box = ['rect', x-20, y-29, x+20, y+29]
        self.cadre = self.toile.cnv.create_rectangle(x-20, y-29, x+20, y+29,fill='grey')
        self.apparence = self.toile.cnv.create_image(x, y,image=image)
        self.nombre = self.toile.cnv.create_text(x, y+20,text=str(self.unite.taille))
        self.etat = self.toile.cnv.create_rectangle(x-15,y-25,x+15,y-20)
    
    def tour(self):
        self.unite.selected = self.select
        if self.select:
            self.toile.cnv.itemconfig(self.cadre, fill= self.unite.color_model)
            self.toile.cnv.itemconfig(self.unite.pointeur.marque, outline= self.unite.color_model)
        else:
            self.toile.cnv.itemconfig(self.cadre, fill= 'grey')
            self.toile.cnv.itemconfig(self.unite.pointeur.marque, outline= self.unite.color)
        self.toile.cnv.itemconfig(self.nombre, text=str(self.unite.taille))