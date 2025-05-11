import librosa, math
REST_PITCH: float = float('nan') # pitch used to represent rest. A rest doesn't have a pitch, so it is set to impossible value nan

def similar(a_freq: float, b_freq: float):
    a_bef_f: float = librosa.midi_to_hz(round(librosa.hz_to_midi(a_freq) - 1))
    a_next_f: float = librosa.midi_to_hz(round(librosa.hz_to_midi(a_freq) + 1))

    lower_bound: float = a_freq - ((a_freq - a_bef_f) * .5)
    upper_bound: float = a_freq + ((a_next_f - a_freq) * .5)

    return lower_bound < b_freq < upper_bound

# compares the sample frequencies of user and expected, returns the number of times they significantly differ (for now, at least)
def accuracy_check(user: list[float], expected: list[float], right_note_hop_window: int) -> int:

    # if the user's is 95% or shorter than the original length, the user didn't record until the end
    if len(user) < .95 * len(expected): 
        print("user's is 95% or shorter than the original length, the user didn't record until the end")
        return (int(.95 * (len(expected) - len(user))))
    
    ret = 0 # for now just how many times the pitches significantly differ

    for i in range(min(len(user), len(expected))):
        if math.isnan(user[i]) != math.isnan(expected[i]): # if one of them is resting but the other isn't
            ret += 1
        
        elif not math.isnan(user[i]) and not math.isnan(expected[i]) and not similar(user[i], expected[i]):
            ret += 1
    return ret