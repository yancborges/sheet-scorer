from mido import MidiFile
import matplotlib.pyplot as plt
from winsound import Beep


def read_midi(file: str) -> object:
    return MidiFile(file)


class Note:

    name_table = [
        'C', 'C#', 'D', 'D#', 'E', 'F', 
        'F#', 'G', 'G#', 'A', 'A#', 'B'
    ]

    frequency_chart = {
        'C': [16, 33, 65, 131, 261, 523, 1046, 2093, 4186],
        'C#': [17, 34, 69, 138, 277, 554, 1108, 2217, 4434],
        'D': [18, 36, 73, 146, 293, 587, 1174, 2349, 4698],
        'D#': [19, 38, 77, 155, 311, 622, 1244, 2489, 4678],
        'E': [20, 41, 82, 164, 329, 659, 1318, 2637, 5274],
        'F': [21.8, 43.6, 87.3, 174, 349, 698, 1396, 2793, 5587],
        'F#': [23, 46, 92, 184, 369, 739, 1479, 2959, 5919],
        'G': [24.5, 48.9, 97.9, 195, 391, 783, 1567, 3135, 6271],
        'G#': [25.9, 51.9, 103, 207, 415, 830, 1161, 3324, 6644],
        'A': [27.5, 55, 110, 220, 440, 880, 1760, 3520, 7040],
        'A#': [29.1, 58.2, 116, 233, 466, 932, 1864, 3729, 7458],
        'B': [30.8, 61.7, 123, 246, 493, 987, 1975, 3951, 7902]
    }
    
    def __init__(self, raw_note, tempo):
        self.__raw = raw_note
        self.position = raw_note.time
        self.value = raw_note.note
        self.attack = raw_note.velocity
        self.duration = raw_note.time
        self.tempo = tempo
        self.enrich()

    def enrich(self):
        value = self.value
        idx = value - (12 * int(value / 12))
        self.name = self.name_table[idx]
        self.octave = int(value / 12)
        self.frequency = self.frequency_chart[self.name][self.octave]
        self.bmp = 60 / (self.tempo / 1000000)
        self.tempo_velocity = self.duration # milliseconds


    

class Song:

    __midi = None

    def __init__(self, file_path):
        self.__midi = read_midi(file_path)
        self.get_messages()
        self.extract_info_from_file()


    def extract_info_from_file(self):
        self.__seconds_lenght = self.__midi.length


    def get_messages(self):
        self.__notes = []
        current_tempo = None
        for track in self.__midi.tracks:
            for msg in track:
                if hasattr(msg, 'type') and msg.type == 'set_tempo':
                    current_tempo = msg.tempo
                elif hasattr(msg, 'type') and msg.type == 'note_on':
                    self.__notes.append(Note(msg, current_tempo))
            
            """
            self.__notes.extend(
                [Note(msg) for msg in track if 
                    hasattr(track, 'type') and track.type == 'note_on'
                ]
            )
            """


    def visualize(self):

        tracks = []
        for track in self.__midi.tracks:
            notes = [note for note in track if hasattr(note, 'name') and note.name == 'Note On']
            pitch = [note.pitch for note in notes]
            tick = [note.tick for note in notes]
            tracks += [tick, pitch]
        plt.plot(*tracks)
        plt.show()


    def play(self):
        for note in self.__notes:
            Beep(note.frequency, note.tempo_velocity)
