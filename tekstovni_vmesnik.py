from model import Voznik, Proga, Dirka, dodaj_rezultate_dirke
from enum import Enum
import baza
def vnesi_izbiro(moznosti):
    """
    Uporabniku da na izbiro podane možnosti.
    """
    moznosti = list(moznosti)
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    izbira = None
    while True:
        try:
            izbira = int(input('> ')) - 1
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira!")


def izpisi_zmage(voznik):
    """
    Izpiše vse zmage podanega voznika.
    """
    vsaj_ena = False
    for proga, lokacija, leto in voznik.poisci_zmage():
        vsaj_ena = True
        print(f'- {proga}, {lokacija}, {leto}')
    if not vsaj_ena:
        print(f"{voznik.ime} {voznik.priimek} nima nobene zmage.")


def izpisi_tocke(voznik):
    """
    Izpiše število točk podanega voznika po letih.
    """
    for st_tock, leto in voznik.poisci_tocke():
        print(f'- {leto}: {st_tock} točk')


def izpisi_ekipe(voznik):
    """
    Izpiše ekipo podanega voznika po letih.
    """
    for ekipa, leto in voznik.poisci_ekipe():
        print(f'- {leto}: {ekipa}')


def izpisi_profil(voznik):
    """
    Izpiše skupno število nastopov, zmag, stopničk in točk podanega voznika.
    """
    st_nastopov = voznik.poisci_skupno_st_nastopov()
    st_zmag = voznik.poisci_skupno_st_zmag()
    st_stopnick = voznik.poisci_skupno_st_stopnick()
    st_tock = voznik.poisci_skupno_st_tock()
    
    print(f'Ime: {voznik.ime} {voznik.priimek}')
    print(f'Število nastopov: {st_nastopov}')
    print(f'Število zmag: {st_zmag}')
    print(f'Število stopničk: {st_stopnick}')
    print(f'Število točk: {st_tock}')


def poisci_voznika():
    """
    Poišče voznika, ki ga vnese uporabnik.
    """
    while True:
        vnos = input('Kdo te zanima? ')
        vozniki = list(Voznik.poisci(vnos))
        if len(vozniki) == 1:
            print(vozniki[0].ime, vozniki[0].priimek)
            return vozniki[0]
        elif len(vozniki) == 0:
            print('Tega voznika ne najdem. Poskusi znova.')
        else:
            print('Našel sem več voznikov, kateri od teh te zanima?')
            return vnesi_izbiro(vozniki)


def izpisi_zmagovalce(proga):
    """
    Izpiše vse zmagovalce podane proge.
    """
    for ime, priimek, datum in proga.poisci_zmagovalce():
        print(f'- ({datum}):  {ime} {priimek}')


def poisci_progo():
    """
    Poišče progo, ki jo vnese uporabnik.
    """
    while True:
        vnos = input('Katera proga te zanima? ')
        proge = list(Proga.poisci(vnos))
        if len(proge) == 1:
            print(proge[0].ime + ", " + proge[0].lokacija)
            return proge[0]
        elif len(proge) == 0:
            print('Te proge ne najdem. Poskusi znova.')
        else:
            print('Našel sem več prog, katera od teh te zanima?')
            return vnesi_izbiro(proge)


def izpisi_dirko():
    """
    Izpiše mesto, ime, priimek in število točk vseh voznikov na dirki.
    """
    dirka = poisci_dirko()
    for mesto, ime, priimek, tocke in dirka.poisci_rezultate_dirke():
        print(f'- {mesto}. mesto - {ime} {priimek} - {tocke} točk')
        

def poisci_dirko():
    """
    Poišče dirko, ki jo vnese uporabnik.
    """
    print('Katera sezona/leto te zanima?')
    leto = vnesi_izbiro(list(Dirka.poisci_leto()))
    print('Katera dirka te zanima?')
    dirka = vnesi_izbiro(list(Dirka.poisci_dirke_v_letu(leto)))
    return dirka
        


def voznik_meni():
    """
    Prikazuje voznikov meni, dokler uporabnik ne izbere izhoda.
    """
    voznik = poisci_voznika()
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(VoznikMeni)
        if izbira == VoznikMeni.SEL_NAZAJ:
            return
        izbira.funkcija(voznik)


def proga_meni():
    """
    Prikazuje meni proge, dokler uporabnik ne izbere izhoda.
    """
    proga = poisci_progo()
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(ProgaMeni)
        if izbira == ProgaMeni.SEL_NAZAJ:
            return
        izbira.funkcija(proga)


def dodaj_dirko():
    """
    Prebere url spletne strani, kjer so rezultati dirke in jih doda v bazo.
    """
    url = input("Vnesi url strani, kjer so rezultati dirke: ")
    dodaj_rezultate_dirke(url)
    


def domov():
    """
    Pozdravi pred izhodom.
    """
    print('Adijo!')


def glavni_meni():
    """
    Prikazuje glavni meni, dokler uporabnik ne izbere izhoda.
    """
    print('Pozdravljen v bazi Formule 1!')
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(GlavniMeni)
        izbira.funkcija()
        if izbira == GlavniMeni.SEL_DOMOV:
            return

class Meni(Enum):
    """
    Razred za izbire v menijih.
    """
    def __init__(self, ime, funkcija):
        """
        Konstruktor izbire.
        """
        self.ime = ime
        self.funkcija = funkcija

    def __str__(self):
        """
        Znakovna predstavitev izbire.
        """
        return self.ime



class VoznikMeni(Meni):
    """
    Izbire v meniju voznika.
    """
    IZPISAL_PROFIL = ('Izpisal profil', izpisi_profil)
    IZPISAL_ZMAGE = ('Izpisal zmage', izpisi_zmage)
    IZPISAL_TOCKE = ('Izpisal število točk', izpisi_tocke)
    IZPISAL_EKIPE = ('Izpisal ekipo', izpisi_ekipe)
    SEL_NAZAJ = ('Šel nazaj', glavni_meni)


class ProgaMeni(Meni):
    """
    Izbire v meniju proge.
    """
    IZPISAL_ZMAGOVALCE = ('Izpisal zmagovalce', izpisi_zmagovalce)
    SEL_NAZAJ = ('Šel nazaj', glavni_meni)


class GlavniMeni(Meni):
    """
    Izbire v glavnem meniju.
    """
    ISKAL_VOZNIKA = ('Iskal voznika', voznik_meni)
    ISKAL_PROGO = ('Iskal progo', proga_meni)
    ISKAL_DIRKO = ('Iskal rezultate dirke', izpisi_dirko)
    DODAL_DIRKO = ('Dodal rezultate dirke', dodaj_dirko)
    SEL_DOMOV = ('Šel domov', domov)






glavni_meni()