# import modułów
import re
import pandas as pd
import time
import warnings
warnings.filterwarnings('ignore')

startTime = time.time()                # start pomiaru czasu wykonania skryptu
inWork = True                          # wybór scieżek: True - praca, False - dom

print('   >>>>> OBLICZENIA W TOKU...  <<<<<')
#############################################################################
# wczytanie rejestru przed scaleniem

if inWork == True:
    path =  r'.\przed_scaleniem.txt'

else:
    path =  r'F:\DataScience\Data\rejestr\przed_scaleniem.txt'  

file = open(path, "r")                # otwarcie pliku przed_scaleniem_raw.txt

numery_przed = []                     # zadeklarowanie list zbierających dane
pow_przed = []
pkt_przed = []
jedn_przed = []

for a in file.readlines():            # przejcie linijka po linijce przez plik
    a = a.strip()                     # usunięcie zbędnych tabulatorów i spacji
    a = re.sub(' +', ' ', a)
    a = a.split(' ')                  # konwersja linijki pliku do postaci listy w zmiennej 'a'

    if a[4].endswith('50'):           # zmuszenie Pythona do poprawnego zaokrąglania '50tki' np. 1.7750 do 1.78 a nie 1.77
        a[4] = a[4] + '1'
    
    numery_przed.append(a[1])         # rozpakowanie danych z listy 'a' i wpisanie do odpowiednich list z linijek 23-26
    pow_przed.append(round(float(a[3]), 4))
    pkt_przed.append(round(float(a[4]), 2))
    jedn_przed.append(int(a[0]))

file.close()

# utworzenie roboczego DataFrame z rejestru przed scaleniem na postawie powyższych 4 list i ustawienie nazw kolumn

data_przed_roboczy = pd.DataFrame(data = [jedn_przed, numery_przed, pow_przed, pkt_przed]).transpose()
data_przed_roboczy.columns = ['jedn_przed','nr_przed','pow_przed','pkt_przed']

unique = sorted(list(set(data_przed_roboczy['nr_przed'].values)))          # utworzenie posortowanej listy unikalnych numerów działek

# zsumowanie użytków w działkach i wygenerowanie ostatecznego Data Frame

pows = []                            # zadeklarowanie list zbierających dane ostateczne
pkts = []
nrs = []
jedns = []

nr_temp_1 = []                       # zadeklarowanie list zbierających dane tymczasowe potrzebne do sortowania dwupoziomowego
nr_temp_2 = []

for i in range(len(unique)):
    
    nr_ok = unique[i]                                                    # odwołanie do kolejnych numerów działek z listy unique
    temp = data_przed_roboczy[data_przed_roboczy['nr_przed'] == nr_ok]   # utworzenie tymczasowego frame obejmującego wszystkie wiersze z daną działką
    
    pow_ok = round(temp['pow_przed'].sum(), 4)                           # zsumowanie wartosci powierzchni
    pkt_ok = round(temp['pkt_przed'].sum(), 2)                           # zsumowanie wartosci punktów
    
    temp.reset_index(inplace = True)                                     # zresetowanie indeksu, by móc odwołać sie do pierwszego elementu linijkę niżej
    jedn_ok = temp['jedn_przed'][0] 

    if '/' not in nr_ok:                                                 # pętla generująca dane do sortwania dwupoziomowego
        
        nr_1 = int(nr_ok)                                                # jesli numer bez '/' to weź go, a numer łamany wpisz jako 0
        nr_2 = 0
        
    else:
        
        nr_oks = nr_ok.split('/')                                        # jesli numer z '/', to rozdziel go na 2 częsci
        nr_1 = int(nr_oks[0])
        nr_2 = int(nr_oks[1])      
   
    jedns.append(jedn_ok)                                                # wypełnienie list (z linijek 52-55) zbierających dane ostateczne
    pows.append(pow_ok) 
    pkts.append(pkt_ok)
    nrs.append(nr_ok)
    
    nr_temp_1.append(nr_1)                                               # wypełnienie list (z linijek 57-58) zbierających dane tymczasowe
    nr_temp_2.append(nr_2)

# utworzenie ostatecznego DataFrame z rejestru przed scaleniem na postawie powyższych 4 list i ustawienie nazw kolumn

data_przed = pd.DataFrame(data = [jedns, nrs, nr_temp_1, nr_temp_2, pows, pkts]).transpose()
data_przed.columns = ['jedn_przed','nr_przed', 'temp_1', 'temp_2', 'pow_przed','pkt_przed']

# sortowanie dwupoziomowe danych dzięki tymczasowym kolumnom

data_przed = data_przed.sort_values(by = ['jedn_przed','temp_1', 'temp_2'], ignore_index = True)

# usunięcie kolumn tymczasowych

del data_przed['temp_1']
del data_przed['temp_2']


###############################################################################
# wczytanie rejestru po scaleniu

if inWork == True:
    path =  r'.\po_scaleniu.txt'

else:
    path =  r'F:\DataScience\Data\rejestr\po_scaleniu.txt' 

file = open(path, "r")             # otwarcie pliku po_scaleniu_raw.txt

