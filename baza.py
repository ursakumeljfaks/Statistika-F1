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


class Voznik(Tabela):
    """
    Tabela za voznike.
    """
    ime = "voznik"
    podatki = "podatki.csv"

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

class Ekipa(Tabela):
    """
    Tabela za ekipe.
    """
    ime = "ekipa"
    podatki = "podatki.csv"

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

class Dirka(Tabela):
    """
    Tabela za dirke.
    """
    ime = "dirka"
    podatki = "podatki.csv"

    def ustvari(self):
        """
        Ustvari tabelo dirke.
        """
        self.conn.execute("""
            CREATE TABLE dirka (
                id              INTEGER PRIMARY KEY AUTOINCREMENT REFERENCES rezultat(dirka_id),
                ime             TEXT,
                datum           DATE,
                proga_id        INTEGER,
                najhitrejsi_cas INTEGER  
            );
        """)

class Proga(Tabela):
    """
    Tabela za proge.
    """
    ime = "proga"
    podatki = "podatki.csv"

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
        
def uvozi_podatke(conn):
    """uvozi vse podatke iz datoteke"""
    with open("podatki.csv", "r", encoding="utf-8") as dat:
        kraj = ""
        datum = ""
        proga = ""
        proga_id = -1
        dirka_id = -1
        for vrstica in dat:
            podatki = vrstica.split(",")
            if podatki[0] == "@":
                proga = podatki[1]
                kraj = podatki[2]
                datum = podatki[3:]

                proga_id = conn.execute("SELECT id FROM proga WHERE ime= :ime", {"ime" : proga}).fetchone()
                if proga_id is None:
                    conn.execute("INSERT INTO proga (ime, lokacija) VALUES (:ime, :lokacija)", {"ime" : proga, "lokacija" : kraj})
                    proga_id = conn.execute("SELECT id FROM proga WHERE ime= :ime AND lokacija= :lokacija", {"ime" : proga, "lokacija" : kraj})
            
            else:

                if podatki[0] == 1:
                    mesto, st_avtomobila, voznik, ekipa, st_krogov, cas, tocke = podatki
                    
                    dirka_id = conn.execute("SELECT id FROM dirka WHERE ime= :ime", {"ime" : proga}).fetchone()
                    if dirka_id is None:
                        conn.execute("INSERT INTO dirka (ime, datum, proga_id, najhitrejsi_cas) VALUES (:ime, :datum, :proga_id, :najhitrejsi_cas)", {"ime" : proga, "datum" : datum, "proga_id" : proga_id, "najhitrejsi_cas" : cas})
                        dirka_id = conn.execute("SELECT id FROM dirka WHERE ime= :ime", {"ime" : proga})
                
                mesto, st_avtomobila, voznik, ekipa, st_krogov, tocke = podatki
                ime, priimek = voznik.split(" ")
                voznik_id = conn.execute("SELECT id FROM voznik WHERE ime= :ime AND priimek = :priimek", {"ime" : ime, "priimek" : priimek}).fetchone()
                if voznik_id is None:
                    conn.execute("INSERT INTO voznik (ime, priimek) VALUES (:ime, :priimek)", {"ime" : ime, "priimek" : priimek})
                    voznik_id = conn.execute("SELECT id FROM voznik WHERE ime= :ime AND priimek = :priimek", {"ime" : ime, "priimek" : priimek})
                
                ekipa_id = conn.execute("SELECT id FROM ekipa WHERE ime= :ime", {"ime" : ekipa}).fetchone()
                if ekipa_id is None:
                    conn.execute("INSERT INTO ekipa (ime) VALUES (:ime)", {"ime" : ekipa})
                    ekipa_id = conn.execute("SELECT id FROM ekipa WHERE ime= :ime", {"ime" : ekipa})

                conn.execute("""INSERT INTO rezultat (dirka_id, voznik_id, ekipa_id, mesto, tocke, st_krogov, st_avtomobila)
                              VALUES (:dirka_id,, :voznik_id, :ekipa_id, :mesto, :tocke, :st_krogov, :st_avtomobila)""",
                              {"dirka_id" : dirka_id, "voznik_id" : voznik_id, "ekipa_id" : ekipa_id, "mesto" : mesto, "tocke" : tocke, "st_krogov" : st_krogov, "st_avtomobila" : st_avtomobila})
                
                            
conn = sqlite3.connect("baza.db")
ustvari_bazo_ce_ne_obstaja(conn)
conn.execute("SELECT * FROM rezultat")
