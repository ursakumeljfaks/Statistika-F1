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
        if niz is None:
            return "Vnesi nekaj!"
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


class Ekipa:
    """
    Razred za ekipo.
    """
    
    def __init__(self, ime, id=None):
        """
        Konstruktor ekipe.
        """
        self.id = id
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev ekipe.
        Vrne ime ekipe.
        """
        return self.ime

    @staticmethod
    def poisci(niz):
        """
        Vrne vse ekipe, ki v imenu vsebujejo dani niz.
        """
        if niz is None:
            return "Vnesi nekaj!"
        sql = "SELECT id, ime FROM ekipa WHERE ime LIKE ?"
        for id, ime in conn.execute(sql, [f'%{niz}%']):
            yield Ekipa(id=id, ime=ime)

    def poisci_voznike(self):
        """
        Vrne voznike ekipe po letih.
        """
        sql = """
            SELECT voznik.ime, voznik.priimek, strftime('%Y',dirka.datum) FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
                JOIN voznik ON voznik.id = rezultat.voznik_id
            WHERE rezultat.ekipa_id = ?
            GROUP BY strftime('%Y',dirka.datum), rezultat.ekipa_id
            ORDER BY strftime('%Y',dirka.datum) DESC;
        """
        for voznik_ime, voznik_priimek, leto in conn.execute(sql, [self.id]):
            yield (leto, voznik_ime, voznik_priimek)

class Proga:
    """
    Razred za progo.
    """

    def __init__(self, ime, lokacija, *, id=None):
        """
        Konstruktor proge.
        """
        self.id = id
        self.ime = ime
        self.lokacija = lokacija

    def __str__(self):
        """
        Znakovna predstavitev proge.
        Vrne ime in lokacijo.
        """
        return self.ime + ", " + self.lokacija
    
    
    def poisci_zmagovalce(self):
        """
        Vrne zmagovalce podane proge po letih.
        """
        sql = """
            SELECT voznik.ime, voznik.priimek, dirka.datum FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
                JOIN proga ON proga.id = dirka.proga_id
                JOIN voznik ON voznik.id = rezultat.voznik_id
            WHERE proga.id = ? AND rezultat.mesto = '1' AND dirka.tip = 'dirka'
            ORDER BY dirka.datum DESC;
        """
        for ime, priimek, datum in conn.execute(sql, [self.id]):
            yield (ime, priimek, datum)
    
    @staticmethod
    def poisci(niz):
        """
        Vrne vse proge, ki v imenu vsebujejo dani niz.
        """
        if niz is None:
            return "Vnesi nekaj!"
        sql = "SELECT id, ime, lokacija FROM proga WHERE ime LIKE ? OR lokacija LIKE ?"
        for id, ime, lokacija in conn.execute(sql, [f'%{niz}%', f'%{niz}%']):
            yield Proga(ime=ime, lokacija=lokacija, id=id)


class Dirka:
    """
    Razred za dirko.
    """

    def __init__(self, tip, ime, datum, proga, *, id=None):
        """
        Konstruktor dirke.
        """
        self.id = id
        self.tip = tip
        self.ime = ime
        self.datum = datum
        self.proga = proga

    def __str__(self):
        """
        Znakovna predstavitev dirke.
        Vrne ime in lokacijo.
        """
        return self.ime + ", " + self.datum + ", "+ self.tip
    
    @staticmethod
    def poisci_leto():
        """
        Vrne seznam sezon/let.
        """
        sql = "SELECT DISTINCT(strftime('%Y',dirka.datum)) FROM dirka"
        for leto in conn.execute(sql):
            yield leto[0]

    @staticmethod
    def poisci_dirke_v_letu(leto):
        """
        Vrne vse dirke in datume v danem letu.
        """
        sql = "SELECT id, tip, ime, datum, proga_id FROM dirka WHERE strftime('%Y',dirka.datum) LIKE ?"
        for id, tip, ime, datum, proga in conn.execute(sql, [leto]):
            yield Dirka(tip=tip, ime=ime, datum=datum, proga=proga, id=id)
            
    def poisci_rezultate_dirke(self):
        """
        Vrne mesto, ime, priimek in število točk vseh voznikov na dirki.
        """
        sql = """
            SELECT rezultat.mesto, voznik.ime, voznik.priimek, rezultat.tocke FROM rezultat
                JOIN dirka ON dirka.id = rezultat.dirka_id
                JOIN voznik ON voznik.id = rezultat.voznik_id
            WHERE dirka.id = ? AND rezultat.mesto > 0
            ORDER BY rezultat.mesto ASC;
        """
        for mesto, ime, priimek, tocke in conn.execute(sql, [self.id]):
            yield (mesto, ime, priimek, tocke)