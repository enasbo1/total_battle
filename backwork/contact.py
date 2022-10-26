from backwork.direction import*

def hitbox(zone1, zone2):
    if zone1[0]=='rect':
        if zone2[0]=='rect':
            X1=zone1[1]
            Y1=zone1[2]
            Xx1=zone1[3]
            Yy1=zone1[4]
            X2=zone2[1]
            Y2=zone2[2]
            Xx2=zone2[3]
            Yy2=zone2[4]
            ret=False
            if X2<=X1<=Xx2 or X1<=X2<=Xx1:
                if Y2<=Y1<=Yy2 or Y1<=Y2<=Yy1:
                    ret=True
    if zone1[0]=='rect':
        if zone2[0]=='circle':
            X1=zone1[1]
            Y1=zone1[2]
            Xx1=zone1[3]
            Yy1=zone1[4]
            X2=zone2[1]
            Y2=zone2[2]
            R=zone2[3]
            ret= X1<X2<=Xx1 and Y1<Y2<=Yy1
            if X1<X2<Xx1:
                ret= ret or abs(Y2-Y1)<R or abs(Y2-Yy1)<R
            elif Y1<Y2<Yy1:
                ret= ret or abs(X2-X1)<R or abs(X2-Xx1)<R
            else:
                R=R**2
                ret= ret or disrap(X1, Y1, X2, Y2)<R or disrap(X1, Yy1, X2, Y2)<R or disrap(Xx1, Y1, X2, Y2)<R or disrap(Xx1, Yy1, X2, Y2)<R
    
    if zone1[0]=='rect':
        if zone2[0]=='point':
            X1=zone1[1]
            Y1=zone1[2]
            Xx1=zone1[3]
            Yy1=zone1[4]
            X2=zone2[1]
            Y2=zone2[2]
            ret= X1<X2<=Xx1 and Y1<Y2<=Yy1
    
    if zone2[0]=='rect':
        if zone1[0]=='point':
            X1=zone2[1]
            Y1=zone2[2]
            Xx1=zone2[3]
            Yy1=zone2[4]
            X2=zone1[1]
            Y2=zone1[2]
            ret= X1<X2<=Xx1 and Y1<Y2<=Yy1
        
    if zone1[0]=='circle':
        if zone2[0]=='rect':
            X1=zone2[1]
            Y1=zone2[2]
            Xx1=zone2[3]
            Yy1=zone2[4]
            X2=zone1[1]
            Y2=zone1[2]
            R=zone1[3]
            ret= X1<=X2<=Xx1 and Y1<=Y2<=Yy1
            if X1<=X2<=Xx1:
                ret= ret or abs(Y2-Y1)<R or abs(Y2-Yy1)<R
            elif Y1<=Y2<=Yy1:
                ret= ret or abs(X2-X1)<R or abs(X2-Xx1)<R
            else:
                R=R**2
                ret= ret or disrap(X1, Y1, X2, Y2)<=R or disrap(X1, Yy1, X2, Y2)<R or disrap(Xx1, Y1, X2, Y2)<=R or disrap(Xx1, Yy1, X2, Y2)<=R
    
    if zone1[0]=='circle':
        if zone2[0]=='circle':
            ret=disrap(zone1[1], zone1[2], zone2[1], zone2[2])<=(zone1[3]+zone2[3])**2

    return(ret)