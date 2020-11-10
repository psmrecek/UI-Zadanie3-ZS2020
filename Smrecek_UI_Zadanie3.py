import math
# import numpy as np
from numpy import random

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
        self.fitnes = self.fitnes_vypocet()

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
        return 1/self.dlzka_cesty()

    def permutuj(self):
        permutacia = random.permutation(self.suradnice)
        permutacia = permutacia.tolist()
        return graf(permutacia)
        # return permutacia

    def mutacia(self):
        # for i in range(100):
        #     index = random.randint(0, self.pocet_miest - 1)
        #     print("{:2d}".format(index), end=" ")
        #     if i % 10 == 0:
        #         print()
        # print()

        index = random.randint(0, self.pocet_miest - 1)
        self.suradnice[index], self.suradnice[index + 1] = self.suradnice[index + 1], self.suradnice[index]

    def __str__(self):
        text = ""
        for index in range(self.pocet_miest):
            text += str(self.suradnice[index])
            if (index + 1) % 10 != 0:
                text += " "
            else:
                text += "\n"
        return text

def main():
    zaciatok_funkcie(main.__name__, True)

    suradnice = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140),
            (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40),
            (200, 40), (20, 20), (60, 20), (160, 20)]

    # suradnice = [(0, 0), (5, 3), (8, 12)]
    # suradnice = [(0, 0)]
    # suradnice = [(0, 0), (5, 3)]

    kontrola = [15, 14, 11, 13, 19, 17, 10, 6, 4, 3, 0, 16, 5, 9, 8, 2, 12, 18, 1, 7]
    kontrolne_suradnice = []
    for index in kontrola:
        kontrolne_suradnice.append(suradnice[index])

    povodny_graf = graf(suradnice)
    kontrolny_graf = graf(kontrolne_suradnice)

    print("Povodny graf")
    print(povodny_graf.pocet_miest)
    print(povodny_graf.dlzka_cesty())
    print(povodny_graf.fitnes)
    print(povodny_graf.fitnes_vypocet())

    # permutacne_suradnice = []
    # for i in range(8):
    #     permutacne_suradnice.append((i, 10-i))
    # permutacny_graf = graf(permutacne_suradnice)
    # print(permutacny_graf.suradnice)
    # novy_permutacny = permutacny_graf.permutuj()
    # with np.printoptions(suppress=True):
    #     print(novy_permutacny.suradnice)
    #     print(novy_permutacny.suradnice[0])

    print("Nahodna permutacia povodneho grafu")
    novy_graf = povodny_graf.permutuj()
    print(novy_graf.pocet_miest)
    print(novy_graf.dlzka_cesty())
    print(novy_graf.fitnes)
    print(novy_graf.fitnes_vypocet())
    # print(novy_graf.suradnice)
    print(novy_graf)
    novy_graf.mutacia()
    print("Po mutacii")
    print(novy_graf)

    print("Kontrolny graf")
    print(kontrolny_graf.pocet_miest)
    print(kontrolny_graf.dlzka_cesty())
    print(kontrolny_graf.fitnes)
    print(kontrolny_graf.fitnes_vypocet())


    zaciatok_funkcie(main.__name__, False)


if __name__ == "__main__":
    main()
