import math
import random
import re
import string

import argparse
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager

def get_resize_size(width, height, T, truncate=False):

    a = width/height
    xbase = math.sqrt(T*a)
    ybase = xbase/a
    
    if truncate:
        return (int(xbase), int(ybase))

    best = 1e20
    bestpair = None
    for x in range(int(xbase), int(xbase)+width//height+2): #maybe + 1 on range
        for y in range(int(ybase), int(ybase)+height//width+2):
            if x*y >= T and x*y-x < T:
                #print("okay", x,y)
                current = x/y
                off = max(current/a,a/current)
                if off < best:
                    best = off
                    bestpair = (x,y)
    return bestpair

def make_image(text, imagepath, font=None, fontsize=48, letterspacing=None, dimensions=None, allowupscaling=False, truncate=False):
    
    if fontsize < 24:
        print("font size too small")
        return
    
    if font is None:
        fontref = font_manager.FontProperties(family='monospace', weight='regular')
        font = font_manager.findfont(fontref)
    
    fonts = [ImageFont.truetype(font, fontsize), 
             ImageFont.truetype(font, fontsize-3),
             ImageFont.truetype(font, fontsize-6),
             ImageFont.truetype(font, fontsize-8),
             ImageFont.truetype(font, fontsize-11),
             ImageFont.truetype(font, fontsize-14)]
    
    if letterspacing is None:
        letterspacing = round(fontsize * 0.625)
    
    def draw_letter(draw,x,y,letter,intensity):
        x_pos = (x+1) * letterspacing  # TODO: change constants 
        y_pos = (y+1) * letterspacing

        if intensity not in range(-3,6): 
            print("uh oh bad intensity")
            return

        if intensity < 0:
            draw.text((x_pos,y_pos), letter, fill=-60*intensity, font=fonts[0], anchor="mm", stroke_width=0)
        else:
            draw.text((x_pos,y_pos), letter, font=fonts[intensity], anchor="mm", stroke_width=intensity)
    
    # remove undesirable characters from text. 
    # maybe improve this later so other small characters don't make it through.
    text = re.sub(r'\W+', '', text)
    
    srcimg = Image.open(imagepath)
    
    # resize based on length of text.
    # will try to resize so that text ends somewhere on the bottom row.
    # if truncate, then will ensure text covers all pixels
    if dimensions is not None:
        srcimg = srcimg.resize(dimensions, resample=Image.BICUBIC)
    elif srcimg.width*srcimg.height > len(text) or allowupscaling:
        newsize = get_resize_size(srcimg.width, srcimg.height, len(text), truncate)
        srcimg = srcimg.resize(newsize, resample=Image.BICUBIC)
    srcimg = srcimg.convert("L")
    width = srcimg.width
    height = srcimg.height

    #
    # experimentally determine intensity thresholds
    #
    breaks = []
    for x in range(-3, 6):
        tot = 0
        for j in range(3):
            n = 10 # The dimension of the test image
            timage = Image.new("L", (n*letterspacing,n*letterspacing), 255)
            draw = ImageDraw.Draw(timage)
            for i in range(n*n):
                l = random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) 
                draw_letter(draw,i%n,i//n,l,x)
            data = timage.getdata()
            tot += (sum(data)/(n*n*letterspacing*letterspacing))
        tot /= 3
        breaks.append(tot)
        
    # create the image
    #print("Generating image with", height, "rows and", width, "columns.")
    image = Image.new("L", ((width+1)*letterspacing,(height+1)*letterspacing), 255)
    draw = ImageDraw.Draw(image)
    data = srcimg.getdata()
    for i in range(min(len(text),width*height)):
        darkness = data[i]/256*(255-breaks[8]) + breaks[8]
        darkness += random.gauss(0,(255-breaks[8])/40) # add some randomness so gradients don't look bad.

        if darkness > breaks[0]:
            val = -3
        elif darkness > breaks[1]:
            val = -2
        elif darkness > breaks[2]:
            val = -1
        elif darkness > breaks[3]:
            val = 0
        elif darkness > breaks[4]:
            val = 1
        elif darkness > breaks[5]:
            val = 2
        elif darkness > breaks[6]:
            val = 3
        elif darkness > breaks[7]:
            val = 4
        else:
            val = 5
        draw_letter(draw,i%width,i//width,text[i],val)
        
    # show the image
    return image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="The path to a file containing the text to make the image out of", type=str)
    parser.add_argument("image", help="THe path to an image to use as a reference", type=str)

    # TODO: make other arguments accessible thru command line
    args = parser.parse_args()
    with open(args.text, 'r', encoding="utf-8") as file:
        text = file.read()
    image = make_image(text, args.image)
    image.show()
