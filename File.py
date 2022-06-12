from ctypes.wintypes import SMALL_RECT
from PIL import Image
import os
PATH = os.path.dirname(__file__)

#3 is wrong
#2 is big, mid
im = Image.open(PATH + '/Ref1.jpg')
width, height = im.size

offset_X = 375
offset_Y = 45

#im.crop((left, top, right, bottom))
InvenPanel = im.crop((offset_X, offset_Y, offset_X + 280, offset_Y + 555))
InvenPanel.save('panel.png')

InvenPanel.show()