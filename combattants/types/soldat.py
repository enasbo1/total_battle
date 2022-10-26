from combattants.types.classifi import*

class Soldat(Persoide):
    def __init__(self, toile, quad, quad_allier, quad_enemis, x, y, unite = None):
        super().__init__(toile, quad, quad_allier, quad_enemis, x, y, unite = unite)
        self.reset_statistique()
        
    def reset_statistique(self):
        self.stats_de_base()
        self.posture = [0,30, 2, 1] #domages, max, regen, contre
        self.competence.append('bouclier')
        self.competence.append('push')

    def shoted(self, item, damage):
        if self.uncontact:
            if randint(0,2)==2 or abs(rot(-self.d, dir(self.x, self.y, 0, item.x, item.y)))>pi/4 or self.stun[0]:
                if item.unite.color==self.unite.color:
                    damage=damage/2
                self.aie(damage)
                return True
            else:
                self.posture[0]-=damage
                return False
        else:
            if item.unite.color==self.unite.color:
                damage=damage/2
            self.aie(damage)
            return True

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

class Stats_soldat(Soldat):
    def __init__(self):
        self.reset_statistique()