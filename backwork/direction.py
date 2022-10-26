from math import*

def tourne(ditem, direction, vitesse):
    if abs(ditem-direction)>pi:
        if rot(-ditem, direction)>0:
            ditem=rot(vitesse,ditem)
        else:
            ditem=rot(-vitesse,ditem)
    elif  abs(ditem-direction)>vitesse:
        if ditem<direction:
            ditem=rot(vitesse,ditem)
        else:
            ditem=rot(-vitesse,ditem)
    else:
        ditem=direction
    return(ditem)

def avix(a,d):
    x=cos(d)*a
    return(x)

def aviy(a,d):
    x=sin(d)*a
    return(x)

def dis(a,b,x,y):
    x1=x-a
    y1=y-b
    n=sqrt(y1**2+x1**2)
    return(n)

def disrap(a,b,x,y):
    x1=x-a
    y1=y-b
    n=y1**2+x1**2
    return(n)

def rot(r,d):
    d+=r
    if d>pi:
        d=d-(2*pi)
    if d<-pi:
        d=d+(2*pi)
    return(d)

def dir(a,b,d,x,y):
    x1=x-a
    y1=y-b
    L=0
    d=-d
    if x1>0:
        if y1>=0:
            L=atan(y1/x1)
        else:
            L=atan(y1/x1)
    elif x1<0:
        if y1>=0:
            L=atan(y1/x1)+pi
        else:
            L=atan(y1/x1)+pi
    else:
        if y1<0:
            L=-pi/2
        else:
            L=pi/2
    L=rot(d,L)
    return(L)

def lim(x,x1,y,y1,a,b,d):
    if b<y or b>y1:
        d=-d
    if a<x:
        d=-d-pi
    if a>x1:
        d=-d+pi
    return(d)

def limxy(a,b,x,x1,y,y1):
    while a<x:
        a=x+5
    while a>x1:
        a=x1-5
    while b<y:
        b=y+5
    while b>y1:
        b=y1-5
    return(a,b)
