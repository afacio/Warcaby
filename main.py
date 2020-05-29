import pygame

plansza = 8 * [0]
for i in range(8):
    plansza[i]= [0]*8

def uzup_plan_pocz():
    """
    0 - pole białe
    1 - pole czarne
    2 - pionek biały
    3 - pionek czarny
    4 - biala damka
    5 - czarna damka
    """

    #pionki czarne
    for y in range(0,3) :
        for x in range(0,8) :
            if y % 2 ==0:
                if x % 2 == 0:
                    plansza[x][y] = 0
                else:
                    plansza[x][y] = 3
            else:
                if x % 2 == 0:
                    plansza[x][y] = 3
                else:
                    plansza[x][y] = 0

    #puste pola
    for y in range(3,5):
        for x in range(0,8):
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

    #pionki biale
    for y in range(5,8):
        for x in range(0,8):
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

"""   for i in range(0,8):
        for j in range(0,8):
            print(plansza[j][i],end='')
        print("") 
"""

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
        self.flaga = f

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

#metoda do graficznej reprezentacji aktualnego przebiegu rozgrywki
    def rysuj_plansze(self):
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

        for i in range(len(self.tab_black)):
            if self.tab_black[i].flaga == 3:
                Game_window.blit(b_pawn, (self.tab_black[i].x * size, self.tab_black[i].y * size))
                pygame.display.flip()
            elif self.tab_black[i].flaga == 5:
                Game_window.blit(b_queen, (self.tab_black[i].x * size, self.tab_black[i].y * size))
                pygame.display.flip()
        for i in range(len(self.tab_white)):
            if self.tab_white[i].flaga == 2:
                Game_window.blit(w_pawn, (self.tab_white[i].x * size, self.tab_white[i].y * size))
                pygame.display.flip()
            elif self.tab_white[i].flaga == 4:
                Game_window.blit(w_queen, (self.tab_white[i].x * size, self.tab_white[i].y * size))
                pygame.display.flip()
        pygame.display.update()

#metoda ruchu i bicia z instrukcjami logicznymi
    def choice_function(self):

#biały
        if self.turn % 2 == 0:
            print("biały rusza")
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
                                if pos[0] // size == self.tab_white[i].x and pos[1] // size == self.tab_white[i].y:
                                    if czy_bicie(self.tab_white[i]):
                                        r = bicie(self.tab_white[i])
                                        self.tab_white[i].x = r.x
                                        self.tab_white[i].y = r.y
                                        # licz_bicie(self.tab_black[i])
                                        self.turn += 1
                                        turn = False
                                    elif czy_ruch(self.tab_white[i]):
                                        r = ruch(self.tab_white[i])
                                        self.tab_white[i].x = r.x
                                        self.tab_white[i].y = r.y
                                        self.turn += 1
                                        turn = False
                                    else:
                                        print("ruch tym pionkiem jest niemozliwy")
                                else:
                                    nie_ma += 1
                                    if nie_ma == len(self.tab_white):
                                        print("Nie wybrałeś bialego pionka")

#czarny
        else:
            print("czarny rusza")
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
                                if pos[0]//size == self.tab_black[i].x and pos[1]//size == self.tab_black[i].y:
                                    if czy_bicie(self.tab_black[i]):
                                        r = bicie(self.tab_black[i])
                                        self.tab_black[i].x = r.x
                                        self.tab_black[i].y = r.y
                                        #licz_bicie(self.tab_black[i])
                                        self.turn += 1
                                        turn = False
                                    elif czy_ruch(self.tab_black[i]):
                                        r = ruch(self.tab_black[i])
                                        self.tab_black[i].x =r.x
                                        self.tab_black[i].y=r.y

                                        self.turn += 1
                                        turn = False
                                    else:
                                        print("ruch tym pionkiem jest niemozliwy")
                                else:
                                    nie_ma +=1
                                    if nie_ma == len(self.tab_black):
                                        print("Nie wybrałeś czarnego pionka")

