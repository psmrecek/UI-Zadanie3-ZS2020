import math
# import numpy as np
from numpy import random as np_random

def zaciatok_funkcie(funkcia, zac):
    """
    Pomocna debuggovacia funkcia ktora vypise ktora funkcia bola prave spustena a ukoncena.

    :param funkcia: nazov funkcie
    :param zac: boolean ci zacina alebo konci
    :return:
    """

    if zac:
        text = "# Zaciatok funkcie {} #".format(funkcia)
    else:
        text = "# Koniec funkcie {} #".format(funkcia)

    ram = "#" * (len(text))

    print(ram)
    print(text)
    print(ram)


class graf:
    def __init__(self, suradnice):
        self.suradnice = suradnice
        self.pocet_miest = len(self.suradnice)
        self.dlzka = self.dlzka_cesty()
        self.fitnes = self.fitnes_vypocet()

    def get_suradnice(self):
        return self.suradnice

    def get_pocet(self):
        return self.pocet_miest

    def get_dlzka(self):
        return self.dlzka

    def get_fitnes(self):
        return self.fitnes

    def euklidova_vzdialenost(self, vrchol1, vrchol2):
        v1 = self.suradnice[vrchol1]
        v2 = self.suradnice[vrchol2]
        vzdialenost_vrcholov = math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)
        return vzdialenost_vrcholov

    def dlzka_cesty(self):
        predosly = -1
        sum_vzdialenost = 0
        for index in range(self.pocet_miest):
            if predosly == -1:
                predosly = index
                prvy_posledny = self.euklidova_vzdialenost(0, self.pocet_miest-1)
                sum_vzdialenost += prvy_posledny
            else:
                vzdialenost_vrcholov = self.euklidova_vzdialenost(predosly, index)
                sum_vzdialenost += vzdialenost_vrcholov
                predosly = index
        return sum_vzdialenost

    def fitnes_vypocet(self):
        return 1 / self.dlzka

    def permutuj(self):
        permutacia = np_random.permutation(self.suradnice)
        permutacia = permutacia.tolist()
        return graf(permutacia)
        # return permutacia

    def mutacia(self, pravdepodobnost):
        # for i in range(100):
        #     index = np_random.randint(0, self.pocet_miest - 1)
        #     print("{:2d}".format(index), end=" ")
        #     if i % 10 == 0:
        #         print()
        # print()
        if self.pravdepodobnost(pravdepodobnost):
            index = np_random.randint(0, self.pocet_miest - 1)
            self.suradnice[index], self.suradnice[index + 1] = self.suradnice[index + 1], self.suradnice[index]
        #     print("Mutujem")
        # else:
        #     print("Nemutujem")

    def __str__(self):
        text = ""
        for index in range(self.pocet_miest):
            text += str(self.suradnice[index])
            if (index + 1) % 10 != 0:
                text += " "
            elif index != self.pocet_miest - 1:
                text += "\n"
        return text

    def pravdepodobnost(self, zadana_pravdepodobnost):
        p = np_random.rand()
        if p <= zadana_pravdepodobnost:
            return True
        return False

    def test_pravdepodobnosti(self, p):
        ano= 0
        for i in range(100):
            vyskyt = self.pravdepodobnost(p)
            ano += vyskyt
        print(ano)


