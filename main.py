#import os
dozwolone = [0,1,2,3,4,5,6,7]
class Pozycja():
    def __init__(self):
        self.x = 0
        self.y = 0

def repr_graf():

    z1 = '[#]'   #chr(9635)
    z2 = '   '   #chr(9634)

    iter = Pozycja()

    print("     ", end='')
    for iter.x in range(0, 8):
        print("", iter.x,"", end='')

    print("")
    print("  ",end = '')
    for iter.x in range(0,10):
        print(z1, end = '')


    for iter.x in range(0,8):
        print("")
        for iter.y in range(0,8):
            if iter.y == 0:
                print(iter.x,z1,end = '')
            if plansza[iter.x][iter.y] == 0:
                print(z2,end = '')
            if plansza[iter.x][iter.y] == 1:
                print("   ",end = '')
            if plansza[iter.x][iter.y] == 2:
                print(" B ",end = '')
                bialy.ilosc_pionkow += 1
            if plansza[iter.x][iter.y] == 3:
                print(" C ",end = '')
                czarny.ilosc_pionkow += 1
        print(z1,iter.x,end = '')


    print("")
    print("  ",end = '')
    for iter.x in range(0,10):
        print(z1, end = '')

    print("")
    print("     ", end='')
    for iter.x in range(0, 8):
        print("", iter.x,"", end='')

