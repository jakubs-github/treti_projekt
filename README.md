treti_projekt
Třetí projekt na Python Akademii od Engeta.

Popis projektu
Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí najdete [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následně:

$ pip3 --version                    # overim verzi manazeru
$ pip3 install -r requirements.txt  # nainstalujeme knihovny

Spuštění projektu
Spuštění souboru election_scraper.py v rámci přík. řádku požaduje dva povinné argumenty.

python election_scraper <odkaz-uzemniho-celku> <vysledny-soubor>

Následně se vám stahnou výsledky jako soubor s příponou .csv.

Ukázka projektu
Výsledky hlasování pro okres Prostějov:

1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
2. argument: vysledky_prostejov.csv

Spuštění programu:

python election-scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'vysledky_prostejov.csv'

Průběh stahování:

STAHUJI DATA Z VYBRANEHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADAM DO SOUBORU: vysledky_prostejov.csv
UKONCUJI election_scraper

Částečný výstup:

code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,Referendum o Evropské unii,TOP 09,ANO 2011,Dobrá volba 2016,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,Bílovice-Lutotín,431,279,275,13,0,0,32,0,8,40,1,0,4,0,0,30,0,3,83,0,0,22,0,0,0,1,38,0
