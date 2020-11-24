# -----------------------------------------------------------
# UI - Zadanie 3 - Finalne odovzdanie
# ZS 2020
#
# Peter Smreček
# email xsmrecek@stuba.sk
# AIS ID 103130
# -----------------------------------------------------------

import math
from numpy import random as np_random
import pandas as pd
from datetime import datetime
import sys


def oddelovac(znak="-", pocet=150):
    """
    Debuggovacia funkcia oddelujuca vypisy
    :param znak: znak oddelovaca
    :param pocet: pocet opakovani oddelovacieho znaku
    """

    print(znak * pocet)


class Graf:
    """
    Trieda grafu
    """

    def __init__(self, suradnice):
        """
        Vytvorenie instancie triedy s uvodnymi parametrami
        :param suradnice: zadane suradnice miest
        """
        self.suradnice = suradnice
        self.pocet_miest = len(self.suradnice)
        self.dlzka = self.dlzka_cesty()
        self.fitnes = self.fitnes_vypocet()

    def get_suradnice(self):
        """
        Getter suradnic
        """

        return self.suradnice

    def get_pocet(self):
        """
        Getter poctu miest
        """

        return self.pocet_miest

    def get_dlzka(self):
        """
        Getter dlzky cesty
        """
        return self.dlzka

    def get_fitnes(self):
        """
        Getter fitnes-u
        """

        return self.fitnes

    def euklidova_vzdialenost(self, vrchol1, vrchol2):
        """
        Funkcia na vypocet euklidovej vzdialenosti medzi 2 vrcholmi
        :param vrchol1:
        :param vrchol2:
        :return: vzdialenost vrcholov
        """

        v1 = self.suradnice[vrchol1]
        v2 = self.suradnice[vrchol2]
        vzdialenost_vrcholov = math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)
        return vzdialenost_vrcholov

    def dlzka_cesty(self):
        """
        Vypocita dlzku cesty pre zadanu postupnost miest
        :return: dlzka grafu
        """

        predosly = -1
        sum_vzdialenost = 0
        for index in range(self.pocet_miest):
            if predosly == -1:
                predosly = index
                prvy_posledny = self.euklidova_vzdialenost(0, self.pocet_miest - 1)
                sum_vzdialenost += prvy_posledny
            else:
                vzdialenost_vrcholov = self.euklidova_vzdialenost(predosly, index)
                sum_vzdialenost += vzdialenost_vrcholov
                predosly = index
        return sum_vzdialenost

    def fitnes_vypocet(self):
        """
        Vypocita fitnes grafu
        :return: fitnes grafu
        """

        return 1 / self.dlzka

    def permutuj(self):
        """
        Vytvori nahodnu permutaciu grafu. Pouziva sa pri uvodnej tvorbe jedincov a pri Novej Krvi.
        :return: instancia triedy graf s novou nahodnou permutaciou sucasneho grafu
        """

        permutacia = np_random.permutation(self.suradnice)
        permutacia = permutacia.tolist()
        return Graf(permutacia)

    def mutacia(self, zadana_pravdepodobnost):
        """
        Mutacia jedinca - ak ma mutaciu prebehnut, vyberie sa jedno nahodne mesto a vymeni sa s jeho susedom
        :param zadana_pravdepodobnost: pravdepodobnost mutacie
        """

        if self.pravdepodobnost(zadana_pravdepodobnost):
            index = np_random.randint(0, self.pocet_miest - 1)
            self.suradnice[index], self.suradnice[index + 1] = self.suradnice[index + 1], self.suradnice[index]

    def __str__(self):
        """
        Vypis grafu
        """

        text = ""
        for index in range(self.pocet_miest):
            text += str(self.suradnice[index])
            if (index + 1) % 10 != 0:
                text += " "
            elif index != self.pocet_miest - 1:
                text += "\n"
        return text

    def pravdepodobnost(self, zadana_pravdepodobnost):
        """
        Zisti, ci sa ma uskutocnit mutacia, alebo nie
        :param zadana_pravdepodobnost: pravdepodobnost mutacia
        :return: boolean
        """

        p = np_random.rand()
        if p <= zadana_pravdepodobnost:
            return True
        return False


