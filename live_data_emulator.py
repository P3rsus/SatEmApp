"""This Script simulates what live data will look like in the finals"""

import time

f = open("/Users/pedrofonseca/Documents/Projects/CANSAT PROJECT/SOFTWARE/Cansat App Project/data.txt", "r")
d = f.readlines()
f.close()

for l in range(len(d)):
    file = open(
        "/Users/pedrofonseca/Documents/Projects/CANSAT PROJECT/SOFTWARE/Cansat App Project/CansatData.txt", "w")
    for i in d[:l]:
        file.write(i)
    file.close()
    time.sleep(0.1)
