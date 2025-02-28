import librosa
import numpy as np

def main():
    # this is work in progress stuff

    audio_path = "user_recording.wav"
    sheet_music_path = "sheet_music.xml"

    f0: np.ndarray

    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    
if __name__ == "__main__":
    main()