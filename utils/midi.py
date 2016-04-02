import numpy as np
from midiutil.MidiFile import MIDIFile

def matrix_to_midi(notes, filename = 'dupa.mid'):
    """ Simplify midi generation
        notes format: PITCH|TIME|DURATION|VOLUME """
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

    print 'yo'
