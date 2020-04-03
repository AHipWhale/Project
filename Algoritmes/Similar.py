import psycopg2
import random

c = psycopg2.connect("dbname=DATABASENAAM user=postgres password=DATABASE WACHTWOORD") #Hiermee connect je met je database
cursor = c.cursor()
"""In dit algoritme worden vier vergelijkbare producten gereturned.Deze producten worden aan de hand 
van verschillen de factoren bepaalt."""

def similar(prodid):
    """Deze definitie is het begin van het algoritme. In deze definitie word gekeken naar het subsubcategorie van het
    meegegeven product id. De definitie pakt de producten met dezelfde subsubcategorie."""
    prodid = str(prodid)

    cursor.execute('select sub_sub_categorieid, naam from producten where id = (%s)', (prodid,))
    terug = cursor.fetchall()[0]

    subsubcat = terug[0]
    productnaam = terug[1]

    cursor.execute('select id from producten where sub_sub_categorieid = (%s)', (subsubcat,))
    subsubid = cursor.fetchall()

    subsubids = []

    for i in subsubid:          #Hier worden alle product ids met hetzelfde subsubcategorie in een lijst gezet.
        subsubids.append(i[0])
    subsubids.remove(prodid)    #Het meegegeven product id word uit de lijst gehaald.

    if subsubcat == 74:         #Als het subsubcategorieid 74 is betekent dit dat het geen subsubcategorie heeft.
        return subcategorie(prodid, productnaam)

    elif len(subsubids) >= 4 and len(subsubids) <= 10:  #Als de lijst genoeg product ids bevat, word de definitie klaar uitgevoerd.
        return klaar(prodid, productnaam, subsubids, [])

    elif len(subsubids) < 4:    #Als de lijst te weinig producten bevat, word er gekeken naar de subcategorie.
        return subcategorie(prodid, productnaam)

    elif len(subsubids) > 10:   #Als de lijst te veel product ids bevat, word er gekeken naar de target audience.
        return target_audience(prodid, productnaam, 'sub_sub_categorieid', subsubcat, [])

    else:
        return woord(prodid, productnaam)

def klaar(prodid, naam, voorkeurlijst, lijst):
    """Deze defintie is de laatste voor dit algoritme. Hier word de voorkeurlijst gereturned.
       Als er te weinig ids in voorkeurlijst zit word het aangevult met de bepaalde hoeveelheid ids uit lijst. Als er
       te veel ids in voorkeurlijst zitten, worden er 4 random van gepakt en gereturned. """
    if 'remove' in voorkeurlijst:   #'remove' word uit de lijst gehaald zodat er alleen maar product ids in zitten.
        voorkeurlijst.remove('remove')

    if 'remove' in lijst:           #'remove' word uit de lijst gehaald zodat er alleen maar product ids in zitten.
        lijst.remove('remove')

    if lijst != [] and len(voorkeurlijst) < 4:  #Als lijst niet leeg is en er minder dan 4 elementen in voorkeurlijst zit.
        lijst = modnar(lijst)                   # Word voorkeurlijst aangevult door elementen uit lijst.
        lengte = 4 - len(voorkeurlijst)
        for i in range(lengte):
            voorkeurlijst.append(lijst[i])

    else:
        if len(voorkeurlijst) > 4:                      #Als er meer dan 4 elementen in voorkeulijstzit dan worder er
            voorkeurlijst = modnar(voorkeurlijst)       #via de definitie modnar, vier random product ids gepakt.
    return voorkeurlijst

def categorie(prodid, naam):
    """In deze definitie word gekeken naar de categorie als er te weinig product ids in subcategorie en subsubcategorie
       zitten. In deze definitie word bijna hetzelfde uitgevoerd als bij subsubcategorie en subcategorie
       alleen dan met categorieën. De definitie pakt de producten met dezelfde categorie."""
    cursor.execute('select categorieid from producten where id = (%s)', (prodid,))
    cat = cursor.fetchall()[0][0]

    cursor.execute('select id from producten where categorieid = (%s)', (cat,))
    catid = cursor.fetchall()

    catids = []

    for i in catid:
        catids.append(i[0])
    catids.remove(prodid)

    if len(catids) >= 4 and len(catids) <= 10:
        return klaar(prodid, naam, catids, [])

    elif len(catids) > 10:
        return target_audience(prodid, naam, 'categorieid', cat, [])

    elif len(catids) < 4:   #Als er te weinig producten zijn met dezelfde categorie, word er gekeken naar de naam van het product.
        return woord(prodid, naam)

