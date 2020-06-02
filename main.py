import pygame

plansza = 8 * [0]
for i in range(8):
    plansza[i]= [0]*8

size = 50
white_color = [200, 200, 200]
black_color = [100, 100, 100]
w_pawn = pygame.transform.scale(pygame.image.load("pawn_white.png"),(size,size))
b_pawn = pygame.transform.scale(pygame.image.load("pawn_black.png"),(size,size))
w_queen = pygame.transform.scale(pygame.image.load("queen_white.png"),(size,size))
b_queen = pygame.transform.scale(pygame.image.load("queen_black.png"),(size,size))
pygame.font.init()

class Pionek():
    def __init__(self,f):
        self.x = 0
        self.y = 0
        self.flaga = f  #flaga koloru i wartosci(pionek badz damka)
        self.f_bicia = 0

class Warcaby():
    def __init__(self):
        self.tab_white =[]
        self.tab_black =[]
        self.turn = 0


#metoda ktora uzupelnia poczatkowe wspolrzedne pionkow dla obu stron
    def start(self):
        tab_black = []
        tab_white = []

        # czarne
        for i in range(0, 12):
            tab_black.append(Pionek(3))
        i=1
        for j in range(0,4):
            tab_black[j].y = 0
            tab_black[j].x = i

            i +=2
        i=0
        for j in range(4,8):
            tab_black[j].y = 1
            tab_black[j].x = i
            i += 2
        i = 1
        for j in range(8,12):
            tab_black[j].y = 2
            tab_black[j].x = i
            i += 2

        #biale
        for i in range(0, 12):
            tab_white.append(Pionek(2))
        i = 0
        for j in range(0, 4):
            tab_white[j].x = i
            tab_white[j].y = 5
            i += 2
        i = 1
        for j in range(4, 8):
            tab_white[j].x = i
            tab_white[j].y = 6
            i += 2
        i = 0
        for j in range(8, 12):
            tab_white[j].x = i
            tab_white[j].y = 7
            i += 2

        self.tab_black = tab_black
        self.tab_white = tab_white

        """
            0 - pole białe
            1 - pole czarne
            2 - pionek biały
            3 - pionek czarny
            4 - biala damka
            5 - czarna damka
            """

        # pionki czarne
        for y in range(0, 3):
            for x in range(0, 8):
                if y % 2 == 0:
                    if x % 2 == 0:
                        plansza[x][y] = 0
                    else:
                        plansza[x][y] = 3
                else:
                    if x % 2 == 0:
                        plansza[x][y] = 3
                    else:
                        plansza[x][y] = 0

        # puste pola
        for y in range(3, 5):
            for x in range(0, 8):
                if y % 2 == 0:
                    if x % 2 == 0:
                        plansza[x][y] = 0
                    else:
                        plansza[x][y] = 1
                else:
                    if x % 2 == 0:
                        plansza[x][y] = 1
                    else:
                        plansza[x][y] = 0

        # pionki biale
        for y in range(5, 8):
            for x in range(0, 8):
                if y % 2 == 0:
                    if x % 2 == 0:
                        plansza[x][y] = 0
                    else:
                        plansza[x][y] = 2
                else:
                    if x % 2 == 0:
                        plansza[x][y] = 2
                    else:
                        plansza[x][y] = 0
        rysuj_plansze(self.tab_white,self.tab_black)

#metoda ruchu i bicia z instrukcjami logicznymi
    def choice_function(self):
