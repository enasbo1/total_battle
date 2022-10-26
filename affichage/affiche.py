from tkinter import*
from affichage.souris import Souris
from keyboard import is_pressed

class Toile:
    def __init__(self, x_cam, y_cam, title='unknow', fond = "pale turquoise", vitesse_lente = 5, vitesse_rapide=100):
        self.x_cam = x_cam
        self.y_cam = y_cam
        self.acceleration = 1
        self.souris = Souris()
        self.fenetre=Tk()
        self.cont = True
        self.fenetre.attributes('-fullscreen', True)
        self.fenetre.bind('<Escape>', self.end)
        self.fenetre.title(title)
        self.fenetre.geometry(str(x_cam+10)+'x'+str(y_cam+10))
        self.cnv = Canvas(self.fenetre, width = x_cam, height = y_cam, bg=fond)
        self.stats = False
        self.cnv.bind('<Button-1>', self.buy)
        self.cnv.place(x=5,y=5)

    
    def charge(self, x_terrain, y_terrain):
        self.cnv.delete(ALL)
        self.x_terrain = x_terrain
        self.y_terrain = y_terrain
        self.horloge = 0
        self.a_jours=0
        self.clicked_droit = False
        self.masqued = [False, True]
        self.stats = False
        self.annee = ''
        self.texte = ''
        self.centre_r = int((self.x_terrain+self.y_terrain)/20)
        self.cnv.bind('<Button-1>', self.onclick)
        self.cnv.bind('<Button-3>', self.click_droit)
        self.x = (x_terrain-self.x_cam)/2
        self.y = (y_terrain-self.y_cam)/2
        self.ile = self.cnv.create_rectangle(0,0,0,0, fill='DarkOliveGreen1')
        self.sommet = self.cnv.create_oval(0,0,0,0, fill='PaleGreen1', width=2)
        self.vue_d_ensemble = False
        
    def coords(self, item, x1, y1, x2, y2):
        if self.vue_d_ensemble:
            X=2
            Y=2
            echelle = (self.x_cam-4)/(self.x_terrain+20)
            if echelle>(self.y_cam-4)/(self.y_terrain+20):
                echelle=(self.y_cam-4)/(self.y_terrain+20)
            X+=(self.x_cam-(self.x_terrain*echelle))/2
            Y+=(self.y_cam-(self.y_terrain*echelle))/2
            self.cnv.coords(item, int(x1*echelle)+X, int(y1*echelle)+Y, int(x2*echelle)+X, int(y2*echelle)+Y)
        else:
            self.cnv.coords(item, int(x1-self.x), int(y1-self.y), int(x2-self.x), int(y2-self.y))
    
    def moove(self, temps):
        touche = False
        self.vue_d_ensemble = False
        if is_pressed('z'):
            self.y-=temps*100*self.acceleration
            touche = True
        if is_pressed('s'):
            self.y+=temps*100*self.acceleration
            touche = True
        if is_pressed('d'):
            self.x+=temps*100*self.acceleration
            touche = True
        if is_pressed('q'):
            self.x-=temps*100*self.acceleration
            touche = True
        if is_pressed(' '):
            self.vue_d_ensemble = True
            self.x = (self.x_terrain-self.x_cam)/2
            self.y = (self.y_terrain-self.y_cam)/2
        if is_pressed('f'):
            if self.masqued[1]:
                self.masqued[0]=not self.masqued[0]
                self.masqued[1]= False
        else:
            self.masqued[1]=True
        if touche:
            if self.acceleration<11:
                self.acceleration+=temps*5
            else:
                self.acceleration=5
        else:
            self.acceleration=1
        self.coords(self.sommet, (self.x_terrain/2)-self.centre_r,(self.y_terrain/2)-self.centre_r,(self.x_terrain/2)+self.centre_r, (self.y_terrain/2)+self.centre_r)
        self.coords(self.ile, -5, -5, self.x_terrain+5, self.y_terrain+5)
    
    def update(self):
        self.cnv.update()
    
    def buy(self, event):
        self.souris.x_ecrant = event.x
        self.souris.y_ecrant = event.y
        self.stats = True
    def onclick(self, event):
        self.souris.x_ecrant = event.x
        self.souris.y_ecrant = event.y
        if not self.vue_d_ensemble:
            self.souris.x = event.x+self.x
            self.souris.y = event.y+self.y
            self.stats = True
        else:
            X=2
            Y=2
            echelle = (self.x_cam-4)/(self.x_terrain+20)
            if echelle>(self.y_cam-4)/(self.y_terrain+20):
                echelle=(self.y_cam-4)/(self.y_terrain+20)
            X+=(self.x_cam-(self.x_terrain*echelle))/2
            Y+=(self.y_cam-(self.y_terrain*echelle))/2
            self.souris.x = (event.x-X)/echelle
            self.souris.y = (event.y-Y)/echelle
            self.stats = True
    
    def click_droit(self, event):
        self.souris.x_ecrant = event.x
        self.souris.y_ecrant = event.y
        if not self.vue_d_ensemble:
            self.souris.x = event.x+self.x
            self.souris.y = event.y+self.y
            self.clicked_droit = True
        else:
            X=2
            Y=2
            echelle = (self.x_cam-4)/(self.x_terrain+20)
            if echelle>(self.y_cam-4)/(self.y_terrain+20):
                echelle=(self.y_cam-4)/(self.y_terrain+20)
            X+=(self.x_cam-(self.x_terrain*echelle))/2
            Y+=(self.y_cam-(self.y_terrain*echelle))/2
            self.souris.x = (event.x-X)/echelle
            self.souris.y = (event.y-Y)/echelle
            self.clicked_droit = True
            
    def end(self, arg):
        self.cont=False
        self.cnv.update()
    
    def grouper(self, groupe):
        self.groupe = groupe
        self.fenetre.bind("<Key>",self.pressed)
            
    def pressed(self, value):
        for i in self.groupe:
            i.pressed()