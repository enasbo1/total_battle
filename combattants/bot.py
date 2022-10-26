class Bot:
    def __init__(self, toile, troupes,color = 'white'):
        self.troupes = troupes
        self.color = color
        self.souris = toile.souris
        self.toile = toile
        self.select = None
        self.taille_plgrosse_unite = 10
    
    def init(self, divinite, quad_unit, quad_unit_ennemi, unit, unit_adv):
        self.divinite=divinite
        self.unit = unit
        self.unit_adv = unit_adv
        self.quad_unit = quad_unit
        self.quad_unit_adv = quad_unit_ennemi
    
    def tour(self):
        for i in self.unit:
            plproche, dist, dir = self.quad_unit_adv.close(i, 2000)
            if plproche!=None:
                i.cible = plproche
            