numery_po = []                     # zadeklarowanie list zbierających dane
pow_po = []
pkt_po = []
jedn_po = []

for a in file.readlines():         # przejcie linijka po linijce przez plik
    a = a.strip()                  # usunięcie zbędnych tabulatorów i spacji
    a = re.sub(' +', ' ', a)
    a = a.split(' ')               # konwersja linijki pliku do postaci listy w zmiennej 'a'

    if a[4].endswith('50'):        # zmuszenie Pythona do poprawnego zaokrąglania '50tki' np. 1.7750 do 1.78 a nie 1.77
        a[4] = a[4] + '1'    

    numery_po.append(a[1])         # rozpakowanie danych z listy 'a' i wpisanie do odpowiednich list z linijek 116-119
    pow_po.append(round(float(a[3]), 4))   
    pkt_po.append(round(float(a[4]), 2))
    jedn_po.append(int(a[0]))

file.close()

# utworzenie roboczego DataFrame z rejestru po scaleniu na postawie powyższych 4 list i ustawienie nazw kolumn

data_po_roboczy = pd.DataFrame(data = [jedn_po, numery_po, pow_po, pkt_po]).transpose()
data_po_roboczy.columns = ['jedn_po','nr_po','pow_po','pkt_po']

unique = sorted(list(set(data_po_roboczy['nr_po'].values)))          # utworzenie posortowanej listy unikalnych numerów działek

pows = []                                                            # zadeklarowanie list zbierających dane ostateczne
pkts = []
nrs = []
jedns = []

nr_temp_1 = []                                                       # zadeklarowanie list zbierających dane tymczasowe potrzebne do sortowania dwupoziomowego
nr_temp_2 = []

for i in range(len(unique)):
    
    nr_ok = unique[i]                                                 # odwołanie do kolejnych numerów działek z listy unique
    temp = data_po_roboczy[data_po_roboczy['nr_po'] == nr_ok]         # utworzenie tymczasowego frame obejmującego wszystkie wiersze z daną działką
    
    pow_ok = round(temp['pow_po'].sum(), 4)                           # zsumowanie wartosci powierzchni
    pkt_ok = round(temp['pkt_po'].sum(), 2)                           # zsumowanie wartosci punktów
    
    temp.reset_index(inplace = True)                                  # zresetowanie indeksu, by móc odwołać sie do pierwszego elementu linijkę niżej
    jedn_ok = temp['jedn_po'][0] 
    
    if '/' not in nr_ok:                                              # pętla generująca dane do sortwania dwupoziomowego
        
        nr_1 = int(nr_ok)                                             # jesli numer bez '/' to weź go, a numer łamany wpisz jako 0
        nr_2 = 0
        
    else:
        
        nr_oks = nr_ok.split('/')                                     # jesli numer z '/', to rozdziel go na 2 częsci
        nr_1 = int(nr_oks[0])
        nr_2 = int(nr_oks[1])        
    
    jedns.append(jedn_ok)                                             # wypełnienie list (z linijek 143-146) zbierających dane ostateczne
    pows.append(pow_ok) 
    pkts.append(pkt_ok)
    nrs.append(nr_ok)
    
    nr_temp_1.append(nr_1)                                            # wypełnienie list (z linijek 148-149) zbierających dane ostateczne
    nr_temp_2.append(nr_2)

# utworzenie ostatecznego DataFrame z rejestru po scaleniu na postawie powyższych 4 list i ustawienie nazw kolumn

data_po = pd.DataFrame(data = [jedns, nrs, nr_temp_1, nr_temp_2, pows, pkts]).transpose()
data_po.columns = ['jedn_po','nr_po', 'temp_1', 'temp_2', 'pow_po','pkt_po']

# sortowanie dwupoziomowe danych dzięki tymczasowym kolumnom

data_po = data_po.sort_values(by = ['jedn_po','temp_1', 'temp_2'], ignore_index = True)

# usunięcie kolumn tymczasowych

del data_po['temp_1']
del data_po['temp_2']

###############################################################################
# zapis danych do pliku wynikowego OUTPUT.txt

lp = 1                                                                     # zainicjowanie zmiennej odpowiadających za numerację - liczba porządkowa
max_jedn = max(data_przed['jedn_przed'].max(), data_po['jedn_po'].max())   # wyznaczenie najwyższego numeru jednostki rejestrowej (przed i po scaleniu - łącznie)

if inWork == True:
    path =  r'.\OUTPUT.txt'

else:
    path =  r'F:\DataScience\Data\rejestr\OUTPUT.txt'

f = open(path, "w")                                                        # utworzenie i otwarcie pliku do zapisu danych (OUTPUT.txt)