class Pionek(Pozycja):
    def __init__(self,nazwa,ID):
        self._nazwa_gracza = nazwa
        self.ilosc_pionkow = 0
        self._gracz_ID = ID
    def wybor_pionka(self,p):
        while(True):
            print("Wybierz pionek ktorym chcesz wykonac ruch")
            p.x = int(input("Wybierz pozycje x pionka:"))
            p.y = int(input("Wybierz pozycje y pionka:"))
            if p.x in dozwolone and p.y in dozwolone and plansza[p.y][p.x] == self._gracz_ID :
                break
            else:
                print("Blad przy wyborze")

    def wybor_ruchu(self,p,przejscie):
        repr_graf()
        print("\nWybierz nastepna pozycje")
        r = Pozycja()

        while (True):
            r.x = int(input("Wybierz pozycje x pionka:"))
            r.y = int(input("Wybierz pozycje y pionka:"))
            if r.x in dozwolone and r.y in dozwolone:
                break
            else:
                print("Blad przy wyborze")

        # ruch do przodu
        if plansza[r.y][r.x] == 1 and przejscie == 0:
            if self._gracz_ID == 2: #ruch do przodu bialy
                if (((r.y - p.y == -1)and(r.x-p.x == -1))or((r.y-p.y == -1)and(r.x -p.x == 1))): #sprawdzam czy ruch jest zgodny z zasadami (o jedno pole w przod)
                    plansza[r.y][r.x]=plansza[p.y][p.x]
                    plansza[p.y][p.x] = 1
                else:
                    #os.system('cls')
                    repr_graf()
                    print("\nWybrales zle pole")
                    p.wybor_ruchu(p) #ponowne wywołanie funcji
            if self._gracz_ID == 3: #ruch do przodu czarny
                if (((r.y - p.y == 1)and(r.x-p.x == 1))or((r.y-p.y == 1)and(r.x -p.x == -1))): #sprawdzam czy ruch jest zgodny z zasadami (o jedno pole w przod)
                    plansza[r.y][r.x] = plansza[p.y][p.x]
                    plansza[p.y][p.x] = 1
                else:
                    #os.system('cls')
                    repr_graf()
                    print("\nWybrales zle pole")
                    p.wybor_ruchu(p) #ponowne wywołanie funcji
        # bicie bialych
        elif plansza[r.y][r.x] == 2 and self._gracz_ID == 3:
            if (((r.y - p.y == -1) and (r.x - p.x == -1)) or ((r.y - p.y == -1) and (r.x - p.x == 1)) or ((r.y - p.y == 1)and(r.x-p.x == 1))or((r.y-p.y == 1)and(r.x -p.x == -1))):
                if r.y + 1 - p.y == 0:  # bicie do gory
                    if r.x + 1 - p.x == 0:  # bicie w lewo
                        if r.x == 0 and plansza[r.y - 1][r.x + 1] == 1:  # rikoszet os x sciana lewo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1,r.x + 1,self._gracz_ID)


                        elif r.y == 0 and plansza[r.y+1][r.x - 1] == 1:  # rikoszet os y sciana lewo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y+1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x - 1,self._gracz_ID)

                        elif plansza[r.y - 1][r.x - 1] == 1:  # przekatna lewo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x - 1,self._gracz_ID)

                        else:
                            print("\nniedozwolony ruch")
                            p.wybor_ruchu(p)

                    else:  # bicie w prawo
                        if r.x == 7 and plansza[r.y - 1][r.x - 1] == 1:  # rikoszet os x sciana prawo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x - 1,self._gracz_ID)

                        elif r.y == 0 and plansza[r.y + 1][r.x + 1] == 1:  # rikoszet os y sciana prawo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x + 1,self._gracz_ID)

                        elif plansza[r.y - 1][r.x + 1] == 1:  # przekatna prawo gora
                             plansza[r.y][r.x] = 1
                             plansza[r.y - 1][r.x + 1] = self._gracz_ID
                             plansza[p.y][p.x] = 1
                             czy_istnieje_bicie(r.y - 1, r.x + 1,self._gracz_ID)

                        else:
                            print("\nniedozwolony ruch")
                            p.wybor_ruchu(p)

                else:  # bicie w dol
                    if r.x + 1 - p.x == 0:  # bicie w lewo
                        if r.x == 0 and plansza[r.y + 1][r.x + 1] == 1:  # rikoszet os x sciana lewo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x + 1,self._gracz_ID)

                        elif r.y == 7 and plansza[r.y - 1][r.x - 1] == 1:  # rikoszet os y sciana lewo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x - 1,self._gracz_ID)

                        elif plansza[r.y + 1][r.x - 1] == 1:  # przekatna lewo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x - 1,self._gracz_ID)

                        else:
                            print("\nniedozwolony ruch")
                            p.wybor_ruchu(p)

                    else:  # bicie w prawo
                        if r.x == 7 and plansza[r.y + 1][r.x - 1] == 1:  # rikoszet os x sciana prawo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x - 1,self._gracz_ID)

                        elif r.y == 7 and plansza[r.y - 1][r.x + 1] == 1:  # rikoszet os y sciana prawo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x + 1,self._gracz_ID)

                        elif plansza[r.y + 1][r.x + 1] == 1:  # przekatna prawo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x + 1,self._gracz_ID)

                        else:
                            print("\nniedozwolony ruch")
                            p.wybor_ruchu(p)
            else:
                repr_graf()
                print("\nWybrales zle pole")
                p.wybor_ruchu(p)
        # bicie czarnych
        elif plansza[r.y][r.x] == 3 and self._gracz_ID == 2:
            if (((r.y - p.y == -1) and (r.x - p.x == -1)) or ((r.y - p.y == -1) and (r.x - p.x == 1)) or (
                    (r.y - p.y == 1) and (r.x - p.x == 1)) or ((r.y - p.y == 1) and (r.x - p.x == -1))):
                if r.y + 1 - p.y == 0:  # bicie do gory
                    if r.x + 1 - p.x == 0:  # bicie w lewo
                        if r.x == 0 and plansza[r.y - 1][r.x + 1] == 1:  # rikoszet os x sciana lewo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x + 1, self._gracz_ID)


                        elif r.y == 0 and plansza[r.y + 1][r.x - 1] == 1:  # rikoszet os y sciana lewo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x - 1, self._gracz_ID)

                        elif plansza[r.y - 1][r.x - 1] == 1:  # przekatna lewo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x - 1, self._gracz_ID)

                        else:
                            print("\nniedozwolony ruch")
                            p.wybor_ruchu(p)

                    else:  # bicie w prawo
                        if r.x == 7 and plansza[r.y - 1][r.x - 1] == 1:  # rikoszet os x sciana prawo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x - 1, self._gracz_ID)

                        elif r.y == 0 and plansza[r.y + 1][r.x + 1] == 1:  # rikoszet os y sciana prawo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x + 1, self._gracz_ID)

                        elif plansza[r.y - 1][r.x + 1] == 1:  # przekatna prawo gora
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x + 1, self._gracz_ID)

                        else:
                            print("\nniedozwolony ruch")
                            p.wybor_ruchu(p)

                else:  # bicie w dol
                    if r.x + 1 - p.x == 0:  # bicie w lewo
                        if r.x == 0 and plansza[r.y + 1][r.x + 1] == 1:  # rikoszet os x sciana lewo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x + 1, self._gracz_ID)

                        elif r.y == 7 and plansza[r.y - 1][r.x - 1] == 1:  # rikoszet os y sciana lewo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y - 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x - 1, self._gracz_ID)

                        elif plansza[r.y + 1][r.x - 1] == 1:  # przekatna lewo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x - 1, self._gracz_ID)

                        else:
                            print("\nniedozwolony ruch")
                            p.wybor_ruchu(p)

                    else:  # bicie w prawo
                        if r.x == 7 and plansza[r.y + 1][r.x - 1] == 1:  # rikoszet os x sciana prawo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x - 1, self._gracz_ID)

                        elif r.y == 7 and plansza[r.y - 1][r.x + 1] == 1:  # rikoszet os y sciana prawo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x - 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y - 1, r.x + 1, self._gracz_ID)

                        elif plansza[r.y + 1][r.x + 1] == 1:  # przekatna prawo dol
                            plansza[r.y][r.x] = 1
                            plansza[r.y + 1][r.x + 1] = self._gracz_ID
                            plansza[p.y][p.x] = 1
                            czy_istnieje_bicie(r.y + 1, r.x + 1, self._gracz_ID)

                        else:
                            print("\nniedozwolony ruch")
                            p.wybor_ruchu(p)
            else:
                repr_graf()
                print("\nWybrales zle pole")
                p.wybor_ruchu(p)
        else:
            #os.system('cls')
            repr_graf()
            print("\nWybrales zle pole")
            p.wybor_ruchu(p)

