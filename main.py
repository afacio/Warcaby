import pygame
# pylint: disable=C0301
plansza = 8 * [0]
for x in range(8):
    plansza[x] = [0]*8

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
MOVES = [
    (-1, -1),
    (+1, -1),
    (+1, +1),
    (-1, +1)]
'''
MOVES = [LG,PG,PD,LD]
'''


class Pionek:
    def __init__(self, flaga):
        self.wspolrzedna_x = 0
        self.wspolrzedna_y = 0
        self.flaga_figury = flaga  #flaga koloru i wartosci(pionek badz damka)
        self.flaga_bicia = 0

class Warcaby:
    def __init__(self):
        self.tab_white = []
        self.tab_black = []
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
        i = 1
        for j in range(0, 4):
            tab_black[j].wspolrzedna_y = 0
            tab_black[j].wspolrzedna_x = i
            i += 2
        i = 0
        for j in range(4, 8):
            tab_black[j].wspolrzedna_y = 1
            tab_black[j].wspolrzedna_x = i
            i += 2
        i = 1
        for j in range(8, 12):
            tab_black[j].wspolrzedna_y = 2
            tab_black[j].wspolrzedna_x = i
            i += 2
        #biale
        for i in range(0, 12):
            tab_white.append(Pionek(BIALY_PIONEK)) #wytłumaczenie na początku metody
        i = 0
        for j in range(0, 4):
            tab_white[j].wspolrzedna_x = i
            tab_white[j].wspolrzedna_y = 5
            i += 2
        i = 1
        for j in range(4, 8):
            tab_white[j].wspolrzedna_x = i
            tab_white[j].wspolrzedna_y = 6
            i += 2
        i = 0
        for j in range(8, 12):
            tab_white[j].wspolrzedna_x = i
            tab_white[j].wspolrzedna_y = 7
            i += 2

        self.tab_black = tab_black
        self.tab_white = tab_white

        # pionki czarne
        for j in range(0, 3):
            for i in range(0, 8):
                if j % 2 == 0:
                    if i % 2 == 0:
                        plansza[i][j] = POLE_BIALE
                    else:
                        plansza[i][j] = CZARNY_PIONEK
                else:
                    if i % 2 == 0:
                        plansza[i][j] = CZARNY_PIONEK
                    else:
                        plansza[i][j] = POLE_BIALE
        # puste pola
        for j in range(3, 5):
            for i in range(0, 8):
                if j % 2 == 0:
                    if i % 2 == 0:
                        plansza[i][j] = POLE_BIALE
                    else:
                        plansza[i][j] = POLE_CZARNE
                else:
                    if i % 2 == 0:
                        plansza[i][j] = POLE_CZARNE
                    else:
                        plansza[i][j] = POLE_BIALE
        # pionki biale
        for j in range(5, 8):
            for i in range(0, 8):
                if j % 2 == 0:
                    if i % 2 == 0:
                        plansza[i][j] = POLE_BIALE
                    else:
                        plansza[i][j] = BIALY_PIONEK
                else:
                    if i % 2 == 0:
                        plansza[i][j] = BIALY_PIONEK
                    else:
                        plansza[i][j] = POLE_BIALE

#metoda przebiegu gry
    def choice_function(self):
        if not self.tab_white:
            print("Wygral gracz czarny")
            exit()
        if not self.tab_black:
            print("Wygral gracz bialy")
            exit()
        rysuj_plansze(self.tab_white, self.tab_black)
        ilosc_ruchu = 0
        nic_wiecej = 0
        turn = True
