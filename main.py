## Imports
import argparse
import csv
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

## Console voor Rich output
console = Console()

## Inventaris bestand
inventory_csv = 'C:\\Users\\Arie\\OneDrive - Florys Groep B.V\\Documenten\\Persoonlijk\\Opleiding\\Python\\superpy\\bought.csv'
sales_csv = 'C:\\Users\\Arie\\OneDrive - Florys Groep B.V\\Documenten\\Persoonlijk\\Opleiding\\Python\\superpy\\sold.csv'

## Datumbeheer functies
def set_current_date(new_date):
    with open('current_date.txt', 'w') as file:
        file.write(new_date)

def get_current_date():
    try:
        with open('current_date.txt', 'r') as file:
            current_date = file.read()
            return datetime.strptime(current_date, '%Y-%m-%d').date()
    except FileNotFoundError:
        return datetime.now().date()

def advance_date(days):
    current_date = get_current_date()
    new_date = current_date + timedelta(days=days)
    set_current_date(new_date.strftime('%Y-%m-%d'))

## Productbeheer functies

# Functie voor product toevoegen aan bought.csv
def add_product_inventory(product_name, buy_date, buy_price, expiration_date, inventory_csv='bought.csv'):
    with open(inventory_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        with open(inventory_csv, 'r') as file:
            reader = csv.reader(file)
            existing_data = list(reader)
            # Bepaal het volgende ID op basis van het aantal bestaande regels (excl. header) in bought.csv
            current_id = len(existing_data)
        current_id += 1
        writer.writerow([current_id, product_name, buy_date, buy_price, expiration_date])

# Functie voor het verkopen van producten die vervolgens toegevoegd worden aan sold.csv
def sell_product(product_name, sell_date, sell_price, inventory_csv=inventory_csv, sales_csv=sales_csv):
    # Lees alle gekochte producten met de gevraagde naam
    with open(inventory_csv, 'r') as file:
        reader = csv.DictReader(file)
        bought_items = [row for row in reader if row['product_name'] == product_name]

    # Lees alle reeds verkochte bought_ids
    sold_ids = set()
    try:
        with open(sales_csv, 'r') as file:
            reader = csv.DictReader(file)
            sold_ids = {row['bought_id'] for row in reader}
    except FileNotFoundError:
        pass

    # Filter de nog niet verkochte producten
    available_items = [item for item in bought_items if item['id'] not in sold_ids]

    if not available_items:
        console.print(f"[red]Geen beschikbaar product gevonden om te verkopen: {product_name}[/red]")
        return

    # Selecteer het oudste beschikbare item (first in first out principe)
    item_to_sell = available_items[0]
    bought_id = item_to_sell['id']

    # Bepaal het verkoop-ID
    try:
        with open(sales_csv, 'r') as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
            current_id = len(existing_data) + 1
    except FileNotFoundError:
        current_id = 1

    # Schrijf de verkoop naar sold.csv
    fieldnames = ['id', 'bought_id', 'sell_date', 'sell_price']
    write_header = not os.path.exists(sales_csv) or os.stat(sales_csv).st_size == 0

    with open(sales_csv, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow({
            'id': current_id,
            'bought_id': bought_id,
            'sell_date': sell_date,
            'sell_price': sell_price
        })

    console.print(f"[green]Product {product_name} (bought_id: {bought_id}) is verkocht.[/green]")

## Rapportage functies

# Inventory report maakt een tabel met Rich output op basis van de producten uit bought.csv
def report_inventory(export=False):
    table = Table(title="Inventory Report")
    table.add_column("ID", style="cyan")
    table.add_column("Product Name", style="cyan")
    table.add_column("Buy Date", style="magenta")
    table.add_column("Buy Price", style="green")
    table.add_column("Expiration Date", style="red")

    export_rows = []

    try:
        with open(inventory_csv, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                table.add_row(row['id'], row['product_name'], row['buy_date'], row['buy_price'], row['expiration_date'])
                export_rows.append(row)
    except FileNotFoundError as fnf_error:
        console.print(f"Het bestand {inventory_csv} is niet gevonden: {fnf_error}", style="bold red")
    except Exception as e:
        console.print(f"Er is een fout opgetreden: {e}", style="bold red")

    console.print(table)

    if export:
        filename = "inventory_report.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date'])
            writer.writeheader()
            writer.writerows(export_rows)
        console.print(f"[green]Inventaris geëxporteerd naar {filename}[/green]")

# Revenue report rapporteert omzet op basis van verkochte producten uit bought.csv
def report_revenue(date_filter=None, export=False):
    total_revenue = 0
    export_rows = []

    with open(sales_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sell_date = row['sell_date']
            if date_filter:
                # Filter op maand als de datumfilter formaat 'YYYY-MM' heeft
                if len(date_filter) == 7:
                    if not sell_date.startswith(date_filter):
                        continue
                else:
                    if sell_date != date_filter:
                        continue
            try:
                total_revenue += float(row['sell_price'])
                export_rows.append(row)
            except ValueError:
                console.print(f"Fout bij het lezen van regel: {row}", style="bold red")

    console.print(f"Total Revenue: {total_revenue:.2f}")

    if export:
        filename = f"revenue_report_{date_filter or 'all'}.csv".replace(":", "-")
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['id', 'bought_id', 'sell_date', 'sell_price'])
            writer.writeheader()
            writer.writerows(export_rows)
        console.print(f"[green]Rapport geëxporteerd naar {filename}[/green]")

# Profit report rapporteert winst op basis van verkoopprijs - inkoopprijs
def report_profit(date_filter=None, export=False):
    total_revenue = 0
    total_cost = 0
    sold_ids = []
    export_rows = []

    with open(sales_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sell_date = row['sell_date']
            if date_filter:
                # Filter op maand als de datumfilter formaat 'YYYY-MM' heeft
                if len(date_filter) == 7:
                    if not sell_date.startswith(date_filter):
                        continue
                else:
                    if sell_date != date_filter:
                        continue
            try:
                total_revenue += float(row['sell_price'])
                sold_ids.append(row['bought_id'])
                export_rows.append(row)
            except ValueError:
                console.print(f"Fout bij het lezen van verkoopregel: {row}", style="bold red")

    with open(inventory_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] in sold_ids:
                try:
                    total_cost += float(row['buy_price'])
                except ValueError:
                    console.print(f"Fout bij het lezen van inkoopregel: {row}", style="bold red")

    profit = total_revenue - total_cost
    rounded_profit = round(profit, 2)
    formatted_profit = f"{rounded_profit:.2f}".rstrip('0').rstrip('.')
    console.print(f"Total Profit: {formatted_profit}")

    if export:
        filename = f"profit_report_{date_filter or 'all'}.csv".replace(":", "-")
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['id', 'bought_id', 'sell_date', 'sell_price'])
            writer.writeheader()
            writer.writerows(export_rows)
        console.print(f"[green]Winstgegevens geëxporteerd naar {filename}[/green]")


# Visualisatie functie in een bar chart van de producten met inkoopprijs
def visualize_inventory():
    product_names = []
    buy_prices = []

    with open(inventory_csv, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Sla de headerregel over bij het lezen van het CSV-bestand
        for row in reader:
            try:
                product_names.append(row[1])       # product_name
                buy_prices.append(float(row[3]))   # buy_price
            except (IndexError, ValueError):
                console.print(f"Fout bij het lezen van regel: {row}", style="bold red")

    plt.bar(product_names, buy_prices)
    plt.xlabel('Product Name')
    plt.ylabel('Buy Price')
    plt.title('Inventory Prices')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Command-Line interface
# Verwerkt CLI-invoer met argparse en voert bijbehorende functies uit.
# - Geen argument → toont overzicht met alle commando's
# - add → voegt product toe met huidige datum
# - sell → verkoopt oudste niet-verkochte product
# - setdate / advance → beheren van interne 'vandaag'-datum
# - report → toont rapportages (inventaris, omzet, winst), met optionele filtering/export
# - visualize → toont visuele weergave van inventarisprijzen

def main():
    parser = argparse.ArgumentParser(
        description='📦 SuperPy - Beheer je supermarktvoorraad'
    )
    subparsers = parser.add_subparsers(dest='command')

    # Subparser voor het toevoegen van producten
    add_parser = subparsers.add_parser('add', help='Voeg een product toe aan de inventaris (product_name, buy_price, expiration_date)')
    add_parser.add_argument('product_name', type=str, help='Naam van het product')
    add_parser.add_argument('buy_price', type=float, help='Koopprijs van het product')
    add_parser.add_argument('expiration_date', type=str, help='Vervaldatum van het product (YYYY-MM-DD)')

    # Subparser voor het verkopen van producten
    sell_parser = subparsers.add_parser('sell', help='Verkoop een product (product_name, sell_price)')
    sell_parser.add_argument('product_name', type=str, help='Naam van het product')
    sell_parser.add_argument('sell_price', type=float, help='Verkoopprijs van het product')

    # Subparser voor het instellen van de huidige datum
    date_parser = subparsers.add_parser('setdate', help='Stel de huidige datum in (YYYY-MM-DD)')
    date_parser.add_argument('new_date', type=str, help='Nieuwe datum (YYYY-MM-DD)')

    # Subparser voor het vooruitzetten van de datum
    advance_parser = subparsers.add_parser('advance', help='Zet de datum vooruit met X dagen')
    advance_parser.add_argument('days', type=int, help='Aantal dagen om vooruit te zetten')

    # Subparser voor rapportage
    report_parser = subparsers.add_parser('report', help='Genereer een rapport (inventory, revenue, profit)')
    report_parser.add_argument('type', type=str, choices=['inventory', 'revenue', 'profit'], help='Type rapport')
    report_parser.add_argument('--today', action='store_true', help='Gebruik de huidige datum voor het rapport')
    report_parser.add_argument('--yesterday', action='store_true', help='Gebruik de datum van gisteren voor het rapport')
    report_parser.add_argument('--date', type=str, help='Specifieke datum (YYYY-MM-DD) of maand (YYYY-MM)')
    report_parser.add_argument('--export', action='store_true', help='Exporteer rapport naar een CSV-bestand')


    # Subparser voor visualisatie
    visualize_parser = subparsers.add_parser('visualize', help='Visualiseer statistieken (momenteel alleen: inventory)')
    visualize_parser.add_argument('type', type=str, choices=['inventory'], help='Type visualisatie')

    args = parser.parse_args()

    # Toon een overzicht van alle commando's als geen subcommando is opgegeven
    if args.command is None:
        console.print("[bold blue]Welkom bij SuperPy CLI![/bold blue]\n")
        console.print("Gebruik een van de volgende commando's:\n", style="bold cyan")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Commando", style="cyan")
        table.add_column("Beschrijving")

        table.add_row("add", "Voeg een product toe (naam, prijs, vervaldatum)")
        table.add_row("sell", "Verkoop een product (naam, verkoopprijs)")
        table.add_row("setdate", "Stel de huidige datum in")
        table.add_row("advance", "Zet de datum x dagen vooruit")
        table.add_row("report", "Genereer rapport (inventory, revenue, profit)")
        table.add_row("visualize", "Visualiseer inventaris als grafiek")

        console.print(table)
        return

    # Uitvoering op basis van subcommando
    if args.command == 'add':
        product_name = args.product_name
        buy_price = args.buy_price
        expiration_date = args.expiration_date
        buy_date = get_current_date().strftime('%Y-%m-%d')
        add_product_inventory(product_name, buy_date, buy_price, expiration_date)
        console.print(f"[green]Product {product_name} is toegevoegd aan bought.csv.[/green]")

    elif args.command == 'sell':
        product_name = args.product_name
        sell_price = args.sell_price
        sell_date = get_current_date().strftime('%Y-%m-%d')
        sell_product(product_name, sell_date, sell_price)
        console.print(f"[green]Product {product_name} is verkocht.[/green]")

    elif args.command == 'setdate':
        new_date = args.new_date
        set_current_date(new_date)
        console.print(f"[yellow]Huidige datum is ingesteld op {new_date}.[/yellow]")

    elif args.command == 'advance':
        days = args.days
        advance_date(days)
        console.print(f"[yellow]Datum is vooruitgezet met {days} dagen.[/yellow]")

    elif args.command == 'report':
        # Bepaal datumfilter op basis van optionele argumenten
        date_filter = None
        if hasattr(args, 'today') and args.today:
            date_filter = get_current_date().strftime('%Y-%m-%d')
        elif hasattr(args, 'yesterday') and args.yesterday:
            date_filter = (get_current_date() - timedelta(days=1)).strftime('%Y-%m-%d')
        elif hasattr(args, 'date') and args.date:
            date_filter = args.date

        # Controleer of export vereist is
        export_to_csv = getattr(args, 'export', False)

        # Roep de juiste rapportfunctie aan met datum en export
        if args.type == 'inventory':
            report_inventory(export_to_csv)
        elif args.type == 'revenue':
            report_revenue(date_filter, export_to_csv)
        elif args.type == 'profit':
            report_profit(date_filter, export_to_csv)

    elif args.command == 'visualize':
        if args.type == 'inventory':
            visualize_inventory()

if __name__ == "__main__":
    main()