def mixuj(pocet, surandnice1, suradnice2, hranica_1, hranica_2):
    stred = surandnice1[hranica_1:hranica_2+1]
    zvysne_suradnice = [suradnica for suradnica in suradnice2 if suradnica not in stred]
    vysledok = []

    vysledok += zvysne_suradnice[:hranica_1]
    vysledok += stred
    vysledok += zvysne_suradnice[hranica_1:]

    return vysledok

    # vysledok2 = []
    # zvysne_suradnice2 = [suradnica for suradnica in suradnice2 if suradnica not in stred]
    # aktualny_index_vysledok2 = 0
    # # print("stred", stred)
    # # print("zvysok", zvysne_suradnice2)
    # while(aktualny_index_vysledok2 < hranica_1):
    #     vysledok2.append(zvysne_suradnice2.pop(0))
    #     aktualny_index_vysledok2 += 1
    # # print("vysledok2 po prvom cykle", vysledok2)
    # # print("aktualne po prvom cykle", aktualny_index_vysledok2)
    # vysledok2 += stred
    # # print("vysledok2 po pridani stredu", vysledok2)
    # aktualny_index_vysledok2 = hranica_2 + 1
    # while(aktualny_index_vysledok2 < pocet):
    #     vysledok2.append(zvysne_suradnice2.pop(0))
    #     aktualny_index_vysledok2 += 1
    # # print("vysledok2", vysledok2)
    # if vysledok != vysledok2:
    #     print("Vysledky sa nerovnaju")
    #     print(hranica_1, hranica_2)
    #     print(vysledok)
    #     print(vysledok2)


def porod(rodic1, rodic2):
    pocet = rodic1.get_pocet()
    suradnice_rodic1 = rodic1.get_suradnice()
    suradnice_rodic2 = rodic2.get_suradnice()
    hranica_1 = np_random.randint(0, pocet - 1)
    hranica_2 = np_random.randint(hranica_1 + 1, pocet)
    vysledok_R1R2 = mixuj(pocet, suradnice_rodic1, suradnice_rodic2, hranica_1, hranica_2)
    vysledok_R2R1 = mixuj(pocet, suradnice_rodic2, suradnice_rodic1, hranica_1, hranica_2)

    dieta_1 = graf(vysledok_R1R2)
    dieta_1.mutacia(0.3)
    dieta_2 = graf(vysledok_R2R1)
    dieta_2.mutacia(0.3)

    return [dieta_1, dieta_2]

    # print(pocet)
    # print(suradnice_rodic1)
    # print(suradnice_rodic2)
    # print(hranica_1, hranica_2)
    # print(suradnice_rodic1[hranica_1:hranica_2+1])
    # print(vysledok_R1R2)
    # print(vysledok_R2R1)


def ruleta(pocet_clenov_populacie, pole_indexov, pravdepodobnosti):
    koeficient = 1 / sum(pravdepodobnosti)
    prenasobene_pravdepodobnosti = [prvok * koeficient for prvok in pravdepodobnosti]

    pocet_vyberov = pocet_clenov_populacie // 2
    dvojice_rodicov = []

    for cislo_vyberu in range(pocet_vyberov):
        vyber = np_random.choice(pole_indexov, 2, p=prenasobene_pravdepodobnosti)
        dvojice_rodicov.append(list(vyber))

    return dvojice_rodicov


def najdi_najlepsieho(populacia):
    max = 0
    najlepsi = None
    for jedinec in populacia:
        if jedinec.get_fitnes() > max:
            max = jedinec.get_fitnes()
            najlepsi = jedinec
    return najlepsi

def najdi_najhorsieho(populacia):
    min = 2
    najhorsi = None
    for jedinec in populacia:
        if jedinec.get_fitnes() < min:
            min = jedinec.get_fitnes()
            najhorsi = jedinec
    return najhorsi

