import librosa, music21
import numpy as np
from music21 import converter, tempo
from compare_pitch import accuracy_check
import compare_pitch

default_tempo: int = 120 # default tempo for a score if no tempo is specified
rest_pitch: float = float('nan') # pitch used to represent rest. A rest doesn't have a pitch, so it is set to impossible value nan

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

def find_expected_pitches(score: music21.stream.Score, tempos_list: list[tuple[float, str]], sample_rate: int, hop_length: int) -> list[float]:
    # TO DO NOW:
    # I think the coded I added works but it doesn't consider hop_length.
    # the resulting array to compare probably won't be larger than 10^8, so probably fine performance wise. 
    # However if it's slow we implement only extending by some hop_length

    def extend_pitches(start: float, end: float, pitch: float, tempo: float):
        duration: float = end - start
        samples: int = int((duration / tempo * 60) * sample_rate)
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

        cur_tempo: int = tempos_list[tempo_ptr][1]
        cur_pitch: float = note.pitch.frequency if note.isNote else rest_pitch # NOTE: IF IT'S A REST FREQUENCY IS SET TO nan

        extend_pitches(start=cur_beat, end=next_note_change, pitch=cur_pitch, tempo=cur_tempo)
        cur_beat = next_note_change # I belive the only case to watch is when note changes, as tempo only changes on note changes as well (at least in MuseScore)

        # increment next tempo if the tempo change occurs at next note
        if next_tempo_change == next_note_change:
            tempo_ptr += 1
        # always increment to next note
        note_ptr += 1
    
    return expected_pitches
        

def use_pyin():
    audio_path = ".\\test_files\\test2.wav"
    sheet_music_path = ".\\test_files\\test2.mxl"

    test_piano_path = ".\\test_files\\775495__tian_yueyao__piano-76.wav"

    score = converter.parse(sheet_music_path)
    print(f"score is ", score)

    y, sample_rate = load_audio(test_piano_path)

    f0: np.ndarray
    voiced_flag: np.ndarray 
    voiced_prob: np.ndarray 

    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    
    for i in range(0, len(f0), 4):
        # if voiced_flag[i]:
        print(f"This is the f0 here: {f0[i]}")
        print(f"This is the voiced_flag here: {voiced_flag[i]}")
        print(f"This is the voiced_probs here: {voiced_probs[i]}")

def testing1():
    audio_path = ".\\test_files\\test2.wav"
    sheet_music_path = ".\\test_files\\test2.mxl"

    score = converter.parse(sheet_music_path)
    for note in score.flatten().notesAndRests:
        if note.isNote:
            freq = note.pitch.frequency
            print(f"Note: {note.nameWithOctave}, Frequency: {freq} Hz")
        else:
            print(f"Rest, Frequency: {rest_pitch} Hz")
        # print(note)
    
# integrate generating the exepcted pitches and comparing the audio to the expected pitches
def integration(): 
    audio_path = ".\\test_files\\test2.wav"         # USER'S recording as wav file
    y_sample_rate: tuple[np.ndarray, int] = load_audio(audio_path)         # get user recording's sample values and sample rate

    sheet_music_path = ".\\test_files\\test2.mxl"   # sheet music mxl
    score = converter.parse(sheet_music_path)     
    expected_pitches: list[float] = find_expected_pitches(score=score, tempos_list=get_tempos(score), sample_rate=y_sample_rate[1], hop_length=4)
    # for i in range(0, len(expected_pitches), 20):
    #     print(expected_pitches[i])
    # print(f"sample rate is {y_sample_rate[1]}")
    # print(f"size of expected_pitches is {len(expected_pitches)}")
    f0: np.ndarray = librosa.pyin(y_sample_rate[0], fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    
    print(accuracy_check(f0, expected_pitches))

def debug1():
    sheet_music_path = ".\\test_files\\test2.mxl" 
    print(get_tempos(converter.parse(sheet_music_path)))


def main():

    # use_pyin()
    # just example
    # user: list[float] = [1,2,3] 
    # expected: list[float] = [1,2,3] 

    # print(f"Number of occurences of pitch differing is {accuracy_check(user, expected)}")   
    integration()
    # testing1()
    # debug1()

            
if __name__ == "__main__":
    main()