import time, pygame, sys
import random
import statistics


class Joc:
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, n, tabla=None):
        self.nr_coloane = n
        self.colt_st_sus = [1, self.nr_coloane, self.nr_coloane + 1]
        self.colt_dr_sus = [-1, self.nr_coloane - 1, self.nr_coloane]
        self.colt_st_jos = [-self.nr_coloane, -self.nr_coloane + 1, 1]
        self.colt_dr_jos = [-self.nr_coloane - 1, -self.nr_coloane, -1]
        self.matr = tabla or [self.__class__.GOL] * (n * n)
        self.stanga = [-self.nr_coloane, -self.nr_coloane + 1, 1, self.nr_coloane, self.nr_coloane + 1]
        self.sus = [-1, +1, self.nr_coloane - 1, self.nr_coloane, self.nr_coloane + 1]
        self.dreapta = [-self.nr_coloane - 1, -self.nr_coloane, -1, self.nr_coloane - 1, self.nr_coloane]
        self.jos = [-self.nr_coloane - 1, -self.nr_coloane, -self.nr_coloane + 1, -1, +1]
        self.oriunde = [-self.nr_coloane - 1, -self.nr_coloane, -self.nr_coloane + 1, -1, 1, self.nr_coloane - 1,
                        self.nr_coloane, self.nr_coloane + 1]

    @classmethod
    def initializeaza(cls, display, NR_COLOANE, dim_celula=50):
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

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def modif(self, stare):
        mod = True
        while mod:
            mod = False
            for i in range(len(stare)):
                sum_juc = 0
                sum_op = 0
                if stare[i] != '#':
                    if i // self.nr_coloane == 0:
                        if not i % self.nr_coloane == 0 and not i % self.nr_coloane == self.nr_coloane - 1:
                            for j in self.sus:
                                # print(stare[i + j])
                                if stare[i + j] == stare[i]:
                                    sum_juc += 1
                                elif stare[i + j] != '#':
                                    sum_op += 1
                    elif i // self.nr_coloane != self.nr_coloane - 1:
                        if i % self.nr_coloane == 0:
                            for j in self.stanga:
                                if stare[i + j] == stare[i]:
                                    sum_juc += 1
                                elif stare[i + j] != '#':
                                    sum_op += 1
                        elif i % self.nr_coloane == self.nr_coloane - 1:
                            for j in self.dreapta:
                                if stare[i + j] == stare[i]:
                                    sum_juc += 1
                                elif stare[i + j] != '#':
                                    sum_op += 1
                        else:
                            for j in self.oriunde:
                                if stare[i + j] == stare[i]:
                                    sum_juc += 1
                                elif stare[i + j] != '#':
                                    sum_op += 1
                    elif i // self.nr_coloane == self.nr_coloane - 1:
                        if i % self.nr_coloane != 0 and i % self.nr_coloane != self.nr_coloane - 1:
                            for j in self.jos:
                                if stare[i + j] == stare[i]:
                                    sum_juc += 1
                                elif stare[i + j] != '#':
                                    sum_op += 1

                    if sum_op > 3 and sum_op > sum_juc:
                        stare[i] = Joc.jucator_opus(stare[i])
                        mod = True
                        break
        return stare

    def mutari(self, jucator_opus):
        l_mutari = []
        for i in range(len(self.matr)):
            if self.matr[i] == self.__class__.GOL:
                matr_tabla_noua = list(self.matr)
                matr_tabla_noua[i] = jucator_opus
                modified = self.modif(matr_tabla_noua)
                l_mutari.append(Joc(self.nr_coloane, modified))
        return l_mutari

    def final(self):
        # print(type(self.matr))
        nr_X = 0
        nr_O = 0
        for i in self.matr:
            if i == 'x':
                nr_X += 1
            elif i == '0':
                nr_O += 1

        if self.__class__.GOL not in self.matr:
            if nr_O > nr_X:
                return '0'
            elif nr_X > nr_O:
                return 'x'
        if self.__class__.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def deseneaza_grid(self, final=False):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(len(self.matr)):
            linie = ind // self.nr_coloane  # // inseamna div
            coloana = ind % self.nr_coloane
            ####################################
            nr_x = self.numar_semn('x')
            nr_0 = self.numar_semn('0')
            culoare = (255, 204, 204)
            if final:
                # culoare = (102, 153, 255)
                if nr_0 > nr_x:
                    if self.matr[ind] == '0':
                        culoare = (102, 153, 255)
                elif nr_x > nr_0:
                    if self.matr[ind] == 'x':
                        culoare = (102, 153, 255)
            #####################################

            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            if self.matr[ind] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))

        pygame.display.flip()  # obligatoriu pentru a actualiza interfata (desenul)

    def numar_semn(self, juc):
        nr = 0
        for i in self.matr:
            if i == juc:
                nr += 1
        return nr

    def numar_semn_cu_ponderi(self, juc):
        nr = 0
        stare = self.matr
        for i in range(len(stare)):
            if stare[i] == juc:
                nr += 1
                if i // self.nr_coloane == 0:
                    if not i % self.nr_coloane == 0 and not i % self.nr_coloane == self.nr_coloane - 1:
                        for j in self.sus:
                            # print(stare[i + j])
                            if stare[i + j] == stare[i]:
                                nr += 1
                    elif i % self.nr_coloane == 0:
                        for j in self.colt_st_sus:
                            if stare[i + j] == stare[i]:
                                nr += 1
                    elif i % self.nr_coloane == self.nr_coloane - 1:
                        for j in self.colt_dr_sus:
                            if stare[i + j] == stare[i]:
                                nr += 1

                elif i // self.nr_coloane != self.nr_coloane - 1:
                    if i % self.nr_coloane == 0:
                        for j in self.stanga:
                            if stare[i + j] == stare[i]:
                                nr += 1
                    elif i % self.nr_coloane == self.nr_coloane - 1:
                        for j in self.dreapta:
                            if stare[i + j] == stare[i]:
                                nr += 1
                    else:
                        for j in self.oriunde:
                            if stare[i + j] == stare[i]:
                                nr += 1
                elif i // self.nr_coloane == self.nr_coloane - 1:
                    if i % self.nr_coloane != 0 and i % self.nr_coloane != self.nr_coloane - 1:
                        for j in self.jos:
                            if stare[i + j] == stare[i]:
                                nr += 1
                    elif i % self.nr_coloane == 0:
                        for j in self.colt_st_jos:
                            if stare[i + j] == stare[i]:
                                nr += 1
                    elif i % self.nr_coloane == self.nr_coloane - 1:
                        for j in self.colt_dr_jos:
                            if stare[i + j] == stare[i]:
                                nr += 1
        return nr

    def estimeaza_scor(self, adancime, estimare="prima estimare"):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        elif estimare == "prima estimare":
            return (self.numar_semn(self.__class__.JMAX) - self.numar_semn(self.__class__.JMIN))
        else:
            return (self.numar_semn_cu_ponderi(self.__class__.JMAX) - self.numar_semn_cu_ponderi(self.__class__.JMIN))

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.nr_coloane)]) + "\n"
        sir += "-" * (self.nr_coloane + 1) * 2 + "\n"
        # sir += "".join([str(i) + " |" + " ".join([str(x) for x in self.matr[i]]) for i in range(len(self.matr))])
        for i in range(len(self.matr)):
            if i % self.nr_coloane == 0:
                sir += str(i // self.nr_coloane) + " |" + self.matr[i]
            else:
                sir += " " + self.matr[i]
            if i % self.nr_coloane == self.nr_coloane - 1:
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
        sir = str(self.tabla_joc) +  "\n"
        return sir


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == 'remiza'):
            print("Remiza!")
        else:
            print("A castigat " + final)
        # print(final)

        return True

    return False


