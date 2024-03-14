# Statistika-F1
Ta repozitorij vsebuje projektno nalogo o statistiki Formule 1, katere glavni namen je bil prikazati rezultate posamezne dirke, nekaj več o voznikih, pregled samih ekip in prog. V repozitoriju sta že objavljeni *baza.db* in *podatki.csv*, saj prenos le teh, zaradi večjega števila podatkov, nekoliko dlje traja, zato lahko zaženete le datoteko *spletni_vmesnik.py*. Prav tako projekt uporablja knjižnici *requests* in *Beautiful Soup*. V primeru, da želite vse skupaj stestirati, je postopek sledeč:
1. prenesite si cel repozitorij
2. poženite *pridobi_podatke.py*
3. poženite *baza.py*
4. poženite *spletni_vmesnik.py* in kliknite na ustvarjeno povezavo

Podatke iz uradne strani Formule 1 lahko administrator posodablja tako, da skopira url ([spletna stran F1](https://www.formula1.com/en.html) > results > leto > races > izberite dirko in skopirajte ta url). Administrator se zaradi enostavnosti prijavi z *uporabniškim imenom **admin*** in *geslom **admin***, saj potrebuje le vnesti nove url povezave za prihajajoče dirke. 

ER diagram:
![ER_diagram](https://github.com/ursakumeljfaks/Statistika-F1/assets/57182920/f31b6705-aeed-456e-bd85-372e01838ba4)

Glavna tabela **Rezultat** predstavlja rezultat določenega voznika na določeni dirki. Tabela ima lastnosti id, dirka, voznik, ekipa, mesto, točke, število krogov in številka avtomobila. Lastnosti dirka, voznik in ekipa so tuji ključi, ki se navezujejo na tabele **Dirka**, **Voznik**, in **Ekipa**. 
Tabela **Voznik** predstavlja voznika in ima lastnosti id, ime in priimek. Podobno tabela **Ekipa** predstavlja ekipo in ima lastnosti id in ime. Tabela **Dirka** predstavlja dirko oziroma dogodek. Ta ima lastnosti id, ime, tip dirke, datum, proga in najhitrejši čas. Pri tem je lastnost proga tuji ključ, ki se navezuje na tabelo **Proga**. Ta predstavlja progo in ima lastnosti id, ime in lokacija.
