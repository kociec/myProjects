import re                                    # importing modules
import math
import time

start = time.time()                          # start time measuring

with open(r'F:\DataScience\Data\coords_input.txt') as file:     # opening file with raw data
    content = file.read()

regExpession = re.compile(r'.* .* .*')       # creating the regular expression pattern and finding all points
result = regExpession.findall(content)


data = []                                    # creating empty list for all rows in file
for row in result:
    row = row.split(' ')
    row[1] = float(row[1])                   # changing str to float type and creating data structure: list of the lists
    row[2] = float(row[2])
    data.append(row)

chosenPointName = input('Please indicate the starting point:  ')     # indicating the first point

chosenPointCoords = []                                        # creating empty list for first point coords

for point in data:                                            # getting the first point coords and removing its from the data
    if point[0] == chosenPointName:
        chosenPointCoords = point
        data.remove(point)


resultList = []                                               # creating empty list to collect all points with correct sequence
resultList.append(chosenPointCoords)


closestDistances = []                                         # creating empty list to collect closest distances

while data:                                                   # loop which calculate distance to all points and chooses the closest distance
    allDistances = []
    for point in data:
        distance = round(math.sqrt((chosenPointCoords[1] - point[1])**2 + (chosenPointCoords[2] - point[2])**2),3)   # calculating the distance from current point to all points
        allDistances.append([distance,point[0]])

    for point in data:                                        # adding closest point to resultList and deleting it from future calculations
        if point[0] == min(allDistances)[1]:
            closestDistances.append(min(allDistances)[0])
            chosenPointCoords = point
            data.remove(point)
            resultList.append(chosenPointCoords)

with open(r'F:\DataScience\Data\coords_output.txt','w') as file:                                              # saving sorted sequence of points to new file
    for point in resultList:
        file.write(point[0] + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n')

stop = time.time()                                            # stop time measuring

print('\nTotal distance between all points : ', round(sum(closestDistances),2), ' meters')      # printing main info
print('Performed at the time : ',round(stop-start,2),'seconds!!!')
