import librosa
import numpy as np

def load_audio(audio_path: str) -> tuple[np.ndarray, int]:
    """Load audio file and it's sample rate"""
    y: np.ndarray
    sample_rate: int
    y, sample_rate = librosa.load(audio_path)
    return y, sample_rate

def main():
    audio_path = ".\\test_files\\test2.wav"
    sheet_music_path = ".\\test_files\\test2.mxl"

    y, sample_rate = load_audio(audio_path)

    f0: np.ndarray
    voiced_flag: np.ndarray 
    voiced_prob: np.ndarray 

    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    
    for i in range(0, len(f0), 4):
        print(f"This is the f0 here: {f0[i]}")
        print(f"This is the voiced_flag here: {voiced_flag[i]}")
        print(f"This is the voiced_probs here: {voiced_probs[i]}")
    
if __name__ == "__main__":
    main()