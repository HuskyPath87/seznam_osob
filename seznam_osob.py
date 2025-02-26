import sqlite3

class Seznam:
    # Vytvoření databáze, která uchová naše osoby
    def __init__(self):
        self.osoby = None
        self.conn = sqlite3.connect("databaze_osob.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS databaze_osob (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            krestni_jmeno TEXT NOT NULL,
            prijmeni TEXT NOT NULL,
            vek INTEGER NOT NULL,
            telefonni_cislo TEXT NOT NULL
            )''') # Vytvoření tabulky
        self.conn.commit()

    def __str__(self):
        if self.osoby:
            return "\n".join(str(osoba) for osoba in self.osoby)
        else:
            return "Seznam je prázdný."

    def __del__(self):
        if self.conn:
            self.conn.close()

    def pridat_osobu(self, osoba):
        # Vložení nového člověka do databáze
        self.cursor.execute('''
        INSERT INTO databaze_osob (krestni_jmeno, prijmeni, vek, telefonni_cislo)
        VALUES (?, ?, ?, ?)
        ''', (osoba.krestni, osoba.prijmeni, osoba._vek, osoba._cislo))
        self.conn.commit()
        return f"\nOsoba {osoba.krestni} {osoba.prijmeni} byl(a) úspěšně přidán(a) do databáze."

    def vyhledat_osobu(self, hledane_jmeno):
        # Vyhledá požadovaného člověka podle křestního jména nebo příjmení
        hledane_jmeno = hledane_jmeno.lower()
        self.cursor.execute('''
        SELECT * FROM databaze_osob
        WHERE LOWER(krestni_jmeno) = ? OR LOWER(prijmeni) = ?
        ''', (hledane_jmeno, hledane_jmeno))
        result = self.cursor.fetchall()
        return result

    def vypsat_vsechny(self):
        # Výpis všech lidí z databáze
        self.cursor.execute('SELECT * FROM databaze_osob')
        rows = self.cursor.fetchall()
        if rows:
            return rows  #Vrátí seznam všech záznamů.
        else:
            return "Databáze je prázdná."

    def smazat_osobu(self, id_ke_smazani):
        # Smaže záznam podle ID ze seznamu
        self.cursor.execute('SELECT * FROM databaze_osob WHERE id = ?', (id_ke_smazani,))
        zaznam = self.cursor.fetchone()
        if not zaznam:
            return None  # ID neexistuje
        self.cursor.execute('DELETE FROM databaze_osob WHERE id = ?', (id_ke_smazani,))
        self.conn.commit()
        return zaznam  # Vrátí údaje o smazaném člověku
