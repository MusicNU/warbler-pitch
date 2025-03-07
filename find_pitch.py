import librosa, music21
import numpy as np
from music21 import converter, tempo
from compare_pitch import accuracy_check

default_tempo: int = 120 # default tempo for a score if no tempo is specified

def load_audio(audio_path: str) -> tuple[np.ndarray, int]:
    """Load audio file and it's sample rate"""
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
    pass

def debuggingtestingstuff():
    audio_path = ".\\test_files\\test2.wav"
    sheet_music_path = ".\\test_files\\test2.mxl"

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

def main():
    # just example
    user: list[float] = [1,2,3] 
    expected: list[float] = [1,2,3] 

    print(f"Number of occurences of pitch differing is {accuracy_check(user, expected)}")    

            
if __name__ == "__main__":
    main()