import bottle

@bottle.get('/')
def naslovna_stran():
    return bottle.template('index.html')

bottle.run(debug=True, reloader=True)