def mixuj(pocet, surandnice1, suradnice2, hranica_1, hranica_2):
    """
    Vymeni casti cesty medzi 2 zadanymi cestami podla zadanych hranic
    :param pocet: pocet miest
    :param surandnice1: cesta prvym grafom
    :param suradnice2: cesta druhym grafom
    :param hranica_1: pociatok vymeny
    :param hranica_2: koniec vymeny
    :return: suradnice dietata
    """

    stred = surandnice1[hranica_1:hranica_2 + 1]
    zvysne_suradnice = [suradnica for suradnica in suradnice2 if suradnica not in stred]
    vysledok = []

    vysledok += zvysne_suradnice[:hranica_1]
    vysledok += stred
    vysledok += zvysne_suradnice[hranica_1:]

    return vysledok


def porod(rodic1, rodic2, pravdepodobnost_mutacie):
    """
    Vytvori z 2 rodicov 2 deti na zaklade 2-bodoveho krizenia opisaneho v zadani. Spusta funkciu mixuj dvakrat s
    vymenenym poradim rodicov.
    :param rodic1: instancia triedy Graf
    :param rodic2: instancia triedy Graf
    :param pravdepodobnost_mutacie: pravdepodobnost mutacie dietata
    :return: 2 deti
    """

    pocet = rodic1.get_pocet()
    suradnice_rodic1 = rodic1.get_suradnice()
    suradnice_rodic2 = rodic2.get_suradnice()
    hranica_1 = np_random.randint(0, pocet - 1)
    hranica_2 = np_random.randint(hranica_1 + 1, pocet)
    vysledok_R1R2 = mixuj(pocet, suradnice_rodic1, suradnice_rodic2, hranica_1, hranica_2)
    vysledok_R2R1 = mixuj(pocet, suradnice_rodic2, suradnice_rodic1, hranica_1, hranica_2)

    dieta_1 = Graf(vysledok_R1R2)
    dieta_1.mutacia(pravdepodobnost_mutacie)
    dieta_2 = Graf(vysledok_R2R1)
    dieta_2.mutacia(pravdepodobnost_mutacie)

    return [dieta_1, dieta_2]


def turnaj(pocet_clenov_populacie, pole_indexov, pravdepodobnosti):
    """
    Vyber rodicov turnajom. Vyberu sa 2 nahodne dvojice jedincov z populacie, z kazdej dvojice sa vyberie
    jeden jedinec s lepsim fitnesom a navzajom sa tito vybrati jedinci skrizia. Toto sa opakuje tolkokrat, kolko je
    jedincov v populacii.
    :param pocet_clenov_populacie: pocet miest v grafe
    :param pole_indexov: pole indexov clenov populacie od 0 po pocet_clenov_populacie - 1
    :param pravdepodobnosti: jednotlive hodnoty fitnes pre zodpovedajucich jedincov namapovanych v pole_indexov
    :return: pole indexov rodicov
    """

    pocet_dvojic_rodicov = pocet_clenov_populacie // 2
    dvojice_rodicov = []

    for i in range(pocet_dvojic_rodicov):
        rodic1, rodic2 = 0, 0
        while rodic1 == rodic2:
            vyber1 = np_random.choice(pole_indexov, 2, replace=False)
            vyber2 = np_random.choice(pole_indexov, 2, replace=False)
            rodic1 = vyber1[0] if pravdepodobnosti[vyber1[0]] > pravdepodobnosti[vyber1[1]] else vyber1[1]
            rodic2 = vyber2[0] if pravdepodobnosti[vyber2[0]] > pravdepodobnosti[vyber2[1]] else vyber2[1]

        dvojice_rodicov.append([rodic1, rodic2])

    return dvojice_rodicov


