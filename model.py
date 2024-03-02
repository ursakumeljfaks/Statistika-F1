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

    def poisci_ekipe(self):
        """
        Vrne ekipo voznika po letih.
        """
        sql = """
            SELECT ekipa.ime, strftime('%Y',dirka.datum) FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
                JOIN ekipa ON ekipa.id = rezultat.ekipa_id
            WHERE rezultat.voznik_id = ?
            GROUP BY strftime('%Y',dirka.datum), ekipa.id
            ORDER BY strftime('%Y',dirka.datum) DESC;
        """
        for ekipa, leto in conn.execute(sql, [self.id]):
            yield (ekipa, leto)
    
    def poisci_skupno_st_tock(self):
        """
        Vrne skupno število točk voznika.
        """
        sql = """
            SELECT SUM(rezultat.tocke) FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
            WHERE rezultat.voznik_id = ?;
        """
        return conn.execute(sql, [self.id]).fetchone()[0]  
        
    def poisci_skupno_st_nastopov(self):
        """
        Vrne skupno število nastopov voznika.
        """
        sql = """
            SELECT COUNT(*) FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
            WHERE rezultat.voznik_id = ? AND dirka.tip = 'dirka';
        """
        return conn.execute(sql, [self.id]).fetchone()[0]
        
    def poisci_skupno_st_zmag(self):
        """
        Vrne skupno število zmag voznika.
        """
        sql = """
            SELECT COUNT(*) FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
            WHERE rezultat.voznik_id = ? AND dirka.tip = 'dirka' AND rezultat.mesto = '1';
        """
        return conn.execute(sql, [self.id]).fetchone()[0] 
    
    def poisci_skupno_st_stopnick(self):
        """
        Vrne skupno število zmag voznika.
        """
        sql = """
            SELECT COUNT(*) FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
            WHERE rezultat.voznik_id = ? AND dirka.tip = 'dirka' AND rezultat.mesto in ('1','2','3');
        """
        return conn.execute(sql, [self.id]).fetchone()[0]
    
    
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