def min_max(stare, estimare="prima estimare"):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, estimare)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    # if len(stare.mutari_posibile) > 0:
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        # stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
        mutariCuEstimare.sort(key=lambda  x: x.estimare, reverse=True)
        cont = 1
        ind = 1
        val = mutariCuEstimare[0].estimare
        while cont < len(mutariCuEstimare):
            if mutariCuEstimare[ind].estimare == val:
                cont +=1
            else:
                break
            ind +=1
        stare.stare_aleasa = mutariCuEstimare[random.randrange(0, cont, 1)]
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare, estimare="prima estimare"):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, estimare)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    # print(type(stare.mutari_posibile))
    # print(stare.mutari_posibile[0])
        # stare.mutari_posibile = stare.mutari_posibile.sort(key=lambda x: x.estimare)

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(0, 0, 0),
                 culoareFundalSel=(128,128,128), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.left = left
        self.top = top
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display):  #, tabla_curenta):
    btn_dim = GrupButoane(
        top=20,
        left=32,
        listaButoane=[
            Buton(display=display, w=31, h=30, text="5", valoare="5"),
            Buton(display=display, w=31, h=30, text="6", valoare="6"),
            Buton(display=display, w=31, h=30, text="7", valoare="7"),
            Buton(display=display, w=31, h=30, text="8", valoare="8"),
            Buton(display=display, w=31, h=30, text="9", valoare="9"),
            Buton(display=display, w=31, h=30, text="10", valoare="10")
        ],
    indiceSelectat=0)
    btn_mode = GrupButoane(
        top=68,
        left=30,
        listaButoane=[
          Buton(display=display, w=73, h=30, text="PCvPC", valoare="pcvpc"),
          Buton(display=display, w=73, h=30, text="PlvPC", valoare="plvpc"),
          Buton(display=display, w=73, h=30, text="PlvPl", valoare="plvpl"),
        ],
    indiceSelectat=1)
    btn_dificulty = GrupButoane(
        top = 116,
        left = 30,
        listaButoane=[
            Buton(display=display, w=73, h=30,text="Easy", valoare="easy"),
            Buton(display=display, w=73, h=30,text="Medium", valoare="medium"),
            Buton(display=display, w=73, h=30,text="Hard", valoare="hard")
        ],
        indiceSelectat=0)

    btn_alg = GrupButoane(
        top=164,
        left=30,
        listaButoane=[
            Buton(display=display, w=115, h=30, text="MINI-MAX", valoare="minimax"),
            Buton(display=display, w=115, h=30, text="ALPHA-BETA", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=212,
        left=95,
        listaButoane=[
            Buton(display=display, w=50, h=30, text="X", valoare="x"),
            Buton(display=display, w=50, h=30, text="ZERO", valoare="0")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=260, left=120, w=60, h=30, text="START", culoareFundal=(155, 0, 55))
    btn_dim.deseneaza()
    btn_mode.deseneaza()
    btn_dificulty.deseneaza()
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_dim.selecteazaDupacoord(pos):
                    if not btn_mode.selecteazaDupacoord(pos):
                        if not btn_dificulty.selecteazaDupacoord(pos):
                            if not btn_alg.selecteazaDupacoord(pos):
                                if not btn_juc.selecteazaDupacoord(pos):
                                    if ok.selecteazaDupacoord(pos):
                                        display.fill((0, 0, 0))  # stergere ecran
                                        # tabla_curenta.deseneaza_grid()
                                        return btn_juc.getValoare(), btn_alg.getValoare(), btn_dificulty.getValoare(), btn_mode.getValoare(), btn_dim.getValoare()
        pygame.display.update()


def coloreaza_castigator(stare_curenta):
    # print("Sunt in Coloreaza Castigator -------------------------------------------")
    if stare_curenta.j_curent == 'x':
        nr_x = Joc.numar_semn(stare_curenta.tabla_joc, stare_curenta.j_curent)
        nr_0 = Joc.numar_semn(stare_curenta.tabla_joc, Joc.jucator_opus(stare_curenta.j_curent))
    else:
        nr_0 = Joc.numar_semn(stare_curenta.tabla_joc, stare_curenta.j_curent)
        nr_x = Joc.numar_semn(stare_curenta.tabla_joc, Joc.jucator_opus(stare_curenta.j_curent))

    print("Scor: X  0\n      {}  {}".format(nr_x, nr_0))
    Joc.deseneaza_grid(stare_curenta.tabla_joc, True)

def iesire(timpi, stare_curenta, timp):
    t = int(round(time.time() * 1000))
    print("Timpul total de joc: {}".format((t-timp)//1000) + " secunde")
    try:
        print("Timpul maxim: {} \nTimpul minim: {} \nTimpul mediu: {}\nMediana: {}".format(max(timpi), min(timpi), statistics.mean(timpi), statistics.median(timpi)))
    except:
        pass
    coloreaza_castigator(stare_curenta)

def main():
    # citirea numarului
    dimensiune_tabla = 6
    pygame.init()
    pygame.display.set_caption("Mihaila Mihai - X si 0")
    # dimensiunea ferestrei in pixeli

    ecran = pygame.display.set_mode(size=(
        dimensiune_tabla * 50, dimensiune_tabla * 50))  # N *w+ N-1= N*(w+1)-1
    pygame.draw.rect(ecran, (0, 204, 0), pygame.Rect(0,0,dimensiune_tabla*50,dimensiune_tabla*50))
    Joc.initializeaza(ecran, dimensiune_tabla)

    # initializare tabla
    # tabla_curenta = Joc(dimensiune_tabla)
    Joc.JMIN, tip_algoritm, dificulty, mode, dimensiune_tabla = deseneaza_alegeri(ecran) #, tabla_curenta)

    dimensiune_tabla = int(dimensiune_tabla)

    ecran = pygame.display.set_mode(size=(
        dimensiune_tabla * 50 + dimensiune_tabla - 1,
        dimensiune_tabla * 50 + dimensiune_tabla - 1))  # N *w+ N-1= N*(w+1)-1
    Joc.initializeaza(ecran, dimensiune_tabla)

    tabla_curenta = Joc(dimensiune_tabla)
    tabla_curenta.deseneaza_grid()

    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    dificultate = 1 if dificulty == 'easy' else 2 if dificulty == 'medium' else 3

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', dificultate)
    print("Muta jucatorul {}".format(stare_curenta.j_curent))
    t_intrare = int(round(time.time() * 1000))
    t_inainte = int(round(time.time() * 1000))
    timpi = []
    while True:
        # time.sleep(0.1)
        pygame.display.flip()

        if stare_curenta.j_curent == Joc.JMIN:

            # muta jucatorul
            # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
            # l=pygame.event.get()
            if mode != "pcvpc":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        iesire(timpi,stare_curenta, t_intrare)
                        pygame.quit()  # inchide fereastra
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        pos = pygame.mouse.get_pos()  # coordonatele clickului

                        for np in range(len(Joc.celuleGrid)):

                            if Joc.celuleGrid[np].collidepoint(
                                    pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                linie = np // dimensiune_tabla
                                coloana = np % dimensiune_tabla
                                ###############################
                                if stare_curenta.tabla_joc.matr[np] == Joc.GOL:
                                    stare_curenta.tabla_joc.matr[linie * dimensiune_tabla + coloana] = Joc.JMIN
                                    stare_curenta.tabla_joc.matr = Joc(dimensiune_tabla, stare_curenta.tabla_joc.matr).modif(stare_curenta.tabla_joc.matr)


                                    # afisarea starii jocului in urma mutarii utilizatorului
                                    print("\nTabla dupa mutarea jucatorului")
                                    print(str(stare_curenta))

                                    stare_curenta.tabla_joc.deseneaza_grid()

                                    t_dupa = int(round(time.time() * 1000))
                                    print("Jucatorul {} a gandit timp de ".format(stare_curenta.j_curent) + str(
                                        t_dupa - t_inainte) + " milisecunde.")
                                    # testez daca jocul a ajuns intr-o stare finala
                                    # si afisez un mesaj corespunzator in caz ca da
                                    if (afis_daca_final(stare_curenta)):
                                        iesire(timpi, stare_curenta, t_intrare)
                                        break


                                    # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                    print("Muta jucatorul {}".format(stare_curenta.j_curent))
                                    t_inainte = int(round(time.time() * 1000))

                                    time.sleep(0.5)
            if mode == "pcvpc":
                # if tip_algoritm == '1':
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)

                # else:  # tip_algoritm==2
                #     stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))

                stare_curenta.tabla_joc.deseneaza_grid()
                # preiau timpul in milisecunde de dupa mutare
                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if (afis_daca_final(stare_curenta)):
                    iesire(timpi,stare_curenta, t_intrare)

                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                print("Muta jucatorul {}".format(stare_curenta.j_curent))
                t_inainte = int(round(time.time() * 1000))

                time.sleep(0.5)
        else:
            if mode != "plvpl":
                t_inainte = int(round(time.time() * 1000))
                if mode == "plvpc":
                    if tip_algoritm == 'minimax':
                        stare_actualizata = min_max(stare_curenta)
                    else:  # tip_algoritm==2
                        stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                else:
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta,estimare="a doua estimare")
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))

                stare_curenta.tabla_joc.deseneaza_grid()
                # preiau timpul in milisecunde de dupa mutare
                t_dupa = int(round(time.time() * 1000))
                timpi.append(t_dupa - t_inainte)

                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if (afis_daca_final(stare_curenta)):
                    iesire(timpi,stare_curenta, t_intrare)

                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                print("Muta jucatorul {}".format(stare_curenta.j_curent))
                t_inainte = int(round(time.time() * 1000))


                # time.sleep(0.5)

            if mode == "plvpl":

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        iesire(timpi,stare_curenta, t_intrare)
                        pygame.quit()  # inchide fereastra
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        pos = pygame.mouse.get_pos()  # coordonatele clickului

                        for np in range(len(Joc.celuleGrid)):

                            if Joc.celuleGrid[np].collidepoint(
                                    pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                linie = np // dimensiune_tabla
                                coloana = np % dimensiune_tabla
                                ###############################
                                if stare_curenta.tabla_joc.matr[np] == Joc.GOL:
                                    stare_curenta.tabla_joc.matr[linie * dimensiune_tabla + coloana] = Joc.JMAX
                                    stare_curenta.tabla_joc.matr = Joc(dimensiune_tabla, stare_curenta.tabla_joc.matr).modif(stare_curenta.tabla_joc.matr)

                                    # afisarea starii jocului in urma mutarii utilizatorului
                                    print("\nTabla dupa mutarea jucatorului")
                                    print(str(stare_curenta))

                                    stare_curenta.tabla_joc.deseneaza_grid()

                                    t_dupa = int(round(time.time() * 1000))
                                    print("Jucatorul {} a gandit timp de ".format(stare_curenta.j_curent) + str(
                                        t_dupa - t_inainte) + " milisecunde.")

                                    if (afis_daca_final(stare_curenta)):
                                        iesire(timpi,stare_curenta, t_intrare)

                                        break

                                    # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                    print("Muta jucatorul {}".format(stare_curenta.j_curent))
                                    t_inainte = int(round(time.time() * 1000))


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