def ruleta(pocet_clenov_populacie, pole_indexov, pravdepodobnosti):
    """
    Vyber rodicov ruletou. Z populacie vyberam 2 rodicov podla vahy.
    :param pocet_clenov_populacie: pocet miest v grafe
    :param pole_indexov: pole indexov clenov populacie od 0 po pocet_clenov_populacie - 1
    :param pravdepodobnosti: jednotlive fitnes pre zodpovedajucich jedincov namapovanych v pole_indexov
    :return: pole indexov rodicov
    """

    koeficient = 1 / sum(pravdepodobnosti)
    prenasobene_pravdepodobnosti = [prvok * koeficient for prvok in pravdepodobnosti]

    pocet_vyberov = pocet_clenov_populacie // 2
    dvojice_rodicov = []

    for cislo_vyberu in range(pocet_vyberov):
        vyber = np_random.choice(pole_indexov, 2, p=prenasobene_pravdepodobnosti)
        dvojice_rodicov.append(list(vyber))

    return dvojice_rodicov


def najdi_najlepsieho(populacia):
    """
    Najde a vrati jedinca s najvacim fitnes v zadanej populacii.
    :param populacia: populacia jedincov
    :return: najlepsi jedinec
    """

    maximum = 0
    najlepsi = None
    for jedinec in populacia:
        if jedinec.get_fitnes() > maximum:
            maximum = jedinec.get_fitnes()
            najlepsi = jedinec
    return najlepsi


def najdi_najhorsieho(populacia):
    """
    Najde a vrati jedinca s najmensim fitnes v zadanej populacii.
    :param populacia: populacia jedincov
    :return: najhorsi jedinec
    """

    minimum = 2
    najhorsi = None
    for jedinec in populacia:
        if jedinec.get_fitnes() < minimum:
            minimum = jedinec.get_fitnes()
            najhorsi = jedinec
    return najhorsi


