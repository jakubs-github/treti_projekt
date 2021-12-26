import csv
import traceback
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def main(url: str, nazev_souboru: str):
    """
    Toto je hlavní funkce, která neobsahuje žádnou
    logiku.
    """
    prubeh_procesu(url, nazev_souboru)


def prubeh_procesu(url: str, nazev_souboru: str):
    """
    Tato funkce zajišťuje celý proces scrapingu,
    tzn. scraping, zpracování dat až po uložení
    do daného souboru.
    """
    print(f"STAHUJI DATA Z VYBRANÉHO URL: {url}")
    data, zahlavi = tvorba_data_list(url)
    print(f"UKLÁDÁM DO SOUBORU: {nazev_souboru}")
    zapis_data(data, zahlavi, nazev_souboru)
    print("UKONČUJI: election_scraper")


def tvorba_data_list(url: str) -> list:
    """
    Tato funkce zahrnuje spouštění jednotlivých
    podfunkcí a finální kompletace, které se týkají
    tvorby konečného listu se všemi potřebnými daty.
    Výstupem je list určený pro zápis csv dat.
    Postup ukládání do listu: zahlavi_list,
    cisla_list, nazvy_obci_list, dalsi_cisla_list,
    cisla_strany_list
    """
    cisla_list = cyklus_pro_cisla(url)
    nazvy_obci_list = cyklus_pro_nazvy_obci(url)
    url_adresy_list = cyklus_pro_href(url)
    nazvy_stran_list = cyklus_pro_jmena_stran(url_adresy_list[0])
    dalsi_cisla_list = cyklus_pro_dalsi_cisla(url_adresy_list)
    cisla_strany_list = cyklus_pro_jmena_stran_pocet(url_adresy_list)
    zahlavi = zpracovani_zahlavi(nazvy_stran_list)

    vse_data_list = list()
    for data in range(len(cisla_list)):
        data_list = list()
        data_list.append(cisla_list[0])
        cisla_list.pop(0)
        data_list.append(nazvy_obci_list[0])
        nazvy_obci_list.pop(0)
        dalsi_cisla_list_bez_zavorek = dalsi_cisla_list[0]
        for dalsi_cislo in dalsi_cisla_list_bez_zavorek:
            data_list.append(dalsi_cislo)
        dalsi_cisla_list.pop(0)
        cisla_strany_list_bez_zavorek = cisla_strany_list[0]
        for cislo_strany in cisla_strany_list_bez_zavorek:
            data_list.append(cislo_strany)
        cisla_strany_list.pop(0)
        vse_data_list.append(data_list)
    return vse_data_list, zahlavi


def zpracovani_odpovedi_serveru(url: str) -> BeautifulSoup:
    """
    Funkce stáhne data ze serveru a vytvoří
    objekt s naparsovaným HTML zdrojovým kódem.
    """
    try:
        odpoved = requests.get(url)
        odpoved.raise_for_status()
        html_kod = BeautifulSoup(odpoved.text, features="html.parser")
        return html_kod
    except:
        print(traceback.sys.exc_info()[:1])
        print("Zadaná cesta neexistuje, zadejte adresu znovu:")


def vyber_hodnoty_ze_sloupce(html_kod: str, nazev_sloupce: str) -> str:
    """
    Tato funkce vybere hodnoty z html dle zadaných tagů a atributů.
    """
    hodnoty_sloupce = html_kod.find_all("td", headers=nazev_sloupce)
    return hodnoty_sloupce


def cyklus_pro_cisla(url) -> list:
    """
    Tato funkce zajišťuje řízení funkcí pro tvorbu
    listu s kódy obcí.
    """
    html = zpracovani_odpovedi_serveru(url)
    cisla_list = iterace_a_ulozeni_cisel(html)
    return cisla_list


def iterace_a_ulozeni_cisel(html_kod) -> list:
    """
    Tato funkce zajišťuje tvorbu listu s kódy
    obcí ze všech sloupců.
    """
    cisla_list = list()
    for index in range(1, 4):
        parametr_pro_cisla = f"t{index}sa1 t{index}sb1"
        sloupec = vyber_hodnoty_ze_sloupce(html_kod, parametr_pro_cisla)
        try:
            for data in sloupec:
                cislo = data.a.get_text()
                cisla_list.append(cislo)
        except TypeError:
            traceback.format_exc()
        except AttributeError:
            traceback.format_exc()
    return cisla_list


def cyklus_pro_nazvy_obci(url: str) -> list:
    """
    Tato funkce zajišťuje řízení funkcí pro tvorbu
    listu s názvy obcí.
    """
    html = zpracovani_odpovedi_serveru(url)
    nazvy_obci_list = iterace_a_ulozeni_obec(html)
    return nazvy_obci_list


def iterace_a_ulozeni_obec(html_kod) -> list:
    """
    Tato funkce zajišťuje vytvoření listu s názvy obcí.
    """
    nazvy_obci_list = list()
    for index in range(1, 4):
        parametr_pro_nazev_obce = f"t{index}sa1 t{index}sb2"
        sloupec = vyber_hodnoty_ze_sloupce(html_kod, parametr_pro_nazev_obce)
        for data in sloupec:
            data_pomlcka = data.string
            if data_pomlcka == "-":
                continue
            else:
                nazev_obce = data.next_element
                nazvy_obci_list.append(nazev_obce)
    return nazvy_obci_list


