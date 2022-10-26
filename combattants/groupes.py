from keyboard import is_pressed
class Groupe:
    def __init__(self, toile, nom, joueur, color='grey'):
        self.dico = ['à', '&', '2', '"', "'", '(', '-', '7']
        self.toile = toile
        self.nom = str(nom)
        self.nom2 = self.dico[nom]
        self.color = color
        self.link = []
        self.taille = 0
        self.apparence = []
        self.texte = []
        self.joueur = joueur
    
    def add_unit(self, unit):
        for i in self.link:
            if i.groupe_up==self:
                i.groupe_up = None
            if i.groupe_down==self:
                i.groupe_down = None
        for i in self.apparence:
            self.toile.cnv.delete(i)
        for i in self.texte:
            self.toile.cnv.delete(i)
        self.link = unit[:]
        self.taille = len(unit)
        self.apparence = [self.toile.cnv.create_rectangle(0,0,0,0, fill=self.color) for _ in self.link]
        self.texte = [self.toile.cnv.create_text(0,0, text = self.nom) for _ in self.link]
    
    def pressed(self):
        if is_pressed(self.nom):
            if is_pressed('e'):
                self.add_unit(self.joueur.select)
            else:
                self.joueur.vide()
                self.joueur.ajoute_list(self.link)
    
    def tour(self):
        if self.taille == len(self.joueur.unit):
            for i, lien in enumerate(self.link):
                if lien.groupe_up==self:
                    lien.groupe_up = None
                if lien.groupe_down==self:
                    lien.groupe_down = None
                self.affiche_haut(lien, i)
        elif self.taille>0:
            for i, lien in enumerate(self.link):
                if lien.groupe_up==None:
                    lien.groupe_up = self
                    self.affiche_up(lien,i)
                elif lien.groupe_up==self:
                    pass
                elif lien.groupe_up.taille<self.taille:
                    lien.groupe_up = self
                    self.affiche_up(lien,i)
                elif lien.groupe_down==None:
                    lien.groupe_down = self
                    self.affiche_down(lien,i)
                elif lien.groupe_down==self:
                    pass
                elif lien.groupe_down.taille<self.taille:
                    lien.groupe_down = self
                    self.affiche_down(lien,i)
                else:
                    self.cache(i)
    
    def cache(self, i):
        self.toile.cnv.coords(self.apparence[i], -1,-1,-1,-1)
        self.toile.cnv.coords(self.texte[i], -1,-1)
    
    def affiche_up(self, lien, i):
        self.toile.cnv.coords(self.apparence[i], lien.carte.x-15, lien.carte.y-25, lien.carte.x+15, lien.carte.y-40)
        self.toile.cnv.coords(self.texte[i], lien.carte.x, lien.carte.y-32)
    
    def affiche_haut(self, lien, i):
        self.toile.cnv.coords(self.apparence[i], lien.carte.x-25, lien.carte.y-42, lien.carte.x+25, lien.carte.y-58)
        self.toile.cnv.coords(self.texte[i], lien.carte.x, lien.carte.y-49)
    
    def affiche_down(self, lien, i):
        self.toile.cnv.coords(self.apparence[i], lien.carte.x-15, lien.carte.y+25, lien.carte.x+15, lien.carte.y+38)
        self.toile.cnv.coords(self.texte[i], lien.carte.x, lien.carte.y+31)