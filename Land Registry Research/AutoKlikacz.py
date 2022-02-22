import pyautogui as p
import time
import pyperclip as pyp
import re
import math

n = 0
startTime = time.time()
while True:
    n += 1
    # STRONA 1 - WPISYWANIE DANYCH, STRONA 2 KLIKNIĘCIE PRZYCISKU, STRONA 3 - KSIĘGA WIECZYSTA

    spowalniacz = 0.5 # spowalniacz w razie słabego neta lub wolnego kompa // cały proces trwa ~26 sekund

    excelPasek = (612, 1065)   #wsp excela na pasku
    przeglPasek = (514, 1061)  #wsp przeglądarki na pasku
    eterExcel = (414,356) # klik w tło w Excel
    srodekStrony = (600,400)  # srodek strony na ekranie EUKW

    kw1Excel = (59, 218)  #wsp komórki z przedrostkiem w excel, czesc pierwsza napisu np. KR1M
    kw2Excel = (116, 218) #wsp komórki z numerem księgi w excel, czesc druga napisu np. 00004356
    kw3Excel = (178, 218) #wsp komórki z cyfra kontrolna, czesc trzecia napisu np. 8

    kw1EUKW = (831, 470)  #wsp pola w EUKW do wklejenia kw1Excel
    kw2EUKW = (936, 470)  #wsp pola w EUKW do wklejenia kw2Excel
    kw3EUKW = (1030, 470) #wsp pola w EUKW do wklejenia kw3Excel

    ISp_EUKW = (334,219)  #wsp hiperłącza do działu 1Sp
    II_EUKW = (627,215)   #wsp hiperłącza do działu II
    III_EUKW = (870, 220)   #wsp hiperłącza do działu III
    IV_EUKW = (1132,222)    # wsp hiperłącza do działu IV

    dzialkiExcel = (354,217)  # komorka dzialki excel
    powierzchniaExcel = (420,216) # komórka powierzchnia ogólna
    Isp_Excel = (477,218) # komórka Isp
    udzialyExcel = (542,218) # wsp komórki z udzialami excel
    nazwaExcel = (604,218) # wsp komorki z imieniem i nazwiskiem excel
    peselExcel = (663,217) #wsp komorki z peselem excel
    rodziceExcel = (725,216) # wsp komorki z rodzicami excel
    podstawaExcel = (785,219) # wsp komorki podstawy prawnej excel
    III_Excel = (844,218) # wsp komórki dział III excel
    IV_Excel = (902,218)  # wsp komórki dział IV excel


    #################################### STRONA 1 ################################

    # przelejenie początkowego numeru księgi np. KR1M
    p.moveTo(excelPasek[0], excelPasek[1])
    p.click()
    p.moveTo(kw1Excel[0], kw1Excel[1])
    p.click()
    p.hotkey('ctrl','c')
    p.moveTo(przeglPasek[0], przeglPasek[1])
    p.click()
    p.moveTo(kw1EUKW[0], kw1EUKW[1])
    p.click()
    p.hotkey('ctrl','v')

    # przeklejenie numeru księgi np. 000634645
    p.moveTo(excelPasek[0], excelPasek[1])
    p.click()
    p.moveTo(kw2Excel[0], kw2Excel[1])
    p.click()
    p.hotkey('ctrl','c')
    p.moveTo(przeglPasek[0], przeglPasek[1])
    p.click()
    p.moveTo(kw2EUKW[0], kw2EUKW[1])
    p.click()
    p.hotkey('ctrl','v')

    # przeklejenie cyfry kontrolnej np. 7
    p.moveTo(excelPasek[0], excelPasek[1])
    p.click()
    p.moveTo(kw3Excel[0], kw3Excel[1])
    p.click()
    p.hotkey('ctrl','c')
    p.moveTo(przeglPasek[0], przeglPasek[1])
    p.click()
    p.moveTo(kw3EUKW[0], kw3EUKW[1])
    p.click()
    p.hotkey('ctrl','v')

    p.moveTo(833, 550) # kliknięcie w eter na stronie EUKW (poniżej nr księgi) dla zatwierdzenia wprowadzonych wartosci
    p.click()

    p.moveTo(1352, 567) # kliknięcie w przycisk "Wyszukaj księgę"
    p.click()

    time.sleep(1) # daje 1 sekunde na przejscie na druga strone

    #################################### STRONA 2 ################################

    p.moveTo(900, 550) # przesunięcie kursora na srodek strony, z której będzie kopiować tekst
    p.click()
    time.sleep(spowalniacz)
    p.hotkey('ctrl','a')
    p.hotkey('ctrl','c')
    txt = pyp.paste()
    txt = txt.replace('\r','').split('uprawniony\n')[1] # wycięcie tekstu OD słowa "uprawniony"

    txt = txt.split('Przeglądanie treści')[0] # wycięcie pozostałego tektu DO słowa "Przeglądanie treści"

    txt = txt.replace('\n ','\n').replace('\n\n','\n').replace('\n\n','\n')[:-1] # oczyszczenie tekstu pod ostateczne rozbicie

    osoby = txt.split('\n') # utworzenie listy osób z tekstu

    # ustalenie współrzędnych przycisku w zależności od ilości podmiotów w KW
    x = 630
    if len(osoby) == 1:
        y = 770
        p.moveTo(x, y)
        
    elif len(osoby) == 2:
        y = 805
        p.moveTo(x, y)
        
    elif len(osoby) == 3:
        y = 845
        p.moveTo(x, y)
        
    else:
        exit()
       
    time.sleep(1) # Czas na ewentualne przesunięcie myszy przy niestandardowej księdze
    p.click()
    time.sleep(1.5) #  wczytanie księgi - daję 1.5 sekundy dla pewnosci


    p.hotkey('ctrl','a') # sprawdzenie czy znajdujemy się już na sttronie działu zerowego czy nadal strona #2
    p.hotkey('ctrl','c')
    test = pyp.paste()
    pointsRegex = re.compile(r'Numer działki\t.*\t')
    points = pointsRegex.findall(test)
    if len(points) == 0:  #jeśli nie jesteśmy na stronie działu zerowego, to dodatkowe kliki i druga próba wczytania
        p.moveTo(x, y + 20)
        p.click()
        p.moveTo(x, y + 45)
        p.click()
        time.sleep(1.5)
        
    p.moveTo(przeglPasek[0], przeglPasek[1])
    p.click()
    
    #################################### STRONA 3 ################################

    #### dział IO (zerowy) #### - działki i powierzchnia całkowita: skopiowanie zawartości
    p.moveTo(przeglPasek[0],przeglPasek[1])
    p.click()
    p.moveTo(srodekStrony[0], srodekStrony[1])
    p.hotkey('ctrl','a')
    p.hotkey('ctrl','c')
    p.moveTo(ISp_EUKW[0],ISp_EUKW[1]) # między czasie klik w dział ISp, żeby się załadowało
    p.click()
    IO = pyp.paste()

    # Wyłapanie i posortowanie działek, utworzenia stringa i wklejenie do Excela
    pointsRegex = re.compile(r'Numer działki\t.*\t')
    points = pointsRegex.findall(IO)
    dzialki = []
    for obj in points:
        obj = obj.replace('Numer działki','').replace('\t','')
        dzialki.append(obj)
    dzialki.sort()

    dzialki_str = ''
    for obj in dzialki:
        dzialki_str = dzialki_str  + obj + '; '
        
    pyp.copy(dzialki_str)
    p.moveTo(excelPasek[0],excelPasek[1])
    p.click()
    p.moveTo(dzialkiExcel[0],dzialkiExcel[1])
    p.click()
    p.hotkey('ctrl','v')
    p.click()

    # Wyłapanie powierzchni całkowitej i wklejenie do Excela
    pointsRegex = re.compile(r'Obszar całej nieruchomości\t.*\t')
    points = pointsRegex.findall(IO)
    points[0] = points[0].replace('Obszar całej nieruchomości','').replace('\t','')
    obszar_str = points[0]
    pyp.copy(obszar_str)
    p.moveTo(eterExcel[0],eterExcel[1])
    p.click()
    p.moveTo(powierzchniaExcel[0], powierzchniaExcel[1])
    p.click()
    p.hotkey('ctrl','v')
    p.moveTo(eterExcel[0],eterExcel[1])
    p.click()
    time.sleep(spowalniacz)

    #### DZIAŁ I Sp #### skopiowanie zawartości 
    p.moveTo(przeglPasek[0],przeglPasek[1])
    p.click()
    p.moveTo(srodekStrony[0], srodekStrony[1])
    p.hotkey('ctrl','a')
    p.hotkey('ctrl','c')
    text = pyp.paste()
    p.moveTo(II_EUKW[0],II_EUKW[1]) # między czasie klik w dział II, żeby się załadowało
    p.click()
    p.moveTo(excelPasek[0],excelPasek[1])
    p.click()
    p.moveTo(Isp_Excel[0],Isp_Excel[1])
    p.click()

    # analiza skopiowanej zawartości i wklejenie wyniku do komórki w Excel
    pointsRegex = re.compile(r'DZIAŁ I-SP - SPIS PRAW ZWIĄZANYCH Z WŁASNOŚCIĄ\r\nBRAK WPISÓW')
    points = pointsRegex.findall(text)
    if len(points) == 1:
        points = points[0].replace('DZIAŁ I-SP - SPIS PRAW ZWIĄZANYCH Z WŁASNOŚCIĄ\r\n','')
    Isp = ''
    if points == 'BRAK WPISÓW':
        Isp = 'BRAK WPISÓW'
    else:
        text = text.split('Spis praw związanych z własnością')
        text = text[1]
        text = text.split('DOKUMENTY BĘDĄCE PODSTAWĄ WPISU')
        Isp = text[0]
    Isp = Isp.replace('\n',' ').replace('\r',' ').replace('\t',' ')   
    pyp.copy(Isp)
    p.hotkey('ctrl','v')
    p.click()
    p.moveTo(eterExcel[0],eterExcel[1])
    p.click()
    time.sleep(spowalniacz)

    #### DZIAŁ II #### skopiowanie zawartości 

    p.moveTo(przeglPasek[0],przeglPasek[1])
    p.click()
    p.moveTo(srodekStrony[0], srodekStrony[1])
    p.hotkey('ctrl','a')
    p.hotkey('ctrl','c')
    text = pyp.paste()
    p.moveTo(III_EUKW[0], III_EUKW[1]) # między czasie klik w dział III, żeby się załadowało
    p.click()
    p.moveTo(excelPasek[0],excelPasek[1])
    p.click()
    p.moveTo(udzialyExcel[0],udzialyExcel[1])
    p.click()

    # analiza tekstu: UDZIAŁY ---->    XXX/XXXXX (max rozmiar) + współwłasność jeśli jest konwersja na "1/1M"
    pointsRegex = re.compile(r'\d?\d?\d?\d\s/\d\d?\d?\d?\d?\t?W?S?P?Ó?')
    points = pointsRegex.findall(text)
    points
    number = 0
    udzialy = ''
    for element in points:
        number += 1
        element = element.replace('\t','').replace('WSPÓ','M').replace(' ','')
        udzialy += str(number) + '. ' + element + '; '

    # wyszukanie właściciela, rodziców i peselu - cała linijka po 'matki'
    pointsRegex = re.compile(r'matki.*')
    points = pointsRegex.findall(text)
    osoby = []

    # oczyszczenie tekstu i utworzenie listy osób do wklejenia
    for element in points:
        element = element.replace('matki)','').replace('matki,','').replace('\t','').replace(' PESEL)','').replace('PESEL)','').replace('\r','')
        osoby.append(element)

    # jeśli mamy instytucje, a nie zwykła osobe to wykona się ten blok, bo w.w. lista "osoby" będzie pusta
    # skopiowanie całej linijki od słowa REGON
    if len(osoby) == 0:
        pointsRegex = re.compile(r'REGON.*')
        points = pointsRegex.findall(text)

    # oczyszczenie tekstu i utworzenie listy instytucji do wklejenia
        for element in points:
            element = element.replace('REGON)','').replace('\t','').replace('\r','')
            osoby.append(element)
            instytucja = osoby[0].split(',')[0] + ',,'
            osoby = []
            osoby.append(instytucja)

    # jeśli coś jeszcze innego typu kościół lub inna organizacja i lista jest nadal pusta, to
    # wykona sie ten blok kodu próbujący to wyłapać 
    if len(osoby) == 0:
        pointsRegex = re.compile(r'Nazwa.*')
        points = pointsRegex.findall(text)

    # oczyszczenie tekstu i utworzenie listy organizacji do wklejenia
        for element in points:
            element = element.replace('Nazwa)','').replace('\t','').replace('\r','')
            osoby.append(element)
            inna = osoby[0].split(',')[0] + ',,'
            osoby = []
            osoby.append(inna)


    imiona = ''
    rodzice = ''
    pesel = ''
    number = 0

    for osoba in osoby:
        number += 1
        osoba = osoba.split(',')
        if len(osoba) == 1:
            osoba.append('---').append('---').append('---')  # jeśli czegoś brakuje, to wypełnij to "---", (np. rodziców, peselu)
        elif len(osoba) == 2:
            osoba.append('---').append('---')
        elif len(osoba) == 3:
            osoba.append('---')
        imiona  += str(number) + '. '+ osoba[0] + '; '
        rodzice += str(number) + '. '+ osoba[1] + ',' + osoba[2] + '; '
        pesel   += str(number) + '. '+ osoba[3] + '; '
    pesel = pesel.replace('\r','')
    rodzice = rodzice.replace('\r','')
    imiona = imiona.replace('\r','')

    # wyszukiwanie podstawy wpisu
    pointsRegex = re.compile(r'Nr podstawy wpisu\t\r\n.*')
    points = pointsRegex.findall(text)
    podst = points[0]
    podst = podst.replace('Nr podstawy wpisu\t\r\n','')
    podst = podst.split('\t')
    podst = podst[1]

    # wklejenie danych z działu II do Excela
    time.sleep(spowalniacz)
    pyp.copy(udzialy)
    p.hotkey('ctrl','v')
    p.click()
    p.moveTo(eterExcel[0],eterExcel[1])
    p.click()

    time.sleep(spowalniacz)
    pyp.copy(imiona)
    p.moveTo(nazwaExcel[0], nazwaExcel[1])
    p.click()
    p.hotkey('ctrl','v')
    p.click()
    p.moveTo(eterExcel[0],eterExcel[1])
    p.click()

    time.sleep(spowalniacz)
    pyp.copy(pesel)
    p.moveTo(peselExcel[0], peselExcel[1])
    p.click()
    p.hotkey('ctrl','v')
    p.click()
    p.moveTo(eterExcel[0],eterExcel[1])
    p.click()

    time.sleep(spowalniacz)
    pyp.copy(rodzice)
    p.moveTo(rodziceExcel[0], rodziceExcel[1])
    p.click()
    p.hotkey('ctrl','v')
    p.click()
    p.moveTo(eterExcel[0],eterExcel[1])
    p.click()

    time.sleep(spowalniacz)
    pyp.copy(podst)
    p.moveTo(podstawaExcel[0], podstawaExcel[1])
    p.click()
    p.hotkey('ctrl','v')
    p.click()
    p.moveTo(eterExcel[0],eterExcel[1])
    p.click()
    time.sleep(spowalniacz)

    #### DZIAŁ III #### skopiowanie zawartości 
    p.moveTo(przeglPasek[0],przeglPasek[1])
    p.click()
    p.moveTo(srodekStrony[0], srodekStrony[1])
    p.hotkey('ctrl','a')
    p.hotkey('ctrl','c')
    text = pyp.paste()
    p.moveTo(IV_EUKW[0],IV_EUKW[1]) # między czasie klik w dział IV, żeby się załadowało
    p.click()
    p.moveTo(excelPasek[0],excelPasek[1])
    p.click()
    p.moveTo(III_Excel[0], III_Excel[1])
    p.click()

    # Analiza skopiowanego tekstu i wklejenie opracowanej zawartości do Excela
    pointsRegex = re.compile(r'DZIAŁ III - PRAWA, ROSZCZENIA I OGRANICZENIA\r\nBRAK WPISÓW')
    points = pointsRegex.findall(text)
    if len(points) == 1:
        points = points[0].replace('DZIAŁ III - PRAWA, ROSZCZENIA I OGRANICZENIA\r\n','')
    III = ''
    if points == 'BRAK WPISÓW':
        III = 'BRAK WPISÓW'
    else:
        text = text.split('DZIAŁ III - PRAWA, ROSZCZENIA I OGRANICZENIA')
        text = text[1]
        text = text.split('DOKUMENTY BĘDĄCE PODSTAWĄ WPISU')
        III = text[0]
    III = III.replace('\n',' ').replace('\r',' ').replace('\t',' ')   
    pyp.copy(III)
    p.hotkey('ctrl','v')
    p.click()
    p.moveTo(eterExcel[0], eterExcel[1])
    p.click()
    time.sleep(spowalniacz)

    #### DZIAŁ IV #### skopiowanie zawartości 
    p.moveTo(przeglPasek[0],przeglPasek[1])
    p.click()
    p.moveTo(srodekStrony[0],srodekStrony[1])
    p.hotkey('ctrl','a')
    p.hotkey('ctrl','c')
    text = pyp.paste()
    p.moveTo(excelPasek[0],excelPasek[1])
    p.click()
    p.moveTo(IV_Excel[0],IV_Excel[1])
    p.click()

    # Analiza skopiowanego tekstu i wklejenie opracowanej zawartości do Excela
    pointsRegex = re.compile(r'DZIAŁ IV - HIPOTEKA\r\nBRAK WPISÓW')
    points = pointsRegex.findall(text)
    if len(points) == 1:
        points = points[0].replace('DZIAŁ IV - HIPOTEKA\r\n','')
    IV = ''
    if points == 'BRAK WPISÓW':
        IV = 'BRAK WPISÓW'
    else:
        text = text.split('DZIAŁ IV - HIPOTEKA')
        text = text[1]
        text = text.split('DOKUMENTY BĘDĄCE PODSTAWĄ WPISU')
        IV = text[0]
    IV = IV.replace('\n',' ').replace('\r',' ').replace('\t',' ')   
    pyp.copy(IV)
    p.hotkey('ctrl','v')
    p.click()
    p.moveTo(eterExcel[0], eterExcel[1])
    p.click()

    #### AUTOMATIC ####
    p.moveTo(1910, 990) # strzałka w Excelu do przesuniecia komórki w dół
    p.click()
    p.moveTo(przeglPasek[0],przeglPasek[1])
    p.click()
    p.moveTo(780, 50) # klik w pole wpisywania adresu dla odświeżenia strony
    p.click()
    p.press('enter')
    time.sleep(1) # poczekanie 1 sekundę na przeładowanie strony

    # obliczenie czasu działania programu
    lapTime = time.time()
    dT = lapTime - startTime
    mins  = math.floor(dT/60)
    secs = dT - mins * 60
    
    print('Zbadano:', n, 'KW. Czas od rozpoczęcia:', mins ,':', math.floor(secs))


    
