from seznam_osob import Seznam
from osoba import Osoba
from menu import Menu

class Rozhrani:
    def __init__(self):
        self.seznam = Seznam()

    @staticmethod
    def _vycisti_obrazovku():
    # Čistič obrazovky
        import os as _os
        _os.system('cls' if _os.name == 'nt' else 'clear')

    def vykresli_menu(self):
    # Zobrazí menu a nechá uživatele vybrat akci
        while True:
            self._vycisti_obrazovku()
            Menu.vykresli_menu()
            vyber = input("Zadejte akci: \n")
            if vyber.strip() == "1" or vyber.lower().startswith("přidat"):
                self._pridej_osobu()
            elif vyber.strip() == "2" or vyber.lower().startswith("vypsat"):
                self._vypis_vsechny()
            elif vyber.strip() == "3" or vyber.lower().startswith("vyhledat"):
                self._vyhledej_osobu()
            elif vyber.strip() == "4" or vyber.lower().startswith("smazat"):
                self._vymaz_osobu()
            elif vyber.strip() == "5" or vyber.lower() == "konec":
                self._ukonci_program()
            else:
                print("Takový povel neznám. Zkusíme to znovu.")
                input("Stiskněte Enter pro pokračování...")

    @staticmethod
    def _ukonci_program():
    # Ukončení celého programu
        print("Nashledanou!")
        exit()

    @staticmethod
    def _ziskej_ano_ne_odpoved(otazka):
    # Pokud je potřeba ano/ne odpověď, bez odpovědi vrátí do hlavního menu
        pokusy = 0
        while pokusy < 6:
            odpoved = input(f"{otazka} (ano/ne): ").strip().lower()
            if odpoved == 'ano':
                return True
            elif odpoved == 'ne':
                return False
            else:
                pokusy += 1
                if pokusy == 4:
                    print("\nAle notak, volba je jen mezi ano a ne.")
                elif pokusy == 6:
                    print("\nOk, na to nemám trpělivost, vrátím tě do hlavní nabídky.")
                    input("Trhni si...")
                    return None  # Tímto se vrátí do hlavní nabídky

    def _pridej_osobu(self):
    # Pridání nového člověka do seznamu
        krestni = self._ziskej_jmeno("Zadejte křestní jméno: ")
        prijmeni = self._ziskej_jmeno("Zadejte příjmení: ")
        vek = self._ziskej_vek()
        cislo = self._ziskej_cislo()
        nova_osoba = Osoba(krestni, prijmeni, vek, cislo)
        print(self.seznam.pridat_osobu(nova_osoba))
        input("\nData byla uložena. Stiskněte Enter pro pokračování...")

    @staticmethod
    def _ziskej_jmeno(dotaz):
    # Zadání křestního jména nebo příjmení a kontrola, že jméno je delší jak dva znaky a není prázdné.
        while True:
            jmeno = input(f"{dotaz}").strip()
            if len(jmeno) < 2 or "":
                print("Jméno musí být delší jak 2 znaky. Zkuste zadat znovu.\n")
            else:
                return jmeno

    @staticmethod
    def _ziskej_vek():
    # Zadání věku a kontrola, že věk je kladné číslo a zároveň není vyšší než 120.
        while True:
            vek = int(input("Zadejte věk: "))
            if 1 < vek < 120:
                return vek
            else:
                print("Věk musí být kladné číslo větší než 0 a menší než 120.")

    @staticmethod
    def _ziskej_cislo():
    # Zadání telefonního čísla a kontrola, že telefonní číslo je platné
        while True:
                cislo = str(input("Zadejte telefonní číslo bez mezer (9 číslis nebo s předvolbou +420): "))
                if len(cislo) == 9 or (cislo.startswith("+420") and len(cislo) == 13):
                    if len(set(cislo)) == 1:  # Kontrola, že všechny znaky nejsou stejné
                        print("Telefonní číslo nemůže být tvořeno stejnými znaky. Zkuste znovu.")
                    else:
                        return cislo
                else:
                    print("Telefonní číslo musí mít 9 číslic nebo předvolbu +420.")

    def _vypis_vsechny(self):
    # Vypíše všechny záznamy v databázi
        vsichni_lidi = self.seznam.vypsat_vsechny()
        if vsichni_lidi:
            self._vypis_nalezene_osoby(vsichni_lidi)
        else:
            self._zpracuj_neuspesne_hledani()
        input("\nStiskněte Enter pro návrat do hlavního menu...")

    def _vyhledej_osobu(self):
    # Vyhledá člověka podle křestního jména nebo příjmení
        while True:
            nalezeni = self._najdi_osobu("vyhledat")
             # Hledá člověka ze seznamu a pokud žádného nenajde, zeptá se, jestli chce uživatel hledat znovu.
            if not nalezeni:
                if not self._zpracuj_neuspesne_hledani():
                    return None
            else:
                self._vypis_nalezene_osoby(nalezeni)
                if not self._ziskej_ano_ne_odpoved("\nChcete zkusit znovu?"):
                    return None

    def _najdi_osobu(self, akce):
    # Pomocná funkce pro vyhledávání lidí podle jména a akce (vyhledat, vymazat atd.)
        while True:
            hledane_jmeno = self._ziskej_jmeno(f"Zadejte křestní jméno nebo příjmení osoby, kterou chcete {akce}: \n")
            nalezeni = self.seznam.vyhledat_osobu(hledane_jmeno)
            return nalezeni

    def _zpracuj_neuspesne_hledani(self):
        # Zpracuje případ, kdy žádný člověk nebyl nalezen.
        print("\nŽádný člověk nebyl nalezen.")
        return self._ziskej_ano_ne_odpoved("\nChcete zkusit znovu?")

    @staticmethod
    def _vypis_nalezene_osoby(nalezeni):
        # Vypíše nalezené záznamy.
        print("\nNalezení lidé:")
        print(f"{'ID':<5} {'Křestní Jméno':<20} {'Příjmení':<20} {'Věk':<10} {'Telefon':<15}")
        print("-" * 75)
        for vysledek in nalezeni:
            print(f"{vysledek[0]:<5} {vysledek[1]:<20} {vysledek[2]:<20} {vysledek[3]:<10} {vysledek[4]:<15}")

    def _vymaz_osobu(self):
    # Najde záznam podle křestního jména nebo příjmení a vypíše je a potom přistoupí ke smazání záznamu.
        while True:
            nalezeni = self._najdi_osobu("vymazat")
            if not nalezeni:
                if not self._zpracuj_neuspesne_hledani():
                    return
            else:
                self._vypis_nalezene_osoby(nalezeni)
                self._zpracuj_smazani_osobu(nalezeni)
                return

    def _zpracuj_smazani_osobu(self, nalezeni):
        # Zpracuje proces smazání záznamu z databáze.
        while True:
            id_ke_smazani = input("\nZadejte ID osoby, kterou chcete smazat, nebo napište 'konec' k vrácení do nabídky: ").strip().lower()
            if id_ke_smazani == 'konec':
                input("Proces ukončen. Vrácení do hlavní nabídky. Stiskněte Enter pro pokračování...")
                return

            if not id_ke_smazani in [str(osoba[0]) for osoba in nalezeni]:
                print("\nZadané ID neexistuje. Zkuste to znovu.")
                continue

            potvrd_smazani = self._ziskej_ano_ne_odpoved("Opravdu chcete smazat tento záznam? ")
            if potvrd_smazani:
                zaznam = self.seznam.smazat_osobu(id_ke_smazani)
                if not zaznam:
                    print("\nZadané ID neexistuje. Zkuste to znovu.")
                else:
                    print("\nVybraný záznam byl smazán:")
                    print(f"{zaznam[1]} {zaznam[2]}")
                    input("\nStiskněte Enter pro návrat do hlavní nabídky...")
                    return
            else:
                print("\nSmazání bylo zrušeno.")
                input("\nStiskněte Enter pro návrat do hlavní nabídky...")
                return



