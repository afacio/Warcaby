import pygame
import sys
import assets
# pylint: disable=C0301

SIZE = 80
BOARD_SIZE = 8
WHITE_COLOR = [200, 200, 200]
BLACK_COLOR = [100, 100, 100]
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
    (-1, +1),
]
#poczatkowe pozycje dla pionkow
POZYCJA_PARZYSTA_X = [0, 2, 4, 6]
POZYCJA_NIE_PARZYSTA_X = [1, 3, 5, 7]
POZYCJA_Y = [0, 1, 2, 5, 6, 7]

ZNAK_1 = '[#]'
ZNAK_2 = '   '

plansza = BOARD_SIZE * [0]
for x in range(BOARD_SIZE):
    plansza[x] = [0]*BOARD_SIZE

class Pionek:
    def __init__(self, x, y, waga):
        self.wspolrzedna_x = x
        self.wspolrzedna_y = y
        self.flaga_wagi = waga  #flaga koloru i wartosci(pionek badz damka)
        self.flaga_bicia = False

class Warcaby:
    def __init__(self):
        self.tab_white = []
        self.tab_black = []
        self.turn = 0

        # metoda ktora uzupelnia poczatkowe wspolrzedne pionkow dla obu stron
        # przypisuje współżędne pionkom na tablicy 8x8

        for j in POZYCJA_Y:
            if j == 0:
                for i in POZYCJA_NIE_PARZYSTA_X:
                    self.tab_black.append(Pionek(i, j, CZARNY_PIONEK))
            if j == 1:
                for i in POZYCJA_PARZYSTA_X:
                    self.tab_black.append(Pionek(i, j, CZARNY_PIONEK))
            if j == 2:
                for i in POZYCJA_NIE_PARZYSTA_X:
                    self.tab_black.append(Pionek(i, j, CZARNY_PIONEK))
            if j == 5:
                for i in POZYCJA_PARZYSTA_X:
                    self.tab_white.append(Pionek(i, j, BIALY_PIONEK))
            if j == 6:
                for i in POZYCJA_NIE_PARZYSTA_X:
                    self.tab_white.append(Pionek(i, j, BIALY_PIONEK))
            if j == 7:
                for i in POZYCJA_PARZYSTA_X:
                    self.tab_white.append(Pionek(i, j, BIALY_PIONEK))

        # pionki czarne
        for j in range(3):
            for i in range(8):
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
            for i in range(8):
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
            for i in range(8):
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
        if self.turn % 2 == 0:
            przebieg_gry(self.tab_white, self.turn, self.tab_white, self.tab_black)
            for pionek in self.tab_white:
                if pionek.wspolrzedna_y == 0:
                    pionek.flaga_wagi = BIALA_DAMKA
                    plansza[pionek.wspolrzedna_x][pionek.wspolrzedna_y] = BIALA_DAMKA
            self.turn += 1
        if self.turn % 2 != 0:
            przebieg_gry(self.tab_black, self.turn, self.tab_white, self.tab_black)
            for pionek in self.tab_black:
                if pionek.wspolrzedna_y == 7:
                    pionek.flaga_wagi = CZARNA_DAMKA
                    plansza[pionek.wspolrzedna_x][pionek.wspolrzedna_y] = CZARNA_DAMKA
            self.turn += 1
        print("Koniec tury")

    #metoda do usowania pionków z planszy
    def usun(self, pionek, usun_x, usun_y):
        if pionek in self.tab_white:
            for figura in self.tab_black:
                if figura.wspolrzedna_x == usun_x and figura.wspolrzedna_y == usun_y:
                    self.tab_black.remove(figura)
                    break
        if pionek in self.tab_black:
            for figura in self.tab_white:
                if figura.wspolrzedna_x == usun_x and figura.wspolrzedna_y == usun_y:
                    self.tab_white.remove(figura)
                    break
        plansza[usun_x][usun_y] = POLE_CZARNE
        plansza[pionek.wspolrzedna_x][pionek.wspolrzedna_y] = POLE_CZARNE

