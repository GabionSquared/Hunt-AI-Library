from PIL import Image
import os
import shutil


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

#returns "small" "mid" or "lorg"
def IdentifyName(im, debug = False, debugname = "1"):
    small = Image.open(PATH + '/Lib/Small Sign.png')
    mid = Image.open(PATH + '/Lib/Medium Sign.png')
    large = Image.open(PATH + '/Lib/Large Sign.png')

    smallSimilarity = 0
    midSimilarity = 0
    largeSimilarity = 0

    def debugstash(origin, decided):
        if(debug):
            origin.save(PATH + BIN + '/origin.png')
            decided.save(PATH + BIN + '/decided.png')

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
        with open('Bin/Diffs ' + debugname +'.txt', 'w') as f:
            for i in range(0, len(diffs)):
                f.write(diffs[i])


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

#void
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
    

    InvenPanel = im.crop((offset_X, offset_Y, offset_X + 280, offset_Y + 555))
    InvenPanel.save(PATH + BIN + "/"+'panel.png')

    #left, top, right, bottom
    sign  = InvenPanel.crop((8, 75, 8+72, 75+13))
    sign2 = InvenPanel.crop((8, 151, 8+72, 151+13))

    sign = Resize(sign, 4)
    sign.save(PATH + BIN + "/"+ str(num) + ' sign Top.png')

    sign2 = Resize(sign2, 4)
    sign2.save(PATH + BIN + "/"+ str(num) + ' sign Btm.png')

    print("")
    print(IdentifyName(sign, True, debugname="top"))
    print("")
    print(IdentifyName(sign2, True, debugname="bottom"))
    print("")

"""
1) large, small
2) large, medium
3) large, large   (ALWAYS BROKEN)
4) medium, small
5) large, small
6) large, small
7) small, small
8) medium, medium
9) small, large
"""
im = Image.open(PATH + '/Refs/Ref1.jpg')
width, height = im.size
#shutil.rmtree(PATH + BIN)
try:
    shutil.rmtree(PATH + BIN)
except:
    print("bin does not exist")
os.mkdir(PATH + BIN, 0o666)

#FindPanel(im, -1)
FindPanel(im, 0)
#FindPanel(im, 1)