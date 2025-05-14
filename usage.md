# SuperPy - Gebruikershandleiding

> ⚙️ Vereisten: Python 3.10 of hoger, werkend getest op Windows 10. Externe modules: `matplotlib`, `rich`.

SuperPy is een command-line applicatie voor het beheren van supermarktvoorraad, aankopen en verkopen, en het genereren van rapporten.

## 📦 Product toevoegen

```bash
python main.py add "Appel" 0.50 2025-06-01
```

Voegt een appel toe met een inkoopprijs van €0,50 en houdbaar tot 1 juni 2025.

## 💰 Product verkopen

```bash
python main.py sell "Appel" 1.20
```

Verkoopt het oudste beschikbare product met naam "Appel" voor €1,20.

## 📅 Datum instellen en vooruit zetten

```bash
python main.py setdate 2025-05-13
python main.py advance 2
```

De eerste regel stelt de huidige datum in. De tweede regel zet de datum twee dagen vooruit.

## 📊 Rapportage

### Inventaris bekijken:

```bash
python main.py report inventory
```

### Omzet of winst opvragen:

```bash
python main.py report revenue --today
python main.py report profit --date 2025-05
```

### Rapporten exporteren naar CSV:

```bash
python main.py report revenue --date 2025-05-14 --export
```

Genereert een CSV-bestand `revenue_report_2025-05-14.csv`.

## 📈 Visualisatie

```bash
python main.py visualize inventory
```

Toont een staafdiagram van alle producten in de inventaris met hun bijbehorende inkoopprijs. Dit maakt prijsvergelijking tussen producten visueel inzichtelijk.

## ℹ️ Help

Gebruik `--help` bij elk commando voor uitleg:

```bash
python main.py --help
python main.py add --help
python main.py sell --help
python main.py report --help
python main.py visualize --help
```

## 🗂️ Bestanden en opslag

De gegevens worden opgeslagen in CSV-bestanden (`bought.csv`, `sold.csv`) in dezelfde map als het script. Zorg ervoor dat je daar lees- en schrijfrechten hebt. Indien gewenst kun je de paden naar deze bestanden aanpassen in `main.py`.