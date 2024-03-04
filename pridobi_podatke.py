import requests
import bs4
import re

def pretvori_cas(cas):
    casi = cas.split(':')
    v_sekundah = 0
    faktor = 1
    for i in range(len(casi) - 1, -1, -1):
        v_sekundah += int(float(casi[i])) * faktor
        faktor *= 60
    return v_sekundah

def poberi_podatke(url, datoteka="podatki.csv"):
    '''pridobi podatke o datumu, lokaciji in rezultatih tekme. To zapiše v datoteko'''
    url = url.strip()
    odgovor1 = requests.get(url) 
    juha1 = bs4.BeautifulSoup(odgovor1.content, "html.parser")

    rezultati = juha1.find("table", attrs={"class": "resultsarchive-table"})
    
    tip_dirke = "dirka"
    if "sprint-results" in url:
        tip_dirke = "sprint"

    lokacija = juha1.find("span", attrs={"class": "circuit-info"}).text.strip().split(",")
    lokacija[1] = lokacija[1].strip() # spredaj en presledek odvec

    datum = juha1.find("span", attrs={"class": "full-date"}).text.strip().split()
    datum[1] = str(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(datum[1]) + 1)
    for i in range(len(datum)):
        if len(datum[i]) == 1:
            datum[i] = "0" + datum[i]


    # zapis v datoteko "podatki.csv"
    with open(datoteka, "a", encoding="utf8") as dat:
        print(f"@,{tip_dirke},{lokacija[0]},{lokacija[1]},{datum[0]},{datum[1]},{datum[2]}", file=dat)
        prva_vrstica = rezultati.find_all("tr")[1].text.strip().split("\n")
        print(f"{prva_vrstica[0]},{prva_vrstica[1]},{prva_vrstica[3] + ' ' + prva_vrstica[4]},{prva_vrstica[7]},{prva_vrstica[8]},{pretvori_cas(prva_vrstica[9])},{prva_vrstica[10]}", file=dat)
        for rezultat in rezultati.find_all("tr")[2:]:
            vrstica = rezultat.text.strip().split('\n')
            mesto = vrstica[0]
            st_avtomobila = vrstica[1]
            voznik = vrstica[3] + ' ' + vrstica[4]
            ekipa = vrstica[7]
            st_krogov = vrstica[8]
            tocke = vrstica[10]
            print(f"{mesto.replace('NC', '0')},{st_avtomobila},{voznik},{ekipa},{st_krogov},{tocke}", file=dat)



if __name__ == "__main__":
    # pred začetkom počisti datoteko "podatki.csv"
    dat = open("podatki.csv", "w")
    dat.close()

    # preberemo podatke
    with open("podatki_urlji.csv", "r", encoding="utf8") as dat:
        vrstica = dat.readline()
        while vrstica != "":
            poberi_podatke(vrstica)
            vrstica = dat.readline()






    