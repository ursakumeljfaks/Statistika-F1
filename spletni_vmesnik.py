import bottle
from model import Voznik

@bottle.get('/')
def naslovna_stran():
    return bottle.template('naslovna_stran.html', napaka=None)

@bottle.get('/voznik/')
def voznik():
    return bottle.template('voznik.html', napaka=None, ime="")

@bottle.post('/voznik/')
def dodaj_voznika_post():
    # zahtevaj_prijavo()
    ime = bottle.request.forms.getunicode('ime')
    if not ime[0].isupper():
        return bottle.template(
            'voznik.html',
            napaka='Ime se mora začeti z veliko začetnico!',
            ime=ime
        )
    else:
        oseba = Voznik(ime)
        oseba.dodaj_v_bazo()
        bottle.redirect('/')

@bottle.get('/voznik/')
def isci():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    osebe = Voznik.poisci(iskalni_niz)
    return bottle.template(
        'voznik.html',
        iskalni_niz=iskalni_niz,
        osebe=osebe
    )




bottle.run(debug=True, reloader=True)