def geneticky_algoritmus(povodne_suradnice, vyber_rodicov, pocet_generacii=2000, pravdepodobnost_mutacie=0.1,
                         pocet_clenov_populacie=40, ponechat_najlepsieho=False, nova_krv=False, vypisy=True):
    """
    Geneticky algoritmus na riesenie problemu obchodneho cestujuceho.
    Z povodne zadaneho grafu vytvori tolko clenov populacie kolko je potrebnych. Nasledne na tychto clenoch populacie
    hlada krizenim globalne optimum.
    Vybera rodicov stanovenou funkciou, vytvori ich deti, prepise detmi povodnu populaciu. Toto vykona tolkokrat, kolko
    je zadany pocet generacii.
    Okrem funkcii vyberu rodicov je mozne zvolit aj ci najlepsi jedinec automaticky postupi do dalsej generacie a aj to,
    ci maju byt 2 nahodne deti nahradene 2 nahodnymi permutaciami, ako prevencia pred uviaznitim v lokalnom optime.
    :param povodne_suradnice: povodna zadana permutacia suradnic
    :param vyber_rodicov: funkcia vyberu rodicov z populacie
    :param pocet_generacii: pocet generacii evolucneho algoritmu
    :param pravdepodobnost_mutacie: pravdepodobnost mutacie dietata
    :param pocet_clenov_populacie: pocet jedincov v populacii
    :param ponechat_najlepsieho: boolean, ak True, tak najlepsi automaticky postupuje do dalsej generacie. Ak False, tak
            najsledujuca generacia moze prist o najlepsieho jedinca
    :param nova_krv: boolean, ak True, 2 nahodne deti v kazdej generacii su nahradene 2 novymi permutaciami, ak False,
            tak vsetky deti su detmi rodicov z predoslej generacie
    :param vypisy: boolean, ak True, tak su ciatkove vypisy po 1000 generaciach aktivne, ak False, tak nie
    :return: pole priemerov fitnes v jednotlivych generaciach, pole maximalnych fitnes v jednotlivych
            generaciach a najlepsieho jedinca z poslednej generacie
    """

    oddelovac(znak="#")
    print("Start genetickeho algoritmu")
    print("Povodne suradnice", povodne_suradnice)
    print("Vyber rodicov", vyber_rodicov.__name__)
    print("Pocet generacii", pocet_generacii)
    print("Pocet clenov populacie", pocet_clenov_populacie)
    print("Pravdepodobnost mutacii deti", pravdepodobnost_mutacie)

    if ponechat_najlepsieho:
        print("Najhorsie z deti je nahradene najlepsim clenom z predoslej populacie")
    if nova_krv:
        print("2 nahodne deti v kazdej generacii su nahradene 2 novymi permutaciami")
    if vypisy:
        print("Ciastkove vypisy pocas evolucie aktivne")

    povodne_suradnice_list = [list(suradnica) for suradnica in povodne_suradnice]

    povodny_graf = Graf(povodne_suradnice_list)
    najlepsi_jedinec_zo_vsetkych = povodny_graf
    populacia = []
    for i in range(pocet_clenov_populacie):
        populacia.append(povodny_graf.permutuj())

    pole_indexov = range(pocet_clenov_populacie)

    pole_priemerov = []
    pole_maxim = []

    for cislo_generacie in range(pocet_generacii):
        pravdepodobnosti = []
        for jedinec in populacia:
            pravdepodobnosti.append(jedinec.get_fitnes())

        priemerny_fitnes_populacie = sum(pravdepodobnosti) / len(pravdepodobnosti)
        pole_priemerov.append(priemerny_fitnes_populacie)

        jedinec = najdi_najlepsieho(populacia)
        pole_maxim.append(jedinec.get_fitnes())

        dvojice_rodicov = vyber_rodicov(pocet_clenov_populacie, pole_indexov, pravdepodobnosti)

        nova_populacia = []
        for rodicia in dvojice_rodicov:
            deti = porod(populacia[rodicia[0]], populacia[rodicia[1]], pravdepodobnost_mutacie)
            nova_populacia += deti

        if nova_krv:
            a = np_random.randint(0, pocet_clenov_populacie)
            b = np_random.randint(0, pocet_clenov_populacie)
            nova_populacia[a] = povodny_graf.permutuj()
            nova_populacia[b] = povodny_graf.permutuj()

        populacia = nova_populacia

        najlepsi_z_populacie = najdi_najlepsieho(populacia)

        if najlepsi_z_populacie.get_dlzka() < najlepsi_jedinec_zo_vsetkych.get_dlzka():
            najlepsi_jedinec_zo_vsetkych = najlepsi_z_populacie
        elif ponechat_najlepsieho:
            najhorsi_jedinec = najdi_najhorsieho(populacia)
            index_najhorsieho = populacia.index(najhorsi_jedinec)
            populacia[index_najhorsieho] = najlepsi_jedinec_zo_vsetkych

        if vypisy:
            if ((cislo_generacie + 1) % 1000) == 0:
                print("Poradove cislo generacie", cislo_generacie + 1)
                print("Oznacenie generacie", cislo_generacie)
                print("Priemerny fitnes populacie v tejto generacii je ", priemerny_fitnes_populacie)
                print("Najlepsi jedinec tejto generacie ma fitnes", najlepsi_z_populacie.get_fitnes())
                print("Najlepsi jedinec zo vsetkych populacii s dlzkou {}".format(
                    (najlepsi_jedinec_zo_vsetkych.get_dlzka())))
                oddelovac()

    najlepsi_z_poslednej = najdi_najlepsieho(populacia)
    print(
        "S dlzkou cesty {} je najlepsi najdeny jedinec z poslednej populacie:".format(najlepsi_z_poslednej.get_dlzka()))
    print(najlepsi_z_poslednej)
    print("Jeho fitnes je", najlepsi_z_poslednej.get_fitnes())
    if najlepsi_z_poslednej.get_dlzka() != najlepsi_jedinec_zo_vsetkych.get_dlzka():
        print("Najlepsi jedinec z poslednej populacie je iny ako najlepsi jedinec zo vsetkych populacii.")
        print("Najlepsi jedinec zo vsetkych populacii s dlzkou {} "
              "je:".format((najlepsi_jedinec_zo_vsetkych.get_dlzka())))
        print(najlepsi_jedinec_zo_vsetkych)
        print("Jeho fitnes je", najlepsi_jedinec_zo_vsetkych.get_fitnes())
    oddelovac()

    return pole_priemerov, pole_maxim, najlepsi_z_poslednej


