import sys
import time
import pygame
import assets
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
ZNAK_1 = '[#]'
ZNAK_2 = '   '

plansza = BOARD_SIZE * [0]
for i in range(BOARD_SIZE):
    plansza[i] = [0]*BOARD_SIZE

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

    def test_bicia_damkami(self):
        self.tab_black = []
        self.tab_white = []
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
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

        self.tab_black.append(Pionek(2, 3, CZARNA_DAMKA))
        self.tab_white.append(Pionek(1, 2, BIALA_DAMKA))

        self.tab_black.append(Pionek(4, 3, CZARNA_DAMKA))
        self.tab_white.append(Pionek(5, 2, BIALA_DAMKA))

        self.tab_black.append(Pionek(2, 5, CZARNA_DAMKA))
        self.tab_white.append(Pionek(1, 6, BIALA_DAMKA))

        self.tab_black.append(Pionek(4, 5, CZARNA_DAMKA))
        self.tab_white.append(Pionek(5, 6, BIALA_DAMKA))

        plansza[2][3] = CZARNA_DAMKA
        plansza[1][2] = BIALA_DAMKA

        plansza[4][3] = CZARNA_DAMKA
        plansza[5][2] = BIALA_DAMKA

        plansza[2][5] = CZARNA_DAMKA
        plansza[1][6] = BIALA_DAMKA

        plansza[4][5] = CZARNA_DAMKA
        plansza[5][6] = BIALA_DAMKA

    def test_bicia_pionkami(self):
        self.tab_black = []
        self.tab_white = []
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
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
        self.tab_black.append(Pionek(2, 3, CZARNY_PIONEK))
        self.tab_white.append(Pionek(1, 2, BIALY_PIONEK))

        self.tab_black.append(Pionek(4, 3, CZARNY_PIONEK))
        self.tab_white.append(Pionek(5, 2, BIALY_PIONEK))

        self.tab_black.append(Pionek(2, 5, CZARNY_PIONEK))
        self.tab_white.append(Pionek(1, 6, BIALY_PIONEK))

        self.tab_black.append(Pionek(4, 5, CZARNY_PIONEK))
        self.tab_white.append(Pionek(5, 6, BIALY_PIONEK))

        plansza[2][3] = CZARNY_PIONEK
        plansza[1][2] = BIALY_PIONEK

        plansza[4][3] = CZARNY_PIONEK
        plansza[5][2] = BIALY_PIONEK

        plansza[2][5] = CZARNY_PIONEK
        plansza[1][6] = BIALY_PIONEK

        plansza[4][5] = CZARNY_PIONEK
        plansza[5][6] = BIALY_PIONEK

    def test_wielokrotnego_bicia(self):
        self.tab_black = []
        self.tab_white = []
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
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
        self.tab_black.append(Pionek(0, 5, CZARNY_PIONEK))
        plansza[0][5] = CZARNY_PIONEK

        self.tab_white.append(Pionek(1, 4, BIALY_PIONEK))
        plansza[1][4] = BIALY_PIONEK
        self.tab_white.append(Pionek(1, 6, BIALY_PIONEK))
        plansza[1][6] = BIALY_PIONEK
        self.tab_white.append(Pionek(3, 2, BIALY_PIONEK))
        plansza[3][2] = BIALY_PIONEK
        self.tab_white.append(Pionek(3, 6, BIALY_PIONEK))
        plansza[3][6] = BIALY_PIONEK
        self.tab_white.append(Pionek(5, 2, BIALY_PIONEK))
        plansza[5][2] = BIALY_PIONEK
        self.tab_white.append(Pionek(5, 4, BIALY_PIONEK))
        plansza[5][4] = BIALY_PIONEK


    # metoda przebiegu gry
    def choice_function(self):
        rysuj_plansze(self.tab_white, self.tab_black)
        for i in range(6):
            if self.tab_white:
                przebieg_testu(self.tab_black, self.tab_white, self.tab_black)
                rysuj_plansze(self.tab_white, self.tab_black)
                reprezentacja_terminal()
                for pionek in self.tab_black:
                    pionek.flaga_bicia=False
            else:
                break
        print("Koniec testu")
        time.sleep(1)



    # metoda do usowania pionków z planszy
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

