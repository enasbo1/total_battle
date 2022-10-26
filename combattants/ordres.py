from tkinter import PhotoImage
class Ordre:
    def __init__(self, toile, x, y, joueur, nom='None'):
        self.x = x
        self.y = y
        self.toile = toile
        self.unites = []
        self.joueur = joueur
        self.nom = nom
        self.select = False
        self.coo = x-20, y-20, x+20, y+20
        self.image = PhotoImage(file = "images/"+self.nom+".png")
        self.box = ['rect', self.coo[0], self.coo[1], self.coo[2], self.coo[3]]
        self.cadre = self.toile.cnv.create_rectangle(self.coo,fill='grey')
        self.apparence = self.toile.cnv.create_image(x, y,image=self.image)
    
    def ordonne(self):
        if self.select:
            for i in self.unites:
                i.formation=self.nom
    
    def compte(self):
        self.unites = self.joueur.select
        ret = True
        for uni in self.unites:
            pres = False
            for i in uni.strategies:
                pres = pres or i==self.nom
            ret = ret and pres
        self.select = ret and self.unites!=[]
        return int(ret)
    
    def choisi(self):
        ret = True
        for uni in self.unites:
            ret = ret and uni.formation==self.nom
        return ret
    
    def color(self):
        ret = self.unites[0].color_model
        unie = True
        for uni in self.unites:
            if unie:
                if uni.color_model!=ret:
                    unie = False
                    ret = self.joueur.color
        return ret
    
    def tour(self,nb, i):
        if self.select:
            X=int((self.joueur.toile.x_cam/2)-(nb*30))
            Y=int(self.joueur.toile.y_cam-30)
            x0 = X+(i*60)
            self.coo = x0-20, Y-20, x0+20, Y+20
            self.x = x0
            self.y = Y
            self.box = ['rect', self.coo[0], self.coo[1], self.coo[2], self.coo[3]]
            self.toile.cnv.coords(self.cadre, self.coo)
            self.toile.cnv.coords(self.apparence, self.x, self.y)
            if self.choisi():
                self.toile.cnv.itemconfig(self.cadre, fill= self.color())
            else:
                self.toile.cnv.itemconfig(self.cadre, fill= 'grey')
            return i+1
        else:
            self.toile.cnv.coords(self.cadre, -1, -1, -1, -1)
            self.toile.cnv.coords(self.apparence, -50,-50)
            return i
