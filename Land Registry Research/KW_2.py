import pyautogui as pag
import pyperclip as pyp
import re

ex = (613,1060)       # współrzędne excela na pasku
pr = (514,1060)       # współrzędne przeglądarki na pasku
sr = (600,400)        # srodek strony na ekranie w EUKW
zer = (354,217)       # komorka dzialki excel
zer1 = (420,216)      # komórka powierzchnia ogólna
eter = (414,356)      # współrzędne komórki w tle w Excel
ISp = (334,219)       # współrzędne hiperłącza do działu 1Sp
II = (627,215)        # współrzędne hiperłącza do działu II
IspEx = (477,218)     # komórka Excel Isp
III = (872,217)       # współrzędne hiperłącza do działu III
udzEx = (542,218)     # współrzędne komórki z udzialami excel
nazwEx = (604,218)    # współrzędne komorki z imieniem i nazwiskiem excel
pesEx = (663,217)     # współrzędne komorki z peselem excel
rodzEx = (725,216)    # współrzędne komorki z rodzicami excel
podstEx = (785,219)   # współrzędne komorki podstawy prawnej excel
IV = (1132,222)       # współrzędne hiperłącza do działu IV
IIIEx = (844,218)     # współrzędne komórki dział III excel
IVEx = (902,218)      # współrzędne komórki dział IV excel

# dział IO (zerowy) - działki i powierzchnia całkowita
pag.moveTo(pr[0],pr[1])
pag.click()
pag.moveTo(sr[0],sr[1])
pag.hotkey('ctrl','a')
pag.hotkey('ctrl','c')
pag.moveTo(ISp[0],ISp[1])
pag.click()
IO = pyp.paste()

# działki
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
pag.moveTo(ex[0],ex[1])
pag.click()
pag.moveTo(zer[0],zer[1])
pag.click()
pag.hotkey('ctrl','v')
pag.click()

# powierzchnia
pointsRegex = re.compile(r'Obszar całej nieruchomości\t.*\t')
points = pointsRegex.findall(IO)
points[0] = points[0].replace('Obszar całej nieruchomości','').replace('\t','')
obszar_str = points[0]
pyp.copy(obszar_str)
pag.moveTo(eter[0],eter[1])
pag.click()
pag.moveTo(zer1[0],zer1[1])
pag.click()
pag.hotkey('ctrl','v')
pag.moveTo(eter[0],eter[1])
pag.click()

# dzial I Sp
pag.moveTo(pr[0],pr[1])
pag.click()
pag.moveTo(sr[0],sr[1])
pag.hotkey('ctrl','a')
pag.hotkey('ctrl','c')
text = pyp.paste()
pag.moveTo(II[0],II[1])
pag.click()
pag.moveTo(ex[0],ex[1])
pag.click()
pag.moveTo(IspEx[0],IspEx[1])
pag.click()

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
pag.hotkey('ctrl','v')
pag.click()
pag.moveTo(eter[0],eter[1])
pag.click()

#dział II

pag.moveTo(pr[0],pr[1])
pag.click()
pag.moveTo(sr[0],sr[1])
pag.hotkey('ctrl','a')
pag.hotkey('ctrl','c')
text = pyp.paste()
pag.moveTo(III[0],III[1])
pag.click()
pag.moveTo(ex[0],ex[1])
pag.click()
pag.moveTo(udzEx[0],udzEx[1])
pag.click()

pointsRegex = re.compile(r'\d?\d?\d?\d\s/\d\d?\d?\d?\d?\t?W?S?P?Ó?')
points = pointsRegex.findall(text)
points
number = 0
udzialy = ''
for element in points:
    number += 1
    element = element.replace('\t','').replace('WSPÓ','M').replace(' ','')
    udzialy += str(number) + '. ' + element + '; '

pointsRegex = re.compile(r'matki.*')
points = pointsRegex.findall(text)
points
osoby = []
for element in points:
    element = element.replace('matki)','').replace('matki,','').replace('\t','').replace(' PESEL)','')
    osoby.append(element)

imiona = ''
rodzice = ''
pesel = ''
number = 0
for osoba in osoby:
    number += 1
    osoba = osoba.split(',')
    if len(osoba) == 1:
        osoba.append('---').append('---').append('---')
    elif len(osoba) == 2:
        osoba.append('---').append('---')
    elif len(osoba) ==3:
        osoba.append('---')
    imiona  += str(number) + '. '+ osoba[0] + '; '
    rodzice += str(number) + '. '+ osoba[1] + ',' + osoba[2] + '; '
    pesel   += str(number) + '. '+ osoba[3] + '; '
pesel = pesel.replace('\r','')

pointsRegex = re.compile(r'Nr podstawy wpisu\t\r\n.*')
points = pointsRegex.findall(text)
podst = points[0]
podst = podst.replace('Nr podstawy wpisu\t\r\n','')
podst = podst.split('\t')
podst = podst[1]

pyp.copy(udzialy)
pag.hotkey('ctrl','v')
pag.click()
pag.moveTo(eter[0],eter[1])
pag.click()

pyp.copy(imiona)
pag.moveTo(nazwEx[0],nazwEx[1])
pag.click()
pag.hotkey('ctrl','v')
pag.click()
pag.moveTo(eter[0],eter[1])
pag.click()

pyp.copy(pesel)
pag.moveTo(pesEx[0],pesEx[1])
pag.click()
pag.hotkey('ctrl','v')
pag.click()
pag.moveTo(eter[0],eter[1])
pag.click()

pyp.copy(rodzice)
pag.moveTo(rodzEx[0],rodzEx[1])
pag.click()
pag.hotkey('ctrl','v')
pag.click()
pag.moveTo(eter[0],eter[1])
pag.click()

pyp.copy(podst)
pag.moveTo(podstEx[0],podstEx[1])
pag.click()
pag.hotkey('ctrl','v')
pag.click()
pag.moveTo(eter[0],eter[1])
pag.click()

# dzial III
pag.moveTo(pr[0],pr[1])
pag.click()
pag.moveTo(sr[0],sr[1])
pag.hotkey('ctrl','a')
pag.hotkey('ctrl','c')
text = pyp.paste()
pag.moveTo(IV[0],IV[1])
pag.click()
pag.moveTo(ex[0],ex[1])
pag.click()
pag.moveTo(IIIEx[0],IIIEx[1])
pag.click()

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
pag.hotkey('ctrl','v')
pag.click()
pag.moveTo(eter[0],eter[1])
pag.click()

# dział IV

pag.moveTo(pr[0],pr[1])
pag.click()
pag.moveTo(sr[0],sr[1])
pag.hotkey('ctrl','a')
pag.hotkey('ctrl','c')
text = pyp.paste()
pag.moveTo(ex[0],ex[1])
pag.click()
pag.moveTo(IVEx[0],IVEx[1])
pag.click()

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
pag.hotkey('ctrl','v')
pag.click()
pag.moveTo(eter[0],eter[1])
pag.click()




















