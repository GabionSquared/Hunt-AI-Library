from ctypes.wintypes import SMALL_RECT
from PIL import Image
import os
PATH = os.path.dirname(__file__)

#returns percentage accuracy
def Similarity(im1, im2, marginOfError = 4, debug = False):
    width1, height1 = im1.size
    width2, height2 = im2.size
    pix1 = im1.load()
    pix2 = im2.load()

    widthSmaller = width1
    HeightSmaller = height1

    if(width1 > width2):
        widthSmaller = width2

    if(height1 > height2):
        HeightSmaller = height2

    pixelsChecked = 0
    pixelsSimilar = 0

    #centralises around 0. MoR = 10 -> lower = -5, upper = +5
    lower = int((marginOfError/2)-marginOfError)
    upper = abs(lower)-1

    if(debug):
        print("margin: " + str(marginOfError) + "\nlower: " + str(lower) + "\nupper: " + str(upper) )

    for x in range(0, widthSmaller):
        for y in range(0, HeightSmaller):

            for err in range(lower, upper):
                pixList1 = list(pix1[x,y])

                for i in range(0, len(pixList1)):
                    pixList1[i] += err

                pixTup1 = tuple(pixList1)

                if(pixTup1 == pix2[x,y]):
                    pixelsSimilar += 1
                    break

            pixelsChecked += 1

    if(debug):
        print (str(pixelsSimilar) + " of " + str(pixelsChecked) + " (" + str((pixelsSimilar/pixelsChecked)*100) + "%)")
    
    return ((pixelsSimilar/pixelsChecked)*100)

def IdentifyName(im, debug = False):
    small = Image.open(PATH + '/Lib/Small Sign.png')
    mid = Image.open(PATH + '/Lib/Medium Sign.png')
    large = Image.open(PATH + '/Lib/Large Sign.png')

    smallSimilarity = 0
    midSimilarity = 0
    largeSimilarity = 0
    margin = 100
    flag = False

    while(not flag):
        
        smallSimilarity = Similarity(im, small, margin) #, debug=debug
        midSimilarity = Similarity(im, mid, margin)
        largeSimilarity = Similarity(im, large, margin)

        arr = [smallSimilarity, midSimilarity, largeSimilarity]
        arr.sort()
        first = arr[-1]
        second = arr[-2]

        if(first - 20 > second):
            flag = True
        else:
            margin -= 4

        if(margin <= 0):
            margin = 4
            print("(defaulting)")
            smallSimilarity = Similarity(im, small, margin) #, debug=debug
            midSimilarity = Similarity(im, mid, margin)
            largeSimilarity = Similarity(im, large, margin)

            flag = True



    if(debug):
        print ("FINAL MARGIN: " + str(margin))
        print ("small: " + str(smallSimilarity))
        print ("mid: " + str(midSimilarity))
        print ("large: " + str(largeSimilarity))

    if((smallSimilarity > midSimilarity) and (smallSimilarity > largeSimilarity)):
        return "small"
    elif(midSimilarity > largeSimilarity):
        return "mid"
    else:
        return "lorg"
    
def ScanInven(im, num):
    if(num == -1):
        offset_X = 66
        offset_Y = 59
    elif(num == 0):
        offset_X = 375
        offset_Y = 45
    else:
        offset_X = 685
        offset_Y = 59
    

    InvenPanel = im.crop((offset_X, offset_Y, offset_X + 280, offset_Y + 555))
    InvenPanel.save('panel.png')

    sign  = InvenPanel.crop((8, 75, 8+72, 75+13))
    sign2 = InvenPanel.crop((8, 151, 8+72, 151+13))

    sign.save(str(num) + 'sign.png')
    sign2.save(str(num) + 'sign2.png')

    print("")
    print(IdentifyName(sign, True))
    print("")
    print(IdentifyName(sign2, True))
    print("")

    #sign.show()
    #sign2.show()

#3 is wrong
#2 is big, mid
im = Image.open(PATH + '/Ref6.jpg')
width, height = im.size

ScanInven(im, -1)
#ScanInven(im, 0)
#ScanInven(im, 1)

#im.crop((left, top, right, bottom))