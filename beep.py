from PIL import Image
from PIL import ImageFilter
import os
import shutil
import random

PATH = os.path.dirname(__file__)
BIN = "/Bin"

"""
def Name(im):
    string = im.filename.split('/')[3][:-4]
    return string

arr = os.listdir(PATH + '/Lib/Traits')
#print(arr)
arr2 = []
for i in range(0, len(arr)):
    arr2.append(Image.open(PATH + '/Lib/Traits/' + arr[i]))

#arr2[4].show()
#print(Name(arr2[4]))


#im.filename.split('/')[3][:-4]
bruh = [31.727430555555557, 23.565297067901234, 29.01234567901235, 32.079475308641975, 28.423996913580247, 26.726466049382715, 27.5390625, 27.58246527777778, 26.666184413580247, 23.982445987654323, 31.33921682098765, 26.5649112654321, 30.17698688271605, 41.63049768518518, 27.032696759259263, 36.42698688271605, 31.095679012345677, 29.164255401234566, 26.302083333333332, 100.0, 24.611786265432098, 
28.766396604938272, 24.25491898148148, 29.955150462962965, 25.226658950617285, 21.6845100308642, 35.33227237654321, 30.50733024691358, 26.244212962962965]

max_index = bruh.index(max(bruh))
print(max_index)
print(bruh[max_index])

del bruh[max_index]

max_index = bruh.index(max(bruh))
print(max_index)
print(bruh[max_index])
"""

allScreenshots = [1]*36
singles = [1,2,3,4,5,7,8,9,17,18,19,20,21,22,23]
for i in range(len(singles)):
        singles[i]-= 1

for i in range(len(allScreenshots)):
        for i2 in range(-1, 2):
            if((i2 == -1 or i2 == 1) and i in singles):
                print("skipping " + str(i+1) + " " + str(i2))
                continue
            print("     THIS IS " + str(i+1) + " " + str(i2))

print()
string = "c:|Users|Timothy|Pictures|Hunt AI Library|Refs|Ref17.jpg"
print(string.split('|')[len(string.split('|'))-1][3:-4])