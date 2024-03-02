import bottle
from model import Voznik

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



bottle.run(debug=True, reloader=True)