def generuj_suradnice():
    """
    Funkcia na generovanie nahodneho poctu miest z rozmedzia <20; 40> so suradnicami <0; 200>
    :return: List suradnic miest
    """

    pocet_miest = np_random.randint(20, 41)
    suradnice = []

    while len(suradnice) != pocet_miest:
        x = np_random.randint(0, 201)
        y = np_random.randint(0, 201)
        mesto = [x, y]
        if mesto not in suradnice:
            suradnice.append(mesto)
    return suradnice


def charakterizuj(seed, vyber_rodicov, pocet_generacii, pravdepodobnost_mutacie,
                         pocet_clenov_populacie, ponechat_najlepsieho, nova_krv):
    """
    Vytvori charakteristiku riesenia do nazvu suboru
    :return: string charakteristiky
    """

    charakteristika = "S"+str(seed)+"V"+vyber_rodicov.__name__[0]+"G"+str(pocet_generacii)+"C"+\
                      str(pocet_clenov_populacie)+"M"+str(pravdepodobnost_mutacie)+\
                      "N"+str(ponechat_najlepsieho)[0].lower()+"K"+str(nova_krv)[0].lower()

    return charakteristika


def generuj_excel(pole_priemerov, pole_maxim, najlepsi_z_poslednej, charakteristika):
    """
    Zapise vystupy funkcie geneticky_algoritmus do excel suboru.
    :param pole_priemerov: pole vratene funkciou geneticky_algoritmus
    :param pole_maxim: pole vratene funkciou geneticky_algoritmus
    :param najlepsi_z_poslednej: jedinec vrateny funkciou geneticky_algoritmus
    """

    df = pd.DataFrame()
    stlpec = 0

    pole_priemerov.append(" ")
    pole_priemerov.append("Fitnes celkoveho najlepsieho")
    pole_priemerov.append(najlepsi_z_poslednej.get_fitnes())
    df.insert(stlpec, "Pokus {} Priemer".format(charakteristika), pole_priemerov, True)
    stlpec += 1
    pole_maxim.append(" ")
    pole_maxim.append("Fitnes celkoveho najlepsieho")
    pole_maxim.append(najlepsi_z_poslednej.get_fitnes())
    df.insert(stlpec, "Pokus {} Maximum".format(charakteristika), pole_maxim, True)
    stlpec += 1

    now = datetime.now()
    nazov = now.strftime("%Y-%m-%d--%H-%M-%S-")
    nazov += charakteristika
    nazov += ".xlsx"

    df.to_excel(nazov, index=True)
    print("Bol vygenerovany subor s vystupmi \"{}\"".format(nazov))


