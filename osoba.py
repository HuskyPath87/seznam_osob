class Osoba:
    def __init__(self, krestni, prijmeni, vek, cislo):
        self.krestni = krestni
        self.prijmeni = prijmeni
        self._vek = vek
        self._cislo = cislo

    def __str__(self):
            return f"{self.krestni}\t{self.prijmeni}\t{self._vek}\t{self._cislo}"

