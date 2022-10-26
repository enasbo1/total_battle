from backwork.direction import*
from random import randint

class Acteur: 
    # moral[
    def choisir(self,pas):
        self.choix[self.unite.formation](pas)
        if self.peur[0]>self.peur[1]:
            self.deplacement = self.fuir
        elif self.colere[0]>self.colere[1]:
            self.deplacement = self.dispertion
    #]
    
    # formation? + buff de formation [
    def groupee(self, distance):
        self.deplacement=self.rattrappe
        di = dir(self.unite.x, self.unite.y, self.unite.d, self.x, self.y)
        self.coo_unite  = (distance, dir(self.x, self.y, 0, self.unite.x, self.unite.y))
        if abs(di)>pi/2:
            self.unite.retardataire = True
            self.avancer = self.courir
        elif abs(di)<pi/3:
            self.avancer = self.marcher
        else:
            self.avancer = self.courir
        
    def groupea(self, pas):
        distance = disrap(self.x, self.y, self.unite.x, self.unite.y)
        if distance>self.unite.zone:
            self.groupee(distance)
        else:
            self.colere[1] += self.colere[3]*0.2*self.dicipline/10
            self.peur[1] += self.peur[3]*0.2*self.dicipline/10
            self.peur[0] -= self.peur[2]*0.5*self.dicipline*pas/10
            self.colere[0] -= self.colere[2]*0.5*self.dicipline*pas/10
            self.corp_a_corp[3]+=int(self.corp_a_corp[4])
            self.charge[4]+=int(self.charge[5])
            self.defence[0]-=int(self.defence[0]*0.3)
            self.pic[0]-=int(self.pic[0]*0.3)
            if self.uncontact:
                if self.charge[0]+(pas*self.charge[2]/20)<self.charge[1]:
                    self.charge[0]+=pas*self.charge[2]/20
                else:
                    self.charge[0]=self.charge[1]
            self.avancer = self.vitesses[self.unite.vitesse]
            self.deplacement = self.formation[self.unite.formation]
            if self.unite.vitesse=='Arret':
                self.defence[0]=int(self.defence[0]*1.5**(self.dicipline/10))
                self.pic[0]=int(self.pic[0]*1.5**(self.dicipline/10))
                 
    def grouped(self, pas):
        distance = disrap(self.x, self.y, self.unite.x, self.unite.y)
        if distance>self.unite.zone:
            self.groupee(distance)
        else:
            self.corp_a_corp[3]-=int(self.corp_a_corp[4]*0.6)
            self.charge[4]-=int(self.charge[5]*0.8)
            self.defence[0]+=int(self.defence[1])
            self.pic[0]+=int(self.pic[2])
            self.pic[1]+=int(self.pic[3]*0.5)
            self.colere[1] += self.colere[3]*0.2*self.dicipline/10
            self.peur[1] += self.peur[3]*0.2*self.dicipline/10
            self.peur[0] -= self.peur[2]*0.5*self.dicipline*pas/10
            self.colere[0] -= self.colere[2]*0.5*self.dicipline*pas/10
            self.avancer = self.vitesses[self.unite.vitesse]
            self.deplacement = self.formation[self.unite.formation]
            if self.unite.vitesse=='Arret':
                self.defence[0]=int(self.defence[0]*1.5**(self.dicipline/10))
                self.pic[0]=int(self.pic[0]*1.5**(self.dicipline/10))
      
    def disperse(self, pas):
        self.avancer = self.vitesses[self.unite.vitesse]
        self.deplacement = self.formation[self.unite.formation]
    #]
    
    #comportements[    
    def boid(self, pas):
        plproche, dist, direc = self.plproche
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            if dist<10:
                e = 2
                di=direc+pi
            elif dist>25:
                e = 1
                di=direc
            else:
                e = 1
                di = plproche.d
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
            if not self.tournaret[0] or abs(rot(-di, self.d))<self.tournaret[1]:
                self.avancer(pas)

        else:
            self.avancer(pas)
    
    def no_formation(self, pas):
        plproche, dist, direc = self.quad_ennemi.close(self, self.vue)
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            if dist<self.corp_a_corp[2]:
                self.ennemi = (plproche, dist, direc)
                self.avancer = self.courir
                self.attaque(pas)
            else:
                self.au_pas(pas)
        else:
            self.au_pas(pas)
    
    def garde(self, pas):
        plproche, dist, direc = self.quad_ennemi.close(self, self.vue)
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            if dist<self.corp_a_corp[2]:
                self.ennemi = (plproche, dist, direc)
                self.combat(pas)
            elif self.portee(dist):
                self.tir(direc, dist, pas)
            else:
                self.au_pas(pas)
        else:
            self.au_pas(pas)
    
    def dispertion(self, pas):
        plproche, dist, direc = self.quad_ennemi.close(self, self.vue)
        self.avancer = self.courir
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            self.ennemi = (plproche, dist, direc)
            if dist<self.corp_a_corp[2]:
                self.attaque(pas)
            else:
                plproche, dist, direc = self.cont_alliers.proche(self, self.vue)
                if plproche!=None:
                    dist -= self.taille+plproche.taille+1
                    if dist<5:
                        self.equart(direc, pas)
                    else:
                        self.attaque(pas)
                else:
                    self.attaque(pas)
        else:
            plproche, dist, direc = self.cont_alliers.proche(self, self.vue)
            if plproche!=None:
                dist -= self.taille+plproche.taille+1
                if dist<5:
                    self.equart(direc, pas)
    
    def fuir(self, pas):
        plproche, dist, direc = self.quad_ennemi.close(self, self.vue)
        self.avancer = self.courir
        if plproche!=None and dist<self.vue:
            self.d = tourne(self.d, direc+pi, e*pi*pas*self.magnabilite/100)
        self.avancer(pas)
    
    def regroupe(self, pas):
        plproche, dist, direc = self.plproche
        avance = False
        self.tapper(pas)
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            if dist<2:
                e = 1
                di = direc+pi
                avance=True
            else:
                di =  dir(self.x, self.y, 0, self.unite.cible.x, self.unite.cible.y)
                e = 1
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
            if abs(rot(-di, self.d))<self.tournaret[1] or avance:
                self.avancer(pas)
        else:
            di =  dir(self.x, self.y, 0, self.unite.cible.x, self.unite.cible.y)
            e = 1
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
            if abs(rot(-di, self.d))<self.tournaret[1]:
                self.avancer(pas)
    
    def rattrappe(self, pas):
        plproche, dist, direc = self.plproche
        avance = False
        self.tapper(pas)
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            if self.coo_unite[0]!=None:
                if dist<2:
                    e = 1
                    di = direc+pi
                    avance=True
                else:
                    di =  self.coo_unite[1]
                    e = 1
                self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
                if abs(rot(-di, self.d))<self.tournaret[1] or avance:
                    self.avancer(pas)
        else:
            di =  self.coo_unite[1]
            e = 1
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
            if abs(rot(-di, self.d))<self.tournaret[1]:
                self.avancer(pas)
    #]
    
    # Modes de combats[
    def attaque(self, pas):
        if not self.stun[0]:
            plproche, dist, direc = self.ennemi
            self.technique(self.ennemi)
            if dist<self.corp_a_corp[1] and abs(rot(-self.d, direc))<pi/3:
                plproche.chargee(self.charge[0]*self.charge[3],self)
            di = direc
            e = 1
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
            if not self.tournaret[0] or abs(rot(-di, self.d))<self.tournaret[2]:
                self.avancer(pas)
                
    def combat(self, pas):
        if not self.stun[0]:
            plproche, dist, direc = self.ennemi
            di = direc
            e = 1
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
            self.technique(self.ennemi)
            if dist<self.corp_a_corp[1] and abs(rot(-self.d, direc))<pi/3:
                plproche.chargee(self.charge[0]*self.charge[3],self)
            else:
                if not self.tournaret[0] or abs(rot(-di, self.d))<self.tournaret[2]:
                    self.avancer(pas)
    
    def tapper(self, pas):
        if not self.stun[0]:
            plproche, dist, direc = self.quad_ennemi.proche(self, self.corp_a_corp[1]+10)
            if plproche!=None:
                self.technique(self.ennemi)
    #]
    
    #attaques[
    def shomen(self, cible): #fonc => technique
        plproche, dist, direc = cible
        if self.coldown<=0:
            if dist<self.corp_a_corp[1] and abs(rot(-self.d, direc))<pi/3:
                pare = plproche.slashed(self.corp_a_corp[0], self, 2)
                self.coldown = 2
                if pare:
                    self.toile.cnv.itemconfig(self.arme, fill = 'grey')
                else:
                    self.toile.cnv.itemconfig(self.arme, fill = 'red')
    
    def tir(self, direc, dist, pas):
        if self.distance[0]<=0 and self.distance[2]<=dist<self.distance[3]:
            precision = pi/(4*self.distance[4])
            direction = self.d+(randint(-100,100)*precision/100)
            distance = int(100/self.distance[4])
            distance = randint(-distance, distance)
            distance += 100
            distance = distance/100
            if abs(rot(-self.d, direc))<precision:
                self.distance[0]=self.distance[1]
                self.carquoi[0]-=1
                self.fleche.tir(direction, dist*distance, self.distance[5])
            di = direc
            e = 1
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
    #]
    
    #vitesses de deplacement: fonc => vitesse[
    def marcher(self,pas):
        self.x+=avix((self.vitesse+self.charge[0])*pas*0.8, self.d)
        self.y+=aviy((self.vitesse+self.charge[0])*pas*0.8, self.d)
    
    def arret(self, pas):
        self.charge[0]=0
    
    def courir(self, pas):
        self.x+=avix((self.vitesse+self.charge[0])*pas, self.d)
        self.y+=aviy((self.vitesse+self.charge[0])*pas, self.d)
    #]
    
    # conditions[
    def portee(self, dist):
        return self.move_portee(dist) and self.avancer==self.arret
    
    def move_portee(self, dist):
        return self.distance[5]>0 and self.carquoi[0]>0 and self.distance[2]<dist<self.distance[3]
    #]
    
    #deplacements recurents[
    def equart(self, direc, pas):
        self.x+=avix(-self.vitesse*pas/10, direc)
        self.y+=aviy(-self.vitesse*pas/10, direc)
    
    def au_pas(self, pas):
        plproche, dist, direc = self.cont_alliers.proche(self, 25)
        if plproche!=None:
            dist -= self.taille+plproche.taille+1
            di = dir(self.unite.x, self.unite.y, 0,self.x, self.y)
            self.equart(di, pas/3)
            if dist<5:
                self.equart(direc, pas)
            e = 1
            di = self.unite.d
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
            if not self.tournaret[0] or abs(rot(-di, self.d))<self.tournaret[2]:
                self.avancer(pas)
        else:
            di = self.unite.d
            e = 1
            self.d = tourne(self.d, di, e*pi*pas*self.magnabilite/100)
            if not self.tournaret[0] or abs(rot(-di, self.d))<self.tournaret[2]:
                self.avancer(pas)
    #]