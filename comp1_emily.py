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
import numpy as np
from typing import Optional

GRAMMAR = {
    '1': ['I', 'Ib7'],
    '2': ['IV', 'IVb7', ['_1_', 'IVb7', 'IVo7'], ['_6-', 'ii/o7', 'Vb9']],
    '3': ['I', 'Ib7', ['_5_', 'ii7', 'V7']],
    '4': ['I', 'Ib7', ['_4_', 'ii', 'V7']],
    '5': ['IV', 'IVb7'],
    '6': ['IV', 'IVb7', 'IVo7', ['_3_', 'ii7', 'V7']],
    '7': ['I', 'IVb7', ['_2_', 'ii7', 'V7']],
    '8': ['I', 'IVb7', ['b2_', 'ii7', 'V7']],
    '9': ['I', 'Ib7', 'ii7'],
    '10': ['I', 'Ib7', 'Vb7'],
    '11': ['I', 'Ib7', ['_2_', 'ii7', 'V7'], ['_1_', 'Ib7', 'bIIIb7']],
    '12': ['I', 'Ib7', 'V#9', ['_1_', 'ii7', 'V7'], ['_1_', 'IIb7', 'bIIb7']]
}


def expand(input: str, stream: stream.Part, k: key.Key, key_list: Optional[list]=None):
    """Expands the grammar nonterminals into specific chords, adds them to the stream, and builds a list of the key centers used in the song.

    Args:
        input (str): The nonterminal to expand.
        stream (stream.Part): The stream.Part object to add to.
        k (key.Key): The primary song key.
        key_list (Optional[list], optional): A list of key centers in the song. Defaults to None.
    """
    possible = GRAMMAR[input]
    choice = possible[randint(len(possible))]
    if isinstance(choice, list):
        k_str, c1_str, c2_str = choice
        degree = int(k_str[1])
        
        # If the key is flat
        if k_str[0] == 'b':
            k_new = key.Key(k.pitchFromDegree(degree).transpose(interval.Interval('-m2')))
        else:
            k_new = key.Key(k.pitchFromDegree(degree))
        # If the key is minor    
        if k_str[2] == '-':
            k_new = k_new.getParallelMinor()
        # Add the key center to the list
        if key_list is not None:
                key_list.append(k_new)
        # Add the two chords, each of length 2 (in quarter notes) to stream    
        stream.append(chord.Chord(roman.RomanNumeral(c1_str, k_new), quarterLength = 2.0))
        stream.append(chord.Chord(roman.RomanNumeral(c2_str, k_new), quarterLength = 2.0))
    else:
        # Add the two chords, each of length 4 (in quarter notes) to stream
        stream.append(chord.Chord(roman.RomanNumeral(choice, k), quarterLength = 4.0))
        # Add the main key to the key list for the bar 
        if key_list is not None:
            key_list.append(k)
            
            
def get_rand_nearest(l: list, i: int):
    """Gets the nearest number in a list `l` to an integer `i`. If there are multiple nearest numbers, it will return one of these at random

    Args:
        l (list): A list of numbers to search.
        i (int): A target integer.

    Returns:
        (int): One of the subset of nearest integers in list `l`.
    """
    # Turn the list into an array
    a = np.asarray(l)
    # Find the absolute difference between `i` and each number in the `l`
    a_abs_diff = np.abs(np.subtract(a, i))
    # Get the minimum absolute distance
    n = np.min(a_abs_diff)
    # Get all the indexes where the absolute difference is equal to the minimum absolute difference
    nearest = np.where(a_abs_diff == np.min(a_abs_diff))[0]

    # Pick a random index from the `nearest` list
    x = random.choice(nearest)
    
    return l[x]


def get_midi_list(pitches: list):
    """Converts a list of pitches (of type pitch.Pitch) into a list of integers representing the pitches' respective midi values.

    Args:
        pitches (list): A list of pitch.Pitch objects

    Returns:
        list: The respective midi values for each pitch.Pitch object in `pitches`
    """
    midi = []
    for p in pitches:
        midi.append(p.midi)
        
    return midi


def get_scale_for_key_tonic_blues(local_key: key.Key, global_key: Optional[key.Key]=None):
    """Returns a scale to use for the melody depending on the key. If the local key is the same as the global key, returns the weighted hexatonic blues scale. Otherwise, returns a major or minor scale depending on whether the local key is major or minor, respectively.

    Args:
        local_key (key.Key): The local key object.
        global_key (key.Key, optional): The global key object. Defaults to None.

    Returns:
        scale: The relevant scale object based on the local and global keys.
    """
    if global_key is not None:
        if local_key.name == global_key.name:
            return scale.WeightedHexatonicBlues(global_key.tonic)
    if local_key.type == 'major':
        return scale.MajorScale(local_key.tonic)
    else:
        return scale.MinorScale(local_key.tonic)
    
    

def main():
    # Define 
    # Set up the score
    score = stream.Score()
    chords = stream.Part()
    melody = stream.Part()

    # Add time signature and key information to the score
    time_signature = meter.TimeSignature('4/4')
    k = key.Key('C')
    score.append(time_signature)
    score.append(k)
    
    # Add chords to the first part object
    key_list = []
    for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
        expand(x, chords, k, key_list)
      
    # Calculate the time in quarter notes occupied by the chords
    chord_length = 0
    for chord in chords.notes:
        chord_length += chord.duration.quarterLength

    # Create the prime row
    prime_row = np.arange(12)
    np.random.shuffle(prime_row)
    p_0 = serial.ToneRow(prime_row)
 
    # Define transformations of the prime row
    inversion = p_0.originalCenteredTransformation('I', 0)
    r_inversion = p_0.originalCenteredTransformation('RI', 0)
    retrograde = p_0.originalCenteredTransformation('R', 0)

    flag = False
    current_chord_idx = 0
    melody_length = 0
    measure_pos = 0
    
    # Add a melody based on the serialistic components, modified to fit the local key centers in the generated blues chords.
    while not flag:
        # Iterate through the row types
        for row in [p_0, inversion, r_inversion, retrograde]:
            # Continue while the melody is not longer than the chords
            if melody_length >= chord_length:
                flag = True
                break
            # Iterate through the pitches in the row
            for p in row.pitches:
                # Figure out what scale to use
                curr_scale = get_scale_for_key_tonic_blues(key_list[current_chord_idx], k)
                print(f'Key: {key_list[current_chord_idx]}')
                # Get a list of midi notes in the currenct scale
                curr_scale_midi = get_midi_list(curr_scale.pitches)
                print(f'Scale MIDI: {curr_scale_midi}')
                # Get the unaltered note's midi value
                temp_note_midi = p.midi
                print(f'Raw MIDI: {temp_note_midi}')
                # Get the nearest midi value within the key
                final_note_midi = get_rand_nearest(curr_scale_midi, temp_note_midi)
                print(f'True MIDI: {final_note_midi}')
                quarter_length = random.choice([0.25, 0.5, 1])
                
                melody.append(note.Note(pitch.Pitch(final_note_midi), quarterLength=quarter_length))
                
                measure_pos += quarter_length
                melody_length += quarter_length
                if melody_length >= chord_length:
                    flag = True
                    break
                if measure_pos > 4:
                    current_chord_idx += 1
                    measure_pos -= 4

    score.insert(1, chords)
    score.insert(1, melody)

    # Play midi, output sheet music, or print the contents of the stream
    if ("-m" in sys.argv):
        score.show('midi')
    elif ("-s" in sys.argv):
        score.show()
    else:
        score.show('text')

if __name__ == "__main__":
    main()