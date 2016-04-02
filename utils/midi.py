from matplotlib import pyplot as plt
import numpy as np
from midiutil.MidiFile import MIDIFile

def matrix_to_midi(notes, filename = 'dupa.mid'):
    """ Simplify midi generation
        notes format: PITCH|START|DURATION|VOLUME """
    # Midi file with one track
    mf = MIDIFile(1)

    track = 0
    time = 0
    mf.addTrackName(track, time, 'merw track')

    # Default
    mf.addTempo(track, time, 120)
    channel = 0

    for note in notes:
        mf.addNote(track, channel, note[0], note[1], note[2], note[3])

    # Save as file
    with open(filename, 'wb') as fout:
        mf.writeFile(fout)

def show_piano_roll(notes):
    """ Another properly named function """
    # Number of avaiable pitches 
    nof_rows = 101

    # Get max time (time of start + duration)
    total_time = notes[-1][1] + notes[-1][2]

    # Get number of samples
    dt = 2**-4
    nof_samples = total_time / dt + 1
    roll = np.zeros((nof_rows, nof_samples))

    for note in notes:
        # Pitch - 3 ::: index 
        note_it = note[0] - 30

        # Time ids
        start_id = note[1] / dt
        end_id = start_id + note[2] / dt

        # Volume dependant color
        roll[note_it, start_id:end_id] = 127.0 / note[3]

    plt.imshow(roll, aspect=4)
    plt.show()

def test():
    """ Example usage """
    pitches = [60 + 2 * it for it in range(20)]
    times   = [0 + 0.5 * it for it in range(20)]
    durations = [0.5 for _ in range(20)]
    volumes = [40 + 3 * it for it in range(20)]

    # Create note array
    notes = np.array([pitches, times, durations, volumes]).transpose()

    # Change to file
    matrix_to_midi(notes, 'yo.mid')

    return notes