#funkcja sprawdzajaca mozliwosc bicia przekazanym jako argument pionekim
def czy_bicie(pionek):
    #print(pionek.x, pionek.y, pionek.flaga)
    i = 0
    if pionek.flaga == 2 :
        if pionek.x - 1 != 0 and pionek.y - 1 != 0:
            if (plansza[pionek.x - 2][pionek.y - 2] == 1) and plansza[pionek.x - 1][pionek.y - 1] == 3 or plansza[pionek.x - 1][pionek.y - 1] == 5:
                print("[lewo-gora]")
                i += 1

        if pionek.x + 1 != 7 and pionek.y - 1 != 0:
            if (plansza[pionek.x + 2][pionek.y - 2] == 1) and plansza[pionek.x + 1][pionek.y - 1] == 3 or plansza[pionek.x + 1][pionek.y - 1] == 5:
                print("[prawo-gora]")
                i += 1

        if pionek.x + 1 != 7 and pionek.y + 1 != 7:
            if (plansza[pionek.x + 2][pionek.y + 2] == 1) and plansza[pionek.x + 1][pionek.y + 1] == 3 or plansza[pionek.x + 1][pionek.y + 1] == 5:
                print("[prawo-dol]")
                i += 1

        if pionek.x - 1 != 0 and pionek.y + 1 != 7:
            if (plansza[pionek.x - 2][pionek.y + 2] == 1) and plansza[pionek.x - 1][pionek.y + 1] == 3 or plansza[pionek.x - 1][pionek.y + 1] == 5:
                print("[lewo-dol]")
                i += 1
        if i != 0:
            return True
        else:
            print("nie można wykonac bica \t{funkcja czy_bicie}")
            return False

    elif pionek.flaga == 3:
        if pionek.x - 1 != 0 and pionek.y - 1 != 0:
            if (plansza[pionek.x - 2][pionek.y - 2] == 1) and plansza[pionek.x - 1][pionek.y - 1] == 2 or \
                    plansza[pionek.x - 1][pionek.y - 1] == 4:
                print("[lewo-gora]")
                i += 1

        if pionek.x + 1 != 7 and pionek.y - 1 != 0:
            if (plansza[pionek.x + 2][pionek.y - 2] == 1) and plansza[pionek.x + 1][pionek.y - 1] == 2 or \
                    plansza[pionek.x + 1][pionek.y - 1] == 4:
                print("[prawo-gora]")
                i += 1

        if pionek.x + 1 != 7 and pionek.y + 1 != 7:
            if (plansza[pionek.x + 2][pionek.y + 2] == 1) and plansza[pionek.x + 1][pionek.y + 1] == 2 or \
                    plansza[pionek.x + 1][pionek.y + 1] == 4:
                print("[prawo-dol]")
                i += 1

        if pionek.x - 1 != 0 and pionek.y + 1 != 7:
            if (plansza[pionek.x - 2][pionek.y + 2] == 1) and plansza[pionek.x - 1][pionek.y + 1] == 2 or \
                    plansza[pionek.x - 1][pionek.y + 1] == 4:
                print("[lewo-dol]")
                i += 1
        if i != 0:
            return True
        else:
            print("nie można wykonac bica \t{funkcja czy_bicie}")
            return False
    else:
        print("flag error")

