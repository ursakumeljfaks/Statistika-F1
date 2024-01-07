import requests
import bs4


url1 = "https://www.formula1.com/en/results.html/2023/races/1141/bahrain/race-result.html"
odgovor1 = requests.get(url1) 
juha1 = bs4.BeautifulSoup(odgovor1.content)

rezultati = juha1.find("table", attrs={"class": "resultsarchive-table"})

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


url2 = "https://www.formula1.com/en/results.html/2023/races/1142/saudi-arabia/race-result.html"
odgovor2 = requests.get(url2) 
juha2 = bs4.BeautifulSoup(odgovor2.content)

rezultati = juha2.find("table", attrs={"class": "resultsarchive-table"})

with open("saudiArabia2023.csv", "w", encoding="utf8") as dat:
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


url3 = "https://www.formula1.com/en/results.html/2023/races/1143/australia/race-result.html"
odgovor3 = requests.get(url3) 
juha3 = bs4.BeautifulSoup(odgovor3.content)

rezultati = juha3.find("table", attrs={"class": "resultsarchive-table"})

with open("australia2023.csv", "w", encoding="utf8") as dat:
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

url4 = "https://www.formula1.com/en/results.html/2023/races/1207/azerbaijan/race-result.html"
odgovor4 = requests.get(url4) 
juha4 = bs4.BeautifulSoup(odgovor4.content)

rezultati = juha4.find("table", attrs={"class": "resultsarchive-table"})

with open("azerbaijan2023.csv", "w", encoding="utf8") as dat:
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


url17 = "https://www.formula1.com/en/results.html/2022/races/1124/bahrain/race-result.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("bahrain2022.csv", "w", encoding="utf8") as dat:
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

url17 = "https://www.formula1.com/en/results.html/2022/races/1125/saudi-arabia/race-result.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("saudiArabia2022.csv", "w", encoding="utf8") as dat:
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


url8 = "https://www.formula1.com/en/results.html/2022/races/1108/australia/race-result.html"
odgovor8 = requests.get(url8) 
juha8 = bs4.BeautifulSoup(odgovor8.content)

rezultati = juha8.find("table", attrs={"class": "resultsarchive-table"})

with open("australia2022.csv", "w", encoding="utf8") as dat:
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


url17 = "https://www.formula1.com/en/results.html/2022/races/1126/azerbaijan/race-result.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("azerbaijan2022.csv", "w", encoding="utf8") as dat:
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

url17 = "https://www.formula1.com/en/results.html/2021/races/1064/bahrain/race-result.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("bahrain2021.csv", "w", encoding="utf8") as dat:
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

url17 = "https://www.formula1.com/en/results.html/2021/races/1106/saudi-arabia/race-result.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("saudiArabia2021.csv", "w", encoding="utf8") as dat:
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


url17 = "https://www.formula1.com/en/results.html/2021/races/1068/azerbaijan/race-result.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("azerbaijan2021.csv", "w", encoding="utf8") as dat:
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


url17 = "https://www.formula1.com/en/results.html/2023/drivers.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("vozniki2023.csv", "w", encoding="utf8") as dat:
    print("mesto,voznik", file=dat)
    for rezultat in rezultati.find_all("tr")[1:]:
        vrstica = rezultat.text.strip().split('\n')
        mesto = vrstica[0]
        voznik = vrstica[3] + ' ' + vrstica[4]
        print(f"{mesto},{voznik}", file=dat)
    
url17 = "https://www.formula1.com/en/results.html/2022/drivers.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("vozniki2022.csv", "w", encoding="utf8") as dat:
    print("mesto,voznik", file=dat)
    for rezultat in rezultati.find_all("tr")[1:]:
        vrstica = rezultat.text.strip().split('\n')
        mesto = vrstica[0]
        voznik = vrstica[3] + ' ' + vrstica[4]
        print(f"{mesto},{voznik}", file=dat)


url17 = "https://www.formula1.com/en/results.html/2021/drivers.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("vozniki2021.csv", "w", encoding="utf8") as dat:
    print("mesto,voznik", file=dat)
    for rezultat in rezultati.find_all("tr")[1:]:
        vrstica = rezultat.text.strip().split('\n')
        mesto = vrstica[0]
        voznik = vrstica[3] + ' ' + vrstica[4]
        print(f"{mesto},{voznik}", file=dat)


url17 = "https://www.formula1.com/en/results.html/2021/team.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("ekipe2021.csv", "w", encoding="utf8") as dat:
    print("ekipa", file=dat)
    for rezultat in rezultati.find_all("tr")[1:]:
        vrstica = rezultat.text.strip().split('\n')
        ekipa = vrstica[2]
        print(f"{ekipa}", file=dat)


url17 = "https://www.formula1.com/en/results.html/2022/team.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("ekipe2022.csv", "w", encoding="utf8") as dat:
    print("ekipa", file=dat)
    for rezultat in rezultati.find_all("tr")[1:]:
        vrstica = rezultat.text.strip().split('\n')
        ekipa = vrstica[2]
        print(f"{ekipa}", file=dat)


url17 = "https://www.formula1.com/en/results.html/2023/team.html"
odgovor17 = requests.get(url17) 
juha17 = bs4.BeautifulSoup(odgovor17.content)

rezultati = juha17.find("table", attrs={"class": "resultsarchive-table"})

with open("ekipe2023.csv", "w", encoding="utf8") as dat:
    print("ekipa", file=dat)
    for rezultat in rezultati.find_all("tr")[1:]:
        vrstica = rezultat.text.strip().split('\n')
        ekipa = vrstica[2]
        print(f"{ekipa}", file=dat)


