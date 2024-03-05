import bottle
from model import Voznik, Ekipa, Proga, Dirka, dodaj_rezultate_dirke


@bottle.route('/prijava/', method=['GET', 'POST'])
def prijava():
    ime = bottle.request.forms.get('uporabnisko_ime')
    geslo = bottle.request.forms.get('geslo')
    if ime == 'admin' and geslo == 'admin':
        bottle.redirect('/izpolnitev/')
    else:
        return bottle.template('prijava.html', uspesnost='Napačno uporabniško ime ali geslo!')


@bottle.get('/izpolnitev/')
def izpolnitev():
    return bottle.template('izpolnitev.html', url="")

@bottle.post('/izpolnitev/')
def izpolnitev():
    url = bottle.request.forms.get('url')
    dodaj_rezultate_dirke(url)
    bottle.redirect('/dirka/')


@bottle.get('/')
def naslovna_stran():
    return bottle.template('naslovna_stran.html', napaka=None)

@bottle.get('/voznik/')
def isci_voznika():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    vozniki = Voznik.poisci(iskalni_niz)
    return bottle.template(
        'voznik.html',
        iskalni_niz=iskalni_niz,
        vozniki=vozniki
    )

@bottle.get('/voznik/<priimek>/')
def tocke_in_zmage_voznika(priimek):
    vozniki = Voznik.poisci(priimek)
    tocke = []
    zmage = []
    profil = []
    ekipe = []
    for voznik in vozniki:
        tocke.extend(voznik.poisci_tocke())
        zmage.extend(voznik.poisci_zmage())
        profil.append((voznik.poisci_skupno_st_nastopov(), 
                       voznik.poisci_skupno_st_zmag(), 
                       voznik.poisci_skupno_st_stopnick(), 
                       voznik.poisci_skupno_st_tock()))
        ekipe.extend(voznik.poisci_ekipe())
    return bottle.template(
        'voznik_vse.html',
        tocke=tocke,
        voznik=voznik,
        zmage=zmage,
        profil=profil,
        ekipe=ekipe
    )

@bottle.get('/ekipa/')
def isci_ekipo():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    ekipe = Ekipa.poisci(iskalni_niz)
    return bottle.template(
        'ekipa.html',
        iskalni_niz=iskalni_niz,
        ekipe=ekipe
    )

@bottle.get('/ekipa/<ime>/')
def voznik_in_leto_ekipe(ime):
    ekipe = Ekipa.poisci(ime)
    vozniki = []
    for ekipa in ekipe:
        vozniki.extend(ekipa.poisci_voznike())
    return bottle.template(
        'ekipa_vse.html',
        vozniki=vozniki,
        ekipa=ekipa
    )

@bottle.get('/proga/')
def isci_progo():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    proge = Proga.poisci(iskalni_niz)
    return bottle.template(
        'proga.html',
        iskalni_niz=iskalni_niz,
        proge=proge
    )

@bottle.get('/proga/<ime>/')
def zmagovalci_proge(ime):
    proge = Proga.poisci(ime)
    zmagovalci = []
    for proga in proge:
        zmagovalci.extend(proga.poisci_zmagovalce())
    return bottle.template(
        'proga_vse.html',
        zmagovalci=zmagovalci,
        proga=proga
    )

@bottle.get('/dirka/')
def isci_leta_dirka():
    leta = Dirka.poisci_leto()
    return bottle.template(
        'dirka.html',
        leta=leta
    )

@bottle.get('/dirka/<leto>/')
def dirka_leto(leto):
    dirke = Dirka.poisci_dirke_v_letu(leto)
    return bottle.template(
        'dirka_leto.html',
        dirke=dirke,
        leto=leto
    )

@bottle.get('/dirka/<leto>/<datum>/')
def dirka_leto(leto, datum):
    rezultati = []
    dirke = Dirka.poisci_dirke_v_letu(leto)
    for dirka in dirke:
        if dirka.datum == datum:
            rezultati.extend(dirka.poisci_rezultate_dirke())

    return bottle.template(
        'dirka_leto_rezultati.html',
        rezultati=rezultati,
        leto=leto,
        dirka=dirka
    )

bottle.run(debug=True, reloader=True)