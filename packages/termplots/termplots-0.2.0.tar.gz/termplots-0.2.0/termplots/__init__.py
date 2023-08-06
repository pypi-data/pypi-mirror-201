from typing import List

def biground(num, roundto):
    if( num%roundto < roundto/2 ):
        return round(num - (num%roundto), 8)
    else:
        return round(num - (num%roundto) + roundto,8)
      
def find(arr: List, num, ystep ,pos):
    ris = -1
    for x in arr:
        try:
            if(biground(x[pos], ystep)==num and ris != -1):
                ris = len(arr)
            elif(biground(x[pos], ystep)==num):
                ris = arr.index(x)
        except IndexError:
            pass

    return ris
        
def frange(start, stop, step=1.0):
    if(start > stop):
        step *= -1
    curr = start
    tmp = []
    while curr >= stop:
        tmp.append(biground(curr, step))
        curr += step
    return tmp

def getSteps(iny):
    arr = [0]
    for set in iny:
        for value in set:
            if(arr.count(value) == 0):
                arr.append(value)
    arr.sort(reverse=True)
    return arr
    


colors = ["\u001b[31m", '\u001b[32m', '\u001b[33m', '\u001b[34m', '\u001b[35m', '\u001b[36m']
reset = '\u001b[0m'


def plot(iny: List, ystep=1, lowlim=None, highlim=None, car: List = ['*', '#', '@'], labels:List=None):
    
    try:
        iny[0][0]
    except TypeError:
        tmp = iny
        iny = []
        iny.append(tmp)

    if(len(iny) > len(car)):
        print(f"{colors[0]}ERROR! The number of chars passed in the car list must be greater of the number of lists{reset}")
        return -1

    if lowlim == None:
        for serie in iny:
            if(iny[0] == serie):
                mymin = min(serie)
            elif(min(serie) < mymin):
                mymin = min(serie)
            lowlim = biground(mymin, ystep) 
    if highlim == None:
        for serie in iny:
            if(iny[0] == serie):
                mymax = max(serie)
            elif(max(serie) > mymax):
                mymax = max(serie)
            highlim = biground(mymax,ystep) + 2*ystep
            
    for serie in iny:
        if(iny[0]== serie):
            xdim = len(serie)
        elif(len(serie) > xdim):
            xdim = len(serie)

    for serie in iny:
        maxLenY = len(str(biground(min(serie), ystep))) if len(str(biground(min(serie), ystep))) > len(str(biground(max(serie), ystep))) else len(str(biground(max(serie), ystep)))


    for y in frange(highlim, lowlim, ystep):
        nSpazi = maxLenY - len(str(abs(y)))
        print(f'{" "*nSpazi}{abs(y)}|', end="")

       
        if(y == 0):
            for x in range(xdim):
                pos = find(iny, y, ystep ,x)
                color = colors[pos] if pos<len(colors) else colors[pos-len(colors)] 
                if(pos != -1):
                    print(f'{color}{car[pos]}{reset}', end="-")
                else:
                    print("--", end="")
            
        else:
            for x in range(xdim):
                pos = find(iny, y, ystep ,x)
                color = colors[pos] if pos<len(colors) else colors[pos-len(colors)] 
                if(pos != -1):
                    print(f'{color}{car[pos]}{reset}', end=" ")
                else:
                    print("  ", end="")
        print("")

    print()
        
    if (labels != None):
        for label in labels:
            pos = labels.index(label)
            color = colors[pos] if pos<len(colors) else colors[pos-len(colors)] 
            print(f'{color}{car[pos]}{reset}: {label}')
        pos += 1
        color = colors[pos] if pos<len(colors) else colors[pos-len(colors)] 
        print(f'{color}{car[-1]}{reset}: overlaps')


def cplot(iny: List,  car: List = ['*', '#', '@'], labels:List=None):
    ystep = 1
    
    try:
        iny[0][0]
    except TypeError:
        tmp = iny
        iny = []
        iny.append(tmp)

    if(len(iny) > len(car)):
        print(f"{colors[0]}ERROR! The number of chars passed in the car list must be greater of the number of lists{reset}")
        return -1

            
    for serie in iny:
        if(iny[0]== serie):
            xdim = len(serie)
        elif(len(serie) > xdim):
            xdim = len(serie)

    for serie in iny:
        maxLenY = len(str(biground(min(serie), ystep))) if len(str(biground(min(serie), ystep))) > len(str(biground(max(serie), ystep))) else len(str(biground(max(serie), ystep)))


    for y in getSteps(iny):
        nSpazi = maxLenY - len(str(abs(y)))
        print(f'{" "*nSpazi}{abs(y)}|', end="")

       
        if(y == 0):
            for x in range(xdim):
                pos = find(iny, y, ystep ,x)
                color = colors[pos] if pos<len(colors) else colors[pos-len(colors)] 
                if(pos != -1):
                    print(f'{color}{car[pos]}{reset}', end="-")
                else:
                    print("--", end="")
            
        else:
            for x in range(xdim):
                pos = find(iny, y, ystep ,x)
                color = colors[pos] if pos<len(colors) else colors[pos-len(colors)] 
                if(pos != -1):
                    print(f'{color}{car[pos]}{reset}', end=" ")
                else:
                    print("  ", end="")
        print("")

    print()
        
    if (labels != None):
        for label in labels:
            pos = labels.index(label)
            color = colors[pos] if pos<len(colors) else colors[pos-len(colors)] 
            print(f'{color}{car[pos]}{reset}: {label}')
        pos += 1
        color = colors[pos] if pos<len(colors) else colors[pos-len(colors)] 
        print(f'{color}{car[-1]}{reset}: overlaps')

# Tests...
#plot([112, 132, 30], ystep=50)
#plot([0,0.1,0.3], ystep=0.3)
#plot([-32,-20,0,20,32], ystep=10)
#mplot([[-32,-20,0],[32,20,0, 112]], ystep=50, labels=["1", "2"])
#plot([[1,0,2], [-1,0,3,0,2,2]], car=['*', '$', '@'], labels=['List 1', 'List 2'])
#plot([1,0,2,-1,0,3,0,2,2], car=['*', '$', '@'], labels=['List 1'])
#print(getSteps([[32,20,0, 112],[-32,-20,0,20]]))
cplot([[32,20,0, 112],[-32,-20,0,20]])
cplot([-3,2,1,15])