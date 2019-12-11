#!/usr/bin/env python



"""

By Siamak Faridani

1/10/2012



call it by: 

python main.py input.txt
c:\Python35>python "C:\Users\kach\Desktop\Temp\main.py" "C:\Users\kach\Desktop\Temp\input.txt"


"""
import sys
import nltk
from nltk import ngrams
import time





if __name__ == '__main__':

    print("Starting...")

    start = time.clock()

    if len(sys.argv) > 1:

        for f in sys.argv[1:]:

            infile = open(f, 'r')

            outfile = open("output.txt", "w")

            while 1:

                output = ''

                word = ''

                line = infile.readline()

                if line == '':

                    break

                else:

                    grams=ngrams(line.split(),n)

                    for gram in grams:

                        outputstring = ''.join(gram,"\n"])

                        outfile.write(outputstring)



            #print wordsseen.keys()

            infile.close()

            outfile.close()

            end = 1000 * (time.clock() - start)

            print('Time elapsed: %.3f ms' % (end))