def subcategorie(prodid, naam):
    """In deze definitie word gekeken naar de subcategorie als er te weinig product ids in subsubcategorie
           zitten. In deze definitie word bijna hetzelfde uitgevoerd als bij subsubcategorie en categorie
           alleen dan met subcategorieën. De definitie pakt de producten met dezelfde subcategorie."""
    cursor.execute('select sub_categorieid from producten where id = (%s)', (prodid,))
    subcat = cursor.fetchall()[0][0]

    cursor.execute('select id from producten where sub_categorieid = (%s)', (subcat,))
    subcatid = cursor.fetchall()

    subcatids = []
    for i in subcatid:
        subcatids.append(i[0])
    subcatids.remove(prodid)

    if len(subcatids) >= 4 and len(subcatids) <= 10:
        return klaar(prodid, naam, subcatids, [])

    elif len(subcatids) > 10:
        return target_audience(prodid, naam, 'sub_categorieid', subcat, [])

    elif len(subcatids) < 4:
        return categorie(prodid, naam)

def target_audience(prodid, naam, zoeken, search, status):
    """In deze definitie word gekeken naar de target audience van het gekozen product en pakt de producten met dezelfde target audience."""
    cursor.execute('select target_audienceid from producten where id = (%s)', (prodid,))
    target = cursor.fetchall()[0][0]

    cursor.execute('select id from producten where '+ zoeken +' = (%s) and target_audienceid = (%s)', (search, target))
    targetid = cursor.fetchall()

    targetids = []

    for i in targetid:
        targetids.append(i[0])
    targetids.remove(prodid)

    if status == []:    #Als een algoritme naar de volgende filter gaat word het status [] meegegeven.
                        #Stel dat bij de volgende filter te weinig product ids uitkomen,
                        #dan geven we deze producten mee naar het vorige algoritme.
        if len(targetids) >= 4 and len(targetids) <= 10:
            return klaar(prodid, naam, targetids, [])

        elif len(targetids) > 10:
            return typetest(prodid, naam, zoeken, search, target, [])

        elif len(targetids) < 4:
            if zoeken == 'sub_sub_categorieid':
                return subcategorie(prodid, naam)

            elif zoeken == 'sub_categorieid':
                return categorie(prodid, naam)

            elif zoeken == 'categorieid':
                return woord(prodid, naam)

    else:               #Als de status niet leeg is, betekent dit dat er niet genoeg product ids uitkwamen bij de volgende filter.
                        #Als voorkeurlijst geeft de definitie de ids van status mee. Deze ids zijn beter gefilterd.
                        #Zo krijgen we het beste resultaat
        return klaar(prodid, naam, status, targetids)

def typetest(prodid, naam, zoeken, search, target, status):
    """In deze definitie word gekeken naar het type van het gekozen product en pakt de producten met hetzelfde type."""
    cursor.execute('select typeid from producten where id = (%s)', (prodid,))
    type = cursor.fetchall()[0][0]

    cursor.execute('select id from producten where ' + zoeken + ' = (%s) and target_audienceid = (%s) and typeid = (%s)',(search, target, type))
    typeid = cursor.fetchall()

    typeids = []

    for i in typeid:
        typeids.append(i[0])
    typeids.remove(prodid)

    if typeids == []:
        return target_audience(prodid, naam, zoeken, search, ['remove'])

    elif status == []:
        if len(typeids) >= 4 and len(typeids) <= 10:
            return klaar(prodid, naam, typeids, [])

        elif len(typeids) > 10:
            return price(prodid, naam, zoeken, search, target, type, [])

        elif len(typeids) < 4:
            return target_audience(prodid, naam, zoeken, search, typeids)

    else:
        return klaar(prodid, naam, status, typeids)

