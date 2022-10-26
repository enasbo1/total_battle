from backwork.direction import*

class Fleche:
    def __init__(self, toile, proprio, quad):
        self.x=0
        self.y=0
        self.toile = toile
        self.proprio = proprio
        self.quad = quad
        self.apparence = None
    
    def place(self, x1, y1, x2, y2):
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.x = (x1+x2)/2
        self.y = (y1+y2)/2
        
    def color(self, color):
        self.toile.cnv.itemconfig(self.apparence, fill=color)
    
    def tir(self, direct, dist, degats):
        self.x1=self.proprio.x+avix(dist, direct)
        self.y1=self.proprio.y+aviy(dist, direct)
        self.x2=self.x1+avix(6, direct)
        self.y2=self.y1+aviy(6, direct)
        self.x = (self.x1+self.x2)/2
        self.y = (self.y1+self.y2)/2
        plproche, dist, dir = self.quad.close(self, 20)
        if plproche!=None:
            if self.contact(plproche, direct) and dist<plproche.taille+2:
                if plproche.shoted(self.proprio,degats):
                    self.color('red')
                else:
                    self.color('grey')
            else:
                self.color('black')
    
    def contact(self, item, d):
        x1=avix(1,d+pi/2)
        y1=aviy(1,d+pi/2)
        x2=item.x-self.x
        y2=item.y-self.y
        return abs(x1*x2+y1*y2)<item.taille+2
    
    def aff(self):
        if self.apparence==None:
             self.apparence=self.toile.cnv.create_line(0,0,0,0, fill=self.proprio.unite.color_model, width=2)
        self.toile.coords(self.apparence, self.x1, self.y1, self.x2, self.y2)
    
    def cache(self):
        self.toile.cnv.coords(self.apparence, -1, -1, -1, -1)