def przebieg_gry(tablica, tura, tab_white, tab_black):
    ilosc_ruchu = 0
    nic_wiecej = 0
    turn = True
    rysuj_plansze(tab_white, tab_black)
    reprezentacja_terminal()
    if not tablica:
        if tura % 2 == 0:
            print("Wygral gracz czarny")
        else:
            print("Wygral gracz bialy")
        sys.exit()
    if tura % 2 == 0:
        print("bialy rusza: tura:", tura)
    else:
        print("czarny rusza: tura:", tura)
    bicie_turn = czy_bicie(tablica)
    for pionek in tablica:
        if not pionek.flaga_bicia:
            ilosc_ruchu += 1
    while turn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                turn = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    x1, y1 = pos[0] // SIZE, pos[1] // SIZE
                    if ilosc_ruchu != len(tablica):
                        for pionek in tablica:
                            if x1 == pionek.wspolrzedna_x and y1 == pionek.wspolrzedna_y and pionek.flaga_bicia:
                                while bicie_turn:
                                    nowa_pozycja_bicia = bicie(pionek)
                                    pionek.wspolrzedna_x = nowa_pozycja_bicia.wspolrzedna_x
                                    pionek.wspolrzedna_y = nowa_pozycja_bicia.wspolrzedna_y
                                    rysuj_plansze(tab_white, tab_black)
                                    reprezentacja_terminal()
                                    bicie_turn = czy_bicie(tablica)
                                    turn = False
                                else:
                                    nic_wiecej += 1
                                if nic_wiecej == len(tablica):
                                    print("musisz wybrac pionka ktorym mozna wykonac bicie")
                                    nic_wiecej = 0
                    if ilosc_ruchu == len(tablica):
                        for pionek in tablica:
                            if x1 == pionek.wspolrzedna_x and y1 == pionek.wspolrzedna_y and czy_ruch(pionek):
                                nowa_pozycja_ruchu = ruch(pionek)
                                pionek.wspolrzedna_x = nowa_pozycja_ruchu.wspolrzedna_x
                                pionek.wspolrzedna_y = nowa_pozycja_ruchu.wspolrzedna_y
                                turn = False
                            else:
                                nic_wiecej += 1
                                if nic_wiecej == len(tablica):
                                    print("Wybierz ponownie")
                                    nic_wiecej = 0

#metoda do graficznej reprezentacji rozgrywki za użyciem biblioteki pygame
def rysuj_plansze(tab_white, tab_black):
    game_window = pygame.display.set_mode((SIZE * 8, SIZE * 8), 0, 32)
    pygame.display.set_caption('Warcaby')
