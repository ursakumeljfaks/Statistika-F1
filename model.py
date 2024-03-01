import baza
import sqlite3

conn = sqlite3.connect('baza.db', timeout=10)
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

class Voznik:
    """
    Razred za voznika.
    """

    def __init__(self, ime, priimek, *, id=None):
        """
        Konstruktor voznika.
        """
        self.id = id
        self.ime = ime
        self.priimek = priimek

    def __str__(self):
        """
        Znakovna predstavitev voznika.
        Vrne ime voznika.
        """
        return self.ime + " " + self.priimek

    def poisci_zmage(self):
        """
        Vrne zmage voznika.
        """
        sql = """
            SELECT proga.ime, proga.lokacija, strftime('%Y',dirka.datum) FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
                JOIN proga ON proga.id = dirka.proga_id
            WHERE rezultat.voznik_id = ? AND rezultat.mesto = '1'
            ORDER BY dirka.datum DESC;
        """
        for proga, lokacija, leto in conn.execute(sql, [self.id]):
            yield (proga, lokacija, leto)
    
    def poisci_tocke(self):
        """
        Vrne število točk voznika po letih.
        """
        sql = """
            SELECT SUM(rezultat.tocke), strftime('%Y',dirka.datum) FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
            WHERE rezultat.voznik_id = ?
            GROUP BY strftime('%Y',dirka.datum)
            ORDER BY strftime('%Y',dirka.datum) DESC;
        """
        for st_tock, leto in conn.execute(sql, [self.id]):
            yield (st_tock, leto)

    @staticmethod
    def poisci(niz):
        """
        Vrne vse voznike, ki v imenu vsebujejo dani niz.
        """
        besede = niz.split(' ')
        if len(besede) == 1:
            besede = [besede[0], besede[0]]
        sql = "SELECT id, ime, priimek FROM voznik WHERE ime LIKE ? OR priimek LIKE ?"
        for id, ime, priimek in conn.execute(sql, [f'%{besede[0]}%', f'%{besede[1]}%']):
            yield Voznik(ime=ime, priimek=priimek, id=id)

    def dodaj_v_bazo(self):
        """
        Doda voznika v bazo.
        """
        assert self.id is None
        with conn:
            podatki_voznika = {"ime" : self.ime, "priimek" : self.priimek}
            self.id = Voznik.dodaj_vrstico(**podatki_voznika)