#biały
        if self.turn % 2 == 0:
            print("biały rusza: tura:", self.turn)
            bicie_turn = czy_bicie(self.tab_white)
            for pionek in self.tab_white:
                if pionek.flaga_bicia == 0:
                    ilosc_ruchu += 1
            while turn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        turn = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            pos = pygame.mouse.get_pos()
                            if ilosc_ruchu != len(self.tab_white):
                                for pionek in self.tab_white:
                                    if pos[0] // SIZE == pionek.wspolrzedna_x and pos[1] // SIZE == pionek.wspolrzedna_y and pionek.flaga_bicia == 1:
                                        while bicie_turn:
                                            nowa_pozycja_bicia = bicie(pionek)
                                            pionek.wspolrzedna_x = nowa_pozycja_bicia.wspolrzedna_x
                                            pionek.wspolrzedna_y = nowa_pozycja_bicia.wspolrzedna_y
                                            rysuj_plansze(self.tab_white, self.tab_black)
                                            reprezentacja_terminal()
                                            bicie_turn = czy_bicie(self.tab_white)
                                        self.turn += 1
                                        turn = False
                                    else:
                                        nic_wiecej += 1
                                        if nic_wiecej == len(self.tab_white):
                                            print("musisz wybrac pionka ktorym mozna wykonac bicie")
                                            nic_wiecej = 0
                            if ilosc_ruchu == len(self.tab_white):
                                for pionek in self.tab_white:
                                    if pos[0] // SIZE == pionek.wspolrzedna_x and pos[1] // SIZE == pionek.wspolrzedna_y and czy_ruch(pionek):
                                        nowa_pozycja_ruchu = ruch(pionek)
                                        pionek.wspolrzedna_x = nowa_pozycja_ruchu.wspolrzedna_x
                                        pionek.wspolrzedna_y = nowa_pozycja_ruchu.wspolrzedna_y
                                        self.turn += 1
                                        turn = False
                                    else:
                                        nic_wiecej += 1
                                        if nic_wiecej == len(self.tab_white):
                                            print("Wybierz ponownie")
                                            nic_wiecej = 0
            for pionek in self.tab_white:
                if pionek.wspolrzedna_y == 0:
                    pionek.flaga_figury = BIALA_DAMKA
                    plansza[pionek.wspolrzedna_x][pionek.wspolrzedna_y] = BIALA_DAMKA
#czarny
        else:
            print("czarny rusza: tura:", self.turn)
            bicie_turn = czy_bicie(self.tab_black)
            for pionek in self.tab_black:
                if pionek.flaga_bicia == 0:
                    ilosc_ruchu += 1
            while turn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        turn = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            pos = pygame.mouse.get_pos()
                            if ilosc_ruchu != len(self.tab_black):
                                for pionek in self.tab_black:
                                    if pos[0] // SIZE == pionek.wspolrzedna_x and pos[1] // SIZE == pionek.wspolrzedna_y and pionek.flaga_bicia == 1:
                                        while bicie_turn:
                                            nowa_pozycja_bicia = bicie(pionek)
                                            pionek.wspolrzedna_x = nowa_pozycja_bicia.wspolrzedna_x
                                            pionek.wspolrzedna_y = nowa_pozycja_bicia.wspolrzedna_y
                                            rysuj_plansze(self.tab_white, self.tab_black)
                                            reprezentacja_terminal()
                                            bicie_turn = czy_bicie(self.tab_black)
                                        self.turn += 1
                                        turn = False
                                    else:
                                        nic_wiecej += 1
                                        if nic_wiecej == len(self.tab_black):
                                            print("musisz wybrac pionka ktorym mozna wykonac bicie")
                                            nic_wiecej = 0
                            if ilosc_ruchu == len(self.tab_black):
                                for pionek in self.tab_black:
                                    if pos[0] // SIZE == pionek.wspolrzedna_x and pos[1] // SIZE == pionek.wspolrzedna_y and czy_ruch(pionek):
                                        nowa_pozycja_ruchu = ruch(pionek)
                                        pionek.wspolrzedna_x = nowa_pozycja_ruchu.wspolrzedna_x
                                        pionek.wspolrzedna_y = nowa_pozycja_ruchu.wspolrzedna_y
                                        self.turn += 1
                                        turn = False
                                    else:
                                        nic_wiecej += 1
                                        if nic_wiecej == len(self.tab_black):
                                            print("Wybierz ponownie")
                                            nic_wiecej = 0
            for pionek in self.tab_black:
                if pionek.wspolrzedna_y == 7:
                    pionek.flaga_figury = CZARNA_DAMKA
                    plansza[pionek.wspolrzedna_x][pionek.wspolrzedna_y] = CZARNA_DAMKA