#biały
        if self.turn % 2 == 0:
            print("biały rusza: tura:",self.turn)
            czy_bicie(self.turn,self.tab_white,self.tab_black)
            turn = True
            while turn == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        turn = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            pos = pygame.mouse.get_pos()
                            nie_ma = 0
                            for i in range(len(self.tab_white)):
                                if pos[0] // size == self.tab_white[i].x and pos[1] // size == self.tab_white[i].y and self.tab_white[i].f_bicia == 1:
                                    while czy_bicie(self.turn,self.tab_white,self.tab_black):
                                        r = bicie(self.tab_white[i])
                                        self.tab_white[i].x = r.x
                                        self.tab_white[i].y = r.y

                                        rysuj_plansze(self.tab_white, self.tab_black)
                                    self.turn += 1
                                    turn = False
                            for i in range(len(self.tab_white)):
                                if pos[0] // size == self.tab_white[i].x and pos[1] // size == self.tab_white[i].y and czy_ruch(self.tab_white[i]):
                                        r = ruch(self.tab_white[i])
                                        self.tab_white[i].x = r.x
                                        self.tab_white[i].y = r.y
                                        rysuj_plansze(self.tab_white, self.tab_black)
                                        self.turn += 1
                                        turn = False
                                else:
                                    nie_ma += 1
                                    if nie_ma == len(self.tab_white):
                                        print("Nie wybrałeś bialego pionka")

#czarny
        else:
            print("czarny rusza: tura:",self.turn)
            czy_bicie(self.turn, self.tab_white, self.tab_black)
            turn = True
            while turn == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        turn = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            pos = pygame.mouse.get_pos()
                            nie_ma = 0
                            for i in range(len(self.tab_black)):
                                if pos[0] // size == self.tab_black[i].x and pos[1] // size == self.tab_black[i].y and self.tab_black[i].f_bicia == 1:
                                    while czy_bicie(self.turn,self.tab_white,self.tab_black):
                                        r = bicie(self.tab_black[i])
                                        self.tab_black[i].x = r.x
                                        self.tab_black[i].y = r.y
                                        rysuj_plansze(self.tab_white, self.tab_black)
                                    self.turn += 1
                                    turn = False

                            for i in range(len(self.tab_black)):
                                if pos[0] // size == self.tab_black[i].x and pos[1] // size == self.tab_black[i].y and czy_ruch(self.tab_black[i]):
                                    r = ruch(self.tab_black[i])
                                    self.tab_black[i].x =r.x
                                    self.tab_black[i].y=r.y
                                    rysuj_plansze(self.tab_white, self.tab_black)
                                    self.turn += 1
                                    turn = False

                                else:
                                    nie_ma +=1
                                    if nie_ma == len(self.tab_black):
                                        print("Nie wybrałeś czarnego pionka")


#metoda do usowania pionków z planszy
    def usun(self,p, x, y):

        if p.flaga == 2:
            for i in range(len(self.tab_black)):
                if self.tab_black[i].x == x and self.tab_black[i].y == y and plansza[x][y]==3:
                    self.tab_black.remove(self.tab_black[i])
        elif p.flaga == 3:
            for i in range(len(self.tab_white)):
                if self.tab_white[i].x == x and self.tab_white[i].y == y and plansza[x][y]==2:
                    self.tab_white.remove(self.tab_white[i])
        else:
            print("flag error")

#metoda do graficznej reprezentacji aktualnego przebiegu rozgrywki
def rysuj_plansze(tab_white,tab_black):
    Game_window = pygame.display.set_mode((400, 400), 0, 32)
    pygame.display.set_caption('Warcaby')

    for x in range(1, 9):
        for y in range(1, 9):
            if x % 2 != 0:
                if y % 2 != 0:
                    pygame.draw.rect(Game_window, white_color, [size * (x - 1), size * (y - 1), size, size])
                else:
                    pygame.draw.rect(Game_window, black_color, [size * (x - 1), size * (y - 1), size, size])
            else:
                if y % 2 != 0:
                    pygame.draw.rect(Game_window, black_color, [size * (x - 1), size * (y - 1), size, size])
                else:
                    pygame.draw.rect(Game_window, white_color, [size * (x - 1), size * (y - 1), size, size])

    for i in range(len(tab_black)):
        if tab_black[i].flaga == 3:
            Game_window.blit(b_pawn, (tab_black[i].x * size, tab_black[i].y * size))
            pygame.display.flip()
        elif tab_black[i].flaga == 5:
            Game_window.blit(b_queen, (tab_black[i].x * size, tab_black[i].y * size))
            pygame.display.flip()
    for i in range(len(tab_white)):
        if tab_white[i].flaga == 2:
            Game_window.blit(w_pawn, (tab_white[i].x * size, tab_white[i].y * size))
            pygame.display.flip()
        elif tab_white[i].flaga == 4:
            Game_window.blit(w_queen, (tab_white[i].x * size, tab_white[i].y * size))
            pygame.display.flip()
    pygame.display.update()

