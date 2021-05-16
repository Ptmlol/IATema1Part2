import statistics
import time
import pygame
import sys


class Joc:
    def __init__(self, n, tabla=None):
        self.dim = n
        self.matr = tabla or [self.__class__.GOL] * (n * n)
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    JMIN = None
    JMAX = None
    GOL = '#'

    @classmethod
    def initializeaza(cls, display, NR_COLOANE, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_COLOANE):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(len(self.matr)):
            linie = ind // self.dim
            coloana = ind % self.dim

            if marcaj == ind:
                # daca am o patratica selectata, o desenez cu rosu
                culoare = (255, 0, 0)
            else:
                # altfel o desenez cu alb
                culoare = (255, 255, 255)
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            if self.matr[ind] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()

    # pygame.display.update()

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def check_simbols(self, matr): # loser verifica daca avem aceleasi simboluri pe linie, coloana, sau diagonale
        for i in range(len(matr)):
            if matr[i] != "#":
                try:
                    if matr[i - 1] == matr[i] == matr[i + 1] and ((i - 1) // self.dim) == (i // self.dim) == ((i + 1) // self.dim):
                        return matr[i], i - 1, i, i + 1
                    elif matr[i - self.dim] == matr[i] == matr[i + self.dim] and not (i - self.dim) < 0 and not (i + self.dim) > len(self.matr):
                        return matr[i], i-self.dim, i, i + self.dim
                    elif matr[i - self.dim - 1] == matr[i] == matr[i + self.dim + 1] and abs((i // self.dim) - ((i - self.dim - 1) // self.dim)) == 1 and (i - self.dim - 1) >= 0 and (i + self.dim + 1) < len(self.matr) and abs((i // self.dim) - ((i + self.dim + 1) // self.dim)) == 1:
                        return matr[i], i - self.dim - 1, i, i + self.dim + 1
                    elif matr[i + self.dim - 1] == matr[i] == matr[i - self.dim + 1] and abs((i // self.dim) - ((i + self.dim - 1) // self.dim)) == 1 and abs((i // self.dim) - ((i - self.dim + 1) // self.dim)) == 1 and (i + self.dim - 1) < len(self.matr) and (i - self.dim + 1) >= 0:
                        return matr[i], i + self.dim - 1, i, i - self.dim + 1
                except IndexError:
                    pass
        return False, False, False, False

    def final(self): # verifica daca suntem in starea finala si daca da pentru a colora, luam pozitia pe care s-a indeplinit starea finala si o coloram
        rez, pos1, pos2, pos3 = self.check_simbols(self.matr) # rez is loser now, get pos of loser
        if rez == 'x':
            rez = '0'
        elif rez == '0':
            rez = 'x'
        if rez:
            self.coloreaza_loser(pos1, pos2, pos3, rez) # coloram pierzatorul cu rosu, iar castigatorul ( rez ) cu verde
            return rez
        elif self.__class__.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def vecini_liberi(self, index):  # verificam pentru fiecare vecin al indexului daca respecta conditia de a fi in jurul pozitiei pe care se afla un simbol
        vecini = [index + 1, index - 1, index + self.dim, index - self.dim, index + self.dim + 1, index + self.dim - 1, index - self.dim + 1, index - self.dim - 1]
        vec_lib = []
        for i in vecini:
            if 0 <= i < len(self.matr) and self.matr[i] == Joc.GOL: # parcurgem lista de vecini si verificam daca suntem pe loc gol
                linie = i // self.dim
                coloana = i % self.dim
                if abs(linie - index // self.dim) > 1 or abs(coloana - index % self.dim) > 1: # daca suntem verficiam sa nu fim la o distanta mai mare de 1 pt conditia pt diagonale
                    continue
                vec_lib.append(i)
        return vec_lib

    def indici_valizi(self, simbol):
        ind_val = []
        for i in range(len(self.matr)):
            if self.matr[i] == simbol:
                vec_lib = self.vecini_liberi(i)
                ind_val += vec_lib
        set_ind_val = set(ind_val) # introducem  indicii valizi intr un set
        return set_ind_val

    def coloreaza_loser(self, pos1, pos2, pos3, simbol_winner):
        for ind in range(len(self.matr)):
            linie = ind // self.dim
            coloana = ind % self.dim

            if pos1 == ind or pos2 == ind or pos3 == ind: # daca suntem pe pozitia pierzatorului o coloram cu rosu
                culoare = (139, 0, 0)
            elif self.matr[ind] == simbol_winner: # coloram pozitiile pe care se  afla celelalt jucator cu verde deoarece el castiga
                culoare = (60, 179, 113)
            else:
                culoare = (255, 255, 255)
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            if self.matr[ind] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()

    def coloreaza_liber(self, indici_valizi, cul=(255, 255, 0)):

        for ind in range(len(self.matr)):
            linie = ind // self.dim
            coloana = ind % self.dim

            if ind in indici_valizi: # coloram pozitiile in care avem mutare valida
                culoare = cul
            else:
                # altfel o desenez cu alb
                culoare = (255, 255, 255)
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            if self.matr[ind] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()

    def mutari(self, jucator_opus):
        l_mutari = []
        for i in range(len(self.matr)):
            if self.matr[i] == self.__class__.GOL:
                ind_val = self.indici_valizi(jucator_opus)
                if i in ind_val or ''.join(self.matr).count(jucator_opus) == 0: # verificam daca avem mutare valida sau daca nu avem nici un simbol introduc pe tabla, daca da, introducem simbolul pe tabla
                    matr_tabla_noua = list(self.matr)
                    matr_tabla_noua[i] = jucator_opus
                    l_mutari.append(Joc(self.dim, matr_tabla_noua))
        return l_mutari

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        elif t_final == 'remiza':
            return 0
        return 0

    def sirAfisare(self):
        try:
            sir = "  |"
            sir += " ".join([str(i) for i in range(self.dim)]) + "\n"
            sir += "-" * (self.dim + 1) * 2 + "\n"
            for i in range(len(self.matr)):
                if i % self.dim == 0:
                    sir += str(i // self.dim) + " |" + self.matr[i]
                else:
                    sir += " " + self.matr[i]
                if i % self.dim == self.dim - 1:
                    sir += "\n"
            return sir
        except TypeError:
            pass

    def __str__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None
        self.parinte = parinte

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]
    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True
    return False


def iesire(timpi, timp):
    t = int(round(time.time() * 1000))
    print("Timpul total de joc: " + str((t-timp)//1000) + " secunde")
    try:
        print("Timpul maxim: " + str(max(timpi)) + "\nTimpul minim: " + str(min(timpi)) + "\nTimpul mediu: " + str(statistics.mean(timpi)) + "\nMediana: " + str(statistics.median(timpi)))
        print("Numar mutari jucator: " + str(mutari_jucator) + "\nNumar mutari calculator: " + str(mutari_calculator))
    except Exception:
        pass

def add_moves(p):
    global mutari_calculator, mutari_jucator
    if p == "j":
        mutari_jucator += 1
    elif p == "c":
        mutari_calculator += 1

mutari_calculator = 0
mutari_jucator = 0
if __name__ == "__main__":
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
        if Joc.JMIN in ['x', '0']:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    try:
        dim = int(input("Introduceti dimensiunea tablei:"))
    except ValueError:
        print("Nu ati introdus nimic!")
        dim = 3
        pass
    while not 4 <= int(dim) <= 10:
        try:
            print("Dimensiunea tablei trebuie sa se incadreze intre 4 si 10. Introduceti o alta dimensiune!")
            dim = int(input("Introduceti dimensiunea tablei:"))
        except Exception:
            pass
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    dificultate = 0
    while not 1 <= dificultate <= 3:
        try:
            dificultate = int(input("Alegeti dificultatea:\n1-Easy\n2-Medium\n3-Hard\n"))
            if not 1 <= dificultate <= 3:
                print("Ati ales o dificultate invalida!")
        except ValueError:
            print("Nu ati introdus nimic!")
            pass
    # initializare tabla
    tabla_curenta = Joc(dim)
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', dificultate)

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('Naiboiu Teodor. X si 0')
    ecran = pygame.display.set_mode(size=(dim * 100 + dim - 1, dim * 100 + dim - 1))
    Joc.initializeaza(ecran, dim)
    tabla_curenta = Joc(dim)
    tabla_curenta.deseneaza_grid()
    stopped = False
    t_intrare = int(round(time.time() * 1000))
    t_inainte = int(round(time.time() * 1000))
    timpi = []
    while not stopped:
        if stare_curenta.j_curent == Joc.JMIN:
            ind_val = stare_curenta.tabla_joc.indici_valizi(Joc.JMIN)
            stare_curenta.tabla_joc.coloreaza_liber(ind_val)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    iesire(timpi, t_intrare)
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.MOUSEMOTION:
                #     pos = pygame.mouse.get_pos()  # coordonatele cursorului
                #     for np in range(len(Joc.celuleGrid)):
                #         if Joc.celuleGrid[np].collidepoint(pos):
                #             stare_curenta.tabla_joc.deseneaza_grid()
                #             break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                    for np in range(len(Joc.celuleGrid)):

                        if Joc.celuleGrid[np].collidepoint(pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                            linie = np // dim
                            coloana = np % dim
                            ###############################
                            if stare_curenta.tabla_joc.matr[np] == Joc.GOL and ( np in stare_curenta.tabla_joc.indici_valizi(Joc.JMIN) or ''.join(stare_curenta.tabla_joc.matr).count(Joc.JMIN)==0):
                                stare_curenta.tabla_joc.matr[linie * dim + coloana] = Joc.JMIN
                                add_moves("j")

                                # afisarea starii jocului in urma mutarii utilizatorului
                                print("\nTabla dupa mutarea jucatorului")
                                print(str(stare_curenta))

                                stare_curenta.tabla_joc.deseneaza_grid()
                                # testez daca jocul a ajuns intr-o stare finala
                                # si afisez un mesaj corespunzator in caz ca da
                                if afis_daca_final(stare_curenta):
                                    iesire(timpi, t_intrare)
                                    stopped = True
                                    break

                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)



        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator
            # preiau timpul in milisecunde de dinainte de mutare

            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == 1:
                stare_actualizata = min_max(stare_curenta)
            else:
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            add_moves("c")
            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timpi.append(t_dupa - t_inainte)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            stare_curenta.tabla_joc.deseneaza_grid()
            if afis_daca_final(stare_curenta):
                iesire(timpi, t_intrare)
                stopped = True
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