#metoda do graficznej reprezentacji rozgrywki za użyciem biblioteki pygame
def rysuj_plansze(tab_white, tab_black):
    game_window = pygame.display.set_mode((SIZE * 8, SIZE * 8), 0, 32)
    pygame.display.set_caption('Test funkcji bicia')
#rysuje plansze wymiarow 8x8
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i % 2 != 0:
                if j % 2 != 0:
                    pygame.draw.rect(game_window, WHITE_COLOR, [SIZE * i, SIZE * j, SIZE, SIZE])
                else:
                    pygame.draw.rect(game_window, BLACK_COLOR, [SIZE * i, SIZE * j, SIZE, SIZE])
            else:
                if j % 2 != 0:
                    pygame.draw.rect(game_window, BLACK_COLOR, [SIZE * i, SIZE * j, SIZE, SIZE])
                else:
                    pygame.draw.rect(game_window, WHITE_COLOR, [SIZE * i, SIZE * j, SIZE, SIZE])
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

def przebieg_testu(tablica, tab_white, tab_black):
    nic_wiecej = 0
    turn = True

    bicie_turn = czy_bicie(tablica)
    while turn:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    x1, y1 = pos[0] // SIZE, pos[1] // SIZE
                    for pionek in tablica:
                        if x1 == pionek.wspolrzedna_x and y1 == pionek.wspolrzedna_y and pionek.flaga_bicia:
                            while bicie_turn:
                                nowa_pozycja_bicia = bicie(pionek)
                                pionek.wspolrzedna_x = nowa_pozycja_bicia.wspolrzedna_x
                                pionek.wspolrzedna_y = nowa_pozycja_bicia.wspolrzedna_y
                                rysuj_plansze(tab_white, tab_black)
                                reprezentacja_terminal()
                                bicie_turn = False
                                turn = False
                            else:
                                nic_wiecej += 1
                            if nic_wiecej == len(tablica):
                                print("musisz wybrac pionka ktorym mozna wykonac bicie")
                                nic_wiecej = 0

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
                for i in range(0, 8):
                    x1, y1 = element.wspolrzedna_x + i * delta_x, element.wspolrzedna_y + i * delta_y             #puste badz twoja figura
                    x2, y2 = element.wspolrzedna_x + (i + 1) * delta_x, element.wspolrzedna_y + (i + 1) * delta_y #figura
                    x3, y3 = element.wspolrzedna_x + (i + 2) * delta_x, element.wspolrzedna_y + (i + 2) * delta_y #puste
                    if element.wspolrzedna_x not in (0, 1) and element.wspolrzedna_y not in (0, 1) and x2 - x1 == -1 and y2 - y1 == -1:
                        if x2 < 1 or y2 < 1:
                            break
                        if plansza[x2][y2] not in (element.flaga_wagi, element.flaga_wagi - 2, POLE_CZARNE):
                            if plansza[x3][y3] == POLE_CZARNE and (plansza[x1][y1] == POLE_CZARNE or (x1 == element.wspolrzedna_x and y1 == element.wspolrzedna_y)):
                                print("TAK:[lewo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                                element.flaga_bicia = True
                                ilosc_bic += 1
                    if element.wspolrzedna_x not in (6, 7) and element.wspolrzedna_y not in (0, 1) and x2 - x1 == 1 and y2 - y1 == -1:
                        if x2 > 6 or y2 < 1:
                            break
                        if plansza[x2][y2] not in (element.flaga_wagi, element.flaga_wagi - 2, POLE_CZARNE):
                            if plansza[x3][y3] == POLE_CZARNE and (plansza[x1][y1] == POLE_CZARNE or (x1 == element.wspolrzedna_x and y1 == element.wspolrzedna_y)):
                                print("TAK:[prawo-gora]", element.wspolrzedna_x, element.wspolrzedna_y)
                                element.flaga_bicia = True
                                ilosc_bic += 1
                    if element.wspolrzedna_x not in (6, 7) and element.wspolrzedna_y not in (6, 7) and x2 - x1 == 1 and y2 - y1 == 1:
                        if x2 > 6 or y2 > 6:
                            break
                        if plansza[x2][y2] not in (element.flaga_wagi, element.flaga_wagi - 2, POLE_CZARNE):
                            if plansza[x3][y3] == POLE_CZARNE and (plansza[x1][y1] == POLE_CZARNE or (x1 == element.wspolrzedna_x and y1 == element.wspolrzedna_y)):
                                print("TAK:[prawo-dol]", element.wspolrzedna_x, element.wspolrzedna_y)
                                element.flaga_bicia = True
                                ilosc_bic += 1
                    if element.wspolrzedna_x not in (0, 1) and element.wspolrzedna_y not in (6, 7) and x2 - x1 == -1 and y2 - y1 == 1:
                        if x2 < 1 or y2 > 6:
                            break
                        if plansza[x2][y2] not in (element.flaga_wagi, element.flaga_wagi - 2, POLE_CZARNE):
                            if plansza[x3][y3] == POLE_CZARNE and (plansza[x1][y1] == POLE_CZARNE or (x1 == element.wspolrzedna_x and y1 == element.wspolrzedna_y)):
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
                    pos_x, pos_y = pos[0] // SIZE, pos[1] // SIZE
                    if plansza[pos_x][pos_y] == POLE_CZARNE:
                        for delta_x, delta_y in MOVES:
                            x1, y1 = pionek.wspolrzedna_x + delta_x, pionek.wspolrzedna_y + delta_y
                            if pionek.flaga_wagi in (CZARNY_PIONEK, BIALY_PIONEK):
                                # lewo gora pionek
                                if pionek.wspolrzedna_x not in (0, 1) and pionek.wspolrzedna_y not in (0, 1) and pos_x - x1 == -1 and pos_y - y1 == -1:
                                    if plansza[x1][y1] not in (pionek.flaga_wagi, pionek.flaga_wagi + 2, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x1, y1, pos_x, pos_y)
                                        return pionek
                                # prawo gora pionek
                                if pionek.wspolrzedna_x not in (6, 7) and pionek.wspolrzedna_y not in (0, 1) and pos_x - x1 == 1 and pos_y - y1 == -1:
                                    if plansza[x1][y1] not in (pionek.flaga_wagi, pionek.flaga_wagi + 2, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x1, y1, pos_x, pos_y)
                                        return pionek
                                # prawo dol pionek
                                if pionek.wspolrzedna_x not in (6, 7) and pionek.wspolrzedna_y not in (6, 7) and pos_x - x1 == 1 and pos_y - y1 == 1:
                                    if plansza[x1][y1] not in (pionek.flaga_wagi, pionek.flaga_wagi + 2, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x1, y1, pos_x, pos_y)
                                        return pionek
                                # lewo dol pionek
                                if pionek.wspolrzedna_x not in (0, 1) and pionek.wspolrzedna_y not in (6, 7) and pos_x - x1 == -1 and pos_y - y1 == 1:
                                    if plansza[x1][y1] not in (pionek.flaga_wagi, pionek.flaga_wagi + 2, POLE_CZARNE):
                                        pionek = podstawianie_dla_bicia(pionek, x1, y1, pos_x, pos_y)
                                        return pionek
                            if pionek.flaga_wagi in (CZARNA_DAMKA, BIALA_DAMKA):
                                for delta_x, delta_y in MOVES:
                                    for i in range(1, 5):
                                        x1, y1 = pionek.wspolrzedna_x + (i - 1) * delta_x, pionek.wspolrzedna_y + (i - 1) * delta_y
                                        x2, y2 = pionek.wspolrzedna_x + i * delta_x, pionek.wspolrzedna_y + i * delta_y
                                        x3, y3 = pionek.wspolrzedna_x + (i + 1) * delta_x, pionek.wspolrzedna_y + (i + 1) * delta_y
                                        if x3 == pos_x and y3 == pos_y:
                                            # lewo gora damka
                                            if pionek.wspolrzedna_x not in (0, 1) and pionek.wspolrzedna_y not in (0, 1) and x2 - x1 == -1 and y2 - y1 == -1:
                                                if x2 < 1 or y2 < 1:
                                                    break
                                                if plansza[x2][y2] not in (pionek.flaga_wagi, pionek.flaga_wagi - 2, POLE_CZARNE) and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (pionek.flaga_wagi, POLE_CZARNE):
                                                    pionek = podstawianie_dla_bicia(pionek, x2, y2, x3, y3)
                                                    return pionek
                                            # prawo gora damka
                                            if pionek.wspolrzedna_x not in (6, 7) and pionek.wspolrzedna_y not in (0, 1) and x2 - x1 == 1 and y2 - y1 == -1:
                                                if x2 > 6 or y2 < 1:
                                                    break
                                                if plansza[x2][y2] not in (pionek.flaga_wagi, pionek.flaga_wagi - 2, POLE_CZARNE) and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (pionek.flaga_wagi, POLE_CZARNE):
                                                    pionek = podstawianie_dla_bicia(pionek, x2, y2, x3, y3)
                                                    return pionek
                                            # prawo dol damka
                                            if pionek.wspolrzedna_x not in (6, 7) and pionek.wspolrzedna_y not in (6, 7) and x2 - x1 == 1 and y2 - y1 == 1:
                                                if x2 > 6 or y2 > 6:
                                                    break
                                                if plansza[x2][y2] not in (pionek.flaga_wagi, pionek.flaga_wagi - 2, POLE_CZARNE) and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (pionek.flaga_wagi, POLE_CZARNE):
                                                    pionek = podstawianie_dla_bicia(pionek, x2, y2, x3, y3)
                                                    return pionek
                                            # lewo dol damka
                                            if pionek.wspolrzedna_x not in (0, 1) and pionek.wspolrzedna_y not in (6, 7) and x2 - x1 == -1 and y2 - y1 == 1:
                                                if x2 < 1 or y2 > 6:
                                                    break
                                                if plansza[x2][y2] not in (pionek.flaga_wagi, pionek.flaga_wagi - 2, POLE_CZARNE) and plansza[x3][y3] == POLE_CZARNE and plansza[x1][y1] in (pionek.flaga_wagi, POLE_CZARNE):
                                                    pionek = podstawianie_dla_bicia(pionek, x2, y2, x3, y3)
                                                    return pionek
                            else:
                                print("wybierz pole zgodne z zasadami gry")
                    if plansza[pos_x][pos_y] == POLE_BIALE:
                        print("wybrane pole nie jest polem czarnym")
                    else:
                        print("wybrane pole nie jest puste")
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
            if plansza[j][i] == CZARNY_PIONEK:
                print(" C ", end='')
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


def test1():
    assets.Assets.load()
    pygame.font.init()
    gra.test_bicia_damkami()
    reprezentacja_terminal()
    gra.choice_function()
def test2():
    assets.Assets.load()
    pygame.font.init()
    gra.test_bicia_pionkami()
    reprezentacja_terminal()
    gra.choice_function()
def test3():
    assets.Assets.load()
    pygame.font.init()
    gra.test_wielokrotnego_bicia()
    reprezentacja_terminal()
    gra.choice_function()

def main():
    test1()
    test2()
    test3()

if __name__ == '__main__':
    gra = Warcaby()
    main()