#funkcja sprawdzajaca mozliwosc bicia
#wywoluje ta funkcje przed kazda tura poniewaz bicie jest obowiazkowe
#sprawdzam wszystkie pionki danego gracza (w zaleznosci od tury) w poszukiwaniu możliwości bica. Jeżeli takie wystąpi, przypisuje do flagi f_bicie wartosc == 1 aby w wyborze pionka, można było wybrać tylko figurę zdolna do bicia
def czy_bicie(turn, tab_white, tab_black):
    print("jestem w funkcji czy_bicie")
    print("czy mozna wykonac bicie ?")
    ilosc_bic = 0
    if turn % 2 == 0 :
        for l in range(len(tab_white)):
            if tab_white[l].x != 1 and tab_white[l].y != 0 and tab_white[l].x != 0 and tab_white[l].y != 1:
                if (plansza[tab_white[l].x - 2][tab_white[l].y - 2] == 1) and plansza[tab_white[l].x - 1][tab_white[l].y - 1] == 3 or plansza[tab_white[l].x - 1][tab_white[l].y - 1] == 5:
                    print("TAK:[lewo-gora]",tab_white[l].x,tab_white[l].y )
                    tab_white[l].f_bicia = 1
                    ilosc_bic += 1

            if tab_white[l].x != 6 and tab_white[l].x != 7 and tab_white[l].y != 0 and tab_white[l].y != 1:
                if (plansza[tab_white[l].x + 2][tab_white[l].y - 2] == 1) and plansza[tab_white[l].x + 1][tab_white[l].y - 1] == 3 or plansza[tab_white[l].x + 1][tab_white[l].y - 1] == 5:
                    print("TAK:[prawo-gora]",tab_white[l].x,tab_white[l].y)
                    tab_white[l].f_bicia = 1
                    ilosc_bic += 1

            if tab_white[l].x != 6 and tab_white[l].x != 7 and tab_white[l].y != 6 and tab_white[l].y != 7:
                if (plansza[tab_white[l].x + 2][tab_white[l].y + 2] == 1) and plansza[tab_white[l].x + 1][tab_white[l].y + 1] == 3 or plansza[tab_white[l].x + 1][tab_white[l].y + 1] == 5:
                    print("TAK:[prawo-dol]",tab_white[l].x,tab_white[l].y)
                    tab_white[l].f_bicia = 1
                    ilosc_bic += 1

            if tab_white[l].x != 0 and tab_white[l].x != 1 and tab_white[l].y != 6 and tab_white[l].y != 7:
                if (plansza[tab_white[l].x - 2][tab_white[l].y + 2] == 1) and plansza[tab_white[l].x - 1][tab_white[l].y + 1] == 3 or plansza[tab_white[l].x - 1][tab_white[l].y + 1] == 5:
                    print("TAK:[lewo-dol]",tab_white[l].x,tab_white[l].y)
                    tab_white[l].f_bicia = 1
                    ilosc_bic += 1

        if ilosc_bic != 0:
            return True
        else:
            print("nie można wykonac bica\nwykonaj zwykly ruch")
            return False

    if turn % 2 != 0:
        for l in range(len(tab_black)):

            if tab_black[l].x != 0 and tab_black[l].x != 1 and tab_black[l].y != 0 and tab_black[l].y != 1:
                if (plansza[tab_black[l].x - 2][tab_black[l].y - 2] == 1) and plansza[tab_black[l].x - 1][tab_black[l].y - 1] == 2 or plansza[tab_black[l].x - 1][tab_black[l].y - 1] == 4:
                    print("TAK:[lewo-gora]",tab_black[l].x,tab_black[l].y)
                    tab_black[l].f_bicia = 1
                    ilosc_bic += 1

            if tab_black[l].x != 6 and tab_black[l].x != 7 and tab_black[l].y != 0 and tab_black[l].y != 1:
                if (plansza[tab_black[l].x + 2][tab_black[l].y - 2] == 1) and plansza[tab_black[l].x + 1][tab_black[l].y - 1] == 2 or plansza[tab_black[l].x + 1][tab_black[l].y - 1] == 4:
                    print("TAK:[prawo-gora]",tab_black[l].x,tab_black[l].y)
                    tab_black[l].f_bicia = 1
                    ilosc_bic += 1

            if tab_black[l].x != 6 and tab_black[l].x != 7 and tab_black[l].y != 6 and tab_black[l].y != 7:
                if (plansza[tab_black[l].x + 2][tab_black[l].y + 2] == 1) and plansza[tab_black[l].x + 1][tab_black[l].y + 1] == 2 or plansza[tab_black[l].x + 1][tab_black[l].y + 1] == 4:
                    print("TAK:[prawo-dol]",tab_black[l].x,tab_black[l].y)
                    tab_black[l].f_bicia = 1
                    ilosc_bic += 1

            if tab_black[l].x != 0 and tab_black[l].x != 1 and tab_black[l].y != 6 and tab_black[l].y != 7:
                if (plansza[tab_black[l].x - 2][tab_black[l].y + 2] == 1) and plansza[tab_black[l].x - 1][tab_black[l].y + 1] == 2 or plansza[tab_black[l].x - 1][tab_black[l].y + 1] == 4:
                    print("TAK:[lewo-dol]",tab_black[l].x,tab_black[l].y)
                    tab_black[l].f_bicia = 1
                    ilosc_bic += 1
        if ilosc_bic != 0:
            return True
        else:
            print("nie można wykonac bica")
            return False

