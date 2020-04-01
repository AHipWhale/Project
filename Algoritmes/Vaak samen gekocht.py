import csv
import psycopg2


def anderenkochten(cursor, product):
    """In deze functie kijken we naar een product. Vervolgens kijken naar welke andere gebruikers ook dit product
     hebben gekocht. En dan kijken we welke producten zij allemaal hebben gekocht. Als andere gebruikers veel dezelfde
     producten hebben gekocht, kan het product relaties hebben met deze andere producten."""

    cursor.execute("""select sessies_id from product_gekocht where producten_id = (%s)""", (product,))
    sessies = cursor.fetchall()  # Hier zitten alle sessies in die het product hebben gekocht

    sessions = []  # Één van elke sessie

    for i in sessies:
        if i not in sessions:
            sessions.append(i)

    alles = []

    for i in sessions:
        cursor.execute("""select producten_id from product_gekocht where sessies_id = (%s)""", i)
        producten = cursor.fetchall()  # Alle producten die in deze sessie werden gekocht
        for j in producten:
            alles.append(j[0])

    for i in alles: # Haalt het product, waar we mee begonnen, weg zodat we die niet aanraden
        if i == product:
            alles.remove(i)

    cursor.execute("""select id from producten""")
    producten = cursor.fetchall() # Id's van alle producten

    count = []

    for i in producten: # Tel hoe vaak andere producten in de sessies werden gekocht
        count.append(alles.count(i[0]))

    products = []

    for i in producten:
        products.append(i)

    recommandaties = []

    for i in range(0, 4): # Kijkt wat de vier ondeling meest gekochte producten zijn
        x = count.index(max(count))
        recommandaties.append(products[x][0])
        count.remove(max(count))
        products.remove(products[x])

    return recommandaties # Geeft vier product id's terug


def main():
    with open('samen_gekocht.csv', 'w', newline='') as csvout: # Maakt een .csv bestand aan
        c = psycopg2.connect("dbname=(naam database) user=postgres password=(je wachtwoord)") # Vul zelf in
        cursor = c.cursor()

        fieldnames = ['productid', 'productnaam', 'pd_1', 'pd_2', 'pd_3', 'pd_4']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        cursor.execute("""select id from producten""")
        producten = cursor.fetchall()

        for product in producten: # Voor elk product
            cursor.execute("""select naam from producten where id = (%s)""", product)
            naam = cursor.fetchall() # Naam van het product

            samen = anderenkochten(cursor, product[0]) # Geeft vier recommandaties

            writer.writerow({ # Schrijft alles in het .csv bestand
                'productid': product[0],
                'productnaam': naam[0][0],
                'pd_1': samen[0],
                'pd_2': samen[1],
                'pd_3': samen[2],
                'pd_4': samen[3]
            })
