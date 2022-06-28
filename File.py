from PIL import Image
from PIL import ImageFilter
import os
import shutil
import random


from pip import main
PATH = os.path.dirname(__file__)
BIN = "/Bin"

#https://stackoverflow.com/a/34325723
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

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

#returns "small" "mid" or "lorg", and creates the log
def IdentifySize(im, debug = False, debugname = "1"):
    small = Image.open(PATH + '/Lib/Small Sign.png')
    mid = Image.open(PATH + '/Lib/Medium Sign.png')
    large = Image.open(PATH + '/Lib/Large Sign.png')
    small = small.filter(ImageFilter.GaussianBlur(radius=3))
    mid  = mid.filter(ImageFilter.GaussianBlur(radius=3))
    large = large.filter(ImageFilter.GaussianBlur(radius=3))

    smallSimilarity = 0
    midSimilarity = 0
    largeSimilarity = 0

    im = im.filter(ImageFilter.GaussianBlur(radius=3))

    encoder = random.randrange(0,1000)

    def debugstash(origin, decided):
        if(debug):
            origin.save(PATH + BIN + '/' + str(encoder) + '_origin.png')
            decided.save(PATH + BIN + '/' + str(encoder) + '_decided.png')

    def compare():
        if((smallSimilarity > midSimilarity) and (smallSimilarity > largeSimilarity)):
            debugstash(im, small)
            return "small"
        elif(midSimilarity > largeSimilarity):
            debugstash(im, mid)
            return "mid"
        else:
            debugstash(im, large)
            return "lorg"
    
    margin = 100
    flag = False

    requiredDif = 20
    #requiredDif = 8.9

    diffs = []

    while(not flag):
        printProgressBar(25 - (margin/4), 24, prefix = 'Examining:', suffix = 'Complete', length = 50)

        smallSimilarity = Similarity(im, small, margin) #, debug=debug
        midSimilarity = Similarity(im, mid, margin)
        largeSimilarity = Similarity(im, large, margin)

        arr = [smallSimilarity, midSimilarity, largeSimilarity]
        arr.sort()
        first = arr[-1]
        second = arr[-2]

        numbers = str(margin) + "|\t" + str(round(smallSimilarity, 3)) + "|\t" + str(round(midSimilarity, 3)) + "|\t" + str(round(largeSimilarity, 3))+ "|\t"
        diffs.append(numbers + str(round(first - second, 3)) + "%\ttoward " + compare() + "\n")

        if(first - requiredDif > second):
            flag = True
        else:
            margin -= 4

        if(margin <= 0):
            diffs.append("\n-- DEFAULTED --\n")
            margin = 8
            print("(defaulting)")
            smallSimilarity = Similarity(im, small, margin) #, debug=debug
            midSimilarity = Similarity(im, mid, margin)
            largeSimilarity = Similarity(im, large, margin)

            flag = True

            diffs.append(str(margin) +"\t"+str(round(first - second, 3)) + "%\ttoward " + compare() + "\n")

    if(debug):
        f =  open(PATH + BIN + '/' + str(encoder) +'_Result_' + debugname +'.txt', 'w+')
        for i in range(0, len(diffs)):
            f.write(diffs[i])
        f.close()

        print ("\nFINAL MARGIN: " + str(margin))
        print ("small: " + str(smallSimilarity))
        print ("mid: " + str(midSimilarity))
        print ("large: " + str(largeSimilarity))

    return compare()

#returns im resized by a factor of amount
def Resize(im, amount):
    width, height = im.size
    im = im.resize((width*amount,height*amount))
    return im

#returns invenpanel
def FindPanel(im, num):
    if(num == -1):
        offset_X = 66
        offset_Y = 59
    elif(num == 0):
        offset_X = 375
        offset_Y = 45
    else:
        offset_X = 685
        offset_Y = 59
    

    InvenPanel = im.crop((offset_X, offset_Y, offset_X + 280, offset_Y + 575))
    InvenPanel.save(PATH + BIN + "/"+'panel' + str(num) +'.png')
    
    return InvenPanel

#returns the size signs
def SignsFromPanel(InvenPanel, num):
    #left, top, right, bottom
    sign1  = InvenPanel.crop((8, 75, 8+72, 75+13))
    sign2 = InvenPanel.crop((8, 151, 8+72, 151+13))

    sign1 = Resize(sign1, 4)
    #sign1.save(PATH + BIN + "/"+ str(num) + ' sign Top.png')

    sign2 = Resize(sign2, 4)
    #sign2.save(PATH + BIN + "/"+ str(num) + ' sign Btm.png')

    arr = [sign1, sign2]
    return arr

