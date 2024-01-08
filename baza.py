import csv

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

    def uvozi(self, encoding="UTF-8"):
        """
        Metoda za uvoz podatkov.

        Argumenti:
        - encoding: kodiranje znakov
        """
        if self.podatki is None:
            return
        with open(self.podatki, encoding=encoding) as datoteka:
            podatki = csv.reader(datoteka)
            stolpci = next(podatki)
            for vrstica in podatki:
                vrstica = {k: None if v == "" else v for k, v in zip(stolpci, vrstica)}
                self.dodaj_vrstico(**vrstica)

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
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                dirka_id  INTEGER,
                voznik_id INTEGER,
                ekipa_id  INTEGER,
                mesto     INTEGER,
                tocke     INTEGER
            )
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
            )
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
            )
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
                id        INTEGER PRIMARY KEY AUTOINCREMENT REFERENCES rezultat(dirka_id),
                ime       TEXT,
                sezona    INTEGER,
                proga_id  INTEGER
            )
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
                lokacija  TEXT,
                drzava    TEXT
            )
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


def uvozi_podatke(tabele):
    """
    Uvozi podatke v podane tabele.
    """
    for t in tabele:
        print("uvozi v tabelo", t.ime)
        t.uvozi()


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
    oblacilo = Oblacilo(conn)
    return [oblacilo]


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)