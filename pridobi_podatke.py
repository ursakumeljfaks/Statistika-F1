import requests
import bs4
import re

def pretvori_cas(cas):
    niz = re.match(r'(\d+):(\d+):(\d+)', cas)
    if niz:
        h, min, s = map(int, niz.groups())
        return h * 3600 + min * 60 + s

def poberi_podatke(url):
    '''pridobi podatke o datumu, lokaciji in rezultatih tekme. To zapiše v datoteko "podatki.csv"'''

    odgovor1 = requests.get(url) 
    juha1 = bs4.BeautifulSoup(odgovor1.content, "html.parser")

    rezultati = juha1.find("table", attrs={"class": "resultsarchive-table"})

    lokacija = juha1.find("span", attrs={"class": "circuit-info"}).text.strip().split(",") 

    datum = juha1.find("span", attrs={"class": "full-date"}).text.strip().split()
    datum[0] = int(datum[0])
    datum[1] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(datum[1]) + 1
    datum[2] = int(datum[2])


    # zapis v datoteko "podatki.csv"
    with open("podatki.csv", "a", encoding="utf8") as dat:
        print(f"@,{lokacija[0]}, {lokacija[1]}, {datum[0]}, {datum[1]}, {datum[2]}", file=dat)
        prva_vrstica = rezultati.find_all("tr")[1].text.strip().split("\n")
        print(f"{prva_vrstica[0]},{prva_vrstica[1]},{prva_vrstica[4] + ' ' + prva_vrstica[4]},{prva_vrstica[7]},{prva_vrstica[8]},{pretvori_cas(prva_vrstica[9])},{prva_vrstica[10]}", file=dat)
        for rezultat in rezultati.find_all("tr")[2:]:
            vrstica = rezultat.text.strip().split('\n')
            mesto = vrstica[0]
            st_avtomobila = vrstica[1]
            voznik = vrstica[3] + ' ' + vrstica[4]
            ekipa = vrstica[7]
            st_krogov = vrstica[8]
            tocke = vrstica[10]
            print(f"{mesto.replace('NC', '0')},{st_avtomobila},{voznik},{ekipa},{st_krogov},{tocke}", file=dat)





# pred začetkom počisti datoteko "podatki.csv"
dat = open("podatki.csv", "w")
dat.close()


urlji = ["https://www.formula1.com/en/results.html/2023/races/1141/bahrain/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1142/saudi-arabia/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1143/australia/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1207/azerbaijan/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1208/miami/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1210/monaco/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1211/spain/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1212/canada/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1213/austria/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1214/great-britain/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1215/hungary/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1216/belgium/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1217/netherlands/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1218/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1219/singapore/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1220/japan/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1221/qatar/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1222/united-states/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1223/mexico/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1224/brazil/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1225/las-vegas/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1226/abu-dhabi/race-result.html"]


for url in urlji:
    poberi_podatke(url)


