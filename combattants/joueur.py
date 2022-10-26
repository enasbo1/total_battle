from keyboard import is_pressed
from tkinter import PhotoImage
from backwork.direction import*
from combattants.cartes import Carte
from combattants.ordres import Ordre
from combattants.groupes import Groupe
from backwork.contact import hitbox

class Joueur:
    def __init__(self, toile, troupes, color = 'DarkGreen'):
        self.souris = toile.souris
        self.troupes = troupes
        self.x = 0
        self.y = 0
        self.x2 = 0
        self.y2 = 0
        self.toile = toile
        self.select = []
        self.taille_plgrosse_unite = 10
        self.color = color
        self.groupe = [Groupe(self.toile, i, self, color = 'grey'+str(i*10)) for i in range(1,7)]
        self.toile.grouper(self.groupe)
        self.appar = self.toile.cnv.create_oval(0,0,0,0,fill='black')
    
    def init(self, divinite, quad_unit, quad_unit_ennemi, unit, unit_adv):
        self.divinite=divinite
        self.unit = unit
        self.toile.x = self.unit[int((len(self.unit)-1)/2)].x-(self.toile.x_cam/2)
        self.toile.y = self.unit[int((len(self.unit)-1)/2)].y-(self.toile.y_cam/2)
        self.unit_adv = unit_adv
        self.quad_unit = quad_unit
        self.quad_unit_adv = quad_unit_ennemi
        self.cartes_images = [PhotoImage(file = "images/"+i.nom+".png") for i in self.unit]
        X=int((self.toile.x_cam/2)-((len(self.unit)*25)))
        Y=int(self.toile.y_cam-90)
        self.tableau = self.toile.cnv.create_rectangle((self.toile.x_cam-800)/2, self.toile.y_cam-130, (self.toile.x_cam+800)/2, self.toile.y_cam-5, fill =self.color)
        self.tableau_box = ['rect', (self.toile.x_cam-800)/2, self.toile.y_cam-130, (self.toile.x_cam+800)/2, self.toile.y_cam-5]
        self.cartes = [Carte(self.toile, X+(i*50),Y, self.unit[i], image = j) for i,j in enumerate(self.cartes_images)]
        for i in self.unit:
            i.formation='Garde'
        self.create()
        self.formation = [False, False]
    
    def tour(self):
        if self.select!=[]:
            if self.toile.vue_d_ensemble:
                x,y=0,0
                for i in self.select:
                    x+=i.x
                    y+=i.y
                x=x/len(self.select)
                y=y/len(self.select)
                self.toile.x = x-self.toile.x_cam/2
                self.toile.y = y-self.toile.y_cam/2
        self.groupe[0].add_unit(self.unit)
        self.taille_plgrosse_unite = 0
        self.taille_plgrosse_unite_adv = 0
        for i in self.cartes:
            i.tour()
        for i in self.unit:
            if i.r>self.taille_plgrosse_unite:
                self.taille_plgrosse_unite = i.r
            self.toile.cnv.itemconfig(i.carte.etat, fill=i.etat)
        for i in self.unit_adv:
            if i.r>self.taille_plgrosse_unite_adv:
                self.taille_plgrosse_unite_adv = i.r
        nb = self.compte()
        j=0
        for i in self.strats:
            j = i.tour(nb,j)
        for i in self.groupe:
            i.tour()
        if self.toile.stats:
            self.toile.stats = False
            self.toile.coords(self.appar, self.souris.x+10, self.souris.y+10, self.souris.x-10, self.souris.y-10)
            self.toile.cnv.itemconfig(self.appar, fill = 'black')
            souris_box = ['point', self.souris.x_ecrant, self.souris.y_ecrant]
            if hitbox(self.tableau_box, souris_box):
                for i in self.cartes:
                    if hitbox(i.box, souris_box):
                        self.select_one(i.unite)
                for i in self.strats:
                    if hitbox(i.box, souris_box):
                        i.ordonne()
            elif self.select==[]:
                plproche, dist, direct = self.quad_unit.close(self.souris, self.taille_plgrosse_unite+10)
                if plproche!=None:
                    if dist<=plproche.taille+10:
                        self.ajoute(plproche)
                """else:
                    self.quad_unit_adv.close(self.souris, self.taille_plgrosse_unite_adv)"""
            else:
                if is_pressed('a'):
                    self.x=self.souris.x
                    self.y=self.souris.y
                    self.formation[0] = True
                else:
                    plproche, dist, direct =self.quad_unit_adv.close(self.souris, self.taille_plgrosse_unite_adv+10)
                    if plproche!=None:
                        if dist<=plproche.taille+10:
                            self.cibler(plproche)
                        else:
                            plproche, dist, direct = self.quad_unit.close(self.souris, self.taille_plgrosse_unite+10)
                            if plproche!=None:
                                if dist<=plproche.taille+10:
                                    self.select_one(plproche)
                                else:
                                    self.deplacement_formation()
                            else:
                                self.deplacement_formation()
                    else:
                        plproche, dist, direct = self.quad_unit.close(self.souris, self.taille_plgrosse_unite+10)
                        if plproche!=None:
                            if dist<=plproche.taille+10:
                                self.select_one(plproche)
                            else:
                                self.deplacement_formation()
                        else:
                            self.deplacement_formation()
        elif not is_pressed('a'):
            self.toile.cnv.coords(self.appar, -1,-1,-1,-1)
            
        if self.toile.clicked_droit:
            self.toile.coords(self.appar, self.souris.x+10, self.souris.y+10, self.souris.x-10, self.souris.y-10)
            self.toile.cnv.itemconfig(self.appar, fill = 'grey')
            self.toile.clicked_droit=False
            if self.select!=[]:
                if is_pressed('a') and self.formation[0] and len(self.select)>1:
                    self.formation[1]=True
                    self.x2 = self.souris.x
                    self.y2 = self.souris.y
                else:
                    self.orienter()
                    
        if not is_pressed('a') and self.formation[0]:
            if self.formation[1]:
                self.destination_formation()
            else:
                self.destination()
            self.formation = [False, False]
        if is_pressed('w'):
            for sel in self.select:
                self.toile.cnv.itemconfig(sel.tete, width = 2)
                sel.carte.select = False
            self.select.clear()
        for sel in self.select:
            self.toile.cnv.itemconfig(sel.tete, width = 5)
        
    def vide(self):
        if not is_pressed('Ctrl'):
            for sel in self.select:
                self.toile.cnv.itemconfig(sel.tete, width = 2)
                sel.carte.select = False
            self.select.clear()
    
    def select_one(self, unit):
        present = self.present(unit)
        if present[0]:
            if is_pressed('Ctrl'):
                self.retire(unit, present[1])
            else:
                self.vide()
                self.ajoute(unit)
        else:
            self.vide()
            self.ajoute(unit)
    
    def present(self, unit):
        ret1 = False
        ret2 = 0 
        for i, sel in enumerate(self.select):
            if sel == unit:
                ret2 = i
                ret1 = True
        return ret1 , ret2
    
    def retire(self, unit, i):
        _temp = 0
        unit.carte.select = False
        self.toile.cnv.itemconfig(unit.tete, width = 2)
        del self.select[i]
    
    def ajoute(self, unit):
        self.select.append(unit)
        unit.carte.select = True
    
    def ajoute_list(self,groupe):
        for i in groupe:
            self.ajoute(i)
    
    def cibler(self, cible):
        for sel in self.select:
            sel.cible=cible
    
    def destination(self):
        for sel in self.select:
            sel.cible = sel.pointeur
            sel.pointeur.place(self.souris)
    
    def deplacement_formation(self):
        X=0
        Y=0
        for sel in self.select:
            X+=sel.x
            Y+=sel.y
        X=X/len(self.select)
        Y=Y/len(self.select)
        X=self.souris.x-X
        Y=self.souris.y-Y
        for sel in self.select:
            sel.cible = sel.pointeur
            sel.pointeur.deplace(X, Y)
        
    
    def destination_formation(self):
        for i in self.select:
            i.cible_cache = [None, 0]
        nb = len(self.select)-1
        _temp = [(i, self.scal(i)) for i in self.select]
        coordonnes = [[
                        ((self.x*i)+(self.x2*(nb-i)))/nb,
                        ((self.y*i)+(self.y2*(nb-i)))/nb
                       ]
                      for i in range(nb+1)]
        _temp.sort(key = lambda x:x[1], reverse = True)
                   
        direc = dir(self.x, self.y, -pi/2, self.x2, self.y2)
        for j, i in enumerate(_temp):
            i[0].cible = i[0].pointeur
            i[0].pointeur.x = coordonnes[j][0]
            i[0].pointeur.y = coordonnes[j][1]
            i[0].pointeur.oriente = True
            i[0].pointeur.d = direc
    
    def scal(self, item):
        x1 = item.x-self.x
        y1 = item.y-self.y
        x2 = self.x2-self.x
        y2 = self.y2-self.y
        return x1*x2+y1*y2
        
    def orienter(self):
        for sel in self.select:
            sel.pointeur.oriente = True
            sel.pointeur.d = dir(sel.pointeur.x, sel.pointeur.y, 0, self.souris.x, self.souris.y)
    
    def compte(self):
        ret = 0
        for i in self.strats:
            ret+= i.compte()
        return ret
    
    def create(self):
        if self.unit!=[]:
            formation =['Groupe','Garde','Cible','Dispertion', 'Regroupe']
            self.strats = [Ordre(self.toile, 0, 0, self, nom = i) for i in formation]