for i in range(1, max_jedn + 1):                                           # przejcie przez wszystkie numery jednostek (i) - od 1 do max_jedn

    nr_jednostki = i                                                       # przechwycenie numeru jednostki
    
    temp_przed = data_przed[data_przed['jedn_przed'] == i]                 # wybranie danych dotyczcych i-tej jednostki z rejestru przed scaleniem
    temp_po = data_po[data_po['jedn_po'] == i]                             # wybranie danych dotyczcych i-tej jednostki z rejestru po scaleniu
    
    concated_roboczy = pd.concat(objs = [temp_przed, temp_po], ignore_index= True)               # robocze złącznie w.w. danych dotyczących tej samej jednostki przed i po scaleniu
    
    przed_roboczy = concated_roboczy[['jedn_przed', 'nr_przed', 'pkt_przed', 'pow_przed']]       # wydzielenie danych przed scaleniem
    
    po_roboczy = concated_roboczy[['jedn_po', 'nr_po', 'pkt_po', 'pow_po']]                      # wydzielenie danych po scaleniu
    po_roboczy.dropna(inplace = True)                                                            # usunięcie pustych wierszy z NaN
    
    po_roboczy.reset_index(inplace = True)                                                       # reset indexu do postaci 0-n
    del po_roboczy['index']                                                                      # usunięcie zbędnej kolumny ze starym indeksem
    po_roboczy.dropna(inplace = True)                                                            # usunięcie pustych wierszy z NaN
    
    joined = przed_roboczy.join(po_roboczy)                                # ostateczne złączenie danych przed i po scaleniu
    joined.dropna(inplace = True, how = 'all')                             # usunięcie ewentualnych pustych wierszy
    joined.fillna(value = 0, inplace = True)                          # wypełnienie wartosci NaN zerami (wartosc numeryczna i zawsze się zsumuje z resztą)
    
    if len(joined) == 0:                # jesli pusty DataFrame (nie było takiego nr jedn. rej. przed i po scaleniu - to nie rób nic i idź dalej)
        pass
    
    else:                               # jeli DataFrme nie był pusty to chcemy go zapisać
    
        for j in range(len(joined)):
        
            if j == 0:                  # zapis I wiersza danej jednostki - z numerem lp oraz numerem jednostki
                
                jednostka_przed = joined['jedn_przed'][j]             # wybór poszczególnych elementów z DataFrame joined - przed scaleniem
                numer_przed = joined['nr_przed'][j]
                powierzchnia_przed = joined['pow_przed'][j]
                punkt_przed = joined['pkt_przed'][j]
                
                jednostka_po = joined['jedn_po'][j]                   # wybór poszczególnych elementów z DataFrame joined - po scaleniu
                numer_po = joined['nr_po'][j]
                powierzchnia_po = joined['pow_po'][j]
                punkt_po = joined['pkt_po'][j]
                
                pattern = "{}\t{}\t{}\t{:.2f}\t{:.4f}\t{}\t{}\t{:.2f}\t{:.4f}\n"      # utworzenie wzorca do zapisu i zapis pierwszej linijki z i-tej jednostki do pliku
                line = pattern.format(lp,jednostka_przed, numer_przed, punkt_przed, powierzchnia_przed, jednostka_po, numer_po, punkt_po, powierzchnia_po)
                f.write(line)
                
            else:                     # zapis kolejnych linijek do pliku
                
                jednostka_przed = joined['jedn_przed'][j]             # wybór poszczególnych elementów z DataFrame joined - przed scaleniem
                numer_przed = joined['nr_przed'][j]
                powierzchnia_przed = joined['pow_przed'][j]
                punkt_przed = joined['pkt_przed'][j]
                
                jednostka_po = joined['jedn_po'][j]                   # wybór poszczególnych elementów z DataFrame joined - po scaleniu
                numer_po = joined['nr_po'][j]
                powierzchnia_po = joined['pow_po'][j]
                punkt_po = joined['pkt_po'][j]
                
                pattern = "{}\t{}\t{}\t{:.2f}\t{:.4f}\t{}\t{}\t{:.2f}\t{:.4f}\n"      # utworzenie wzorca do zapisu i zapis kolejnych linijek z i-tej jednostki do pliku
                line = pattern.format('','', numer_przed, punkt_przed, powierzchnia_przed, '', numer_po, punkt_po, powierzchnia_po)
                f.write(line)
                    
        sum_pkt_przed = round(joined['pkt_przed'].sum(), 2)          # obliczenie sumy punktów i powierzchni przed scaleniem
        sum_pow_przed = round(joined['pow_przed'].sum(), 4)
        
        sum_pkt_po = round(joined['pkt_po'].sum(), 2)                # obliczenie sumy punktów i powierzchni po scaleniu
        sum_pow_po = round(joined['pow_po'].sum(), 4)
        
        pattern = "{}\t{}\t{}\t{:.2f}\t{:.4f}\t{}\t{}\t{:.2f}\t{:.4f}\n"             # utworzenie wzorca do zapisu i zapis podsumowania i-tej jednostki do pliku
        line = pattern.format('', '', 'Razem:', sum_pkt_przed, sum_pow_przed, '','Razem:', sum_pkt_po, sum_pow_po)
        f.write(line)
        
        lp += 1                                                      # inkrementacja liczby porzadkowej Lp po skończonym zapisie danej jednostki
                
f.close()

stopTime = time.time()                                               # zakończenie pomiaru czasu i wydruk wyniku
print('SCRIPT EXECUTED IN:', round(stopTime - startTime, 2), 's')












