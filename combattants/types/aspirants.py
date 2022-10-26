from combattants.types.classifi import*

class Aspirant(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.reset_statistique()
        
    def reset_statistique(self):
        self.stats_de_base()
        self.vie = 150
        self.vie_max = 100
        self.regen = 0.1
        self.posture = [0,30, 2, 1] #domages, max, regen, contre
        self.defence = [6, 6]
        self.competence.append('push')
    
    def create_affichage(self):
        self.corp = self.toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill=self.unite.color)
        self.arme = self.toile.cnv.create_line(0,0,0,0, fill=self.unite.color_model, width=3)

    def affiche(self, pas):
        x1 = self.x + avix(6, self.d+pi/2)
        y1 = self.y + aviy(6, self.d+pi/2)
        x2 = x1 + avix(8, self.d+pi/6)
        y2 = y1 + aviy(8, self.d+pi/6)
        self.toile.coords(self.corp, int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5)
        self.toile.coords(self.arme, x1, y1, x2, y2)
        
    def aff_mort(self):
        self.toile.coords(self.corp, self.x+4, self.y+4, self.x-4, self.y-4)
        self.toile.coords(self.arme, self.x+4, self.y-4, self.x+5, self.y+4)
    
    def cache(self):
        self.toile.cnv.coords(self.corp, -1, -1, -1, -1)
        self.toile.cnv.coords(self.arme, -1, -1, -1, -1)
        
    def shomen(self, cible):
        plproche, dist, direc = cible
        if self.coldown<=0:
            if dist<self.corp_a_corp[1] and abs(rot(-self.d, direc))<pi/3:
                plproche.x+=avix(1, self.unite.d)
                plproche.y+=aviy(1, self.unite.d)
                pare = plproche.slashed(self.corp_a_corp[0], self, 2)
                self.coldown = 2
                if pare:
                    self.toile.cnv.itemconfig(self.arme, fill = 'grey')
                else:
                    self.toile.cnv.itemconfig(self.arme, fill = 'red')

class Stats_aspirants(Aspirant):
    def __init__(self):
        self.reset_statistique()