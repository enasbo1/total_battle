from backwork.direction import*

class Pointeur:
    def __init__(self,toile, unite):
        self.x=unite.x
        self.y=unite.y
        self.xa = self.x
        self.ya = self.y
        self.d = unite.d
        self.toile = toile
        self.unite = unite
        self.marque = toile.cnv.create_arc(0,0,0,0,start=60, extent = 360, width = 2, outline=unite.color)
        self.visible=True
        self.oriente = False
    
    def tour(self):
        if self.visible and (not self.toile.masqued[0] or self.unite.selected):
            if self.unite.selected:
                r = self.unite.r*10/7
            else:
                r = self.unite.r*0.5
            if self.unite.cible!=self:
                self.x=self.unite.cible.x
                self.y=self.unite.cible.y
                self.d = self.unite.d
            if self.oriente:
                self.toile.cnv.itemconfig(self.marque, start=self.degre1(), extent = 60)
                self.xa = self.x+avix(2*r/3, self.d)
                self.ya = self.y+aviy(2*r/3, self.d)
            else:
                self.toile.cnv.itemconfig(self.marque, start=self.degre(), extent = 359)
                self.xa = self.x
                self.ya = self.y  
            
            self.toile.coords(self.marque, self.xa+r,self.ya+r, self.xa-r, self.ya-r)
        else:
            self.toile.cnv.coords(self.marque, -1,-1, -1, -1)
            
    def place(self, item):
        self.x = item.x
        self.y = item.y
        self.oriente = False
        
    def deplace(self, x, y):
        self.x = self.unite.x+x
        self.y = self.unite.y+y
        self.oriente = False
        
    def degre1(self):
        return (int(-180*self.d/pi)+150)%360
    
    def degre(self):
        return (int(-180*self.d/pi))%360