def geneticky_algoritmus(povodne_suradnice):
    povodne_suradnice_list = [list(suradnica) for suradnica in povodne_suradnice]
    pocet_clenov_populacie = 40
    povodny_graf = graf(povodne_suradnice_list)
    najlepsi_jedinec = povodny_graf
    populacia = []
    for i in range(pocet_clenov_populacie):
        populacia.append(povodny_graf.permutuj())

    # pocitadlo = 0
    # slabe = 0
    # for jedinec in populacia:
    #     print(pocitadlo, jedinec, jedinec.get_fitnes())
    #     pocitadlo += 1
    #     if jedinec.get_fitnes() < 0.02:
    #         slabe += 1
    # print(slabe)
    # print("-" * 100)

    pole_indexov = range(pocet_clenov_populacie)

    # print("Dlzka povodneho grafu je ", povodny_graf.get_dlzka())

    for cislo_generacie in range(10000):
        pravdepodobnosti = []
        for jedinec in populacia:
            pravdepodobnosti.append(jedinec.get_fitnes())

        dvojice_rodicov = ruleta(pocet_clenov_populacie, pole_indexov, pravdepodobnosti)
        # print(dvojice_rodicov)
        nova_populacia = []
        for rodicia in dvojice_rodicov:
            deti = porod(populacia[rodicia[0]], populacia[rodicia[1]])
            nova_populacia += deti

        # pocitadlo = 0
        # slabe = 0
        # for jedinec in nova_populacia:
        #     # print(pocitadlo, jedinec, jedinec.get_fitnes())
        #     pocitadlo += 1
        #     if jedinec.get_fitnes() < 0.02:
        #         slabe += 1
        # print("Generacia {} ma {} slabych jedincov".format(cislo_generacie + 1, slabe))
        # print("-" * 100)

        populacia = nova_populacia

        najlepsi_z_populacie = najdi_najlepsieho(populacia)
        if najlepsi_z_populacie.get_dlzka() < najlepsi_jedinec.get_dlzka():
            najlepsi_jedinec = najlepsi_z_populacie
            # print("Teraz")
        else:
            najhorsi_jedinec = najdi_najhorsieho(populacia)
            index_najhorsieho = populacia.index(najhorsi_jedinec)
            populacia[index_najhorsieho] = najlepsi_jedinec

        if ((cislo_generacie + 1) % 1000) == 0:
            print("Cislo generacie", cislo_generacie + 1)
            print("Najlepsi jedinec zo vsetkych populacii s dlzkou {} je:".format((najlepsi_jedinec.get_dlzka())))
            print(najlepsi_jedinec)

    # pocitadlo = 0
    # for jedinec in nova_populacia:
    #     print(pocitadlo, jedinec, jedinec.get_fitnes())
    #     pocitadlo += 1


    najlepsi_z_poslednej = najdi_najlepsieho(populacia)
    print("S dlzkou cesty {} je najlepsi najdeny jedinec z poslednej populacie:".format(najlepsi_z_poslednej.get_dlzka()))
    print(najlepsi_z_poslednej)
    if najlepsi_z_poslednej.get_dlzka() != najlepsi_jedinec.get_dlzka():
        print("Najlepsi jedinec zo vsetkych populacii s dlzkou {} je:".format((najlepsi_jedinec.get_dlzka())))
        print(najlepsi_jedinec)
    print("-" * 100)




