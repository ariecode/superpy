# Technisch verslag: SuperPy

## 1. Visualisatie van de inkoopprijs per product met Matplotlib

Om inzicht te krijgen in de inkoopprijzen van producten heb ik een functie toegevoegd die gebruikmaakt van Matplotlib. Met het commando `python main.py visualize inventory` genereert de applicatie automatisch een staafdiagram waarin de namen van de producten op de x-as staan en de bijbehorende inkoopprijzen op de y-as. Dit maakt het voor de gebruiker mogelijk om snel prijsverhoudingen te zien en bijvoorbeeld dure of goedkope producten visueel te identificeren.

De gegevens worden rechtstreeks uit het bestand `bought.csv` gelezen. Door de header over te slaan en elke regel te verwerken, worden foutmeldingen bij onvolledige of incorrecte regels voorkomen. Vervolgens worden de namen en prijzen opgeslagen in aparte lijsten die als invoer dienen voor Matplotlib.

De reden dat ik deze visualisatie heb toegevoegd, is omdat het gebruikers helpt om in één oogopslag trends te herkennen in hun inkoopgedrag. Daarnaast ben ik in mijn dagelijkse werk bezig met het visualiseren van data wat maakt dat ik dat ook graag in deze opdracht doe. Als laatste voegt het een visueel element toe aan een verder tekstgebaseerde CLI-toepassing, wat het gebruiksgemak verhoogt.

Door deze functionaliteit in een apart subcommando (`visualize`) onder te brengen, blijft de code overzichtelijk en uitbreidbaar voor toekomstige grafieken, zoals verkooptrends of winst per maand.

## 2. FIFO-verkooplogica gekoppeld aan `bought_id`

Bij het verkopen van producten moest worden voorkomen dat een product dubbel verkocht wordt. Hiervoor heb ik een systeem gebouwd dat alle aangekochte producten met dezelfde naam opzoekt, en vervolgens controleert of de `bought_id` reeds verkocht is. Alleen het oudste ongebruikte item wordt geselecteerd voor verkoop (First In First Out). Deze aanpak voorkomt dubbele verkopen en maakt winstberekening betrouwbaarder, omdat de originele inkoopprijs van het verkochte item bekend blijft.

## 3. Rapportage met export en filtering

Voor rapportage van omzet en winst heb ik functies gebouwd die data filteren op datum (bijvoorbeeld `--today` of `--date 2025-05`). Deze filters maken het mogelijk om gerichte analyses te doen. Daarnaast kunnen rapporten met de `--export` optie naar CSV worden geschreven, wat nuttig is voor archivering of verdere verwerking in bijvoorbeeld Excel. Deze combinatie van filtering en export verhoogt de praktische bruikbaarheid van de tool aanzienlijk.

Tot slot zijn `rich` en `matplotlib` geïntegreerd voor een aantrekkelijke CLI en grafische visualisatie, wat het gebruiksgemak verder versterkt.