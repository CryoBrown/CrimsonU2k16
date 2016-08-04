from PIL import Image
import os

#Note that you need to run pip install pillow before using this
#Also I didn't feel like fucking with command line arguments so just change them here
PREFIX = "cb_pb_0_"
EXTENSION = ".jpg"
CONVERT = True

def rename_format(f, prefix, count):
    new = prefix + str(count) + os.path.splitext(f)[1]
    os.rename(f, new)
    print(f + " renamed " + new)
    return new

def img_to_pgm(filename):
    im = Image.open(filename)
    im = im.convert('RGB')
    new = os.path.splitext(filename)[0] + '.pgm'
    im.save(new)
    os.remove(filename)
    print(filename + " converted to " + new)

def main():
    count = 0
    for f in os.listdir(os.getcwd()):
        if (f.endswith(EXTENSION)):
            nf = rename_format(f, PREFIX, count)
            if (CONVERT):
                img_to_pgm(nf)
        count+=1
    return count

main()








