from this import s
from PIL import Image
from PIL import ImageFilter
import os
import shutil
import random

PATH = os.path.dirname(__file__)
BIN = "/Bin"

CONSUMABLE_LIST = []
TOOL_LIST = []
TRAIT_LIST = []
WEAPONS_LARGE_LIST = []
WEAPONS_MEDIUM_LIST = []
WEAPONS_SMALL_LIST = []


arr = os.listdir(PATH + '/Lib/Consumables')
for i in range(0, len(arr)):
    CONSUMABLE_LIST.append(Image.open(PATH + '/Lib/Consumables/' + arr[i]))
arr = os.listdir(PATH + '/Lib/Tools')
for i in range(0, len(arr)):
    TOOL_LIST.append(Image.open(PATH + '/Lib/Tools/' + arr[i]))
arr = os.listdir(PATH + '/Lib/Traits')
for i in range(0, len(arr)):
    TRAIT_LIST.append(Image.open(PATH + '/Lib/Traits/' + arr[i]))
arr = os.listdir(PATH + '/Lib/WeaponsLarge')
for i in range(0, len(arr)):
    WEAPONS_LARGE_LIST.append(Image.open(PATH + '/Lib/WeaponsLarge/' + arr[i]))
arr = os.listdir(PATH + '/Lib/WeaponsMedium')
for i in range(0, len(arr)):
    WEAPONS_MEDIUM_LIST.append(Image.open(PATH + '/Lib/WeaponsMedium/' + arr[i]))
arr = os.listdir(PATH + '/Lib/WeaponsSmall')
for i in range(0, len(arr)):
    WEAPONS_SMALL_LIST.append(Image.open(PATH + '/Lib/WeaponsSmall/' + arr[i]))



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

#returns "small" "mid" or "large", and creates the log
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
            return "large"
    
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

def IdentifyWithinList(list, im):
    similarityarr = []
    flag = False
    margin = 4
    while(not flag):
        similarityarr = []
        for i in range(0, len(list)):
            similarityarr.append(Similarity(list[i], im, margin))
        #print(similarityarr)

        max_index = similarityarr.index(max(similarityarr))
        value = similarityarr[max_index]
        del similarityarr[max_index]

        second_max_index = similarityarr.index(max(similarityarr))
        secondvalue = similarityarr[second_max_index]
        confidence = value-secondvalue

        if(confidence > 30):
            flag = True
        else:
            margin += 1
        if(margin == 10):
            print("(defaulting)")
            flag = True
            similarityarr = []
            for i in range(0, len(list)):
                similarityarr.append(Similarity(list[i], im, margin))
            #print(similarityarr)

            max_index = similarityarr.index(max(similarityarr))
            value = similarityarr[max_index]
            del similarityarr[max_index]

            second_max_index = similarityarr.index(max(similarityarr))
            secondvalue = similarityarr[second_max_index]
            confidence = value-secondvalue

    print(list[max_index].filename.split('/')[3][:-4] + "\t\t(" + str(round(confidence, 3)) + "%)")

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

#returns a 2d jagged array of the tools and consumable images
def findtoolsandcons(panel, QuickAndDirty = False, ImportedEncoder = "_"):
    jaglist = [[],[]]
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

        #this detects if the slot is empty
        similar = Similarity(emptyslot,img,5)
        #print(str(encoder) + " is empty:" + str(similar))
        if(QuickAndDirty):
            similar = 0
            encoder = ImportedEncoder
        if(similar > 45):
            break
            img.save(PATH + BIN + "/"+'zEMPTYTOOL_' + str(encoder) +'.png')
        else:
            img.save(PATH + BIN + "/"+'ztool_' + str(encoder) +'.png')
            jaglist[0].append(img)

    for i in range(0,4):
        encoder = random.randrange(0,1000)
        img = panel.crop((offset_X[i], consumable_Y, offset_X[i] + spacing[i], consumable_Y + offset_Y))
        img = Resize(img, 4).filter(ImageFilter.GaussianBlur(radius=1))
        similar = Similarity(emptyslot,img,5)
        #print(str(encoder) + " is empty:" + str(similar))
        if(QuickAndDirty):
            similar = 0
            encoder = ImportedEncoder
        if(similar > 50):
            break
            img.save(PATH + BIN + "/"+'zEMPTYCONS_' + str(encoder) +'.png')
        else:
            img.save(PATH + BIN + "/"+'zcons_' + str(encoder) +'.png')
            jaglist[1].append(img)

    return jaglist

