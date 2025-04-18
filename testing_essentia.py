import essentia.standard as es
loader = es.MonoLoader(filename='.\\test_files\\775495__tian_yueyao__piano-76.wav')
audio = loader()
# choose a chord detection algorithm
chords, _ = es.ChordsDetection()(audio)
print(chords)  # list of (timestamp, chord_name, strength)
