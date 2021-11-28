import pandas as pd                                          # 1.remove the Scal_input.txt file header so that the first number is the parcel number

path =  r'F:\DataScience\Data\GEO\Scal_input.txt'            # 2. check the file path

file = open(path, "r")

nmb = []
area = []
for a in file.readlines():
    a = a.lstrip()
    while True:
        if '  ' in a:
            a = a.replace('  ', ' ')
        else:
            break
    if ' ' in a:
        x, y = a.split(' ')
        y = int(y.replace('\n',''))
        nmb.append(x)
        area.append(y)
    
nr = []
use = []
                                                             # 3. check  DataFrame "data" for unusual land usages to be added on line 26 if neccesery
for i in nmb:
    if ('I' in i) or ('V' in i) or ('pusty' in i) or ('B' in i):
        for j in range(10):
            i = i.replace(str(j), '')
        i = i.replace('/', '')
        use_temp = i
    else:
        numer = i
        use_temp = ''
    nr.append(numer)
    use.append(use_temp)
    
data = pd.DataFrame(data = [nr, use, area]).transpose()
data.columns = ['ParcelNumber','LandUse','Area']

groups = data.groupby(by = 'ParcelNumber')
groups.size()

f = open(r'F:\DataScience\Data\GEO\Scal_output.txt', "w")

for a,b in groups:
    unique = list(set(b['LandUse'].values))
    for i in unique:
        temp = b[b['LandUse'] == i]
        sum_uz = temp['Area'].sum()
        line = a + '\t' + i + '\t' + str(sum_uz) + '\n'
        f.write(line)
    f.write('\n')
f.close()       
    
