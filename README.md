# Statistika-F1
Ta repozitorij vsebuje projektno nalogo o statistiki Formule 1, katere glavni namen je bil prikazati rezultate posamezne dirke, nekaj več o voznikih, pregled samih ekip in prog. V repozitoriju sta že objavljeni *baza.db* in *podatki.csv*, saj prenos le teh, zaradi večjega števila podatkov, nekoliko dlje traja, zato lahko zaženete le datoteko *spletni_vmesnik.py*. Prav tako projekt uporablja knjižnici *requests* in *Beautiful Soup*. V primeru, da želite vse skupaj stestirati, je postopek sledeč:
1. prenesite si cel repozitorij
2. poženite *pridobi_podatke.py*
3. poženite *baza.py*
4. poženite *spletni_vmesnik.py* in kliknite na ustvarjeno povezavo

Podatke iz uradne strani Formule 1 lahko administrator posodablja tako, da skopira url ([spletna stran F1](https://www.formula1.com/en.html) > results > leto > races > izberite dirko in skopirajte ta url). Administrator se zaradi enostavnosti prijavi z *uporabniškim imenom **admin*** in *geslom **admin***, saj potrebuje le vnesti nove url povezave za prihajajoče dirke. 

![ER diagram F1](https://github.com/ursakumeljfaks/Statistika-F1/assets/57182920/8ccc3eb7-8228-49ce-b05e-ac981af0be97)
