import os
import shutil

directory = os.getcwd()
count = 0
for filename in os.listdir(directory):
    if (filename.endswith('v1.pgm') or filename.endswith('v2.pgm') or filename.endswith('v3.pgm')):
        print(filename)
        shutil.move(filename, "../Positive_images/" + filename)
        count+=1
print ("count: " + str(count))