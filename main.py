import pygame
#5,6

plansza = 8 * [0]
for i in range(8):
    plansza[i]= [0]*8

SIZE = 50
WHITE_COLOR = [200, 200, 200]
BLACK_COLOR = [100, 100, 100]
WHITE_PAWN = pygame.transform.scale(pygame.image.load("pawn_white.png"), (SIZE, SIZE))
BLACK_PAWN = pygame.transform.scale(pygame.image.load("pawn_black.png"), (SIZE, SIZE))
WHITE_QUEEN = pygame.transform.scale(pygame.image.load("queen_white.png"), (SIZE, SIZE))
BLACK_QUEEN = pygame.transform.scale(pygame.image.load("queen_black.png"), (SIZE, SIZE))
POLE_BIALE = 0
POLE_CZARNE = 1
BIALY_PIONEK = 2
CZARNY_PIONEK = 3
BIALA_DAMKA = 4
CZARNA_DAMKA = 5


class Pionek:
    def __init__(self, flaga):
        self.x = 0
        self.y = 0
        self.flaga_figury = flaga  #flaga koloru i wartosci(pionek badz damka)
        self.flaga_bicia = 0

class Warcaby:
    def __init__(self):
        self.tab_white =[]
        self.tab_black =[]
        self.turn = 0

#metoda ktora uzupelnia poczatkowe wspolrzedne pionkow dla obu stron
#przypisuje współżędne pionkom na tablicy 8x8
    def start(self):
        """
        Wypełniam planszę oraz tablice białych/czarnych pionków odpowiednimi flagami:
            0 - pole białe
            1 - pole czarne
            2 - pionek biały
            3 - pionek czarny
            4 - biala damka
            5 - czarna damka
        """
        tab_black = []
        tab_white = []

        #wypełniam plansze pionkami z odpowiednimi wspolrzednymi
        # czarne
        for i in range(0, 12):
            tab_black.append(Pionek(CZARNY_PIONEK)) #wytłumaczenie na początku metody
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
            tab_white.append(Pionek(BIALY_PIONEK)) #wytłumaczenie na początku metody
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

        # pionki czarne
        for y in range(0, 3):
            for x in range(0, 8):
                if y % 2 == 0:
                    if x % 2 == 0:
                        plansza[x][y] = POLE_BIALE
                    else:
                        plansza[x][y] = CZARNY_PIONEK
                else:
                    if x % 2 == 0:
                        plansza[x][y] = CZARNY_PIONEK
                    else:
                        plansza[x][y] = POLE_BIALE
        # puste pola
        for y in range(3, 5):
            for x in range(0, 8):
                if y % 2 == 0:
                    if x % 2 == 0:
                        plansza[x][y] = POLE_BIALE
                    else:
                        plansza[x][y] = POLE_CZARNE
                else:
                    if x % 2 == 0:
                        plansza[x][y] = POLE_CZARNE
                    else:
                        plansza[x][y] = POLE_BIALE
        # pionki biale
        for y in range(5, 8):
            for x in range(0, 8):
                if y % 2 == 0:
                    if x % 2 == 0:
                        plansza[x][y] = POLE_BIALE
                    else:
                        plansza[x][y] = BIALY_PIONEK
                else:
                    if x % 2 == 0:
                        plansza[x][y] = BIALY_PIONEK
                    else:
                        plansza[x][y] = POLE_BIALE

#metoda ruchu i bicia z instrukcjami logicznymi
    def choice_function(self):
        if not self.tab_white:
            print("Wygral gracz czarny")
            exit()
        if not self.tab_black:
            print("Wygral gracz bialy")
            exit()
        rysuj_plansze(self.tab_white, self.tab_black)
        ilosc_ruchu = 0
        nic_wiecej =0
#biały
        if self.turn % 2 == 0:
            print("biały rusza: tura:",self.turn)
            bicie_turn = czy_bicie(self.turn,self.tab_white,self.tab_black)
            for i in range(len(self.tab_white)):
                if self.tab_white[i].flaga_bicia == 0:
                    ilosc_ruchu += 1
            turn = True
            while turn == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        turn = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            pos = pygame.mouse.get_pos()
                            if ilosc_ruchu != len(self.tab_white):
                                for i in range(len(self.tab_white)):
                                    if pos[0] // SIZE == self.tab_white[i].x and pos[1] // SIZE == self.tab_white[i].y and self.tab_white[i].flaga_bicia == 1:
                                        while bicie_turn:
                                            nowa_pozycja_bicia = bicie(self.tab_white[i])
                                            self.tab_white[i].x = nowa_pozycja_bicia.x
                                            self.tab_white[i].y = nowa_pozycja_bicia.y
                                            rysuj_plansze(self.tab_white, self.tab_black)
                                            reprezentacja_terminal()
                                            bicie_turn = czy_bicie(self.turn, self.tab_white, self.tab_black)
                                        self.turn += 1
                                        turn = False
                                    else:
                                        nic_wiecej += 1
                                        if nic_wiecej == len(self.tab_white):
                                            print("musisz wybrac pionka ktorym mozna wykonac bicie")
                                            nic_wiecej = 0
                            if ilosc_ruchu == len(self.tab_white):
                                for i in range(len(self.tab_white)):
                                    if pos[0] // SIZE == self.tab_white[i].x and pos[1] // SIZE == self.tab_white[i].y and czy_ruch(self.tab_white[i]):
                                        nowa_pozycja_ruchu = ruch(self.tab_white[i])
                                        self.tab_white[i].x = nowa_pozycja_ruchu.x
                                        self.tab_white[i].y = nowa_pozycja_ruchu.y
                                        self.turn += 1
                                        turn = False
                                    else:
                                        nic_wiecej += 1
                                        if nic_wiecej == len(self.tab_white):
                                            print("Nie wybrałeś bialego pionka")
                                            nic_wiecej = 0
            for i in range(len(self.tab_white)):
                if self.tab_white[i].y == 0:
                    self.tab_white[i].flaga_figury = BIALA_DAMKA
                    plansza[self.tab_white[i].x][self.tab_white[i].y] = BIALA_DAMKA
