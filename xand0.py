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

    def check_simbols(self, matr):
        for i in range(len(matr)):
            if matr[i] != "#":
                if matr[i - 1] == matr[i] == matr[i + 1]:
                    return matr[i]
                elif matr[i - self.dim] == matr[i] == matr[i + self.dim]:
                    return matr[i]
                elif matr[i - self.dim - 1] == matr[i] == matr[i + self.dim + 1]:
                    return matr[i]
                elif matr[i + self.dim - 1] == matr[i] == matr[i - self.dim + 1]:
                    return matr[i]
            return False

    def final(self):
        rez = self.check_simbols(self.matr)
        if rez:
            return rez
        elif self.__class__.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def modif_matr(self, conf_tabla, pos, simbol):
        count = 0
        for sim in conf_tabla:
            if sim == simbol:
                count += 1
        if count == 1:
            return conf_tabla
        try:
            if conf_tabla[pos + self.dim] == simbol or conf_tabla[pos - self.dim] == simbol:
                return conf_tabla
            elif conf_tabla[pos + 1] == simbol or conf_tabla[pos - 1] == simbol:
                return conf_tabla
            elif conf_tabla[pos + self.dim - 1] == simbol or conf_tabla[pos + self.dim + 1]:
                return conf_tabla
            elif conf_tabla[pos - self.dim - 1] == simbol or conf_tabla[pos - self.dim + 1]:
                return conf_tabla
        except IndexError:
            pass

    def mutari(self, jucator_opus):
        l_mutari = []
        for i in range(len(self.matr)):
            if self.matr[i] == self.__class__.GOL:
                matr_tabla_noua = list(self.matr)
                matr_tabla_noua[i] = jucator_opus
                matr_modif = self.modif_matr(matr_tabla_noua, i, jucator_opus)
                l_mutari.append(Joc(self.dim, matr_modif))
        return l_mutari

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        elif t_final == 'remiza':
            return 0

    def sirAfisare(self):
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


def main():
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
    dim = int(input("Introduceti dimensiunea tablei:"))
    while not 4 <= int(dim) <= 10:
        print("Dimensiunea tablei trebuie sa se incadreze intre 4 si 10. Introduceti o alta dimensiune!")
        dim = int(input("Introduceti dimensiunea tablei:"))
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    dificultate = 0
    while not 1 <= dificultate <= 3:
        dificultate = int(input("Alegeti dificultatea:\n1-Easy\n2-Medium\n3-Hard\n"))
        if not 1 <= dificultate <= 3:
            print("Ati ales o dificultate invalida!")
    # initializare tabla
    tabla_curenta = Joc(dim)
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', dificultate)

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('Naiboiu Teodor x si 0')
    ecran = pygame.display.set_mode(size=(dim * 100 + dim - 1, dim * 100 + dim - 1))
    Joc.initializeaza(ecran, dim)
    tabla_curenta = Joc(dim)
    tabla_curenta.deseneaza_grid()
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # iesim din program
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului
                    for np in range(len(Joc.celuleGrid)):
                        if Joc.celuleGrid[np].collidepoint(pos):
                            stare_curenta.tabla_joc.deseneaza_grid()
                            break

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului

                    for np in range(len(Joc.celuleGrid)):

                        if Joc.celuleGrid[np].collidepoint(
                                pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                            linie = np // dim
                            coloana = np % dim
                            ###############################
                            if stare_curenta.tabla_joc.matr[np] == Joc.GOL:
                                stare_curenta.tabla_joc.matr[linie * dim + coloana] = Joc.JMIN
                                stare_curenta.tabla_joc.matr = Joc(dim,
                                                                   stare_curenta.tabla_joc.matr).modif_matr(
                                    stare_curenta.tabla_joc.matr, linie * dim + coloana, Joc.JMIN)

                                # afisarea starii jocului in urma mutarii utilizatorului
                                print("\nTabla dupa mutarea jucatorului")
                                print(str(stare_curenta))

                                stare_curenta.tabla_joc.deseneaza_grid()
                                # testez daca jocul a ajuns intr-o stare finala
                                # si afisez un mesaj corespunzator in caz ca da
                                if (afis_daca_final(stare_curenta)):
                                    break

                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)



        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if int(tip_algoritm) == 1:
                stare_actualizata = min_max(stare_curenta)
            elif int(tip_algoritm) == 2:
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            stare_curenta.tabla_joc.deseneaza_grid()
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
