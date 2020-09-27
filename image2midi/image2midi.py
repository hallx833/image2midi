import mido, numpy as np
from PIL import Image

image = Image.open('tree.png')
width, height = image.size
if height > 127:
    scale = height / 127
    image = image.resize((int(width/scale), int(height/scale)))
image = image.convert('1')
image = np.array(image)

mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

notes = [0,2,4,5,7,9,11]
(x,y) = image.shape
for i in range(y):
    note = 127
    ons = []
    for j in range(x):
        if not image[j,i]:
            # comment out this if for more accurate picture, leave it in for better music
            # if (note-j) % 12 not in notes:
            #     note -= 1 
            track.append(mido.Message('note_on', note=note-j, velocity=100, time = 0))
            ons.append(note-j)
    if ons:
        track.append(mido.Message('note_off', note=ons[0], velocity=100, time = 120))
        for on in ons[1:]:
            track.append(mido.Message('note_off', note=on, velocity=100, time = 0))
    else:
        track.append(mido.Message('note_off', note=0, velocity=100, time = 120))


mid.save('song.mid')