#funkcja bicia
def bicie(pionek):
    print("jestem w funkcji bicie")
    i = 0
    turn = True
    while turn == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                turn = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pionek.f_bicia == 1:
                        # lewo gora
                        if (pos[0] // size + 2 - pionek.x == 0) and (pos[1] // size + 2 - pionek.y == 0) and plansza[pos[0] // size][pos[1] // size] == 1 and plansza[pos[0] // size + 1][pos[1] // size + 1] != pionek.flaga and plansza[pos[0] // size + 1][pos[1] // size + 1] != pionek.flaga + 2:
                            i += 1
                            plansza[pos[0] // size][pos[1] // size] = pionek.flaga
                            plansza[pionek.x][pionek.y] = 1
                            plansza[pionek.x - 1][pionek.y - 1] = 1
                            game.usun(pionek, pionek.x - 1, pionek.y - 1)
                            pionek.x = pos[0] // size
                            pionek.y = pos[1] // size
                            return pionek
                        # prawo gora
                        if (pos[0] // size - 2 - pionek.x == 0) and (pos[1] // size + 2 - pionek.y == 0) and plansza[pos[0] // size][pos[1] // size] == 1 and plansza[pos[0] // size + 1][pos[1] // size + 1] != pionek.flaga and plansza[pos[0] // size + 1][pos[1] // size + 1] != pionek.flaga + 2:
                            i += 1
                            plansza[pos[0] // size][pos[1] // size] = pionek.flaga
                            plansza[pionek.x][pionek.y] = 1
                            plansza[pionek.x + 1][pionek.y - 1] = 1
                            game.usun(pionek, pionek.x + 1, pionek.y - 1)
                            pionek.x = pos[0] // size
                            pionek.y = pos[1] // size
                            return pionek
                        # prawo dol
                        if (pos[0] // size - 2 - pionek.x == 0) and (pos[1] // size - 2 - pionek.y == 0) and plansza[pos[0] // size][pos[1] // size] == 1 and plansza[pos[0] // size + 1][pos[1] // size + 1] != pionek.flaga and plansza[pos[0] // size + 1][pos[1] // size + 1] != pionek.flaga + 2:
                            i += 1
                            plansza[pos[0] // size][pos[1] // size] = pionek.flaga
                            plansza[pionek.x][pionek.y] = 1
                            plansza[pionek.x+1][pionek.y+1] = 1
                            game.usun(pionek,pionek.x+1,pionek.y+1)
                            pionek.x = pos[0] // size
                            pionek.y = pos[1] // size
                            return pionek
                        # lewo dol
                        if (pos[0] // size + 2 - pionek.x == 0) and (pos[1] // size - 2 - pionek.y == 0) and plansza[pos[0] // size][pos[1] // size] == 1 and plansza[pos[0] // size + 1][pos[1] // size + 1] != pionek.flaga and plansza[pos[0] // size + 1][pos[1] // size + 1] != pionek.flaga + 2:
                            i += 1
                            plansza[pos[0] // size][pos[1] // size] = pionek.flaga
                            plansza[pionek.x][pionek.y] = 1
                            plansza[pionek.x - 1][pionek.y + 1] = 1
                            game.usun(pionek, pionek.x - 1, pionek.y + 1)
                            pionek.x = pos[0] // size
                            pionek.y = pos[1] // size
                            return pionek
                        if i != 0:

                            return pionek

                        else:
                            print("koniec bić")
                            turn = False
                    else:
                        print("musisz wybrac pionek ktorym mozna wykonac bicie")

#funkcja sprawdzajaca mozliwosc ruchu przekazanym jako argument pionekim
def czy_ruch(pionek):
    print("jestem w funkcji czy_ruch")

    print("czy mozna wykonac ruch ?")
    i = 0
    if pionek.flaga == 2 :
        if pionek.x != 0 and pionek.y != 0 and plansza[pionek.x - 1][pionek.y - 1] == 1:
            print("[lewo-gora]",pionek.x,pionek.y)
            i +=1

        if pionek.x != 7 and pionek.y != 0 and plansza[pionek.x + 1][pionek.y - 1] == 1:
            print("[prawo-gora]",pionek.x,pionek.y)
            i +=1

        if i != 0:
            return True
        else:
            print("nie można wykonac ruchu")
            return False

    else:

        if pionek.x != 7 and pionek.y != 7 and plansza[pionek.x + 1][pionek.y + 1] == 1:
            print("[prawo-dol]",pionek.x,pionek.y)
            i += 1

        if pionek.x != 0 and pionek.y != 7 and plansza[pionek.x - 1][pionek.y + 1] == 1:
            print("[lewo-dol]",pionek.x,pionek.y)
            i += 1

        if i != 0:
            return True
        else:
            print("nie można wykonac ruchu")
            return False

#funkcja ruchu
def ruch(pionek):
    print("jestem w funkcji ruch")

    game = True
    while game == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if (plansza[pos[0]//size][pos[1]//size] == 1):
                        if (pos[0] // size - pionek.x == -1 or pos[0] // size - pionek.x == 1) and (pos[1] // size - pionek.y == 1): #dla bialych
                            plansza[pionek.x][pionek.y] = 1
                            pionek.x = pos[0] // size
                            pionek.y = pos[1] // size
                            plansza[pionek.x][pionek.y] = pionek.flaga
                            return pionek
                        if (pos[0] // size - pionek.x == -1 or pos[0] // size - pionek.x == 1) and (pos[1] // size - pionek.y == -1): #dla czarnych
                            plansza[pionek.x][pionek.y] = 1
                            pionek.x = pos[0] // size
                            pionek.y = pos[1] // size
                            plansza[pionek.x][pionek.y] = pionek.flaga
                            return pionek
                        else:
                            print("nie można poruszyc sie w wyznaczona pozycje {funkcja czy_ruch}")

                    if plansza[pos[0]//size][pos[1]//size] == 0:
                        print("wybrane pole nie jest czarne")

game = Warcaby()
game.start()
#game.rysuj_plansze()
while True:
    print("============================")
    game.choice_function()
    #game.rysuj_plansze()