def automaticky_testovac():
    """
    Funkcia pouzita na vygenerovanie testovacich vystupov z testovacich vstupov. Pouzita na vytvorenie vystupov
    popisanych v dokumentacii v casti Testovanie.
    """

    original = sys.stdout
    now = datetime.now()
    nazov = now.strftime("%Y-%m-%d--%H-%M-%S-")
    nazov +="vystup_z_konzoly.txt"

    with open(nazov, "w") as vystup:
        sys.stdout = vystup
        for i in range(8):

            zadane_suradnice = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140),
                                (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40),
                                (200, 40), (20, 20), (60, 20), (160, 20)]

            suradnice = None
            vyber_rodicov = None
            pocet_generacii = 10000
            pocet_clenov_populacie = 40
            pravdepodobnost_mutacie = 0.1
            ponechat_najlepsieho = True
            nova_krv = True
            vypisy = True

            vyber = i

            print("Bola zvolena moznost", vyber)
            if vyber == 0 or vyber == 1:
                seed = 3
                np_random.seed(seed)
                suradnice = zadane_suradnice
                vyber_rodicov = ruleta if vyber == 0 else turnaj
                print("Tato moznost zodpoveda suradniciam zo zadania, cize sa negeneruju. Seed je nastaveny na", seed)
            if vyber == 2 or vyber == 3:
                seed = 11
                np_random.seed(seed)
                suradnice = generuj_suradnice()
                vyber_rodicov = ruleta if vyber == 2 else turnaj
                print("Tato moznost zopoveda suradniciam vygenerovanym randomom so seedom", seed)
            if vyber == 4 or vyber == 5:
                seed = 99
                np_random.seed(seed)
                suradnice = generuj_suradnice()
                vyber_rodicov = ruleta if vyber == 4 else turnaj
                print("Tato moznost zopoveda suradniciam vygenerovanym randomom so seedom", seed)
            if vyber == 6 or vyber == 7:
                seed = 111
                np_random.seed(seed)
                suradnice = generuj_suradnice()
                vyber_rodicov = ruleta if vyber == 6 else turnaj
                print("Tato moznost zopoveda suradniciam vygenerovanym randomom so seedom", seed)

            pole_priemerov, pole_maxim, najlepsi_z_poslednej = geneticky_algoritmus(suradnice, vyber_rodicov,
                                                                                    pocet_generacii=pocet_generacii,
                                                                                    pravdepodobnost_mutacie=pravdepodobnost_mutacie,
                                                                                    pocet_clenov_populacie=pocet_clenov_populacie,
                                                                                    ponechat_najlepsieho=ponechat_najlepsieho,
                                                                                    nova_krv=nova_krv, vypisy=vypisy)

            charakteristika = charakterizuj(seed, vyber_rodicov, pocet_generacii, pravdepodobnost_mutacie,
                                            pocet_clenov_populacie, ponechat_najlepsieho, nova_krv)
            generuj_excel(pole_priemerov, pole_maxim, najlepsi_z_poslednej, charakteristika)

    sys.stdout = original