#rysuje plansze wymiarow 8x8
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i % 2 != 0:
                if j % 2 != 0:
                    pygame.draw.rect(game_window, WHITE_COLOR, [SIZE * (i), SIZE * (j), SIZE, SIZE])
                else:
                    pygame.draw.rect(game_window, BLACK_COLOR, [SIZE * (i), SIZE * (j), SIZE, SIZE])
            else:
                if j % 2 != 0:
                    pygame.draw.rect(game_window, BLACK_COLOR, [SIZE * (i), SIZE * (j), SIZE, SIZE])
                else:
                    pygame.draw.rect(game_window, WHITE_COLOR, [SIZE * (i), SIZE * (j), SIZE, SIZE])
    a = assets.Assets
    for pionek in tab_black:
        if pionek.flaga_wagi == CZARNY_PIONEK:
            game_window.blit(a.BLACK_PAWN, (pionek.wspolrzedna_x * SIZE, pionek.wspolrzedna_y * SIZE))
            pygame.display.flip()
        elif pionek.flaga_wagi == CZARNA_DAMKA:
            game_window.blit(a.BLACK_QUEEN, (pionek.wspolrzedna_x * SIZE, pionek.wspolrzedna_y * SIZE))
            pygame.display.flip()
    for pionek in tab_white:
        if pionek.flaga_wagi == BIALY_PIONEK:
            game_window.blit(a.WHITE_PAWN, (pionek.wspolrzedna_x * SIZE, pionek.wspolrzedna_y * SIZE))
            pygame.display.flip()
        elif pionek.flaga_wagi == BIALA_DAMKA:
            game_window.blit(a.WHITE_QUEEN, (pionek.wspolrzedna_x * SIZE, pionek.wspolrzedna_y * SIZE))
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
        if element.flaga_wagi in (CZARNY_PIONEK, BIALY_PIONEK):
            for delta_x, delta_y in MOVES:
                x1, y1 = element.wspolrzedna_x + delta_x, element.wspolrzedna_y + delta_y
                x2, y2 = element.wspolrzedna_x + 2 * delta_x, element.wspolrzedna_y + 2 * delta_y
                if not x1 >= 7 and not y1 >= 7 and not x1 <= 0 and not y1 <= 0:
                    if element.wspolrzedna_x not in (0, 1) and element.wspolrzedna_y not in (0, 1) and x2 - x1 == -1 and y2 - y1 == -1:
                        if plansza[x2][y2] == POLE_CZARNE and plansza[x1][y1] not in (element.flaga_wagi, element.flaga_wagi + 2, POLE_CZARNE):
                            print("TAK:[lewo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                            element.flaga_bicia = True
                            ilosc_bic += 1
                    if element.wspolrzedna_x not in (6, 7) and element.wspolrzedna_y not in (0, 1) and x2 - x1 == 1 and y2 - y1 == -1:
                        if plansza[x2][y2] == POLE_CZARNE and plansza[x1][y1] not in (element.flaga_wagi, element.flaga_wagi + 2, POLE_CZARNE):
                            print("TAK:[prawo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                            element.flaga_bicia = True
                            ilosc_bic += 1
                    if element.wspolrzedna_x not in (6, 7) and element.wspolrzedna_y not in (6, 7) and x2 - x1 == 1 and y2 - y1 == 1:
                        if plansza[x2][y2] == POLE_CZARNE and plansza[x1][y1] not in (element.flaga_wagi, element.flaga_wagi + 2, POLE_CZARNE):
                            print("TAK:[prawo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                            element.flaga_bicia = True
                            ilosc_bic += 1
                    if element.wspolrzedna_x not in (0, 1) and element.wspolrzedna_y not in (6, 7) and x2 - x1 == -1 and y2 - y1 == 1:
                        if plansza[x2][y2] == POLE_CZARNE and plansza[x1][y1] not in (element.flaga_wagi, element.flaga_wagi + 2, POLE_CZARNE):
                            print("TAK:[lewo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                            element.flaga_bicia = True
                            ilosc_bic += 1
        if element.flaga_wagi in (CZARNA_DAMKA, BIALA_DAMKA):
            for delta_x, delta_y in MOVES:
                for i in range(1, 5):
                    x1, y1 = element.wspolrzedna_x + (i - 1) * delta_x, element.wspolrzedna_y + (i - 1) * delta_y
                    x2, y2 = element.wspolrzedna_x + i * delta_x, element.wspolrzedna_y + i * delta_y
                    x3, y3 = element.wspolrzedna_x + (i + 1) * delta_x, element.wspolrzedna_y + (i + 1) * delta_y
                    if element.wspolrzedna_x not in (0, 1) and element.wspolrzedna_y not in (0, 1) and x2 - x1 == -1 and y2 - y1 == -1:
                        if x2 <= 1 or y2 <= 1:
                            break
                        if plansza[x2][y2] != POLE_CZARNE and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (POLE_CZARNE, element.flaga_wagi):
                            if plansza[x2][y2] not in (element.flaga_wagi, element.flaga_wagi - 2):
                                print("TAK:[lewo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                                element.flaga_bicia = True
                                ilosc_bic += 1
                    if element.wspolrzedna_x not in (6, 7) and element.wspolrzedna_y not in (0, 1) and x2 - x1 == 1 and y2 - y1 == -1:
                        if 6 <= x2 or y2 <= 1:
                            break
                        if plansza[x2][y2] != POLE_CZARNE and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (POLE_CZARNE, element.flaga_wagi):
                            if plansza[x2][y2] not in (element.flaga_wagi, element.flaga_wagi - 2):
                                print("TAK:[prawo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                                element.flaga_bicia = True
                                ilosc_bic += 1
                    if element.wspolrzedna_x not in (6, 7) and element.wspolrzedna_y not in (6, 7) and x2 - x1 == 1 and y2 - y1 == 1:
                        if 6 <= x2 or 6 <= y2:
                            break
                        if plansza[x2][y2] != POLE_CZARNE and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (POLE_CZARNE, element.flaga_wagi):
                            if plansza[x2][y2] not in (element.flaga_wagi, element.flaga_wagi - 2):
                                print("TAK:[prawo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                                element.flaga_bicia = True
                                ilosc_bic += 1
                    if element.wspolrzedna_x not in (0, 1) and element.wspolrzedna_y not in (6, 7) and x2 - x1 == -1 and y2 - y1 == 1:
                        if x2 <= 1 or 6 <= y2:
                            break
                        if plansza[x2][y2] != POLE_CZARNE and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (POLE_CZARNE, element.flaga_wagi):
                            if plansza[x2][y2] not in (element.flaga_wagi, element.flaga_wagi - 2):
                                print("TAK:[lewo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                                element.flaga_bicia = True
                                ilosc_bic += 1
    if ilosc_bic != 0:
        return True
    if ilosc_bic == 0:
        print("nie mozna wykonac bica\nwykonaj zwykly ruch")
        for pionek in tablica:
            pionek.flaga_bicia = False
        return False

def podstawianie_dla_bicia(pionek, x1, y1, x2, y2):
    plansza[x2][y2] = pionek.flaga_wagi
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
                            if pionek.flaga_wagi in (CZARNY_PIONEK, BIALY_PIONEK):
                                # lewo gora pionek
                                if pionek.wspolrzedna_x not in (0, 1) and pionek.wspolrzedna_y not in (0, 1) and x2 - x1 == -1 and y2 - y1 == -1:
                                    if plansza[x1][y1] not in (pionek.flaga_wagi, pionek.flaga_wagi + 2, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x1, y1, x2, y2)
                                        return pionek
                                # prawo gora pionek
                                if pionek.wspolrzedna_x not in (6, 7) and pionek.wspolrzedna_y not in (0, 1) and x2 - x1 == 1 and y2 - y1 == -1:
                                    if plansza[x1][y1] not in (pionek.flaga_wagi, pionek.flaga_wagi + 2, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x1, y1, x2, y2)
                                        return pionek
                                # prawo dol pionek
                                if pionek.wspolrzedna_x not in (6, 7) and pionek.wspolrzedna_y not in (6, 7) and x2 - x1 == 1 and y2 - y1 == 1:
                                    if plansza[x1][y1] not in (pionek.flaga_wagi, pionek.flaga_wagi + 2, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x1, y1, x2, y2)
                                        return pionek
                                # lewo dol pionek
                                if pionek.wspolrzedna_x not in (0, 1) and pionek.wspolrzedna_y not in (6, 7) and x2 - x1 == -1 and y2 - y1 == 1:
                                    if plansza[x1][y1] not in (pionek.flaga_wagi, pionek.flaga_wagi + 2, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x1, y1, x2, y2)
                                        return pionek
                            if pionek.flaga_wagi in (CZARNA_DAMKA, BIALA_DAMKA):
                                for delta_x, delta_y in MOVES:
                                    for i in range(1, 5):
                                        x1, y1 = pionek.wspolrzedna_x + (i - 1) * delta_x, pionek.wspolrzedna_y + (i - 1) * delta_y
                                        x2, y2 = pionek.wspolrzedna_x + i * delta_x, pionek.wspolrzedna_y + i * delta_y
                                        x3, y3 = pionek.wspolrzedna_x + (i + 1) * delta_x, pionek.wspolrzedna_y + (i + 1) * delta_y
                                # lewo gora damka
                                if pionek.wspolrzedna_x not in (0, 1) and pionek.wspolrzedna_y not in (0, 1) and x2 - x1 == -1 and y2 - y1 == -1:
                                    if plansza[x2][y2] not in (pionek.flaga_wagi, pionek.flaga_wagi - 2, POLE_CZARNE) and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (pionek.flaga_wagi, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x2 , y2, x3, y3)
                                        return pionek
                                # prawo gora damka
                                if pionek.wspolrzedna_x not in (6, 7) and pionek.wspolrzedna_y not in (0, 1) and x2 - x1 == 1 and y2 - y1 == -1:
                                    if plansza[x2][y2] not in (pionek.flaga_wagi, pionek.flaga_wagi - 2, POLE_CZARNE) and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (pionek.flaga_wagi, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x2, y2, x3, y3)
                                        return pionek
                                # prawo dol damka
                                if pionek.wspolrzedna_x not in (6, 7) and pionek.wspolrzedna_y not in (6, 7) and x2 - x1 == 1 and y2 - y1 == 1:
                                    if plansza[x2][y2] not in (pionek.flaga_wagi, pionek.flaga_wagi - 2, POLE_CZARNE) and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (pionek.flaga_wagi, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x2, y2, x3, y3)
                                        return pionek
                                # lewo dol damka
                                if pionek.wspolrzedna_x not in (0, 1) and pionek.wspolrzedna_y not in (6, 7) and x2 - x1 == -1 and y2 - y1 == 1:
                                    if plansza[x2][y2] not in (pionek.flaga_wagi, pionek.flaga_wagi - 2, POLE_CZARNE) and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (pionek.flaga_wagi, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x2, y2, x3, y3)
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
        if pionek.flaga_wagi in (BIALY_PIONEK, CZARNA_DAMKA, BIALA_DAMKA):
            if not pionek.wspolrzedna_x == 0 and not pionek.wspolrzedna_y == 0 and pionek.wspolrzedna_x - x1 == 1 and pionek.wspolrzedna_y - y1 == 1 and plansza[x1][y1] == POLE_CZARNE:
                print("[lewo-gora]", pionek.wspolrzedna_x, pionek.wspolrzedna_y)
                ilosc_ruchow += 1
            if not pionek.wspolrzedna_x == 7 and not pionek.wspolrzedna_y == 0 and pionek.wspolrzedna_x - x1 == -1 and pionek.wspolrzedna_y - y1 == 1 and plansza[x1][y1] == POLE_CZARNE:
                print("[prawo-gora]", pionek.wspolrzedna_x, pionek.wspolrzedna_y)
                ilosc_ruchow += 1
        if pionek.flaga_wagi in (CZARNY_PIONEK, CZARNA_DAMKA, BIALA_DAMKA):
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
    plansza[x2][y2] = pionek.flaga_wagi
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
                            if (x2 == x1 and y2 == y1) and y2 - pionek.wspolrzedna_y == 1 and pionek.flaga_wagi == CZARNY_PIONEK:
                                pionek = podstawianie_dla_ruchu(pionek, x2, y2)
                                return pionek
                            if (x2 == x1 and y2 == y1) and y2 - pionek.wspolrzedna_y == -1 and pionek.flaga_wagi == BIALY_PIONEK:
                                pionek = podstawianie_dla_ruchu(pionek, x2, y2)
                                return pionek
                            if CZARNA_DAMKA >= pionek.flaga_wagi >= BIALA_DAMKA:
                                if x2 - pionek.wspolrzedna_x == y2 - pionek.wspolrzedna_y or x2 - pionek.wspolrzedna_x == -1 * (y2 - pionek.wspolrzedna_y):
                                    pionek = podstawianie_dla_ruchu(pionek, x2, y2)
                                    return pionek
                    else:
                        print("nie można poruszyc sie w wyznaczona pozycje")
                    if plansza[x2][y2] == POLE_BIALE:
                        print("wybrane pole nie jest czarne")

#funkcja do graficznej reprezentacji planszy wyswietlanej w terminalu
def reprezentacja_terminal():
    print("      ", end='')
    for i in range(8):
        print(i, " ", end='')
    print("\n  ", end='')
    for i in range(10):
        print(ZNAK_1, end='')
    for i in range(8):
        print("")
        for j in range(8):
            if j == 0:
                print(i, ZNAK_1, end='')
            if plansza[j][i] == POLE_BIALE:
                print(ZNAK_2, end='')
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
        print(ZNAK_1, i, end='')
    print("\n  ", end='')
    for i in range(10):
        print(ZNAK_1, end='')
    print("\n      ", end='')
    for i in range(8):
        print(i, " ", end='')
    print("\n")

def main():
    assets.Assets.load()
    pygame.font.init()
    while True:
        print("============================")
        reprezentacja_terminal()
        gra.choice_function()

if __name__ == '__main__':
    gra = Warcaby()
    main()