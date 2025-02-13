#!/usr/bin/env python3
# Purpose: <TODO>
#
# This program currently just provides some code that you might find useful as
# you work on your first composition lab. Please remove this comment (and any
# unused starter code) and explain your actual program once you have a plan for
# your composition!
# 
# Author(s): <TODO>
# Date: <TODO>


import sys
from music21 import *
import random

#Useful Python functions (choice and choices) to randomly select something from
#a collection


C_MIDI = 60  #middle C in midi notation

# Given an integer representing a pitch in midi notation, build up a major triad
# with that pitch as the root.
def build_triad(root):
    return chord.Chord([root, root + 4, root + 7])

# Build a 12-tone row from pcs, after which you can manipulate the row using
# other useful functions in the 'serial' module of the music21 library
p10 = serial.TwelveToneRow([10, 9, 4, 5, 6, 3, 2, 8, 7, 11, 0, 1]) 

def main():

    prime_row = random.sample(range(12), 12)
    p_0 = serial.TwelveToneRow(prime_row)
    mat = p_0.matrix()
    inversion = p_0.originalCenteredTransformation('I', 0)



    s = stream.Part()


    for pitch in p_0.pitches:
        n = note.Note(pitch, quarterLength = random.choice([0.25, 0.5, 1]))
        s.append(n)

    for pitch in inversion.pitches:
        n = note.Note(pitch, quarterLength = random.choice([0.25, 0.5, 1]))
        s.append(n)











    
    if ("-m" in sys.argv):
        s.show('midi')
    elif ("-s" in sys.argv):
        s.show()
    else:
        s.show('text')

if __name__ == "__main__":
    main()