#returns weapon images
def FindWeaponIm(size1, size2, panel):

    top_left_X = 8
    top_left_Y = 89

    if(size1 == "small"):
        offset_X = 101
    elif(size1 == "mid"):
        offset_X = 151
    else:
        offset_X = 201

    offset_Y = 56

    wep1 = panel.crop((top_left_X, top_left_Y, top_left_X + offset_X, top_left_Y + offset_Y))

    top_left_Y = 165
    if(size2 == "small"):
        offset_X = 101
    elif(size2 == "mid"):
        offset_X = 151
    else:
        offset_X = 201

    wep2 = panel.crop((top_left_X, top_left_Y, top_left_X + offset_X, top_left_Y + offset_Y))

    arr = [wep1, wep2]
    return arr

def findtoolsandcons(panel):
    emptyslot = Image.open(PATH + '/Lib/EmptySlot.png')
    emptyslot = Resize(emptyslot, 4).filter(ImageFilter.GaussianBlur(radius=1))

    tool_Y = 241
    consumable_Y = 316

    offset_X = [8,59,109,160]
    offset_Y = 57
    spacing = [49,48,49,48]

    for i in range(0,4):
        encoder = random.randrange(0,1000)
        img = panel.crop((offset_X[i], tool_Y, offset_X[i] + spacing[i], tool_Y + offset_Y))
        img = Resize(img, 4).filter(ImageFilter.GaussianBlur(radius=1))
        similar = Similarity(emptyslot,img,5)
        #print(str(encoder) + " is empty:" + str(similar))
        if(similar > 45):
            break
            img.save(PATH + BIN + "/"+'zEMPTYTOOL_' + str(encoder) +'.png')
        else:
            img.save(PATH + BIN + "/"+'ztool_' + str(encoder) +'.png')

    for i in range(0,4):
        encoder = random.randrange(0,1000)
        img = panel.crop((offset_X[i], consumable_Y, offset_X[i] + spacing[i], consumable_Y + offset_Y))
        img = Resize(img, 4).filter(ImageFilter.GaussianBlur(radius=1))
        similar = Similarity(emptyslot,img,5)
        #print(str(encoder) + " is empty:" + str(similar))
        if(similar > 50):
            break
            img.save(PATH + BIN + "/"+'zEMPTYCONS_' + str(encoder) +'.png')
        else:
            img.save(PATH + BIN + "/"+'zcons_' + str(encoder) +'.png')

def findtraits(panel):
    emptytrait = Image.open(PATH + '/Lib/EmptyTrait.png')
    emptytrait = Resize(emptytrait, 4)

    left = 9
    top = 393

    width = 48
    height = 54
    
    leftadder = 52
    topadder = 57

    usingleft = left

    for x in range(0,3):
        for y in range(0,5):
            trait = panel.crop((usingleft, top, usingleft + width, top + height))
            trait = Resize(trait, 4)
            if(Similarity(emptytrait,trait) > 90):
                break
            encoder = random.randrange(0,1000)
            trait.save(PATH + BIN + "/"+'ztrait' + str(encoder) +'.png')
            usingleft += leftadder

        usingleft = left
        top += topadder


def Process(im, num):

    InvenPanel = FindPanel(im, num)
    #"""
    signs = SignsFromPanel(InvenPanel, num)

    size1 = IdentifySize(signs[0], True, debugname="top")
    size2 = IdentifySize(signs[1], True, debugname="bottom")

    weaponIms = FindWeaponIm(size1, size2, InvenPanel)

    encoder = random.randrange(0,1000)
    weaponIms[0].save(PATH + BIN + "/"+'wep' + str(encoder) +'.png')
    encoder = random.randrange(0,1000)
    weaponIms[1].save(PATH + BIN + "/"+'wep' + str(encoder) +'.png')
    #"""
    findtoolsandcons(InvenPanel)
    findtraits(InvenPanel)



"""
1) large, small
2) large, medium  (full traits)
3) large, large   (ALWAYS BROKEN)
4) medium, small
5) large, small
6) large, small     (6 panels)
7) small, small
8) medium, medium
9) small, large
"""
im = Image.open(PATH + '/Refs/Ref2.jpg')
width, height = im.size

try:
    shutil.rmtree(PATH + BIN)
except:
    print("bin does not exist")
os.mkdir(PATH + BIN, 0o666)


#Process(im, -1)
Process(im, 0)
#Process(im, 1)


def Batch():
    #for i in range(1,24):
    #    im = Image.open(PATH + '/Refs/Ref'+ str(i) +'.jpg')
    #    Process(im, 0)

    for i in range (10,17):
        im = Image.open(PATH + '/Refs/Ref'+ str(i) +'.jpg')
        Process(im, -1)
        Process(im, 1)

#Batch()

def test():
    small = Image.open(PATH + '/Lib/Small Sign.png')
    for i in range(0,3):
        gauss = small.filter(ImageFilter.GaussianBlur(radius=i))
        gauss.save(PATH + '/' + str(i) + 'im.png')