#czarny
        else:
            print("czarny rusza: tura:",self.turn)
            bicie_turn = czy_bicie(self.turn,self.tab_white,self.tab_black)
            for i in range(len(self.tab_black)):
                if self.tab_black[i].flaga_bicia == 0:
                    ilosc_ruchu += 1
            turn = True
            while turn == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        turn = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            pos = pygame.mouse.get_pos()
                            if ilosc_ruchu != len(self.tab_black):
                                for i in range(len(self.tab_black)):
                                    if pos[0] // SIZE == self.tab_black[i].x and pos[1] // SIZE == self.tab_black[i].y and self.tab_black[i].flaga_bicia == 1:
                                        while bicie_turn:
                                            nowa_pozycja_bicia = bicie(self.tab_black[i])
                                            self.tab_black[i].x = nowa_pozycja_bicia.x
                                            self.tab_black[i].y = nowa_pozycja_bicia.y
                                            rysuj_plansze(self.tab_white, self.tab_black)
                                            reprezentacja_terminal()
                                            bicie_turn = czy_bicie(self.turn, self.tab_white, self.tab_black)
                                        self.turn += 1
                                        turn = False
                                    else:
                                        nic_wiecej += 1
                                        if nic_wiecej == len(self.tab_black):
                                            print("musisz wybrac pionka ktorym mozna wykonac bicie")
                                            nic_wiecej = 0
                            if ilosc_ruchu == len(self.tab_black):
                                for i in range(len(self.tab_black)):
                                    if pos[0] // SIZE == self.tab_black[i].x and pos[1] // SIZE == self.tab_black[i].y and czy_ruch(self.tab_black[i]):
                                        nowa_pozycja_ruchu = ruch(self.tab_black[i])
                                        self.tab_black[i].x = nowa_pozycja_ruchu.x
                                        self.tab_black[i].y = nowa_pozycja_ruchu.y
                                        self.turn += 1
                                        turn = False
                                    else:
                                        nic_wiecej += 1
                                        if nic_wiecej == len(self.tab_black):
                                            print("Nie wybrałeś czarnego pionka")
                                            nic_wiecej = 0
            for i in range(len(self.tab_black)):
                if self.tab_black[i].y == 7:
                    self.tab_black[i].flaga_figury = CZARNA_DAMKA
                    plansza[self.tab_black[i].x][self.tab_black[i].y] = CZARNA_DAMKA

#metoda do usowania pionków z planszy
    def usun(self, pionek, usun_x, usun_y):
        if pionek.flaga_figury == BIALY_PIONEK or pionek.flaga_figury == BIALA_DAMKA and plansza[usun_x][usun_y] == CZARNY_PIONEK or plansza[usun_x][usun_y] == CZARNA_DAMKA:
            for i in range(len(self.tab_black)):
                if self.tab_black[i].x == usun_x and self.tab_black[i].y == usun_y :
                    self.tab_black.remove(self.tab_black[i])
                    plansza[usun_x][usun_y] = POLE_CZARNE
                    plansza[pionek.x][pionek.y] = POLE_CZARNE
                    break
        if pionek.flaga_figury == CZARNY_PIONEK or pionek.flaga_figury == CZARNA_DAMKA and plansza[usun_x][usun_y] == BIALY_PIONEK or plansza[usun_x][usun_y] == BIALA_DAMKA:
            for i in range(len(self.tab_white)):
                if self.tab_white[i].x == usun_x and self.tab_white[i].y == usun_y :
                    self.tab_white.remove(self.tab_white[i])
                    plansza[usun_x][usun_y] = POLE_CZARNE
                    plansza[pionek.x][pionek.y] = POLE_CZARNE
                    break