def czy_istnieje_bicie(y,x,ID):
        p = Pionek('kopia',ID)
        p.x = x
        p.y = y

        if p._gracz_ID == 3:
            if plansza[p.y - 1][p.x - 1] == 2: #LEWO GORA
                if p.y - 1 == 0 and plansza[p.y][p.x - 2] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p,1)
                elif p.x - 1 == 0 and plansza[p.y - 2][p.x] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif plansza[p.y - 2][p.x - 2] == 1: #PRZEKATNA
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)

            elif plansza[p.y - 1][p.x + 1] == 2: #PRAWO GORA
                if p.y - 1 == 0 and plansza[p.y][p.x+2]==1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif p.x + 1 == 7 and plansza[p.y-2][p.x]==1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif plansza[p.y - 2][p.x + 2] == 1: #PRZEKATNA
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)

            elif plansza[p.y + 1][p.x + 1] == 2:  # PRAWO DOL
                if p.y + 1 == 7 and plansza[p.y][p.x+2] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif p.x + 1 == 7 and plansza[p.y+2][p.x]==1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif plansza[p.y + 2][p.x + 2] == 1: #PRZEKATNA
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)

            elif plansza[p.y + 1][p.x - 1] == 2:  # LEWO DOL
                if p.y + 1 == 7 and plansza[p.y][p.x -2]==1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif p.x - 1 == 0 and plansza[p.y +2][p.x] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif plansza[p.y + 2][p.x - 2] == 1: #PRZEKATNA
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)

            else:
                print("Nie masz więcej ruchow")

        elif p._gracz_ID == 2:
            if plansza[p.y - 1][p.x - 1] == 3:  # LEWO GORA
                if p.y - 1 == 0 and plansza[p.y][p.x - 2] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif p.x - 1 == 0 and plansza[p.y - 2][p.x] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif plansza[p.y - 2][p.x - 2] == 1:  # PRZEKATNA
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)

            if plansza[p.y - 1][p.x + 1] == 3:  # PRAWO GORA
                if p.y - 1 == 0 and plansza[p.y][p.x + 2] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif p.x + 1 == 7 and plansza[p.y - 2][p.x] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif plansza[p.y - 2][p.x + 2] == 1:  # PRZEKATNA
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)

            if plansza[p.y + 1][p.x + 1] == 3:  # PRAWO DOL
                if p.y + 1 == 7 and plansza[p.y][p.x + 2] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif p.x + 1 == 7 and plansza[p.y + 2][p.x] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif plansza[p.y + 2][p.x + 2] == 1:  # PRZEKATNA
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)

            if plansza[p.y + 1][p.x - 1] == 3:  # LEWO DOL
                if p.y + 1 == 7 and plansza[p.y][p.x - 2] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif p.x - 1 == 0 and plansza[p.y + 2][p.x] == 1:
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)
                elif plansza[p.y + 2][p.x - 2] == 1:  # PRZEKATNA
                    print("Możliwe następne bicie")
                    p.wybor_ruchu(p, 1)

            else:
                print("Nie masz więcej ruchow")
        else:
            print("Blad!")

