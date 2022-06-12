from ctypes.wintypes import SMALL_RECT
from PIL import Image
import os
PATH = os.path.dirname(__file__)

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

#3 is wrong
#2 is big, mid
im = Image.open(PATH + '/Ref1.jpg')
width, height = im.size

offset_X = 375
offset_Y = 45

#im.crop((left, top, right, bottom))
InvenPanel = im.crop((offset_X, offset_Y, offset_X + 280, offset_Y + 555))
#InvenPanel.save('panel.png')
#InvenPanel.show()

sign  = InvenPanel.crop((8, 75, 8+72, 75+13))
sign2 = InvenPanel.crop((8, 151, 8+72, 151+13))

small = Image.open(PATH + '/Lib/Small Sign.png')
mid = Image.open(PATH + '/Lib/Medium Sign.png')
large = Image.open(PATH + '/Lib/Large Sign.png')

print("small: " + str(Similarity(sign, small)))
print("mid: " + str(Similarity(sign, mid)))
print("large: " + str(Similarity(sign, large)))