import librosa, music21
import numpy as np
from music21 import converter, tempo
from compare_pitch import accuracy_check

default_tempo: int = 120 # default tempo for a score if no tempo is specified

def load_audio(audio_path: str) -> tuple[np.ndarray, int]:
    """Load audio file and it's sample rate"""
    """Returns time-series data and sample_rate of audio file"""
    y: np.ndarray
    sample_rate: int
    y, sample_rate = librosa.load(audio_path)
    return y, sample_rate

def get_tempos(score: music21.stream.Score) -> list[tuple[float, int]]:
    """Get tempo in beats per second."""
    tempos = []
    for metronome_mark in score.flatten().getElementsByClass(tempo.MetronomeMark):
        tempos.append((metronome_mark.offset, metronome_mark.number))
        
    # if the tempo is not provided for the score, or the tempo is not provided until mid-way through the music
    if not tempos or tempos[0][0] > 0.0:
        tempos.insert(0, (0.0, default_tempo))
    return tempos

def find_expected_pitches(score: music21.stream.Score, tempos_list: list[tuple[float, str]], sample_rate: int, hop_length: int) -> list[int]:

    # TO DO NOW:
    # I think the coded I added works but it doesn't consider hop_length.
    # the resulting array to compare could be big asf so now I need to implement only extending by some hop_length

    def extend_pitches(start: float, end: float, pitch: float, tempo: float):
        duration: float = end - start
        samples: int = int((duration / tempo) * sample_rate)
        expected_pitches.extend([pitch] * samples)

    expected_pitches: list[float] = []
    note_ptr, tempo_ptr = 0, 0
    cur_beat = 0.0

    # only consider the first part in the score, for now at least
    notes_and_rests = list(score.parts[0].recurse().notesAndRests)

    while note_ptr < len(notes_and_rests):
        note = notes_and_rests[note_ptr]

        note_length: float = note.duration.quarterLength
        next_note_change: float = cur_beat + note_length
        next_tempo_change: float = tempos_list[tempo_ptr + 1][0] if tempo_ptr < len(tempos_list) - 1 else float('inf')

        cur_end: float = next_note_change
        cur_tempo: int = tempos_list[tempo_ptr][1]
        cur_pitch: float = note.pitch.frequency if note.isNote else -1 # NOTE: IF IT'S A REST FREQUENCY IS SET TO -1

        # increment next tempo if the tempo change occurs at next note
        if next_tempo_change == next_note_change:
            tempo_ptr += 1
        # always increment to next note
        note_ptr += 1

        extend_pitches(start=cur_beat, end=cur_end, pitch=cur_pitch, tempo=cur_tempo)
        cur_beat = next_note_change # I belive the only case to watch is when note changes, as tempo only changes on note changes as well (at least in MuseScore)
        

def debuggingtestingstuff():
    audio_path = ".\\test_files\\test2.wav"
    sheet_music_path = ".\\test_files\\test2.mxl"

    score = converter.parse(sheet_music_path)
    print(f"score is ", score)

    y, sample_rate = load_audio(audio_path)

    f0: np.ndarray
    voiced_flag: np.ndarray 
    voiced_prob: np.ndarray 

    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    
    for i in range(0, len(f0), 4):
        if voiced_flag[i]:
            print(f"This is the f0 here: {f0[i]}")
            print(f"This is the voiced_flag here: {voiced_flag[i]}")
            print(f"This is the voiced_probs here: {voiced_probs[i]}")

def testing1():
    audio_path = ".\\test_files\\test2.wav"
    # sheet_music_path = ".\\test_files\\test2.mxl"
    sheet_music_path = ".\\test_files\\test1.mxl"

    score = converter.parse(sheet_music_path)
    for note in score.flatten().notesAndRests:
        if note.isRest:
            freq = note.pitch.frequency
            print(f"Note: {note.nameWithOctave}, Frequency: {freq} Hz")
        # print(note)
    


def main():
    # just example
    user: list[float] = [1,2,3] 
    expected: list[float] = [1,2,3] 

    print(f"Number of occurences of pitch differing is {accuracy_check(user, expected)}")   

    testing1()

            
if __name__ == "__main__":
    main()