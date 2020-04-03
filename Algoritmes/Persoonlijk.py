with open('persoonlijk.csv', 'w', newline='') as csvout:
    fieldnames = ['profileid', 'pd_1', 'pd_2', 'pd_3', 'pd_4']
    writer = csv.DictWriter(csvout, fieldnames=fieldnames)
    writer.writeheader()

    profielid = '59dceaaea56ac6edb4d7be6a'      #Profiel id van gekozen profiel

    cursor.execute("""select producten_id from eerder_bekeken where profielen_id = (%s)""", (profielid,))
    p1 = cursor.fetchall()

    cursor.execute("""select productenid from eerder_aangeraden where profielenid = (%s)""", (profielid,))
    p2 = cursor.fetchall()

    lijst_eb = []
    lijst_ea = []

    for i in p1:
        lijst_eb.append(i[0])
    for i in p2:
        lijst_ea.append(i[0])

    for i in lijst_eb:
        if i in lijst_ea:   #Haalt dezelfde producten uit de lijst
            lijst_ea.remove(i)
            lijst_eb.remove(i)

    cursor.execute("""select id from sessies where profielen_id = (%s)""", (profielid,))
    p3 = cursor.fetchall()

    lijst_s = []
    for i in p3:
        lijst_s.append(i[0])

    gekocht = []
    for i in lijst_s:
        cursor.execute("""select producten_id from product_gekocht where sessies_id = (%s)""", (i,))
        p4 = cursor.fetchall()
        for i in p4:
            gekocht.append(i[0])

    for i in lijst_eb:
       if i in gekocht:     #Haalt gekochte producten uit lijst
           lijst_eb.remove(i)
    alle_eb = []
    if len(lijst_eb) == 1:
        resultaat = similar(lijst_eb[0])    #Zoekt naar similar producten
    elif len(lijst_eb) > 1:
        for i in lijst_eb:
            terug = similar(i)
            for y in terug:
                alle_eb.append(y)
        random.shuffle(alle_eb)
        resultaat = alle_eb[:4]
    else:
        keuze = random.choice(lijst_ea)
        resultaat = similar(keuze)

    writer.writerow({           #Schrijft resulaat in csv bestand
        'profileid': profielid,
        'pd_1': resultaat[0],
        'pd_2': resultaat[1],
        'pd_3': resultaat[2],
        'pd_4': resultaat[3]
    })
    break
