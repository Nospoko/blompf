from matplotlib import pyplot as plt
import numpy as np
from midiutil.MidiFile import MIDIFile

# TODO make transition from ticks to seconds possible

def matrix_to_midi(notes, filename = 'dupa.mid'):
    """ Simplify midi generation
        note format: PITCH|START|DURATION|VOLUME """
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
    nof_rows = 128

    # FIXME this require the last note in the list to be the last in time
    # and that might not be guaranteed for more than one finger playing
    # So try to sort by time
    notes.sort(key=lambda x: x[1]+x[2])
    # Get max time (time of start + duration)::of the last note
    total_time = notes[-1][1] + notes[-1][2]

    # Get number of samples
    dt = 2**-4
    nof_samples = total_time / dt + 1
    roll = np.zeros((nof_rows, nof_samples))

    for note in notes:
        # FIXME no kurwa co to za fuszera
        # Pitch - 30 ::: index 
        note_it = note[0] - 0

        # Time ids
        start_id = note[1] / dt
        end_id = start_id + note[2] / dt

        # Volume dependant color
        roll[note_it, start_id:end_id] = 127.0 / note[3]

    plt.imshow(roll, aspect=nof_samples/nof_rows, origin='lower')
    plt.show()

def test():
    """ Example usage """
    nof_notes = 100
    cosy_fun = lambda jt: np.cos(2*jt) * np.cos(5*jt)
    picz_fun = lambda it: np.floor(30.0 * cosy_fun(4.0 * it/nof_notes))
    pitches = [80 + picz_fun(it) for it in range(nof_notes)]
    times   = [0 + 0.5 * it for it in range(nof_notes)]
    durations = [0.5 for _ in range(nof_notes)]
    volumes = [40 + 0.3 * it for it in range(nof_notes)]

    # Create note array
    notes = np.array([pitches, times, durations, volumes]).transpose()

    # Change to file
    matrix_to_midi(notes, 'yo.mid')

    # Show roll
    show_piano_roll(notes)
