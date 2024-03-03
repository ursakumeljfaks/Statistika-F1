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

def poberi_podatke(url):
    '''pridobi podatke o datumu, lokaciji in rezultatih tekme. To zapiše v datoteko "podatki.csv"'''

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
    with open("podatki.csv", "a", encoding="utf8") as dat:
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





# pred začetkom počisti datoteko "podatki.csv"
dat = open("podatki.csv", "w")
dat.close()


urlji = ["https://www.formula1.com/en/results.html/2023/races/1141/bahrain/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1142/saudi-arabia/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1143/australia/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1207/azerbaijan/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1207/azerbaijan/sprint-results.html",
         "https://www.formula1.com/en/results.html/2023/races/1208/miami/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1210/monaco/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1211/spain/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1212/canada/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1213/austria/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1213/austria/sprint-results.html",
         "https://www.formula1.com/en/results.html/2023/races/1214/great-britain/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1215/hungary/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1216/belgium/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1216/belgium/sprint-results.html",
         "https://www.formula1.com/en/results.html/2023/races/1217/netherlands/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1218/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1219/singapore/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1220/japan/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1221/qatar/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1221/qatar/sprint-results.html",
         "https://www.formula1.com/en/results.html/2023/races/1222/united-states/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1222/united-states/sprint-results.html",
         "https://www.formula1.com/en/results.html/2023/races/1223/mexico/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1224/brazil/race-result.html",
         "https://www.formula1.com/en/results.html/2023/races/1224/brazil/sprint-results.html",
         "https://www.formula1.com/en/results.html/2023/races/1225/las-vegas/race-result.html", "https://www.formula1.com/en/results.html/2023/races/1226/abu-dhabi/race-result.html",
         
         "https://www.formula1.com/en/results.html/2022/races/1124/bahrain/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1125/saudi-arabia/race-result.html",
         "https://www.formula1.com/en/results.html/2022/races/1108/australia/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1109/italy/race-result.html", 
         "https://www.formula1.com/en/results.html/2022/races/1109/italy/sprint-results.html",
         "https://www.formula1.com/en/results.html/2022/races/1110/miami/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1111/spain/race-result.html",
         "https://www.formula1.com/en/results.html/2022/races/1112/monaco/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1126/azerbaijan/race-result.html",
         "https://www.formula1.com/en/results.html/2022/races/1113/canada/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1114/great-britain/race-result.html",
         "https://www.formula1.com/en/results.html/2022/races/1115/austria/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1115/austria/sprint-results.html", 
         "https://www.formula1.com/en/results.html/2022/races/1116/france/race-result.html",
         "https://www.formula1.com/en/results.html/2022/races/1117/hungary/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1118/belgium/race-result.html",
         "https://www.formula1.com/en/results.html/2022/races/1119/netherlands/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1120/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2022/races/1133/singapore/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1134/japan/race-result.html", 
         "https://www.formula1.com/en/results.html/2022/races/1135/united-states/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1136/mexico/race-result.html",
         "https://www.formula1.com/en/results.html/2022/races/1137/brazil/race-result.html", "https://www.formula1.com/en/results.html/2022/races/1137/brazil/sprint-results.html",
         "https://www.formula1.com/en/results.html/2022/races/1138/abu-dhabi/race-result.html",
         
         "https://www.formula1.com/en/results.html/2021/races/1064/bahrain/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1065/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1066/portugal/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1086/spain/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1067/monaco/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1068/azerbaijan/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1070/france/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1092/austria/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1071/austria/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1072/great-britain/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1072/great-britain/sprint-results.html",
         "https://www.formula1.com/en/results.html/2021/races/1073/hungary/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1074/belgium/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1075/netherlands/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1076/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1076/italy/sprint-results.html",
         "https://www.formula1.com/en/results.html/2021/races/1077/russia/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1078/turkey/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1102/united-states/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1103/mexico/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1104/brazil/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1104/brazil/sprint-results.html",
         "https://www.formula1.com/en/results.html/2021/races/1105/qatar/race-result.html",
         "https://www.formula1.com/en/results.html/2021/races/1106/saudi-arabia/race-result.html", "https://www.formula1.com/en/results.html/2021/races/1107/abu-dhabi/race-result.html",
         
         "https://www.formula1.com/en/results.html/2020/races/1045/austria/race-result.html", "https://www.formula1.com/en/results.html/2020/races/1046/austria/race-result.html", 
         "https://www.formula1.com/en/results.html/2020/races/1047/hungary/race-result.html", "https://www.formula1.com/en/results.html/2020/races/1048/great-britain/race-result.html",
         "https://www.formula1.com/en/results.html/2020/races/1049/great-britain/race-result.html", "https://www.formula1.com/en/results.html/2020/races/1050/spain/race-result.html",
         "https://www.formula1.com/en/results.html/2020/races/1051/belgium/race-result.html", "https://www.formula1.com/en/results.html/2020/races/1052/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2020/races/1053/italy/race-result.html", "https://www.formula1.com/en/results.html/2020/races/1054/russia/race-result.html",
         "https://www.formula1.com/en/results.html/2020/races/1055/germany/race-result.html", "https://www.formula1.com/en/results.html/2020/races/1056/portugal/race-result.html",
         "https://www.formula1.com/en/results.html/2020/races/1057/italy/race-result.html", "https://www.formula1.com/en/results.html/2020/races/1058/turkey/race-result.html",
         "https://www.formula1.com/en/results.html/2020/races/1059/bahrain/race-result.html", "https://www.formula1.com/en/results.html/2020/races/1060/bahrain/race-result.html",
         "https://www.formula1.com/en/results.html/2020/races/1061/abu-dhabi/race-result.html", 
         
         "https://www.formula1.com/en/results.html/2019/races/1000/australia/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1001/bahrain/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1002/china/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1003/azerbaijan/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1004/spain/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1005/monaco/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1006/canada/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1007/france/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1008/austria/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1009/great-britain/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1010/germany/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1011/hungary/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1012/belgium/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1013/italy/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1014/singapore/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1015/russia/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1016/japan/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1017/mexico/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1018/united-states/race-result.html",
         "https://www.formula1.com/en/results.html/2019/races/1019/brazil/race-result.html", "https://www.formula1.com/en/results.html/2019/races/1020/abu-dhabi/race-result.html"
         
         "https://www.formula1.com/en/results.html/2018/races/979/australia/race-result.html", "https://www.formula1.com/en/results.html/2018/races/980/bahrain/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/981/china/race-result.html", "https://www.formula1.com/en/results.html/2018/races/982/azerbaijan/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/983/spain/race-result.html", "https://www.formula1.com/en/results.html/2018/races/984/monaco/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/985/canada/race-result.html", "https://www.formula1.com/en/results.html/2018/races/986/france/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/987/austria/race-result.html", "https://www.formula1.com/en/results.html/2018/races/988/great-britain/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/989/germany/race-result.html", "https://www.formula1.com/en/results.html/2018/races/990/hungary/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/991/belgium/race-result.html", "https://www.formula1.com/en/results.html/2018/races/992/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/993/singapore/race-result.html", "https://www.formula1.com/en/results.html/2018/races/994/russia/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/995/japan/race-result.html", "https://www.formula1.com/en/results.html/2018/races/996/united-states/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/997/mexico/race-result.html", "https://www.formula1.com/en/results.html/2018/races/998/brazil/race-result.html",
         "https://www.formula1.com/en/results.html/2018/races/999/abu-dhabi/race-result.html",
         
         "https://www.formula1.com/en/results.html/2017/races/959/australia/race-result.html", "https://www.formula1.com/en/results.html/2017/races/960/china/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/961/bahrain/race-result.html", "https://www.formula1.com/en/results.html/2017/races/962/russia/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/963/spain/race-result.html", "https://www.formula1.com/en/results.html/2017/races/964/monaco/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/965/canada/race-result.html", "https://www.formula1.com/en/results.html/2017/races/966/azerbaijan/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/967/austria/race-result.html", "https://www.formula1.com/en/results.html/2017/races/968/great-britain/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/969/hungary/race-result.html", "https://www.formula1.com/en/results.html/2017/races/970/belgium/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/971/italy/race-result.html", "https://www.formula1.com/en/results.html/2017/races/972/singapore/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/973/malaysia/race-result.html", "https://www.formula1.com/en/results.html/2017/races/974/japan/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/975/united-states/race-result.html", "https://www.formula1.com/en/results.html/2017/races/976/mexico/race-result.html",
         "https://www.formula1.com/en/results.html/2017/races/977/brazil/race-result.html", "https://www.formula1.com/en/results.html/2017/races/978/abu-dhabi/race-result.html",
         
         "https://www.formula1.com/en/results.html/2016/races/938/australia/race-result.html", "https://www.formula1.com/en/results.html/2016/races/939/bahrain/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/940/china/race-result.html", "https://www.formula1.com/en/results.html/2016/races/941/russia/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/942/spain/race-result.html", "https://www.formula1.com/en/results.html/2016/races/943/monaco/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/944/canada/race-result.html", "https://www.formula1.com/en/results.html/2016/races/958/europe/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/945/austria/race-result.html", "https://www.formula1.com/en/results.html/2016/races/946/great-britain/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/947/hungary/race-result.html", "https://www.formula1.com/en/results.html/2016/races/948/germany/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/949/belgium/race-result.html", "https://www.formula1.com/en/results.html/2016/races/950/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/951/singapore/race-result.html", "https://www.formula1.com/en/results.html/2016/races/952/malaysia/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/953/japan/race-result.html", "https://www.formula1.com/en/results.html/2016/races/954/united-states/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/955/mexico/race-result.html", "https://www.formula1.com/en/results.html/2016/races/956/brazil/race-result.html",
         "https://www.formula1.com/en/results.html/2016/races/957/abu-dhabi/race-result.html",
         
         "https://www.formula1.com/en/results.html/2015/races/917/australia/race-result.html", "https://www.formula1.com/en/results.html/2015/races/918/malaysia/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/919/china/race-result.html", "https://www.formula1.com/en/results.html/2015/races/920/bahrain/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/921/spain/race-result.html", "https://www.formula1.com/en/results.html/2015/races/922/monaco/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/923/canada/race-result.html", "https://www.formula1.com/en/results.html/2015/races/924/austria/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/925/great-britain/race-result.html", "https://www.formula1.com/en/results.html/2015/races/927/hungary/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/928/belgium/race-result.html", "https://www.formula1.com/en/results.html/2015/races/929/italy/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/930/singapore/race-result.html", "https://www.formula1.com/en/results.html/2015/races/931/japan/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/932/russia/race-result.html", "https://www.formula1.com/en/results.html/2015/races/933/united-states/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/934/mexico/race-result.html", "https://www.formula1.com/en/results.html/2015/races/935/brazil/race-result.html",
         "https://www.formula1.com/en/results.html/2015/races/936/abu-dhabi/race-result.html",
         
         "https://www.formula1.com/en/results.html/2014/races/898/australia/race-result.html", "https://www.formula1.com/en/results.html/2014/races/899/malaysia/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/900/bahrain/race-result.html", "https://www.formula1.com/en/results.html/2014/races/901/china/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/902/spain/race-result.html", "https://www.formula1.com/en/results.html/2014/races/903/monaco/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/904/canada/race-result.html", "https://www.formula1.com/en/results.html/2014/races/905/austria/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/906/great-britain/race-result.html", "https://www.formula1.com/en/results.html/2014/races/907/germany/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/908/hungary/race-result.html", "https://www.formula1.com/en/results.html/2014/races/909/belgium/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/910/italy/race-result.html", "https://www.formula1.com/en/results.html/2014/races/911/singapore/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/912/japan/race-result.html", "https://www.formula1.com/en/results.html/2014/races/913/russia/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/914/united-states/race-result.html", "https://www.formula1.com/en/results.html/2014/races/915/brazil/race-result.html",
         "https://www.formula1.com/en/results.html/2014/races/916/abu-dhabi/race-result.html"]


for url in urlji:
    poberi_podatke(url)