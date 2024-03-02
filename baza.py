import csv
import sqlite3

PARAM_FMT = ":{}" # za SQLite
# PARAM_FMT = "%s({})" # za PostgreSQL/MySQL


class Tabela:
    """
    Razred, ki predstavlja tabelo v bazi.

    Polja razreda:
    - ime: ime tabele
    - podatki: ime datoteke s podatki ali None
    """
    ime = None
    podatki = None

    def __init__(self, conn):
        """
        Konstruktor razreda.
        """
        self.conn = conn

    def ustvari(self):
        """
        Metoda za ustvarjanje tabele.
        Podrazredi morajo povoziti to metodo.
        """
        raise NotImplementedError

    def izbrisi(self):
        """
        Metoda za brisanje tabele.
        """
        self.conn.execute(f"DROP TABLE IF EXISTS {self.ime};")


    def izprazni(self):
        """
        Metoda za praznjenje tabele.
        """
        self.conn.execute(f"DELETE FROM {self.ime};")

    def dodajanje(self, stolpci=None):
        """
        Metoda za gradnjo poizvedbe.

        Argumenti:
        - stolpci: seznam stolpcev
        """
        return f"""
            INSERT INTO {self.ime} ({", ".join(stolpci)})
            VALUES ({", ".join(PARAM_FMT.format(s) for s in stolpci)});
        """

    def dodaj_vrstico(self, **podatki):
        """
        Metoda za dodajanje vrstice.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        podatki = {kljuc: vrednost for kljuc, vrednost in podatki.items()
                   if vrednost is not None}
        poizvedba = self.dodajanje(podatki.keys())
        cur = self.conn.execute(poizvedba, podatki)
        return cur.lastrowid
    


class Rezultat(Tabela):
    """
    Tabela za rezultate.
    """
    ime = "rezultat"
    podatki = "podatki.csv"

    # def __init__(self, conn, rezultat):
    #     super().__init__(conn)
    #     self.rezultat = rezultat

    def ustvari(self):
        """
        Ustvari tabelo rezultat.
        """
        self.conn.execute("""
            CREATE TABLE rezultat (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                dirka_id      INTEGER,
                voznik_id     INTEGER,
                ekipa_id      INTEGER,
                mesto         INTEGER,
                tocke         INTEGER,
                st_krogov     INTEGER,
                st_avtomobila INTEGER
            );
        """)
    
    def dodaj_vrstico(self, **podatki):
        return super().dodaj_vrstico(**podatki)

class Voznik(Tabela):
    """
    Tabela za voznike.
    """
    ime = "voznik"
    podatki = "podatki.csv"

    # def __init__(self, conn, voznik):
    #     super().__init__(conn)
    #     self.voznik = voznik

    def ustvari(self):
        """
        Ustvari tabelo voznik.
        """
        self.conn.execute("""
            CREATE TABLE voznik (
                id        INTEGER PRIMARY KEY AUTOINCREMENT REFERENCES rezultat(voznik_id),
                ime       TEXT,
                priimek   TEXT
            );
        """)

    def dodaj_vrstico(self, **podatki):
        assert "ime", "priimek" in podatki
        rez = self.conn.execute("SELECT id FROM voznik WHERE ime= :ime AND priimek = :priimek", podatki).fetchone()
        if rez is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = rez
            return id

class Ekipa(Tabela):
    """
    Tabela za ekipe.
    """
    ime = "ekipa"
    podatki = "podatki.csv"

    # def __init__(self, conn, ekipa):
    #     super().__init__(conn)
    #     self.ekipa = ekipa

    def ustvari(self):
        """
        Ustvari tabelo ekipa.
        """
        self.conn.execute("""
            CREATE TABLE ekipa (
                id        INTEGER PRIMARY KEY AUTOINCREMENT REFERENCES rezultat(ekipa_id),
                ime       TEXT
            );
        """)

    def dodaj_vrstico(self, **podatki):
        assert "ime" in podatki
        rez = self.conn.execute("SELECT id FROM ekipa WHERE ime= :ime", podatki).fetchone()
        if rez is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = rez
            return id

class Dirka(Tabela):
    """
    Tabela za dirke.
    """
    ime = "dirka"
    podatki = "podatki.csv"

    # def __init__(self, conn, dirka):
    #     super().__init__(conn)
    #     self.dirka = dirka

    def ustvari(self):
        """
        Ustvari tabelo dirke.
        """
        self.conn.execute("""
            CREATE TABLE dirka (
                id              INTEGER PRIMARY KEY AUTOINCREMENT REFERENCES rezultat(dirka_id),
                tip             TEXT,
                ime             TEXT,
                datum           DATE,
                proga_id        INTEGER,
                najhitrejsi_cas INTEGER  
            );
        """)

    def dodaj_vrstico(self, **podatki):
        assert "ime" in podatki
        rez = self.conn.execute("SELECT id FROM dirka WHERE tip= :tip AND ime= :ime AND datum= :datum AND proga_id= :proga_id AND najhitrejsi_cas= :najhitrejsi_cas", podatki).fetchone()
        if rez is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = rez
            return id

class Proga(Tabela):
    """
    Tabela za proge.
    """
    ime = "proga"
    podatki = "podatki.csv"

    # def __init__(self, conn, proga):
    #     super().__init__(conn)
    #     self.proga = proga

    def ustvari(self):
        """
        Ustvari tabelo proga.
        """
        self.conn.execute("""
            CREATE TABLE proga (
                id        INTEGER PRIMARY KEY AUTOINCREMENT REFERENCES dirka(proga_id),
                ime       TEXT,
                lokacija  TEXT
            );
        """)
    
    def dodaj_vrstico(self, **podatki):
        assert "ime" in podatki
        rez = self.conn.execute("SELECT id FROM proga WHERE ime= :ime AND lokacija= :lokacija", podatki).fetchone()
        if rez is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = rez
            return id


def ustvari_tabele(tabele):
    """
    Ustvari podane tabele.
    """
    for t in tabele:
        t.ustvari()


def izbrisi_tabele(tabele):
    """
    Izbriši podane tabele.
    """
    for t in tabele:
        t.izbrisi()


# def uvozi_podatke(tabele):
#     """
#     Uvozi podatke v podane tabele.
#     """
#     for t in tabele:
#         print("uvozi v tabelo", t.ime)
#         t.uvozi()


