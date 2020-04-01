import psycopg2
import csv
import random

c = psycopg2.connect("dbname=(voer naam van je database in) user=postgres password=(voer je wachtwoord in)") # Vul zelf in
cursor = c.cursor()


def similar(prodid):
    prodid = str(prodid)
    cursor.execute('select sub_sub_categorieid, naam from producten where id = (%s)', (prodid,))
    iets = cursor.fetchall()[0]
    subsubcat = iets[0]
    productnaam = iets[1]
    cursor.execute('select id from producten where sub_sub_categorieid = (%s)', (subsubcat,))
    tussen = cursor.fetchall()

    lijst = []
    for i in tussen:
        lijst.append(i[0])
    lijst.remove(prodid)

    if subsubcat == 74:
        subcategorie(prodid, productnaam)
    elif len(lijst) >= 4 and len(lijst) <= 10:
        klaar(prodid, productnaam, lijst, [])

    elif len(lijst) < 4:
        subcategorie(prodid, productnaam)

    elif len(lijst) > 10:
        target_audience(prodid, productnaam, 'sub_sub_categorieid', subsubcat, [])
    else:
        woord(prodid, productnaam)


def categorie(prodid, naam):
    cursor.execute('select categorieid from producten where id = (%s)', (prodid,))
    cat = cursor.fetchall()[0][0]
    cursor.execute('select id from producten where categorieid = (%s)', (cat,))
    terug = cursor.fetchall()
    lijst3 = []
    for i in terug:
        lijst3.append(i[0])
    lijst3.remove(prodid)
    if len(lijst3) >= 4 and len(lijst3) <= 10:
        klaar(prodid, naam, lijst3, [])
    elif len(lijst3) > 10:
        target_audience(prodid, naam, 'categorieid', cat, [])
    elif len(lijst3) < 4:
        woord(prodid, naam)


def subcategorie(prodid, naam):
    cursor.execute('select sub_categorieid from producten where id = (%s)', (prodid,))
    subcat = cursor.fetchall()[0][0]
    cursor.execute('select id from producten where sub_categorieid = (%s)', (subcat,))
    terug = cursor.fetchall()
    lijst2 = []
    for i in terug:
        lijst2.append(i[0])
    lijst2.remove(prodid)
    if len(lijst2) >= 4 and len(lijst2) <= 10:
        klaar(prodid, naam, lijst2, [])
    elif len(lijst2) > 10:
        target_audience(prodid, naam, 'sub_categorieid', subcat, [])
    elif len(lijst2) < 4:
        categorie(prodid, naam)


def target_audience(prodid, naam, zoeken, search, status):
    cursor.execute('select target_audienceid from producten where id = (%s)', (prodid,))
    target = cursor.fetchall()[0][0]
    cursor.execute('select id from producten where '+ zoeken +\
                   ' = (%s) and target_audienceid = (%s)', (search, target))
    rug = cursor.fetchall()
    lijst4 = []
    for i in rug:
        lijst4.append(i[0])
    lijst4.remove(prodid)
    if status == []:
        if len(lijst4) >= 4 and len(lijst4) <= 10:
            klaar(prodid, naam, lijst4, [])
        elif len(lijst4) > 10:
            print(str(len(lijst4)) + ' GROTER')
            type(prodid, naam, zoeken, search, target, [])
        elif len(lijst4) < 4:
            if zoeken == 'sub_sub_categorieid':
                subcategorie(prodid, naam)
            elif zoeken == 'sub_categorieid':
                categorie(prodid, naam)
            elif zoeken == 'categorieid':
                woord(prodid, naam)
    else:
        klaar(prodid, naam, status, lijst4)


