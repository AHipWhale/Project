import csv
import psycopg2

c = psycopg2.connect("dbname=(voer naam van je database in) user=postgres password=(voer je wachtwoord in)") # Vul zelf in
curs = c.cursor()


def aanbieding(cursor):
    """In deze definitie kijken we welke populaire producten ook in de aanbieding zijn en zetten die in een .csv bestand"""
    with open('aanbieding.csv', 'w', newline='') as csvout:
        fieldnames = ['productid', 'productnaam', 'aanbieding']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        cursor.execute("""select producten_id from product_gekocht""")
        prod = cursor.fetchall() # Kijkt hoe vaak elk product is gekocht

        cursor.execute("""select id from producten""")
        producten = cursor.fetchall() # Pakt één van elk product
        
        populair = []
        optellen = []

        for i in producten: # Kijkt hoe vaak een product gekocht is en over welk product dit gaat en plaatst dit in verschillende lists
            optellen.append(prod.count(i))
            populair.append(i[0])
            
        top10 = []

        while len(top10) < 11:
            maxi = optellen.index(max(optellen)) # Op welke index staat het product dat het vaakst voorkomt
            prod = populair[maxi] # Welk product staat op die index (dus is het populairst)

            cursor.execute("""select aanbieding from producten where id = (%s)""", (prod, ))
            produ = cursor.fetchall() # Kijkt of dit product een aanbieding heeft

            try:
                if produ[0][0] == 'None' or produ[0][0] == None: # Zo nee, dan wissen we hem en gaan we door
                    optellen.remove(optellen[maxi])
                    populair.remove(prod)
                else:
                    top10.append([prod[1], produ[0][0]]) # Zo ja, dan slaan we hem op, wissen we hem en gaan we door
                    optellen.remove(optellen[maxi])
                    populair.remove(prod)
            except:
                continue

        for top in top10: # Schrijft de top tien populairste producten in een .csv bestand
            cursor.execute("""select naam from producten where id = (%s)""", (top[0],))
            naam = cursor.fetchall()

            writer.writerow({
                'productid': top[0],
                'productnaam': naam[0][0],
                'aanbieding': top[1]
            })