def izprazni_tabele(tabele):
    """
    Izprazni podane tabele.
    """
    for t in tabele:
        t.izprazni()


def ustvari_bazo(conn):
    """
    Izvede ustvarjanje baze.
    """
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)
    uvozi_podatke(tabele)


def pripravi_tabele(conn):
    """
    Pripravi objekte za tabele.
    """
    rezultat = Rezultat(conn)
    voznik = Voznik(conn)
    ekipa = Ekipa(conn)
    dirka = Dirka(conn)
    proga = Proga(conn)
    return [rezultat, voznik, ekipa, dirka, proga]


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        #if cur.fetchone() == (0, ):
        ustvari_bazo(conn)
        
def uvozi_podatke(tabele):
    """uvozi vse podatke iz datoteke"""

    rezultat_tabela = tabele[0]
    voznik_tabela = tabele[1]
    ekipa_tabela = tabele[2]
    dirka_tabela = tabele[3]
    proga_tabela = tabele[4]

    with open("podatki.csv", "r", encoding="utf-8") as dat:
        tip_dirke = ""
        kraj = ""
        datum = ""
        proga = ""
        for vrstica in dat:
            podatki = vrstica.split(",")
            if podatki[0] == "@":
                tip_dirke = podatki[1]
                proga = podatki[2]
                kraj = podatki[3]
                
                podatki[-1] = podatki[-1].strip() # pri letu na koncu en odvec preseledek
                datum = "-".join(podatki[4:][::-1])
                

                podatki_proga = {"ime" : proga, "lokacija" : kraj}

            else:

                if podatki[0] == '1':
                    mesto, st_avtomobila, voznik, ekipa, st_krogov, cas, tocke = podatki

                    proga_id = proga_tabela.dodaj_vrstico(**podatki_proga)
                    podatki_dirka = {"tip" : tip_dirke, "ime" : proga, "datum" : datum, "proga_id" : proga_id, "najhitrejsi_cas" : cas}

                else:
                    mesto, st_avtomobila, voznik, ekipa, st_krogov, tocke = podatki
                  
                    
                ime, priimek = voznik.split(" ", 1)

                podatki_voznik = {"ime" : ime, "priimek" : priimek}                        
                podatki_ekipa = {"ime" : ekipa}

                ekipa_id = ekipa_tabela.dodaj_vrstico(**podatki_ekipa)
                dirka_id = dirka_tabela.dodaj_vrstico(**podatki_dirka)
                voznik_id = voznik_tabela.dodaj_vrstico(**podatki_voznik)

                podatki_rezultat = {"dirka_id" : dirka_id, "voznik_id" : voznik_id, "ekipa_id" : ekipa_id, "mesto" : mesto, "tocke" : tocke, "st_krogov" : st_krogov, "st_avtomobila" : st_avtomobila}
                rezultat_tabela.dodaj_vrstico(**podatki_rezultat)
                    
import os
os.remove("baza.db")
conn = sqlite3.connect("baza.db", timeout=10)
#ustvari_bazo_ce_ne_obstaja(conn)
#conn.execute("SELECT * FROM rezultat")