#metoda do graficznej reprezentacji aktualnego przebiegu rozgrywki
def rysuj_plansze(tab_white,tab_black):
    Game_window = pygame.display.set_mode((400, 400), 0, 32)
    pygame.display.set_caption('Warcaby')

    for x in range(1, 9):
        for y in range(1, 9):
            if x % 2 != 0:
                if y % 2 != 0:
                    pygame.draw.rect(Game_window, WHITE_COLOR, [SIZE * (x - 1), SIZE * (y - 1), SIZE, SIZE])
                else:
                    pygame.draw.rect(Game_window, BLACK_COLOR, [SIZE * (x - 1), SIZE * (y - 1), SIZE, SIZE])
            else:
                if y % 2 != 0:
                    pygame.draw.rect(Game_window, BLACK_COLOR, [SIZE * (x - 1), SIZE * (y - 1), SIZE, SIZE])
                else:
                    pygame.draw.rect(Game_window, WHITE_COLOR, [SIZE * (x - 1), SIZE * (y - 1), SIZE, SIZE])

    for i in range(len(tab_black)):
        if tab_black[i].flaga_figury == CZARNY_PIONEK:
            Game_window.blit(BLACK_PAWN, (tab_black[i].x * SIZE, tab_black[i].y * SIZE))
            pygame.display.flip()
        elif tab_black[i].flaga_figury == CZARNA_DAMKA:
            Game_window.blit(BLACK_QUEEN, (tab_black[i].x * SIZE, tab_black[i].y * SIZE))
            pygame.display.flip()
    for i in range(len(tab_white)):
        if tab_white[i].flaga_figury == BIALY_PIONEK:
            Game_window.blit(WHITE_PAWN, (tab_white[i].x * SIZE, tab_white[i].y * SIZE))
            pygame.display.flip()
        elif tab_white[i].flaga_figury == BIALA_DAMKA:
            Game_window.blit(WHITE_QUEEN, (tab_white[i].x * SIZE, tab_white[i].y * SIZE))
            pygame.display.flip()
    pygame.display.update()