def cyklus_pro_href(url: str) -> list:
    """
    Tato funkce zajišťuje řízení funkcí pro tvorbu
    listu adresami na jednotlivé obce.
    """
    html = zpracovani_odpovedi_serveru(url)
    url_adresy_list = iterace_a_ulozeni_href(html)
    return url_adresy_list


def iterace_a_ulozeni_href(html_kod) -> list:
    """
    Tato funkce zajišťuje tvorbu listu s url adresami na
    jednotlivé obce.
    """
    url_adresy_list = list()
    for index in range(1, 4):
        parametr_pro_href = f"t{index}sa1 t{index}sb1"
        sloupec = vyber_hodnoty_ze_sloupce(html_kod, parametr_pro_href)
        try:
            for data in sloupec:
                cast_cesty = data.a["href"]
                url_adresa = urljoin("https://volby.cz/pls/ps2017nss/", cast_cesty)
                url_adresy_list.append(url_adresa)
        except TypeError:
            traceback.format_exc()
    return url_adresy_list


def cyklus_pro_jmena_stran(url: str) -> list:
    """
    Tato funkce zajišťuje řízení funkcí pro tvorbu
    listu s jmény stran.
    """
    html = zpracovani_odpovedi_serveru(url)
    jmena_stran_list = iterace_a_ulozeni_jmen_stran(html)
    return jmena_stran_list


def iterace_a_ulozeni_jmen_stran(html_kod) -> list:
    """
    Tato funkce zajišťuje uložení jmen jednotlivých
    volených stran jejiž výstupem je list.
    """
    jmena_stran_list = []
    for index in range(1, 3):
        parametr_pro_strany = f"t{index}sa1 t{index}sb2"
        sloupec = vyber_hodnoty_ze_sloupce(html_kod, parametr_pro_strany)
        for data in sloupec:
            data_pomlcka = data.string
            if data_pomlcka == "-":
                continue
            else:
                strana = data.get_text()
                jmena_stran_list.append(strana)
    return jmena_stran_list


def cyklus_pro_dalsi_cisla(url: list) -> list:
    """
    Tato funkce zajišťuje průběh cyklu pros získání
    dalších hodnot pro jednotlivé obce a vrací jejich
    list.
    """
    dalsi_cisla_list = list()
    for link in url:
        html = zpracovani_odpovedi_serveru(link)
        jeden_link = vyber_a_ulozeni_hodnoty_dalsi_cisla(html)
        dalsi_cisla_list.append(jeden_link)
    return dalsi_cisla_list


def vyber_a_ulozeni_hodnoty_dalsi_cisla(html_kod) -> list:
    """
    Tato funkce tvoří dílčí řadu dalších čísel,
    která je dále zpracována nadřazenou funkcí.
    """
    dohromady = list()
    registrovanych = html_kod.find("td", headers="sa2")
    sloupec_1 = registrovanych.get_text()
    dohromady.append(sloupec_1)
    obalek = html_kod.find("td", headers="sa5")
    sloupec_2 = obalek.get_text()
    dohromady.append(sloupec_2)
    platnych = html_kod.find("td", headers="sa6")
    sloupec_3 = platnych.get_text()
    dohromady.append(sloupec_3)
    return dohromady


def cyklus_pro_jmena_stran_pocet(url: list) -> list:
    """
    Tato funkce zajišťuje průběh cyklu pros získání
    počtu hlasů pro jednotlivé strany a vrací jejich
    list.
    """
    cisla_strany_list = list()
    for link in url:
        html = zpracovani_odpovedi_serveru(link)
        jedna_rada = iterace_a_ulozeni_jmen_stran_pocet(html)
        cisla_strany_list.append(jedna_rada)
    return cisla_strany_list


def iterace_a_ulozeni_jmen_stran_pocet(html_kod) -> list:
    """
    Tato funkce tvoří dílčí řadu čísel, která je
    dále zpracována nadřazenou funkcí.
    """
    cisla_strany_list = list()
    for index in range(1, 3):
        parametr_pro_cislo = f"t{index}sa2 t{index}sb3"
        sloupec = html_kod.find_all("td", headers=parametr_pro_cislo)
        for data in sloupec:
            data_pomlcka = data.string
            if data_pomlcka == "-":
                continue
            else:
                strana = data.get_text()
                cisla_strany_list.append(strana)
    return cisla_strany_list


def zpracovani_zahlavi(jmena_stran: list) -> list:
    """
    Vytvoří kompletní záhlaví, tzn. pevně dané
    počateční pozice + jména obci.
    """
    zahlavi_list = ["code", "location", "registered", "envelopes", "valid"]
    for jmeno in jmena_stran:
        zahlavi_list.append(jmeno)
    return zahlavi_list


def zapis_data(data: list, zahlavi: list, nazev_souboru: str) -> str:
    """
    Pokusí se zapsat údaje se záhlavím a daty
    do souboru formatu .csv.
    """
    try:
        csv_soubor = open(nazev_souboru, "w")
    except FileExistsError:
        return traceback.format_exc()
    except IndexError:
        return traceback.format_exc()
    else:
        zapis_dat = csv.writer(csv_soubor)
        zapis_dat.writerow(zahlavi)
        zapis_dat.writerows(data)
        return "ULOŽENO"
    finally:
        csv_soubor.close()


if __name__ == "__main__":
	main(str(sys.argv[1]), str(sys.argv[2]))