def price(prodid, naam, zoeken, search, target, type, status):
    """In deze definitie word gekeken naar de prijs van het gekozen product. We pakken dan producten binnen de pricerange.
    De pricerange is per prijscategorie anders zodat de resultaten het best zijn."""
    cursor.execute('select verkoopprijs from producten where id = (%s)', (prodid,))
    prijs = cursor.fetchall()[0][0]

    if prijs <= 2000:
        prijsrangemax = prijs * 2
        prijsrangemin = prijs // 2

    elif prijs > 2000 and prijs <= 5000:
        prijsrangemax = prijs * 1.75
        prijsrangemin = prijs // 1.75

    elif prijs > 5000 and prijs <= 30000:
        prijsrangemax = prijs * 1.5
        prijsrangemin = prijs // 1.5

    else:
        prijsrangemax = prijs * 1.25
        prijsrangemin = prijs // 1.25

    cursor.execute('select id from producten where ' + zoeken + ' = (%s) and target_audienceid = (%s) and typeid = (%s) and verkoopprijs > (%s) and verkoopprijs <= (%s)',(search, target, type, int(prijsrangemin), int(prijsrangemax)))
    prijsid = cursor.fetchall()

    prijsids = []

    for i in prijsid:
        prijsids.append(i[0])
    prijsids.remove(prodid)

    if prijsids == []:
        return typetest(prodid, naam, zoeken, search, target, ['remove'])

    elif status == []:
        if len(prijsids) >= 4 and len(prijsids) <= 10:
            return klaar(prodid, naam, prijsids, [])

        elif len(prijsids) < 4:
            return typetest(prodid, naam, zoeken, search, target, prijsids)

        elif len(prijsids) > 10:
            return brand(prodid, naam, zoeken, search, target, type, prijsrangemax, prijsrangemin, [])

    else:
        return klaar(prodid, naam, status, prijsids)

def brand(prodid, naam, zoeken, search, target, type, prijsrangemax, prijsrangemin, status):
    """Deze definitie kijkt naar het merk van het gekozen product en pakt de producten met hetzelfde merk."""
    cursor.execute('select merkid from producten where id = (%s)', (prodid,))
    merk = cursor.fetchall()[0][0]

    cursor.execute('select id from producten where ' + zoeken + ' = (%s) and target_audienceid = (%s) and typeid = (%s) and verkoopprijs >= (%s) and verkoopprijs <= (%s) and merkid = (%s)',(search, target, type, int(prijsrangemin), int(prijsrangemax), merk))
    merkid = cursor.fetchall()

    merkids = []

    for i in merkid:
        merkids.append(i[0])
    merkids.remove(prodid)

    if merkids == []:
        return price(prodid, naam, zoeken, search, target, type, ['remove'])

    elif status == []:
        if len(merkids) < 4:
            return price(prodid, naam, zoeken, search, target, type, merkids)

        else:
            return klaar(prodid, naam, merkids, [])

    else:
        return klaar(prodid, naam, status, merkids)

def woord(prodid, naam):
    """In deze definite word er gekeken naar het eerste woord van het gekozen product en pakt de producten die
       hetzelfde woord bevatten."""
    if ' ' in naam:
        naamlijst = naam.split(' ')
        name = naamlijst[0]

    else:
        name = naam

    cursor.execute('select id from producten where naam like (%s)', ('% '+name+' %',))
    ids = cursor.fetchall()

    lijst8 = []

    for i in ids:
        lijst8.append(i[0])
    lijst8.remove(prodid)
    return klaar(prodid, naam, lijst8, [])

def modnar(lijst):
    """Deze definitie zorgt ervoor dat de meegegeven lijst 4 random elementen uit die lijst overhoud."""
    random.shuffle(lijst)   #De lijst word gehusselt
    return lijst[:4]        #De eerste 4 elementen word gereturned
