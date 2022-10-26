from turtle import width
from backwork.contact import*

class Quad:
    def __init__(self, pere, a, b, level, x, y, donnee = lambda x : x.localise):
        self.pere = pere
        self.x = a
        self.y = b
        self.level = level
        self.localise = donnee
        self.L = x
        self.l = y
        self.box= ['rect', a, b , a+self.L, b+self.l]
        self.fils = []
        self.item = None
            
    def insert(self, item):
        #input('-continue-')
        #self.etat()
        #print(item)
        #print('point__:', item.x, item.y)
        #print('dans___:', hitbox(self.box, ['point', item.x, item.y]))
        if self.item == None:
            if self.fils == []:
                self.item = item
                self.localise(item)(self)
                #print('= prend', self.item,'=')
            else:
                i = (item.x > (self.x + self.L/2)) *2 + (item.y > (self.y + self.l/2))
                #print('= relai ->', i,'=')
                self.fils[i].insert(item)
        else:
            if dis(self.item.x, self.item.y, item.x, item.y)>4:
                #print('= fils =')
                self.fils = [Quad(
                    self,
                    self.x+(i//2)*(self.L/2),
                    self.y+(i%2)*(self.l/2),
                    self.level+1,
                    self.L/2,
                    self.l/2,
                    donnee=self.localise) for i in range(4)]
                temp_item = self.item
                self.item = None
                self.insert(item)
                self.insert(temp_item)
            else:
                pass
                #print('= trop pres =')

    def etat(self):
        print('level__:', self.level)
        print('fils___:', self.fils!=[])
        print('plein__:', self.item)
        print('coord__:', self.x, self.y)
        print('taille_:', self.L, self.l)
        print('box____', self.box)
    
    def recherche(self, zone, item):
        if self.item == None:
            if self.fils != []:
                if hitbox(self.box, zone):
                    for i in range(4):
                        item.append(self.fils[i].recherche(zone, item))
        else:
            if hitbox(self.box, zone):
                print(self.item)
                return(self.item)
    
    def proxi(self, item, dist):
        box=['circle', item.x, item.y, dist]
        items=[]
        self.proximites(items,item, box)
        return items
    
    def proximites(self, items, item, box):
        if self.item == None:
            if self.fils != []:
                if hitbox(self.box, box):
                    for i in range(4):
                        self.fils[i].proximites(items, item, box)
        else:
            if hitbox(self.box, box) and item!=self.item:
                if dis(item.x, item.y, self.item.x, self.item.y)<=box[3]:
                    items.append(self.item)
    
    def pluproche(self, item):
        dist=self.l+self.L
        box=['circle', item.x, item.y, dist]
        items=[None]
        if self.pere!=None:
            self.pere.plusproche_monte(items,item, box, self)

        if items[0]!=None:
            return items[0], box[3], dir(item.x, item.y,0, items[0].x, items[0].y)
        else:
            return None, None, None
    
    def proche(self, item, dist):
        dist=dist
        box=['circle', item.x, item.y, dist]
        items=[None]
        if self.pere!=None:
            self.pere.plusproche_monte(items,item, box, self)
        if items[0]!=None:
            return items[0], box[3], dir(item.x, item.y,0, items[0].x, items[0].y)
        else:
            return None, None, None
    
    def close(self, item, dist):
        dist=dist
        box=['circle', item.x, item.y, dist]
        items=[None]
        self.plusproche_decend(items,item, box, None)
        if items[0]!=None:
            return items[0], box[3], dir(item.x, item.y,0, items[0].x, items[0].y)
        else:
            return None, None, None
        
    def plusproche_monte(self, items, item, box, presc):
        if self!=presc:
            if self.item==None:
                if self.fils != []:
                    if hitbox(self.box, box):
                        for i in self.fils:
                            i.plusproche_decend(items, item, box, presc)
                        if self.pere!=None:
                            self.pere.plusproche_monte(items, item, box, self)
            else:
                if hitbox(self.box, box) and item!=self.item:
                    di=dis(item.x, item.y, self.item.x, self.item.y)
                    if di<=box[3]:
                        box[3]=di
                        items[0]=self.item
        
    def plusproche_decend(self, items, item, box, presc):
        if self!=presc:
            if self.item==None:
                if self.fils != []:
                    if hitbox(self.box, box):
                        for i in self.fils:
                            i.plusproche_decend(items, item, box, presc)
            else:
                if hitbox(self.box, box) and item!=self.item:
                    di=dis(item.x, item.y, self.item.x, self.item.y)
                    if di<=box[3]:
                        box[3]=di
                        items[0]=self.item
            
    def delete(self):
        for i in self.fils:
            i.delete()
        self.fils.clear()
        self.item = None