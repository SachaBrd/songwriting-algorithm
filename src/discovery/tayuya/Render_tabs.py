import tabs

# La range c'est de F2

test_notes = [('C#3', 5, 4),
 ('G#3', 4, 6),
 ('C#4', 3, 6),
 ('F4', 2, 6),
 ('B2', 6, 7),
 ('D#3', 5, 6),
 ('F#3', 4, 4),
 ('B3', 3, 4),
 ('D#4', 3, 8),
 ('F#2', 6, 2)]
test_key = 'LOCRIAN'

tabs = tabs.Tabs(notes=test_notes, key=test_key)

#to_play = tabs.generate_notes()

print(tabs.find_start())

#tabs.render(to_play, **kwargs)

tabs.render(test_notes)