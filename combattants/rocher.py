from random import randint
from backwork.direction import*

class Rocher:
    def __init__(self, toile, quad, x , y, ecr_x, ecr_y):
        self.toile = toile
        self.x = x
        self.y = y
        self.ecr_x = ecr_x
        self.ecr_y = ecr_y
        self.taille = int(sqrt(randint(81,256)))
        self.corp = self.toile.cnv.create_oval(0,0,0,0, fill="grey")
        self.quad = quad
        self.cont = self.quad
        self.deplacable = False
    
    def localise(self, cont):
        pass
    
    def shoted(self, item, damage):
        return False

    def slashed(self, degats, acteur, pas):
        return False
    
    def tour(self):
        proxi = self.quad.proxi(self, self.taille+10)
        for i in proxi:
            dist = disrap(i.x,i.y, self.x, self.y)
            if dist<(self.taille+i.taille+1)**2:
                d = dir(self.x, self.y, 0, i.x, i.y)
                dist = (self.taille+i.taille+1)-sqrt(dist)
                i.x+=avix(dist, d)
                i.y+=aviy(dist, d)
        self.toile.coords(self.corp, self.x-self.taille, self.y-self.taille, self.x+self.taille, self.y+self.taille )
                