#!/usr/bin/env python3
# Purpose: <TODO>
#
# This program currently just provides some code that you might find useful as
# you work on your first composition lab. Please remove this comment (and any
# unused starter code) and explain your actual program once you have a plan for
# your composition!
# 
# Author(s): Emily Ertle and Dan Little
# Date: 3/17/24
import random
import sys
from music21 import *
from numpy.random import randint

#Useful Python functions (choice and choices) to randomly select something from
#a collection
from random import choice, choices 

C_MIDI = 60  #middle C in midi notation

GRAMMAR = {
        '1': ['I', 'I7'],
        '2': ['IV', 'IV7', ['1', 'IV7', 'IVo7'], ['6', 'ii/o7', 'Vb9']],
        '3': ['I', 'I7', ['5', 'ii7', 'V7']],
        '4': ['I', 'I7', ['4', 'ii', 'V7']],
        '5': ['IV', 'IV7'],
        '6': ['IV', 'IV7', 'IVo7', ['3', 'ii7', 'V7']],
        '7': ['I', 'IV', ['2', 'ii7', 'V7']],
        '8': ['I', 'IV', ['b2', 'ii7', 'V7']],
        '9': ['I', 'I7', 'ii7'],
        '10': ['I', 'I7', 'V7'],
        '11': ['I', 'I7', ['2', 'ii7', 'V7'], ['1', 'I7', 'bIII7']],
        '12': ['I', 'I7', 'V#9', ['1', 'ii7', 'V7'], ['1', 'II7', 'bII7']]
}

# Given an integer representing a pitch in midi notation, build up a major triad
# with that pitch as the root.
def build_triad(root):
    return chord.Chord([root, root + 4, root + 7])

# Build a 12-tone row from pcs, after which you can manipulate the row using
# other useful functions in the 'serial' module of the music21 library
# p10 = serial.TwelveToneRow([10, 9, 4, 5, 6, 3, 2, 8, 7, 11, 0, 1]) 

def expand(input: str, stream, k):
    possible = GRAMMAR[input]
    choice = possible[randint(len(possible))]
    if isinstance(choice, list):
        k_str, c1_str, c2_str = choice
        degree = int(k_str[-1])
        
        if len(k_str) > 1 and k_str[0] == 'b':
            k_new = key.Key(k.pitchFromDegree(degree).transpose(interval.Interval('-m2')))
        else:
            k_new = key.Key(k.pitchFromDegree(degree))

        stream.append(chord.Chord(roman.RomanNumeral(c1_str, k_new), quarterLength = 2.0))
        # stream[-1].quarterLength = 2.0
        stream.append(chord.Chord(roman.RomanNumeral(c2_str, k_new), quarterLength = 2.0))
        # stream[-1].quarterLength = 2.0
    else:
        stream.append(chord.Chord(roman.RomanNumeral(choice, k), quarterLength = 4.0))
        # stream[-1].quarterLength = 4.0
        

def main():



    score = stream.Score()
    part = stream.Part()   # A single instrument/voice
    
    time_signature = meter.TimeSignature('4/4')
    k = key.Key('C')

    b = scale.WeightedHexatonicBlues('C')
    
    part.append(time_signature)
    part.append(k)

    for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
        expand(x, part, k)

        

    scale_notes = [p.nameWithOctave for p in b.getPitches("C4", "C6")]
    prime_row = random.sample(scale_notes, 8)
    p_0 = serial.ToneRow(prime_row)
 
    inversion = p_0.originalCenteredTransformation('I', 0)
    r_inversion = p_0.originalCenteredTransformation('RI', 0)
    retrograde = p_0.originalCenteredTransformation('R', 0)
    melody = stream.Part()

    chord_length = 0
    for chord in part.notes:
        chord_length += chord.duration.quarterLength


    for pitch in p_0.pitches:
        n = note.Note(pitch, quarterLength = random.choice([0.25, 0.5, 1]))
        melody.append(n)

    # for pitch in inversion.pitches:
    #     n = note.Note(pitch, quarterLength = random.choice([0.25, 0.5, 1]))
    #     melody.append(n)

    # for pitch in r_inversion.pitches:
    #     n = note.Note(pitch, quarterLength = random.choice([0.25, 0.5, 1]))
    #     melody.append(n)
    
    for pitch in retrograde.pitches:
        n = note.Note(pitch, quarterLength = random.choice([0.25, 0.5, 1]))
        melody.append(n)
    
    melody_length = 0
    for inote in melody.notes:
        melody_length += inote.duration.quarterLength

    while melody_length < chord_length:
        n = note.Note(pitch=random.choice(p_0.pitches), quarterLength = random.choice([0.25, 0.5, 1]))
        melody.append(n)
        melody_length += n.duration.quarterLength




    # Let's kick things off with a banjo playing the chords
    # stream1.insert(0, instrument.Banjo())
    # And then, assuming there are at least 4 chords, start playing the violin
    # from the 3rd onwards
    # if len(stream1) > 2:
    #    stream1.insert(3, instrument.Violin())

    score.append(part)
    score.append(melody)

    # Play midi, output sheet music, or print the contents of the stream
    if ("-m" in sys.argv):
        score.show('midi')
    elif ("-s" in sys.argv):
        score.show()
    else:
        part.show('text')

if __name__ == "__main__":
    main()