#funkcja sprawdzajaca mozliwosc bicia
#poniewaz bicie jest obowiazkowe to wywoluje ta funkcje na poczatku kazdej tury
#sprawdzam wszystkie pionki danego gracza (w zaleznosci od tury) w poszukiwaniu możliwości bica. Jeżeli takie wystąpi, przypisuje do flagi pionka f_bicie wartosc == 1 aby w wyborze pionka, można było wybrać tylko figurę zdolna do bicia
def czy_bicie(turn, tab_white, tab_black):
    print("jestem w funkcji czy_bicie")
    print("czy mozna wykonac bicie ?")
    ilosc_bic = 0
    if turn % 2 == 0 :
        for l in range(len(tab_white)):
            if tab_white[l].flaga_figury == BIALY_PIONEK:
                if tab_white[l].x != 1 and tab_white[l].y != 0 and tab_white[l].x != 0 and tab_white[l].y != 1:
                    if (plansza[tab_white[l].x - 2][tab_white[l].y - 2] == POLE_CZARNE) and (plansza[tab_white[l].x - 1][tab_white[l].y - 1] == CZARNY_PIONEK or plansza[tab_white[l].x - 1][tab_white[l].y - 1] == CZARNA_DAMKA):
                        print("TAK:[lewo-gora]",tab_white[l].x,tab_white[l].y )
                        tab_white[l].flaga_bicia = 1
                        ilosc_bic += 1

                if tab_white[l].x != 6 and tab_white[l].x != 7 and tab_white[l].y != 0 and tab_white[l].y != 1:
                    if (plansza[tab_white[l].x + 2][tab_white[l].y - 2] == POLE_CZARNE) and (plansza[tab_white[l].x + 1][tab_white[l].y - 1] == CZARNY_PIONEK or plansza[tab_white[l].x + 1][tab_white[l].y - 1] == CZARNA_DAMKA):
                        print("TAK:[prawo-gora]",tab_white[l].x,tab_white[l].y)
                        tab_white[l].flaga_bicia = 1
                        ilosc_bic += 1

                if tab_white[l].x != 6 and tab_white[l].x != 7 and tab_white[l].y != 6 and tab_white[l].y != 7:
                    if (plansza[tab_white[l].x + 2][tab_white[l].y + 2] == POLE_CZARNE) and (plansza[tab_white[l].x + 1][tab_white[l].y + 1] == CZARNY_PIONEK or plansza[tab_white[l].x + 1][tab_white[l].y + 1] == CZARNA_DAMKA):
                        print("TAK:[prawo-dol]",tab_white[l].x,tab_white[l].y)
                        tab_white[l].flaga_bicia = 1
                        ilosc_bic += 1

                if tab_white[l].x != 0 and tab_white[l].x != 1 and tab_white[l].y != 6 and tab_white[l].y != 7:
                    if (plansza[tab_white[l].x - 2][tab_white[l].y + 2] == POLE_CZARNE) and (plansza[tab_white[l].x - 1][tab_white[l].y + 1] == CZARNY_PIONEK or plansza[tab_white[l].x - 1][tab_white[l].y + 1] == CZARNA_DAMKA):
                        print("TAK:[lewo-dol]",tab_white[l].x,tab_white[l].y)
                        tab_white[l].flaga_bicia = 1
                        ilosc_bic += 1

            if tab_white[l].flaga_figury == BIALA_DAMKA:
                if tab_white[l].x != 1 and tab_white[l].y != 0 and tab_white[l].x != 0 and tab_white[l].y != 1:
                    for i in range(1, 5):
                        if (tab_white[l].x - i == 1 or tab_white[l].y - i == 1 or tab_white[l].x - i == 0 or tab_white[l].y - i == 0):
                            break
                        elif (tab_white[l].x - i != 1 and tab_white[l].y - i != 1 and tab_white[l].x - i != 0 and tab_white[l].y - i != 0):
                            if plansza[tab_white[l].x - i][tab_white[l].y - i] != POLE_CZARNE and plansza[tab_white[l].x - i - 1][tab_white[l].y - i - 1] == POLE_CZARNE:
                                if (plansza[tab_white[l].x - i][tab_white[l].y - i] == CZARNY_PIONEK or plansza[tab_white[l].x - i][tab_white[l].y - i] == CZARNA_DAMKA) and (plansza[tab_white[l].x - i + 1][tab_white[l].y - i + 1] == POLE_CZARNE or plansza[tab_white[l].x - i + 1][tab_white[l].y - i + 1] == BIALA_DAMKA):
                                    print("TAK:[lewo-gora]", tab_white[l].x, tab_white[l].y)
                                    tab_white[l].flaga_bicia = 1
                                    ilosc_bic += 1

                if tab_white[l].x != 6 and tab_white[l].x != 7 and tab_white[l].y != 0 and tab_white[l].y != 1:
                    for i in range(1, 5):
                        if (tab_white[l].x + i == 6 or tab_white[l].y - i == 1 or tab_white[l].x + i == 7 or tab_white[l].y - i == 0):
                            break
                        elif (tab_white[l].x + i != 6 and tab_white[l].y - i != 1 and tab_white[l].x + i != 7 and tab_white[l].y - i != 0):
                            if plansza[tab_white[l].x + i][tab_white[l].y - i] != POLE_CZARNE and plansza[tab_white[l].x + i + 1][tab_white[l].y - i - 1] == POLE_CZARNE:
                                if (plansza[tab_white[l].x + i][tab_white[l].y - i] == CZARNY_PIONEK or plansza[tab_white[l].x + i][tab_white[l].y - i] == CZARNA_DAMKA) and (plansza[tab_white[l].x + i - 1][tab_white[l].y - i + 1] == POLE_CZARNE or plansza[tab_white[l].x + i - 1][tab_white[l].y - i + 1] == BIALA_DAMKA):
                                    print("TAK:[prawo-gora]", tab_white[l].x, tab_white[l].y)
                                    tab_white[l].flaga_bicia = 1
                                    ilosc_bic += 1

                if tab_white[l].x != 6 and tab_white[l].x != 7 and tab_white[l].y != 6 and tab_white[l].y != 7:
                    for i in range(1, 5):
                        if (tab_white[l].x + i == 6 or tab_white[l].y + i == 6 or tab_white[l].x + i == 7 or tab_white[l].y + i == 7):
                            break
                        elif (tab_white[l].x + i != 6 and tab_white[l].y + i != 6 and tab_white[l].x + i != 7 and tab_white[l].y + i != 7):
                            if plansza[tab_white[l].x + i][tab_white[l].y + i] != POLE_CZARNE and plansza[tab_white[l].x + i + 1][tab_white[l].y + i + 1] == POLE_CZARNE:
                                if (plansza[tab_white[l].x + i][tab_white[l].y + i] == CZARNY_PIONEK or plansza[tab_white[l].x + i][tab_white[l].y + i] == CZARNA_DAMKA) and (plansza[tab_white[l].x + i - 1][tab_white[l].y + i - 1] == POLE_CZARNE or plansza[tab_white[l].x + i - 1][tab_white[l].y + i - 1] == BIALA_DAMKA):
                                    print("TAK:[prawo-dol]", tab_white[l].x, tab_white[l].y)
                                    tab_white[l].flaga_bicia = 1
                                    ilosc_bic += 1

                if tab_white[l].x != 0 and tab_white[l].x != 1 and tab_white[l].y != 6 and tab_white[l].y != 7:
                    for i in range(1, 5):
                        if (tab_white[l].x - i == 1 or tab_white[l].y + i == 6 or tab_white[l].x - i == 0 or tab_white[l].y + i == 7):
                            break
                        elif (tab_white[l].x - i != 1 and tab_white[l].y + i != 6 and tab_white[l].x - i != 0 and tab_white[l].y + i != 7):
                            if plansza[tab_white[l].x - i][tab_white[l].y + i] != POLE_CZARNE and plansza[tab_white[l].x - i - 1][tab_white[l].y + i + 1] == POLE_CZARNE:
                                if (plansza[tab_white[l].x - i][tab_white[l].y + i] == CZARNY_PIONEK or plansza[tab_white[l].x - i][tab_white[l].y + i] == CZARNA_DAMKA) and (plansza[tab_white[l].x - i + 1][tab_white[l].y + i - 1] == POLE_CZARNE or plansza[tab_white[l].x - i + 1][tab_white[l].y + i - 1] == BIALA_DAMKA):
                                    print("TAK:[lewo-dol]", tab_white[l].x, tab_white[l].y)
                                    tab_white[l].flaga_bicia = 1
                                    ilosc_bic += 1

    if turn % 2 != 0:
        for l in range(len(tab_black)):
            if tab_black[l].flaga_figury == CZARNY_PIONEK:
                if tab_black[l].x != 0 and tab_black[l].x != 1 and tab_black[l].y != 0 and tab_black[l].y != 1:
                    if (plansza[tab_black[l].x - 2][tab_black[l].y - 2] == POLE_CZARNE) and plansza[tab_black[l].x - 1][tab_black[l].y - 1] == BIALY_PIONEK or plansza[tab_black[l].x - 1][tab_black[l].y - 1] == BIALA_DAMKA:
                        print("TAK:[lewo-gora]",tab_black[l].x,tab_black[l].y)
                        tab_black[l].flaga_bicia = 1
                        ilosc_bic += 1

                if tab_black[l].x != 6 and tab_black[l].x != 7 and tab_black[l].y != 0 and tab_black[l].y != 1:
                    if (plansza[tab_black[l].x + 2][tab_black[l].y - 2] == POLE_CZARNE) and plansza[tab_black[l].x + 1][tab_black[l].y - 1] == BIALY_PIONEK or plansza[tab_black[l].x + 1][tab_black[l].y - 1] == BIALA_DAMKA:
                        print("TAK:[prawo-gora]",tab_black[l].x,tab_black[l].y)
                        tab_black[l].flaga_bicia = 1
                        ilosc_bic += 1

                if tab_black[l].x != 6 and tab_black[l].x != 7 and tab_black[l].y != 6 and tab_black[l].y != 7:
                    if (plansza[tab_black[l].x + 2][tab_black[l].y + 2] == POLE_CZARNE) and plansza[tab_black[l].x + 1][tab_black[l].y + 1] == BIALY_PIONEK or plansza[tab_black[l].x + 1][tab_black[l].y + 1] == BIALA_DAMKA:
                        print("TAK:[prawo-dol]",tab_black[l].x,tab_black[l].y)
                        tab_black[l].flaga_bicia = 1
                        ilosc_bic += 1

                if tab_black[l].x != 0 and tab_black[l].x != 1 and tab_black[l].y != 6 and tab_black[l].y != 7:
                    if (plansza[tab_black[l].x - 2][tab_black[l].y + 2] == POLE_CZARNE) and plansza[tab_black[l].x - 1][tab_black[l].y + 1] == BIALY_PIONEK or plansza[tab_black[l].x - 1][tab_black[l].y + 1] == BIALA_DAMKA:
                        print("TAK:[lewo-dol]",tab_black[l].x,tab_black[l].y)
                        tab_black[l].flaga_bicia = 1
                        ilosc_bic += 1

            if tab_black[l].flaga_figury == CZARNA_DAMKA:
                if tab_black[l].x != 1 and tab_black[l].y != 0 and tab_black[l].x != 0 and tab_black[l].y != 1:
                    for i in range(1, 5):
                        if (tab_black[l].x + i == 0 or tab_black[l].y + i == 0 or tab_black[l].x + i == 1 or tab_black[l].y + i == 1):
                            break
                        if (tab_black[l].x - i != 1 and tab_black[l].y - i != 1 and tab_black[l].x - i != 0 and tab_black[l].y - i != 0):
                            if plansza[tab_black[l].x - i][tab_black[l].y - i] != POLE_CZARNE and plansza[tab_black[l].x - i - 1][tab_black[l].y - i - 1] == POLE_CZARNE:
                                if (plansza[tab_black[l].x - i][tab_black[l].y - i] == BIALY_PIONEK or plansza[tab_black[l].x - i][tab_black[l].y - i] == BIALA_DAMKA) and (plansza[tab_black[l].x - i + 1][tab_black[l].y - i + 1] == POLE_CZARNE or plansza[tab_black[l].x - i + 1][tab_black[l].y - i + 1] == CZARNA_DAMKA):
                                    print("TAK:[lewo-gora]", tab_black[l].x, tab_black[l].y)
                                    tab_black[l].flaga_bicia = 1
                                    ilosc_bic += 1

                if tab_black[l].x != 6 and tab_black[l].x != 7 and tab_black[l].y != 0 and tab_black[l].y != 1:
                    for i in range(1, 5):
                        if (tab_black[l].x + i == 6 or tab_black[l].y + i == 0 or tab_black[l].x + i == 7 or tab_black[l].y + i == 1):
                            break
                        elif (tab_black[l].x + i != 6 and tab_black[l].y - i != 1 and tab_black[l].x + i != 7 and tab_black[l].y - i != 0):
                            if plansza[tab_black[l].x + i][tab_black[l].y - i] != POLE_CZARNE and plansza[tab_black[l].x + i + 1][tab_black[l].y - i - 1] == POLE_CZARNE:
                                if (plansza[tab_black[l].x + i][tab_black[l].y - i] == BIALY_PIONEK or plansza[tab_black[l].x + i][tab_black[l].y - i] == BIALA_DAMKA) and (plansza[tab_black[l].x + i - 1][tab_black[l].y - i + 1] == POLE_CZARNE or plansza[tab_black[l].x + i - 1][tab_black[l].y - i + 1] == CZARNA_DAMKA):
                                    print("TAK:[prawo-gora]", tab_black[l].x, tab_black[l].y)
                                    tab_black[l].flaga_bicia = 1
                                    ilosc_bic += 1

                if tab_black[l].x != 6 and tab_black[l].x != 7 and tab_black[l].y != 6 and tab_black[l].y != 7:
                    for i in range(1, 5):
                        if (tab_black[l].x + i == 6 or tab_black[l].y + i == 6 or tab_black[l].x + i == 7 or tab_black[l].y + i == 7):
                            break
                        elif (tab_black[l].x + i != 6 and tab_black[l].y + i != 6 and tab_black[l].x + i != 7 and tab_black[l].y + i != 7) :
                            if plansza[tab_black[l].x + i][tab_black[l].y + i] != POLE_CZARNE and plansza[tab_black[l].x + i + 1][tab_black[l].y + i + 1] == POLE_CZARNE:
                                if (plansza[tab_black[l].x + i][tab_black[l].y + i] == BIALY_PIONEK or plansza[tab_black[l].x + i][tab_black[l].y + i] == BIALA_DAMKA) and (plansza[tab_black[l].x + i - 1][tab_black[l].y + i - 1] == POLE_CZARNE or plansza[tab_black[l].x + i - 1][tab_black[l].y + i - 1] == CZARNA_DAMKA):
                                    print("TAK:[prawo-dol]", tab_black[l].x, tab_black[l].y)
                                    tab_black[l].flaga_bicia = 1
                                    ilosc_bic += 1

                if tab_black[l].x != 0 and tab_black[l].x != 1 and tab_black[l].y != 6 and tab_black[l].y != 7:
                    for i in range(1, 5):
                        if (tab_black[l].x + i == 0 or tab_black[l].y + i == 6 or tab_black[l].x + i == 1 or tab_black[l].y + i == 7):
                            break
                        elif (tab_black[l].x - i != 1 and tab_black[l].y + i != 6 and tab_black[l].x - i != 0 and tab_black[l].y + i != 7) :
                            if plansza[tab_black[l].x - i][tab_black[l].y + i] != POLE_CZARNE and plansza[tab_black[l].x - i - 1][tab_black[l].y + i + 1] == POLE_CZARNE:
                                if (plansza[tab_black[l].x - i][tab_black[l].y + i] == BIALY_PIONEK or plansza[tab_black[l].x - i][tab_black[l].y + i] == BIALA_DAMKA) and (plansza[tab_black[l].x - i + 1][tab_black[l].y + i - 1] == POLE_CZARNE or plansza[tab_black[l].x - i + 1][tab_black[l].y + i - 1] == CZARNA_DAMKA):
                                    print("TAK:[lewo-dol]", tab_black[l].x, tab_black[l].y)
                                    tab_black[l].flaga_bicia = 1
                                    ilosc_bic += 1

    if ilosc_bic != 0:
        return True
    else:
        print("nie mozna wykonac bica\nwykonaj zwykly ruch")
        for i in range(len(tab_white)):
            tab_white[i].flaga_bicia = 0
        for i in range(len(tab_black)):
            tab_black[i].flaga_bicia = 0
        return False