def bicie(pionek):
    ile_razy = 0
    j = True
    while j == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    # lewo gora
                    if (pos[0] // size + 2 - pionek.x == 0) and (pos[1] // size + 2 - pionek.y == 0) and \
                            plansza[pos[0] // size][pos[1]] // size == 1 and plansza[pos[0] // size + 1][
                        pos[1] // size + 1] != pionek.flaga and plansza[pos[0] // size + 1][
                        pos[1] // size + 1] != pionek.flaga + 2:
                        plansza[pos[0] // size][pos[1] // size] = pionek.flaga
                        plansza[pionek.x][pionek.y] = 1
                        pionek.x = pos[0] // size
                        pionek.y = pos[1] // size
                        ile_razy += 1
                        return pionek
                    # prawo gora
                    if (pos[0] // size - 2 - pionek.x == 0) and (pos[1] // size + 2 - pionek.y == 0) and \
                            plansza[pos[0] // size][pos[1]] // size == 1 and plansza[pos[0] // size + 1][
                        pos[1] // size + 1] != pionek.flaga and plansza[pos[0] // size + 1][
                        pos[1] // size + 1] != pionek.flaga + 2:
                        plansza[pos[0] // size][pos[1] // size] = pionek.flaga
                        plansza[pionek.x][pionek.y] = 1
                        pionek.x = pos[0] // size
                        pionek.y = pos[1] // size
                        ile_razy += 1
                        return pionek
                    # prawo dol
                    if (pos[0] // size - 2 - pionek.x == 0) and (pos[1] // size - 2 - pionek.y == 0) and \
                            plansza[pos[0] // size][pos[1]] // size == 1 and plansza[pos[0] // size + 1][
                        pos[1] // size + 1] != pionek.flaga and plansza[pos[0] // size + 1][
                        pos[1] // size + 1] != pionek.flaga + 2:
                        plansza[pos[0] // size][pos[1] // size] = pionek.flaga
                        plansza[pionek.x][pionek.y] = 1
                        pionek.x = pos[0] // size
                        pionek.y = pos[1] // size
                        ile_razy += 1
                        return pionek
                    # lewo dol
                    if (pos[0] // size + 2 - pionek.x == 0) and (pos[1] // size - 2 - pionek.y == 0) and \
                            plansza[pos[0] // size][pos[1]] // size == 1 and plansza[pos[0] // size + 1][
                        pos[1] // size + 1] != pionek.flaga and plansza[pos[0] // size + 1][
                        pos[1] // size + 1] != pionek.flaga + 2:
                        plansza[pos[0] // size][pos[1] // size] = pionek.flaga
                        plansza[pionek.x][pionek.y] = 1
                        pionek.x = pos[0] // size
                        pionek.y = pos[1] // size
                        ile_razy += 1
                        return pionek
                    elif ile_razy != 0:
                        print("koniec bić")


                    else:
                        print("nie można poruszyc sie w wyznaczona pozycje \t{funkcja czy_bicie}")
                        return False

def czy_ruch(pionek):
    i = 0
    if pionek.flaga == 2 :
        if pionek.x != 0 and pionek.y != 0:
            if (plansza[pionek.x - 1][pionek.y - 1] == 1):
                print("[lewo-gora]")
                i +=1
            else:
                print("jestem tu [lewo-gora]")

        if pionek.x != 7 and pionek.y != 0:
            if (plansza[pionek.x + 1][pionek.y - 1] == 1):
                print("[prawo-gora]")
                i +=1
            else:
                print("jestem tu [prawo-gora]")
        if i != 0:
            return True
        else:
            print("nie można wykonac ruchu \t{funkcja czy_ruch}")
            return False

    elif pionek.flaga == 3:

        if pionek.x != 7 and pionek.y != 7:
            if (plansza[pionek.x + 1][pionek.y + 1] == 1):
                print("[prawo-dol]")
                i += 1

        if pionek.x != 0 and pionek.y != 7:
            if (plansza[pionek.x - 1][pionek.y + 1] == 1):
                print("[lewo-dol]")
                i += 1
        if i != 0:
            return True

        else:
            print("nie można wykonac ruchu \t{funkcja czy_ruch}")
            return False
    else:
        print("error")

def ruch(pionek):
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

                    if plansza[pos[0]][pos[1]] == 0:
                        print("wybrane pole nie jest biale")


uzup_plan_pocz()
game = Warcaby()
game.start()
game.rysuj_plansze()
while True:
    game.choice_function()
    game.rysuj_plansze()
