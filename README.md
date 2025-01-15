Elections Scraper

Popis projektu:

Tento projekt slúži k extrahovaniu výsledkov z parlamentných volieb v roku 2017. Odkaz k prehliadnutiu nájdete [tu](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

Inštalácia knihovní:
Knihovne, ktoré sú použité v kódu, sú uložené v súbore requirements.txt
Pre inštaláciu sa doporúča použiť nové virtuálne prostredie a spustiť nasledovne:
pip install -r requirements.txt

Spustenie projektu:
Spustenie súboru election_scraper.py v rámci príkazového riadku požaduje 2 povinné argumenty:
python election_scraper.py <odkaz-územného-celku> <výsledný-súbor>
Následne sa Vám stiahnu výsledky ako súbor s príponou .csv.

Ukážka projektu:
Výsledky hlasovania pre okres Prostějov:
1.argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
2.argument: results_prostejov.csv

Spustenie programu:
python election_scraper.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'results_prostejov.csv'

Priebeh sťahovania:
STAHUJI DATA Z VYBRANÉHO URL:https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADÁM DO SÚBORU: results_prostejov.csv
UKONČUJI election-scraper

Čiastočný výstup: 
číslo,název,voliči v seznamu,vydané obálky,platné hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie.....
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,Bílovice-Lutotín,431,279,275,13,0,0,32,0,8,40,1,0,4,0,0,30,0,3,83,0,0,22,0,0,0,1,38,0
...