#funkcja bicia
def bicie(pionek):
    print("jestem w funkcji bicie")
    turn = True
    while turn == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                turn = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if plansza[pos[0] // SIZE][pos[1] // SIZE] == 1 :
                        if pionek.flaga_figury == BIALY_PIONEK or pionek.flaga_figury == CZARNY_PIONEK:
                            # lewo gora pionek
                            if (pos[0] // SIZE + 2 - pionek.x == 0) and (pos[1] // SIZE + 2 - pionek.y == 0) and plansza[pos[0] // SIZE + 1][pos[1] // SIZE + 1] != pionek.flaga_figury and plansza[pos[0] // SIZE + 1][pos[1] // SIZE + 1] != pionek.flaga_figury + 2:
                                plansza[pos[0] // SIZE][pos[1] // SIZE] = pionek.flaga_figury
                                game.usun(pionek, pos[0] // SIZE + 1, pos[1] // SIZE + 1)
                                pionek.x = pos[0] // SIZE
                                pionek.y = pos[1] // SIZE
                                return pionek
                            # prawo gora pionek
                            if (pos[0] // SIZE - 2 - pionek.x == 0) and (pos[1] // SIZE + 2 - pionek.y == 0) and plansza[pos[0] // SIZE - 1][pos[1] // SIZE + 1] != pionek.flaga_figury and plansza[pos[0] // SIZE - 1][pos[1] // SIZE + 1] != pionek.flaga_figury + 2:
                                plansza[pos[0] // SIZE][pos[1] // SIZE] = pionek.flaga_figury
                                game.usun(pionek, pos[0] // SIZE - 1, pos[1] // SIZE + 1)
                                pionek.x = pos[0] // SIZE
                                pionek.y = pos[1] // SIZE
                                return pionek
                            # prawo dol pionek
                            if (pos[0] // SIZE - 2 - pionek.x == 0) and (pos[1] // SIZE - 2 - pionek.y == 0) and plansza[pos[0] // SIZE - 1][pos[1] // SIZE - 1] != pionek.flaga_figury and plansza[pos[0] // SIZE - 1][pos[1] // SIZE - 1] != pionek.flaga_figury + 2:
                                plansza[pos[0] // SIZE][pos[1] // SIZE] = pionek.flaga_figury
                                game.usun(pionek, pos[0] // SIZE - 1, pos[1] // SIZE - 1)
                                pionek.x = pos[0] // SIZE
                                pionek.y = pos[1] // SIZE
                                return pionek
                            # lewo dol pionek
                            if (pos[0] // SIZE + 2 - pionek.x == 0) and (pos[1] // SIZE - 2 - pionek.y == 0) and plansza[pos[0] // SIZE + 1][pos[1] // SIZE - 1] != pionek.flaga_figury and plansza[pos[0] // SIZE + 1][pos[1] // SIZE - 1] != pionek.flaga_figury + 2:
                                plansza[pos[0] // SIZE][pos[1] // SIZE] = pionek.flaga_figury
                                game.usun(pionek, pos[0] // SIZE + 1, pos[1] // SIZE - 1)
                                pionek.x = pos[0] // SIZE
                                pionek.y = pos[1] // SIZE
                                return pionek
                            else:
                                print("wybierz pole zgodne z zasadami gry")
                        if pionek.flaga_figury == BIALA_DAMKA or pionek.flaga_figury == CZARNA_DAMKA:
                            # lewo gora damka
                            if pos[0]//SIZE - pionek.x == pos[1]//SIZE - pionek.y and plansza[pos[0] // SIZE + 1][pos[1] // SIZE + 1] != pionek.flaga_figury and plansza[pos[0] // SIZE + 1][pos[1] // SIZE + 1] != pionek.flaga_figury - 2:
                                plansza[pos[0] // SIZE][pos[1] // SIZE] = pionek.flaga_figury
                                game.usun(pionek, pos[0] // SIZE + 1, pos[1] // SIZE + 1)
                                pionek.x = pos[0] // SIZE
                                pionek.y = pos[1] // SIZE
                                return pionek
                            # prawo gora damka
                            if -1*(pos[0] // SIZE - pionek.x) == pos[1]//SIZE - pionek.y and plansza[pos[0] // SIZE - 1][pos[1] // SIZE + 1] != pionek.flaga_figury and plansza[pos[0] // SIZE - 1][pos[1] // SIZE + 1] != pionek.flaga_figury - 2:
                                plansza[pos[0] // SIZE][pos[1] // SIZE] = pionek.flaga_figury
                                game.usun(pionek, pos[0] // SIZE - 1, pos[1] // SIZE + 1)
                                pionek.x = pos[0] // SIZE
                                pionek.y = pos[1] // SIZE
                                return pionek
                            # prawo dol damka
                            if pos[0]//SIZE - pionek.x == pos[1]//SIZE - pionek.y and plansza[pos[0] // SIZE - 1][pos[1] // SIZE - 1] != pionek.flaga_figury and plansza[pos[0] // SIZE - 1][pos[1] // SIZE - 1] != pionek.flaga_figury - 2:
                                plansza[pos[0] // SIZE][pos[1] // SIZE] = pionek.flaga_figury
                                game.usun(pionek, pos[0] // SIZE - 1, pos[1] // SIZE - 1)
                                pionek.x = pos[0] // SIZE
                                pionek.y = pos[1] // SIZE
                                return pionek
                            # lewo dol damka
                            if -1*(pos[0] // SIZE - pionek.x) == pos[1]//SIZE - pionek.y and plansza[pos[0] // SIZE + 1][pos[1] // SIZE - 1] != pionek.flaga_figury and plansza[pos[0] // SIZE + 1][pos[1] // SIZE - 1] != pionek.flaga_figury - 2:
                                plansza[pos[0] // SIZE][pos[1] // SIZE] = pionek.flaga_figury
                                game.usun(pionek, pos[0] // SIZE + 1, pos[1] // SIZE - 1)
                                pionek.x = pos[0] // SIZE
                                pionek.y = pos[1] // SIZE
                                return pionek
                            else:
                                print("wybierz pole zgodne z zasadami gry")

                    elif plansza[pos[0] // SIZE][pos[1] // SIZE] == POLE_BIALE:
                        print("wybrane pole nie jest polem czarnym")
                    else:
                        print("wybrane pole nie jest puste")

#funkcja sprawdzajaca mozliwosc ruchu przekazanym jako argument pionekim
def czy_ruch(pionek):
    print("jestem w funkcji czy_ruch")
    print("czy mozna wykonac ruch ?")
    ilosc_ruchow = 0
    if pionek.flaga_figury == BIALY_PIONEK :
        if pionek.x != 0 and pionek.y != 0 and plansza[pionek.x - 1][pionek.y - 1] == POLE_CZARNE:
            print("[lewo-gora]",pionek.x,pionek.y)
            ilosc_ruchow +=1
        if pionek.x != 7 and pionek.y != 0 and plansza[pionek.x + 1][pionek.y - 1] == POLE_CZARNE:
            print("[prawo-gora]",pionek.x,pionek.y)
            ilosc_ruchow +=1

    if pionek.flaga_figury == CZARNY_PIONEK:
        if pionek.x != 7 and pionek.y != 7 and plansza[pionek.x + 1][pionek.y + 1] == POLE_CZARNE:
            print("[prawo-dol]",pionek.x,pionek.y)
            ilosc_ruchow += 1
        if pionek.x != 0 and pionek.y != 7 and plansza[pionek.x - 1][pionek.y + 1] == POLE_CZARNE:
            print("[lewo-dol]",pionek.x,pionek.y)
            ilosc_ruchow += 1

    if pionek.flaga_figury == BIALA_DAMKA or pionek.flaga_figury == CZARNA_DAMKA:
        if pionek.x != 0 and pionek.y != 0 and plansza[pionek.x - 1][pionek.y - 1] == POLE_CZARNE:
            print("[lewo-gora]",pionek.x,pionek.y)
            ilosc_ruchow +=1
        if pionek.x != 7 and pionek.y != 0 and plansza[pionek.x + 1][pionek.y - 1] == POLE_CZARNE:
            print("[prawo-gora]",pionek.x,pionek.y)
            ilosc_ruchow +=1
        if pionek.x != 7 and pionek.y != 7 and plansza[pionek.x + 1][pionek.y + 1] == POLE_CZARNE:
            print("[prawo-dol]", pionek.x, pionek.y)
            ilosc_ruchow += 1
        if pionek.x != 0 and pionek.y != 7 and plansza[pionek.x - 1][pionek.y + 1] == POLE_CZARNE:
            print("[lewo-dol]", pionek.x, pionek.y)
            ilosc_ruchow += 1
    if ilosc_ruchow != 0:
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
                    if (plansza[pos[0] // SIZE][pos[1] // SIZE] == POLE_CZARNE):
                        if (pos[0] // SIZE - pionek.x == -1 or pos[0] // SIZE - pionek.x == 1) and (pos[1] // SIZE - pionek.y == 1) and pionek.flaga_figury == CZARNY_PIONEK:
                            plansza[pionek.x][pionek.y] = POLE_CZARNE
                            pionek.x = pos[0] // SIZE
                            pionek.y = pos[1] // SIZE
                            plansza[pionek.x][pionek.y] = pionek.flaga_figury
                            return pionek
                        if (pos[0] // SIZE - pionek.x == -1 or pos[0] // SIZE - pionek.x == 1) and (pos[1] // SIZE - pionek.y == -1) and pionek.flaga_figury == BIALY_PIONEK:
                            plansza[pionek.x][pionek.y] = POLE_CZARNE
                            pionek.x = pos[0] // SIZE
                            pionek.y = pos[1] // SIZE
                            plansza[pionek.x][pionek.y] = pionek.flaga_figury
                            return pionek
                        if (pionek.flaga_figury == BIALA_DAMKA or pionek.flaga_figury == CZARNA_DAMKA) and (pos[0] // SIZE - pionek.x == pos[1] // SIZE - pionek.y or pos[0] // SIZE - pionek.x == -1 * (pos[1] // SIZE - pionek.y)):
                            plansza[pionek.x][pionek.y] = POLE_CZARNE
                            pionek.x = pos[0] // SIZE
                            pionek.y = pos[1] // SIZE
                            plansza[pionek.x][pionek.y] = pionek.flaga_figury
                            return pionek
                        else:
                            print("nie można poruszyc sie w wyznaczona pozycje")

                    if plansza[pos[0] // SIZE][pos[1] // SIZE] == POLE_BIALE:
                        print("wybrane pole nie jest czarne")

def reprezentacja_terminal():
    z1 = '[#]'   #chr(9635)
    z2 = '   '   #chr(9634)
    print("     ", end='')
    for x in range(0, 8):
        print("", x,"", end='')

    print("")
    print("  ",end = '')
    for x in range(0,10):
        print(z1, end = '')

    for x in range(0,8):
        print("")
        for y in range(0,8):
            if y == 0:
                print(x,z1,end = '')
            if plansza[y][x] == POLE_BIALE:
                print(z2,end = '')
            if plansza[y][x] == POLE_CZARNE:
                print("   ",end = '')
            if plansza[y][x] == BIALY_PIONEK:
                print(" B ",end = '')
                #bialy.ilosc_pionkow += 1
            if plansza[y][x] == CZARNY_PIONEK:
                print(" C ",end = '')
                #czarny.ilosc_pionkow += 1
            if plansza[y][x] == BIALA_DAMKA:
                print("^B^",end = '')
            if plansza[y][x] == CZARNA_DAMKA:
                print("^C^",end = '')
        print(z1,x,end = '')

    print("")
    print("  ",end = '')
    for x in range(0,10):
        print(z1, end = '')

    print("")
    print("     ", end='')
    for x in range(0, 8):
        print("", x,"", end='')
    print("\n")

game = Warcaby()

def main():
    game.start()
    pygame.font.init()
    while True:
        print("============================")
        reprezentacja_terminal()
        game.choice_function()

main()