def riadic():
    """
    Riadiaca funkcia genetickeho algoritmu. Umoznuje pouzivatelovi zvolit rozne rezimy funkcii pre porovnanie vysledkov.
    """

    zadane_suradnice = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140),
                 (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40),
                 (200, 40), (20, 20), (60, 20), (160, 20)]

    pokracovat = "P"

    while pokracovat == "P":
        suradnice = None
        vyber_rodicov = None
        pocet_generacii = 10000
        pocet_clenov_populacie = 40
        pravdepodobnost_mutacie = 0.1
        ponechat_najlepsieho = True
        nova_krv = True
        vypisy = True

        vyber = -1
        while vyber not in range(0, 9):
            oddelovac()
            print("Zvol 0 pre spustenie so suradnicami zo zadania s ruletou")
            print("Zvol 1 pre spustenie so suradnicami zo zadania s turnajom")
            print("Zvol 2 pre testovaciu sadu suradnic A s testovacimi nastaveniami a ruletou")
            print("Zvol 3 pre testovaciu sadu suradnic A s testovacimi nastaveniami a turnajom")
            print("Zvol 4 pre testovaciu sadu suradnic B s testovacimi nastaveniami a ruletou")
            print("Zvol 5 pre testovaciu sadu suradnic B s testovacimi nastaveniami a turnajom")
            print("Zvol 6 pre testovaciu sadu suradnic C s testovacimi nastaveniami a ruletou")
            print("Zvol 7 pre testovaciu sadu suradnic C s testovacimi nastaveniami a turnajom")
            print("Zvol 8 pre vygenerovanie novej nahodnej sady suradnic s vlastnymi nastaveniami")
            vyber = int(input())
            oddelovac()
        print("Bola zvolena moznost", vyber)
        if vyber == 0 or vyber == 1:
            seed = 3
            np_random.seed(seed)
            suradnice = zadane_suradnice
            vyber_rodicov = ruleta if vyber == 0 else turnaj
            print("Tato moznost zodpoveda suradniciam zo zadania, cize sa negeneruju. Seed je nastaveny na", seed)
        if vyber == 2 or vyber == 3:
            seed = 11
            np_random.seed(seed)
            suradnice = generuj_suradnice()
            vyber_rodicov = ruleta if vyber == 2 else turnaj
            print("Tato moznost zopoveda suradniciam vygenerovanym randomom so seedom", seed)
        if vyber == 4 or vyber == 5:
            seed = 99
            np_random.seed(seed)
            suradnice = generuj_suradnice()
            vyber_rodicov = ruleta if vyber == 4 else turnaj
            print("Tato moznost zopoveda suradniciam vygenerovanym randomom so seedom", seed)
        if vyber == 6 or vyber == 7:
            seed = 111
            np_random.seed(seed)
            suradnice = generuj_suradnice()
            vyber_rodicov = ruleta if vyber == 6 else turnaj
            print("Tato moznost zopoveda suradniciam vygenerovanym randomom so seedom", seed)
        if vyber == 8:
            seed = int(input("Zadaj seed pre random: "))
            np_random.seed(seed)
            suradnice = generuj_suradnice()
            print("Tato moznost zopoveda suradniciam vygenerovanym randomom so seedom", seed)

            vyber = -1
            while vyber not in range(20, 41):
                vyber = int(input("Zadaj parny pocet clenov populacie: "))
            pocet_clenov_populacie = vyber

            vyber = -1
            while vyber not in range(1, 100001):
                vyber = int(input("Zadaj pocet generacii: "))
            pocet_generacii = vyber

            vyber_2 = "v"
            while vyber_2 not in ["r", "t"]:
                vyber_2 = input("Zadaj sposob vyberu rodicov, pre ruletu zvol r, pre turnej zvol t: ")
            vyber_rodicov = ruleta if vyber_2 == "r" else turnaj

            vyber_3 = -1.0
            while vyber_3 < 0 or vyber_3 > 1:
                vyber_3 = float(input("Zadaj pravdepodobnosti mutacii deti: "))
            pravdepodobnost_mutacie = vyber_3

            vyber_2 = "v"
            while vyber_2 not in ["a", "n"]:
                vyber_2 = input("Ponechat najlepsieho? Zadaj a pre ano, n pre nie: ")
            ponechat_najlepsieho = True if vyber_2 == "a" else False

            vyber_2 = "v"
            while vyber_2 not in ["a", "n"]:
                vyber_2 = input("Pouzit Novu krv? Zadaj a pre ano, n pre nie: ")
            nova_krv = True if vyber_2 == "a" else False

            vyber_2 = "v"
            while vyber_2 not in ["a", "n"]:
                vyber_2 = input("Vypisat vypis kazdych 1000 generacii? Zadaj a pre ano, n pre nie: ")
            vypisy = True if vyber_2 == "a" else False

        pole_priemerov, pole_maxim, najlepsi_z_poslednej = geneticky_algoritmus(suradnice, vyber_rodicov,
                                    pocet_generacii=pocet_generacii, pravdepodobnost_mutacie=pravdepodobnost_mutacie,
                                    pocet_clenov_populacie=pocet_clenov_populacie, ponechat_najlepsieho=ponechat_najlepsieho,
                                    nova_krv=nova_krv, vypisy=vypisy)

        vyber_2 = "v"
        while vyber_2 not in ["a", "n"]:
            vyber_2 = input("Vygenerovat excel subor s vystupmi? Zadaj a pre ano, n pre nie: ")
        excel = True if vyber_2 == "a" else False

        if excel:
            charakteristika = charakterizuj(seed, vyber_rodicov, pocet_generacii, pravdepodobnost_mutacie,
                             pocet_clenov_populacie, ponechat_najlepsieho, nova_krv)
            generuj_excel(pole_priemerov, pole_maxim, najlepsi_z_poslednej, charakteristika)

        pokracovat = input("Ak si prajete pokracovat, zadajte P: ")


def main():
    """
    Hlavna funkcia programu. Spusta sa nou riadiaca funkcia genetickeho algoritmu, alebo testovacia funkcia.
    """

    # automaticky_testovac()

    riadic()


if __name__ == "__main__":
    main()
