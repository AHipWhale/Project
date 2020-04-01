import csv
import psycopg2

c = psycopg2.connect("dbname=(vul database in) user=postgres password=(vul wachtwoord in)") # Voer voor jezelf in
cursor = c.cursor()


def aanbied(cursor):
    """In deze definitie pakken we de meest populaire producten van een database en schrijven die in een .csv bestand"""
    with open('populair.csv', 'w', newline='') as csvout:
        fieldnames = ['productid', 'productnaam']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        cursor.execute("""select producten_id from product_gekocht""")
        prod = cursor.fetchall() # Kijkt hoe vaak elk product is verkocht

        cursor.execute("""select id from producten""")
        producten = cursor.fetchall() # Pakt van elk product één
        
        populair = []
        optellen = []

        for i in producten: # Kijkt hoe vaak een product is verkocht en kijkt ook welk product het is
            optellen.append(prod.count(i))
            populair.append(i[0]])

        top10 = []

        for i in range(0, 10): # Kijkt welk product het vaakst gekocht is en plaatst dit in top10
            maxi = optellen.index(max(optellen))
            top10.append(populair[maxi])
            optellen.remove(optellen[maxi])
            populair.remove(populair[maxi])

        for top in top10: # Zet de top 10 populairste producten in een .csv bestand
            cursor.execute("""select naam from producten where id = (%s)""", (top,))
            naam = cursor.fetchall()

            writer.writerow({
                'productid': top,
                'productnaam': naam[0][0]
            })