plansza = 8 * [0]
for i in range(8):
    plansza[i]= [0]*8

bialy = Pionek('Bialy', 2)
czarny = Pionek('Czarny', 3)

def uzup_plan_pocz():

    """
	0 - pole białe
	1 - pole czarne
	2 - pionek biały
	3 - pionek czarny
    """

    #pionki czarne
    poz_plan = Pozycja()

    for poz_plan.y in range(0,3) :
        for poz_plan.x in range(0,8) :
            if poz_plan.y % 2 ==0:
                if poz_plan.x % 2 == 0:
                    plansza[poz_plan.y][poz_plan.x] = 0
                else:
                    plansza[poz_plan.y][poz_plan.x] = 3
            else:
                if poz_plan.x % 2 == 0:
                    plansza[poz_plan.y][poz_plan.x] = 3
                else:
                    plansza[poz_plan.y][poz_plan.x] = 0



    #puste pola
    for poz_plan.y in range(3,5):
        for poz_plan.x in range(0,8):
            if poz_plan.y % 2 == 0:
                if poz_plan.x % 2 == 0:
                    plansza[poz_plan.y][poz_plan.x] = 0
                else:
                    plansza[poz_plan.y][poz_plan.x] = 1
            else:
                if poz_plan.x % 2 == 0:
                    plansza[poz_plan.y][poz_plan.x] = 1
                else:
                    plansza[poz_plan.y][poz_plan.x] = 0



    #pionki biale
    for poz_plan.y in range(5,8):
        for poz_plan.x in range(0,8):
            if poz_plan.y % 2 == 0:
                if poz_plan.x % 2 == 0:
                    plansza[poz_plan.y][poz_plan.x] = 0
                else:
                    plansza[poz_plan.y][poz_plan.x] = 2
            else:
                if poz_plan.x % 2 == 0:
                    plansza[poz_plan.y][poz_plan.x] = 2
                else:
                    plansza[poz_plan.y][poz_plan.x] = 0

def main():
    uzup_plan_pocz()


    wygrana = False
    dlugosc_gry = 0

    while(wygrana == False):
        if dlugosc_gry % 2 == 0:
            #os.system('cls')
            repr_graf()
            print("\nRuch gracza: ",format(bialy._nazwa_gracza))
            bialy.wybor_pionka(bialy)
            bialy.wybor_ruchu(bialy,0)
        else:
            #os.system('cls')
            repr_graf()
            print("\nRuch gracza: ",format(czarny._nazwa_gracza))
            czarny.wybor_pionka(czarny)
            czarny.wybor_ruchu(czarny,0)

        if dlugosc_gry == 30 and bialy.ilosc_pionkow == 12 and czarny.ilosc_pionkow ==12:
            print("Remis!")
            break
        dlugosc_gry += 1

main()