#return a list of the trait images
def findtraits(panel, QuickAndDirty = False, ImportedEncoder = "_"):
    traitlist = []

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
            encoder = random.randrange(0,1000)
            if(Similarity(emptytrait,trait) > 90):
                break
            if(QuickAndDirty):
                encoder = ImportedEncoder
            trait.save(PATH + BIN + "/"+'ztrait' + str(encoder) +'.png')
            traitlist.append(trait)
            usingleft += leftadder

        usingleft = left
        top += topadder

    return traitlist

def Process(im, num):

    InvenPanel = FindPanel(im, num)
    
    signs = SignsFromPanel(InvenPanel, num)

    size1 = IdentifySize(signs[0], True, debugname="top")
    size2 = IdentifySize(signs[1], True, debugname="bottom")

    weaponIms = FindWeaponIm(size1, size2, InvenPanel)

    encoder = random.randrange(0,1000)
    weaponIms[0].save(PATH + BIN + "/"+'wep' + str(encoder) +'.png')
    encoder = random.randrange(0,1000)
    weaponIms[1].save(PATH + BIN + "/"+'wep' + str(encoder) +'.png')
    
    jaggedlist = findtoolsandcons(InvenPanel)
    traitlist = findtraits(InvenPanel)

    print("----------")

    if(size1 == "small"):
        IdentifyWithinList(WEAPONS_SMALL_LIST, weaponIms[0])
    elif (size1 == "mid"):
        IdentifyWithinList(WEAPONS_MEDIUM_LIST, weaponIms[0])
    else:
        IdentifyWithinList(WEAPONS_LARGE_LIST, weaponIms[0])

    if(size2 == "small"):
        IdentifyWithinList(WEAPONS_SMALL_LIST, weaponIms[1])
    elif (size2 == "mid"):
        IdentifyWithinList(WEAPONS_MEDIUM_LIST, weaponIms[1])
    else:
        IdentifyWithinList(WEAPONS_LARGE_LIST, weaponIms[1])

    for i in range(0, len(jaggedlist[0])):
        IdentifyWithinList(TOOL_LIST, jaggedlist[0][i])
    for i in range(0, len(jaggedlist[1])):
        IdentifyWithinList(CONSUMABLE_LIST, jaggedlist[1][i])
    for i in range(0, len(traitlist)):
        IdentifyWithinList(TRAIT_LIST, traitlist[i])


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
#Process(im, 0)
#Process(im, 1)


def BatchProcess():
    for i in range(1,24):
        im = Image.open(PATH + '/Refs/Ref'+ str(i) +'.jpg')
        Process(im, 0)
#BatchProcess()

def collectNewImages():
    singles = [1,2,3,4,5,7,8,9,17,18,19,20,21,22,23]
    for i in range(len(singles)):
        singles[i]-= 1

    allScreenshots = []
    arr = os.listdir(PATH + '/Refs')
    for i in range(0, len(arr)):
        allScreenshots.append(Image.open(PATH + '/Refs/' + arr[i]))
    print("ASS LENGTH: " + str(len(allScreenshots)) + "\n\n")

    for i in range(len(allScreenshots)):
        filename = allScreenshots[i].filename
        filenumer = filename.split('/')[len(filename.split('/'))-1][3:-4]

        #print(filename)
        #print(int(filenumer) in singles)

        for i2 in range(-1, 2):
            if((i2 == -1 or i2 == 1) and int(filenumer) in singles):
                print("skipping IM " + str(filenumer) + " SPOT " + str(i2))
                continue
            print("\n\n     THIS IS IM " + str(filenumer) + " SPOT " + str(i2))

            encoder = str(random.randrange(0,1000)) + "_" + str(filenumer) +"_" + str(i2)
            #encoder = random.randrange(0,1000)

            InvenPanel = FindPanel(allScreenshots[i], i2)
            signs = SignsFromPanel(InvenPanel, i2)
            size1 = IdentifySize(signs[0], True, debugname="top")
            size2 = IdentifySize(signs[1], True, debugname="bottom")
            weaponIms = FindWeaponIm(size1, size2, InvenPanel)

            
            weaponIms[0].save(PATH + BIN + "/"+'wep' + str(encoder) +'.png')
            weaponIms[1].save(PATH + BIN + "/"+'wep' + str(encoder) +'.png')

            findtoolsandcons(InvenPanel, True, encoder)
            findtraits(InvenPanel, True, encoder)

collectNewImages()