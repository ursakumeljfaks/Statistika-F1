import requests
import bs4


url = "https://www.formula1.com/en/results.html/2023/races/1141/bahrain/race-result.html"
odgovor = requests.get(url) 
juha = bs4.BeautifulSoup(odgovor.content)

rezultati = juha.find("table", attrs={"class": "resultsarchive-table"})

with open("bahrain2023.csv", "w", encoding="utf8") as dat:
    print("mesto,st_avtomobila,voznik,ekipa,st_krogov,cas,tocke", file=dat)
    for rezultat in rezultati.find_all("tr")[1:]:
        vrstica = rezultat.text.strip().split('\n')
        mesto = vrstica[0]
        st_avtomobila = vrstica[1]
        voznik = vrstica[3] + ' ' + vrstica[4]
        ekipa = vrstica[7]
        st_krogov = vrstica[8]
        cas = vrstica[9]
        tocke = vrstica[10]
        print(f"{mesto},{st_avtomobila},{voznik},{ekipa},{st_krogov},{cas},{tocke}", file=dat)