def main():
    zaciatok_funkcie(main.__name__, True)

    suradnice = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140),
            (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40),
            (200, 40), (20, 20), (60, 20), (160, 20)]

    # np_random.seed(0)

    # suradnice = [(0, 0), (5, 3), (8, 12)]
    # suradnice = [(0, 0)]
    # suradnice = [(0, 0), (5, 3)]

    # print("Povodny graf")
    # povodny_graf = graf(suradnice)
    # print(povodny_graf.pocet_miest)
    # print(povodny_graf.dlzka_cesty())
    # print(povodny_graf.fitnes)
    # print(povodny_graf.fitnes_vypocet())
    # print(povodny_graf)

    # print("Test spravnosti permutacii")
    # permutacne_suradnice = []
    # for i in range(8):
    #     permutacne_suradnice.append((i, 10-i))
    # permutacny_graf = graf(permutacne_suradnice)
    # print(permutacny_graf)
    # novy_permutacny = permutacny_graf.permutuj()
    # print(novy_permutacny)
    # zhoda, nezhoda = 0, 0
    # for i in range(100):
    #     novy_permutacny = permutacny_graf.permutuj()
    #     if set(tuple(row) for row in permutacny_graf.suradnice) == set(tuple(row) for row in novy_permutacny.suradnice):
    #         zhoda += 1
    #     else:
    #         nezhoda += 1
    # print(zhoda, nezhoda)

    # print("Nahodna permutacia povodneho grafu")
    # novy_graf = povodny_graf.permutuj()
    # print(novy_graf.pocet_miest)
    # print(novy_graf.dlzka_cesty())
    # print(novy_graf.fitnes)
    # print(novy_graf.fitnes_vypocet())
    # print(novy_graf)
    # novy_graf.mutacia(0.8)
    # print("Po mutacii")
    # print(novy_graf)

    # print("Test vyskytu mutacii")
    # ano, nie = 0, 0
    # for i in range(100):
    #     stare = novy_graf.suradnice.copy()
    #     novy_graf.mutacia(0.8)
    #     if stare != novy_graf.suradnice:
    #         # print("---------- Teraz sa mutovalo")
    #         ano += 1
    #     else:
    #         # print("---------- Teraz sa NEMUTOVALO")
    #         nie += 1
    # print(ano, nie)

    # print("Kontrolny graf")
    # kontrola = [15, 14, 11, 13, 19, 17, 10, 6, 4, 3, 0, 16, 5, 9, 8, 2, 12, 18, 1, 7]
    # kontrolne_suradnice = []
    # for index in kontrola:
    #     kontrolne_suradnice.append(suradnice[index])
    # kontrolny_graf = graf(kontrolne_suradnice)
    # print(kontrolny_graf.pocet_miest)
    # print(kontrolny_graf.dlzka_cesty())
    # print(kontrolny_graf.fitnes)
    # print(kontrolny_graf.fitnes_vypocet())
    # kontrolny_graf.test_pravdepodobnosti(0.3)

    # print("Tvorba deti z rodicov")
    # dummy_suradnice_tuples = [(10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19)]
    # dummy_suradnice_lists = [list(suradnica) for suradnica in dummy_suradnice_tuples]
    # graf_rodic_1 = graf(dummy_suradnice_lists)
    # # graf_rodic_2 = graf_rodic_1.permutuj()
    # graf_rodic_2 = graf([[17, 17], [10, 10], [16, 16], [15, 15], [18, 18], [14, 14], [12, 12], [11, 11], [13, 13], [19, 19]])
    # porod(graf_rodic_1, graf_rodic_2)

    # print("Vazeny vyber rodicov")
    # pole_indexov = range(10)
    # nahodne_suradnice = [[17, 17], [10, 10], [16, 16], [15, 15], [18, 18], [14, 14], [12, 12], [11, 11], [13, 13], [19, 19]]
    # pravdepodobnosti = [0.05, 0.06, 0.07, 0.08, 0.09, 0.05, 0.04, 0.03, 0.02, 0.01]
    # koeficient = 1/sum(pravdepodobnosti)
    # pravdepodobnosti = [prvok*koeficient for prvok in pravdepodobnosti]
    # pole_indexov = range(len(nahodne_suradnice))
    # vyber = np_random.choice(pole_indexov, 2, p=pravdepodobnosti)
    # print(vyber)
    # print(nahodne_suradnice[vyber[0]], nahodne_suradnice[vyber[1]])

    # print("Test genetickeho algoritmu")
    # dummy_suradnice_tuples2 = [(10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18),
    #                           (19, 19)]
    # nahodne_suradnice2 = [[17, 17], [10, 10], [16, 16], [15, 15], [18, 18], [14, 14], [12, 12], [11, 11], [13, 13],
    #                      [19, 19]]
    # geneticky_algoritmus(dummy_suradnice_tuples2)
    # geneticky_algoritmus(nahodne_suradnice2)


    print("Geneticky algoritmus na povodnom grafe")
    for i in range(1):
        geneticky_algoritmus(suradnice)


    # print("Rozne suradnice")
    # www-m9.ma.tum.de

    # Kod hry E005GR0bdfc058e265c7a51ff68b17616785ac4
    # Length of the optimal tour: 1723.8 pixel
    # geneticky_algoritmus([[15, 1], [30, 3], [22, 29], [52, 46], [1, 49]])



    zaciatok_funkcie(main.__name__, False)


if __name__ == "__main__":
    main()