def type(prodid, naam, zoeken, search, target, status):
    cursor.execute('select typeid from producten where id = (%s)', (prodid,))
    type = cursor.fetchall()[0][0]
    cursor.execute('select id from producten where ' + zoeken + \
                   ' = (%s) and target_audienceid = (%s) and typeid = (%s)',(search, target, type))
    epyt = cursor.fetchall()
    lijst5 = []
    for i in epyt:
        lijst5.append(i[0])
    lijst5.remove(prodid)
    if lijst5 == []:
        target_audience(prodid, naam, zoeken, search, ['remove'])
    elif status == []:
        if len(lijst5) >= 4 and len(lijst5) <= 10:
            klaar(prodid, naam, lijst5, [])
        elif len(lijst5) > 10:
            price(prodid, naam, zoeken, search, target, type, [])
        elif len(lijst5) < 4:
            target_audience(prodid, naam, zoeken, search, lijst5)
    else:
        klaar(prodid, naam, status, lijst5)


def price(prodid, naam, zoeken, search, target, type, status):
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
    cursor.execute('select id from producten where ' + zoeken +\
                   ' = (%s) and target_audienceid = (%s) and typeid = \
                   (%s) and verkoopprijs > (%s) and verkoopprijs <= (%s)',\
                   (search, target, type, int(prijsrangemin), int(prijsrangemax)))
    ding = cursor.fetchall()
    lijst6 = []
    for i in ding:
        lijst6.append(i[0])
    lijst6.remove(prodid)
    if lijst6 == []:
        type(prodid, naam, zoeken, search, target, ['remove'])
    elif status == []:
        if len(lijst6) >= 4 and len(lijst6) <= 10:
            #print('price')
            klaar(prodid, naam, lijst6, [])
        elif len(lijst6) < 4:
            type(prodid, naam, zoeken, search, target, lijst6)
        elif len(lijst6) > 10:
            brand(prodid, naam, zoeken, search, target, type, prijsrangemax, prijsrangemin, [])
    else:
        klaar(prodid, naam, status, lijst6)

def brand(prodid, naam, zoeken, search, target, type, prijsrangemax, prijsrangemin, status):
    cursor.execute('select merkid from producten where id = (%s)', (prodid,))
    merk = cursor.fetchall()[0][0]
    cursor.execute('select id from producten where ' + zoeken +\
                   '= (%s) and target_audienceid = (%s) and typeid = (%s) and verkoopprijs >= \
                   (%s) and verkoopprijs <= (%s) and merkid = (%s)',\
                   (search, target, type, int(prijsrangemin), int(prijsrangemax), merk))
    burn = cursor.fetchall()
    lijst7 = []
    for i in burn:
        lijst7.append(i[0])
    lijst7.remove(prodid)
    if lijst7 == []:
        print('lijst7')
        price(prodid, naam, zoeken, search, target, type, ['remove'])
    elif status == []:
        if len(lijst7) < 4:
            price(prodid, naam, zoeken, search, target, type, lijst7)
        else:

            klaar(prodid, naam, lijst7, [])
    else:
        klaar(prodid, naam, status, lijst7)


def woord(prodid, naam):
    cursor.execute('select naam from merk')
    merken = cursor.fetchall()
    merks = []
    for i in merken:
        merks.append(i[0])
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
    klaar(prodid, naam, lijst8, [])


def modnar(lijst):
    random.shuffle(lijst)
    return lijst[:4]


def klaar(prodid, naam, voorkeurlijst, lijst):
    print(voorkeurlijst)
    print(lijst)
    if 'remove' in voorkeurlijst:
        voorkeurlijst.remove('remove')
    if 'remove' in lijst:
        lijst.remove('remove')

    if lijst!=[]:
        lijst = modnar(lijst)
        lengte = 4 - len(voorkeurlijst)
        for i in range(lengte):
            voorkeurlijst.append(lijst[i])
    else:
        if len(voorkeurlijst) > 4:
            voorkeurlijst = modnar(voorkeurlijst)
    with open('simielr.csv', 'w', newline='') as csvfile:
        fieldnames = ['productid', 'productnaam', 'pd_1', 'pd_2', 'pd_3', 'pd_4']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerow({'productid': prodid,
                         'productnaam': naam,
                         'pd_1': voorkeurlijst[0],
                         'pd_2': voorkeurlijst[1],
                         'pd_3': voorkeurlijst[2],
                         'pd_4': voorkeurlijst[3]
                         })
        csvfile.close()
