import librosa, music21
import numpy as np
from librosa.sequence import dtw
from music21 import converter, dynamics, tempo

#: get all the frequency at all the time point
#compare that as expected frequency art all the time point. 
#provide feedback on the pitch. 
## when they get it wrong. 
#find the points the user playing is wrong. 

#Extract expected pitches from the sheet music and convert them to frequencies.
def extract_expected_pitch(sheet_music_path: str) -> np.ndarray:
    score = converter.parse(sheet_music_path)
    expected_pitches = []
    for note in score.flat.notes:  # Iterate through all notes
        if note.isNote:  # If single note
            freq = note.pitch.frequency  # Convert note name (like C4) to Hz
            expected_pitches.append(freq)
        elif note.isChord:  # If it's a chord, take the lowest pitch 
            freq = min(p.frequency for p in note.pitches)
            expected_pitches.append(freq)
    return np.array(expected_pitches) 

def main():
    # Paths to user recording and sheet music
    audio_path = "user_recording.wav"
    sheet_music_path = "sheet_music.xml"
    y, sample_rate = librosa.load(audio_path, sr=None) #y: numpy array of waveform; sr: samples per sec in Hz

    expected_pitches = extract_expected_pitch(sheet_music_path)
    print("Expected Pitches (Hz):", expected_pitches)

    f0: np.ndarray
    # Estimate the fundamental frequency (F0) using pYIN
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

    f0_clean = f0[~np.isnan(f0)] # Remove Not-a-number values (unvoiced frames)
    librosa.estimate_tuning()
    
if __name__ == "__main__":
    main()