#metoda do usowania pionków z planszy
    def usun(self, pionek, usun_x, usun_y):
        if pionek.flaga_figury == BIALY_PIONEK or pionek.flaga_figury == BIALA_DAMKA and plansza[usun_x][usun_y] == CZARNY_PIONEK or plansza[usun_x][usun_y] == CZARNA_DAMKA:
            for figura in self.tab_black:
                if figura.wspolrzedna_x == usun_x and figura.wspolrzedna_y == usun_y:
                    self.tab_black.remove(figura)
                    plansza[usun_x][usun_y] = POLE_CZARNE
                    plansza[pionek.wspolrzedna_x][pionek.wspolrzedna_y] = POLE_CZARNE
                    break
        if pionek.flaga_figury == CZARNY_PIONEK or pionek.flaga_figury == CZARNA_DAMKA and plansza[usun_x][usun_y] == BIALY_PIONEK or plansza[usun_x][usun_y] == BIALA_DAMKA:
            for figura in self.tab_white:
                if figura.wspolrzedna_x == usun_x and figura.wspolrzedna_y == usun_y:
                    self.tab_white.remove(figura)
                    plansza[usun_x][usun_y] = POLE_CZARNE
                    plansza[pionek.wspolrzedna_x][pionek.wspolrzedna_y] = POLE_CZARNE
                    break

#metoda do graficznej reprezentacji aktualnego przebiegu rozgrywki
def rysuj_plansze(tab_white, tab_black):
    game_window = pygame.display.set_mode((400, 400), 0, 32)
    pygame.display.set_caption('Warcaby')

    for i in range(1, 9):
        for j in range(1, 9):
            if i % 2 != 0:
                if j % 2 != 0:
                    pygame.draw.rect(game_window, WHITE_COLOR, [SIZE * (i - 1), SIZE * (j - 1), SIZE, SIZE])
                else:
                    pygame.draw.rect(game_window, BLACK_COLOR, [SIZE * (i - 1), SIZE * (j - 1), SIZE, SIZE])
            else:
                if j % 2 != 0:
                    pygame.draw.rect(game_window, BLACK_COLOR, [SIZE * (i - 1), SIZE * (j - 1), SIZE, SIZE])
                else:
                    pygame.draw.rect(game_window, WHITE_COLOR, [SIZE * (i - 1), SIZE * (j - 1), SIZE, SIZE])

    for pionek in tab_black:
        if pionek.flaga_figury == CZARNY_PIONEK:
            game_window.blit(BLACK_PAWN, (pionek.wspolrzedna_x * SIZE, pionek.wspolrzedna_y * SIZE))
            pygame.display.flip()
        elif pionek.flaga_figury == CZARNA_DAMKA:
            game_window.blit(BLACK_QUEEN, (pionek.wspolrzedna_x * SIZE, pionek.wspolrzedna_y * SIZE))
            pygame.display.flip()
    for pionek in tab_white:
        if pionek.flaga_figury == BIALY_PIONEK:
            game_window.blit(WHITE_PAWN, (pionek.wspolrzedna_x * SIZE, pionek.wspolrzedna_y * SIZE))
            pygame.display.flip()
        elif pionek.flaga_figury == BIALA_DAMKA:
            game_window.blit(WHITE_QUEEN, (pionek.wspolrzedna_x * SIZE, pionek.wspolrzedna_y * SIZE))
            pygame.display.flip()
    pygame.display.update()

#funkcja sprawdzajaca mozliwosc bicia
#poniewaz bicie jest obowiazkowe to wywoluje ta funkcje na poczatku kazdej tury
#sprawdzam wszystkie pionki danego gracza (w zaleznosci od tury) w poszukiwaniu możliwości bica. Jeżeli takie wystąpi, przypisuje do flagi pionka f_bicie wartosc == 1 aby w wyborze pionka, można było wybrać tylko figurę zdolna do bicia
def czy_bicie(tablica):
    print("jestem w funkcji czy_bicie")
    print("czy mozna wykonac bicie ?")
    ilosc_bic = 0
    for element in tablica:
        if BIALY_PIONEK <= element.flaga_figury <= CZARNY_PIONEK:
            for delta_x, delta_y in MOVES:
                x1, y1 = element.wspolrzedna_x + delta_x, element.wspolrzedna_y + delta_y
                x2, y2 = element.wspolrzedna_x + 2 * delta_x, element.wspolrzedna_y + 2 * delta_y
                if not x1 == 7 and not y1 == 7 and not x1 == 0 and not y1 == 0:
                    if not 0 <= element.wspolrzedna_x <= 1 and not 0 <= element.wspolrzedna_y <= 1 and element.wspolrzedna_x - x1 == 1 and element.wspolrzedna_y - y1 == 1:
                        if plansza[x2][y2] == POLE_CZARNE and plansza[x1][y1] != element.flaga_figury and plansza[x1][y1] != element.flaga_figury + 2 and plansza[x1][y1] != POLE_CZARNE:
                            print("TAK:[lewo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                            element.flaga_bicia = 1
                            ilosc_bic += 1
                    if not 6 <= element.wspolrzedna_x <= 7 and not 0 <= element.wspolrzedna_y <= 1 and element.wspolrzedna_x - x1 == -1 and element.wspolrzedna_y - y1 == 1:
                        if plansza[x2][y2] == POLE_CZARNE and plansza[x1][y1] != element.flaga_figury and plansza[x1][y1] != element.flaga_figury + 2 and plansza[x1][y1] != POLE_CZARNE:
                            print("TAK:[prawo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                            element.flaga_bicia = 1
                            ilosc_bic += 1
                    if not 6 <= element.wspolrzedna_x <= 7 and not 6 <= element.wspolrzedna_y <= 7 and element.wspolrzedna_x - x1 == -1 and element.wspolrzedna_y - y1 == -1:
                        if plansza[x2][y2] == POLE_CZARNE and plansza[x1][y1] != element.flaga_figury and plansza[x1][y1] != element.flaga_figury + 2 and plansza[x1][y1] != POLE_CZARNE:
                            print("TAK:[prawo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                            element.flaga_bicia = 1
                            ilosc_bic += 1
                    if not 0 <= element.wspolrzedna_x <= 1 and not 6 <= element.wspolrzedna_y <= 7 and element.wspolrzedna_x - x1 == 1 and element.wspolrzedna_y - y1 == -1:
                        if plansza[x2][y2] == POLE_CZARNE and plansza[x1][y1] != element.flaga_figury and plansza[x1][y1] != element.flaga_figury + 2 and plansza[x1][y1] != POLE_CZARNE:
                            print("TAK:[lewo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                            element.flaga_bicia = 1
                            ilosc_bic += 1
        if BIALA_DAMKA <= element.flaga_figury <= CZARNA_DAMKA:
            for i in range(1, 5):
                for delta_x, delta_y in MOVES:
                    x3, y3 = element.wspolrzedna_x + i * delta_x, element.wspolrzedna_y + i * delta_y
                    if not 0 <= element.wspolrzedna_x <= 1 and not 0 <= element.wspolrzedna_y <= 1:
                        if 0 <= x3 <= 1 or 0 <= y3 <= 1:
                            break
                        if not 0 <= x3 <= 1 and not 0 <= y3 <= 1:
                            if plansza[x3][y3] != POLE_CZARNE and plansza[x3 - 1][y3 - 1] == POLE_CZARNE and (plansza[x3 + 1][y3 + 1] == POLE_CZARNE or plansza[x3 + 1][y3 + 1] == element.flaga_figury):
                                if plansza[x3][y3] != element.flaga_figury or plansza[x3][y3] != element.flaga_figury - 2:
                                    print("TAK:[lewo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                                    element.flaga_bicia = 1
                                    ilosc_bic += 1
                    if not 6 <= element.wspolrzedna_x <= 7 and not 0 <= element.wspolrzedna_y <= 1:
                        if 6 <= x3 <= 7 or 0 <= y3 <= 1:
                            break
                        if not 6 <= x3 <= 7 and not 0 <= y3 <= 1:
                            if plansza[x3][y3] != POLE_CZARNE and plansza[x3 + 1][y3 - 1] == POLE_CZARNE and (plansza[x3 - 1][y3 + 1] == POLE_CZARNE or plansza[x3 - 1][y3 + 1] == element.flaga_figury):
                                if plansza[x3][y3] != element.flaga_figury or plansza[x3][y3] != element.flaga_figury - 2:
                                    print("TAK:[prawo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                                    element.flaga_bicia = 1
                                    ilosc_bic += 1
                    if not 6 <= element.wspolrzedna_x <= 7 and not 6 <= element.wspolrzedna_y <= 7:
                        if 6 <= x3 <= 7 or 6 <= y3 <= 7:
                            break
                        if not 6 <= x3 <= 7 and not 6 <= y3 <= 7:
                            if plansza[x3][y3] != POLE_CZARNE and plansza[x3 + 1][y3 + 1] == POLE_CZARNE and (plansza[x3 - 1][y3 - 1] == POLE_CZARNE or plansza[x3 - 1][y3 - 1] == element.flaga_figury):
                                if plansza[x3][y3] != element.flaga_figury or plansza[x3][y3] != element.flaga_figury - 2:
                                    print("TAK:[prawo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                                    element.flaga_bicia = 1
                                    ilosc_bic += 1
                    if not 0 <= element.wspolrzedna_x <= 1 and not 6 <= element.wspolrzedna_y <= 7:
                        if 0 <= x3 <= 1 or 6 <= y3 <= 7:
                            break
                        if not 0 <= x3 <= 1 and not 6 <= y3 <= 7:
                            if plansza[x3][y3] != POLE_CZARNE and plansza[x3 - 1][y3 + 1] == POLE_CZARNE and (plansza[x3 + 1][y3 - 1] == POLE_CZARNE or plansza[x3 + 1][y3 - 1] == element.flaga_figury):
                                if plansza[x3][y3] != element.flaga_figury or plansza[x3][y3] != element.flaga_figury - 2:
                                    print("TAK:[lewo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                                    element.flaga_bicia = 1
                                    ilosc_bic += 1
    if ilosc_bic != 0:
        return True
    if ilosc_bic == 0:
        print("nie mozna wykonac bica\nwykonaj zwykly ruch")
        for pionek in tablica:
            pionek.flaga_bicia = 0
        return False

def podstawianie_dla_bicia(pionek, x1, x2, y1, y2):
    plansza[x2][y2] = pionek.flaga_figury
    gra.usun(pionek, x1, y1)
    pionek.wspolrzedna_x = x2
    pionek.wspolrzedna_y = y2
    return pionek

#funkcja bicia
def bicie(pionek):
    print("jestem w funkcji bicie")
    turn = True
    while turn:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    x2, y2 = pos[0] // SIZE, pos[1] // SIZE
                    if plansza[x2][y2] == POLE_CZARNE:
                        for delta_x, delta_y in MOVES:
                            x1, y1 = pionek.wspolrzedna_x + delta_x, pionek.wspolrzedna_y + delta_y
                            if BIALY_PIONEK <= pionek.flaga_figury <= CZARNY_PIONEK:
                                # lewo gora pionek
                                if not pionek.wspolrzedna_x == 0 and not pionek.wspolrzedna_y == 0 and pionek.wspolrzedna_x - x1 == 1 and pionek.wspolrzedna_y - y1 == 1:
                                    if plansza[x1][y1] != POLE_CZARNE and plansza[x1][y1] != pionek.flaga_figury and plansza[x1][y1] != pionek.flaga_figury + 2:
                                        pionek = podstawianie_dla_bicia(pionek, x1, x2, y1, y2)
                                        return pionek
                                # prawo gora pionek
                                if not pionek.wspolrzedna_x == 7 and not pionek.wspolrzedna_y == 0 and pionek.wspolrzedna_x - x1 == -1 and pionek.wspolrzedna_y - y1 == 1:
                                    if plansza[x1][y1] != POLE_CZARNE and plansza[x1][y1] != pionek.flaga_figury and plansza[x1][y1] != pionek.flaga_figury + 2:
                                        pionek = podstawianie_dla_bicia(pionek, x1, x2, y1, y2)
                                        return pionek
                                # prawo dol pionek
                                if not pionek.wspolrzedna_x == 7 and not pionek.wspolrzedna_y == 7 and pionek.wspolrzedna_x - x1 == -1 and pionek.wspolrzedna_y - y1 == -1:
                                    if plansza[x1][y1] != POLE_CZARNE and plansza[x1][y1] != pionek.flaga_figury and plansza[x1][y1] != pionek.flaga_figury + 2:
                                        pionek = podstawianie_dla_bicia(pionek, x1, x2, y1, y2)
                                        return pionek
                                # lewo dol pionek
                                if not pionek.wspolrzedna_x == 0 and not pionek.wspolrzedna_y == 7 and pionek.wspolrzedna_x - x1 == 1 and pionek.wspolrzedna_y - y1 == -1:
                                    if plansza[x1][y1] != POLE_CZARNE and plansza[x1][y1] != pionek.flaga_figury and plansza[x1][y1] != pionek.flaga_figury + 2:
                                        pionek = podstawianie_dla_bicia(pionek, x1, x2, y1, y2)
                                        return pionek
                            if BIALA_DAMKA <= pionek.flaga_figury <= CZARNA_DAMKA:
                                # lewo gora damka
                                if x2 - pionek.wspolrzedna_x == y2 - pionek.wspolrzedna_y and plansza[x2 + 1][y2 + 1] != pionek.flaga_figury and plansza[x2 + 1][y2 + 1] != pionek.flaga_figury - 2:
                                    pionek = podstawianie_dla_bicia(pionek, x2 + 1, x2, y2 + 1, y2)
                                    return pionek
                                # prawo gora damka
                                if -1 * (x2 - pionek.wspolrzedna_x) == y2 - pionek.wspolrzedna_y and plansza[x2 - 1][x2 + 1] != pionek.flaga_figury and plansza[x2 - 1][x2 + 1] != pionek.flaga_figury - 2:
                                    pionek = podstawianie_dla_bicia(pionek, x2 - 1, x2, y2 + 1, y2)
                                    return pionek
                                # prawo dol damka
                                if x2 - pionek.wspolrzedna_x == y2 - pionek.wspolrzedna_y and plansza[x2 - 1][y2 - 1] != pionek.flaga_figury and plansza[x2 - 1][y2 - 1] != pionek.flaga_figury - 2:
                                    pionek = podstawianie_dla_bicia(pionek, x2 - 1, x2, y2 - 1, y2)
                                    return pionek
                                # lewo dol damka
                                if -1 * (x2 - pionek.wspolrzedna_x) == y2 - pionek.wspolrzedna_y and plansza[x2 + 1][y2 - 1] != pionek.flaga_figury and plansza[x2 + 1][y2 - 1] != pionek.flaga_figury - 2:
                                    pionek = podstawianie_dla_bicia(pionek, x2 + 1, x2, y2 - 1, y2)
                                    return pionek
                            else:
                                print("wybierz pole zgodne z zasadami gry")
                    if plansza[x2][y2] == POLE_BIALE:
                        print("wybrane pole nie jest polem czarnym")
                    else:
                        print("wybrane pole nie jest puste")

#funkcja sprawdzajaca mozliwosc ruchu przekazanym jako argument pionekim
def czy_ruch(pionek):
    print("jestem w funkcji czy_ruch")
    print("czy mozna wykonac ruch ?")
    ilosc_ruchow = 0
    for delta_x, delta_y in MOVES:
        x1, y1 = pionek.wspolrzedna_x + delta_x, pionek.wspolrzedna_y + delta_y
        if pionek.flaga_figury == BIALY_PIONEK or CZARNA_DAMKA >= pionek.flaga_figury >= BIALA_DAMKA:
            if not pionek.wspolrzedna_x == 0 and not pionek.wspolrzedna_y == 0 and pionek.wspolrzedna_x - x1 == 1 and pionek.wspolrzedna_y - y1 == 1 and plansza[x1][y1] == POLE_CZARNE:
                print("[lewo-gora]", pionek.wspolrzedna_x, pionek.wspolrzedna_y)
                ilosc_ruchow += 1
            if not pionek.wspolrzedna_x == 7 and not pionek.wspolrzedna_y == 0 and pionek.wspolrzedna_x - x1 == -1 and pionek.wspolrzedna_y - y1 == 1 and plansza[x1][y1] == POLE_CZARNE:
                print("[prawo-gora]", pionek.wspolrzedna_x, pionek.wspolrzedna_y)
                ilosc_ruchow += 1
        if pionek.flaga_figury == CZARNY_PIONEK or CZARNA_DAMKA >= pionek.flaga_figury >= BIALA_DAMKA:
            if not pionek.wspolrzedna_x == 7 and not pionek.wspolrzedna_y == 7 and pionek.wspolrzedna_x - x1 == -1 and pionek.wspolrzedna_y - y1 == -1 and plansza[x1][y1] == POLE_CZARNE:
                print("[prawo-dol]", pionek.wspolrzedna_x, pionek.wspolrzedna_y)
                ilosc_ruchow += 1
            if not pionek.wspolrzedna_x == 0 and not pionek.wspolrzedna_y == 7 and pionek.wspolrzedna_x - x1 == 1 and pionek.wspolrzedna_y - y1 == -1 and plansza[x1][y1] == POLE_CZARNE:
                print("[lewo-dol]", pionek.wspolrzedna_x, pionek.wspolrzedna_y)
                ilosc_ruchow += 1
    if ilosc_ruchow != 0:
        return True
    if ilosc_ruchow == 0:
        print("nie można wykonac ruchu tym pionkiem")
        return False

#funkcja stworzona do podstawiania wartosci po wykonanym ruchu
def podstawianie_dla_ruchu(pionek, x2, y2):
    plansza[pionek.wspolrzedna_x][pionek.wspolrzedna_y] = POLE_CZARNE
    pionek.wspolrzedna_x = x2
    pionek.wspolrzedna_y = y2
    plansza[x2][y2] = pionek.flaga_figury
    return pionek

#funkcja ruchu
def ruch(pionek):
    print("jestem w funkcji ruch")
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    x2, y2 = pos[0] // SIZE, pos[1] // SIZE
                    if plansza[x2][y2] == POLE_CZARNE:
                        for delta_x, delta_y in MOVES:
                            x1, y1 = pionek.wspolrzedna_x + delta_x, pionek.wspolrzedna_y + delta_y
                            if (x2 == x1 and y2 == y1) and y2 - pionek.wspolrzedna_y == 1 and pionek.flaga_figury == CZARNY_PIONEK:
                                pionek = podstawianie_dla_ruchu(pionek, x2, y2)
                                return pionek
                            if (x2 == x1 and y2 == y1) and y2 - pionek.wspolrzedna_y == -1 and pionek.flaga_figury == BIALY_PIONEK:
                                pionek = podstawianie_dla_ruchu(pionek, x2, y2)
                                return pionek
                            if CZARNA_DAMKA >= pionek.flaga_figury >= BIALA_DAMKA:
                                if x2 - pionek.wspolrzedna_x == y2 - pionek.wspolrzedna_y or x2 - pionek.wspolrzedna_x == -1 * (y2 - pionek.wspolrzedna_y):
                                    pionek = podstawianie_dla_ruchu(pionek, x2, y2)
                                    return pionek
                    else:
                        print("nie można poruszyc sie w wyznaczona pozycje")
                    if plansza[x2][y2] == POLE_BIALE:
                        print("wybrane pole nie jest czarne")

#funkcja do graficznej reprezentacji planszy wyswietlanej w terminalu
def reprezentacja_terminal():
    znak_1 = '[#]'   #chr(9635)
    znak_2 = '   '   #chr(9634)
    print("     ", end='')
    for i in range(0, 8):
        print("", i, "", end='')
    print("")
    print("  ", end='')
    for i in range(0, 10):
        print(znak_1, end='')
    for i in range(0, 8):
        print("")
        for j in range(0, 8):
            if j == 0:
                print(i, znak_1, end='')
            if plansza[j][i] == POLE_BIALE:
                print(znak_2, end='')
            if plansza[j][i] == POLE_CZARNE:
                print("   ", end='')
            if plansza[j][i] == BIALY_PIONEK:
                print(" B ", end='')
                #bialy.ilosc_pionkow += 1
            if plansza[j][i] == CZARNY_PIONEK:
                print(" C ", end='')
                #czarny.ilosc_pionkow += 1
            if plansza[j][i] == BIALA_DAMKA:
                print("^B^", end='')
            if plansza[j][i] == CZARNA_DAMKA:
                print("^C^", end='')
        print(znak_1, i, end='')
    print("")
    print("  ", end='')
    for i in range(0, 10):
        print(znak_1, end='')
    print("")
    print("     ", end='')
    for i in range(0, 8):
        print("", i, "", end='')
    print("\n")

gra = Warcaby()

def main():
    gra.start()
    pygame.font.init()
    while True:
        print("============================")
        reprezentacja_terminal()
        gra.choice_function()

if __name__ == '__main__':
    main()