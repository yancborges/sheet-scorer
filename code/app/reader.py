from mido import MidiFile
import matplotlib.pyplot as plt
from winsound import Beep
import time


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
    
    def __init__(self, raw_note, tempo, position, bar_size):
        self.__raw = raw_note
        self.position = position
        self.value = raw_note.note
        self.attack = raw_note.velocity # How strong note must be played (i think it should be 0 when silent
        self.duration = raw_note.time   #                                  but it didnt worked this way)                                   
        self.tempo = tempo
        self.bar_size = bar_size
        self.enrich()

    def enrich(self):
        value = self.value
        idx = value - (12 * int(value / 12))
        self.name = self.name_table[idx]
        self.octave = int(value / 12)
        self.frequency = self.frequency_chart[self.name][self.octave]
        self.bmp = round(60 / (self.tempo / 1000000), 0) # tempo is given in microseconds
        self.tempo_velocity = self.duration # milliseconds
        self.is_silent = False if self.attack == 0 else True


    
class Song:

    __midi = None

    def __init__(self, file_path):
        self.__midi = read_midi(file_path)


    def generate_map(self):
        self.__map = {}
        track_counter = 1
        position = 0
        current_tempo = 60
        bar_size = (4,4)
        for track in self.__midi.tracks:
            track_name = 'track' + str(track_counter)
            self.__map[track_name] = {}
            track_dict = self.__map[track_name]
            for msg in track:
                if hasattr(msg, 'type') and msg.type == 'set_tempo':
                    current_tempo = msg.tempo
                elif hasattr(msg, 'type') and msg.type == 'note_on':
                    #if msg.time:
                    n = Note(msg, current_tempo, position, bar_size)
                    if n.position in track_dict:
                        track_dict[n.position].append(n)
                    else:
                        track_dict[n.position] = [n]
                    position += n.tempo_velocity
                elif hasattr(msg, 'type') and msg.type == 'time_signature':
                    bar_size = (int(msg.clocks_per_click / msg.notated_32nd_notes_per_beat), msg.notated_32nd_notes_per_beat)
            track_counter += 1


    def visualize(self):

        tracks = []
        for track in self.__midi.tracks:
            notes = [note for note in track if hasattr(note, 'name') and note.name == 'Note On']
            pitch = [note.pitch for note in notes]
            tick = [note.tick for note in notes]
            tracks += [tick, pitch]
        plt.plot(*tracks)
        plt.show()


    def score(self):
        self.generate_map()
        track_info = {track: 
            {
                'milliseconds_total': 0,
                'notes': 0,
                'attack_total': 0,
                'bar_variation': [],
                'note_size_avg_ms': 0
            } 
            for track in self.__map}
        for track in self.__map:
            for key in self.__map[track]:
                for note in self.__map[track][key]:
                    track_info[track]['milliseconds_total'] += note.tempo_velocity
                    track_info[track]['notes'] += 1
                    track_info[track]['attack_total'] += note.attack
                    track_info[track]['bar_variation'].append(note.bar_size)
            
            track_info[track]['bar_variation'] = set(track_info[track]['bar_variation'])
            track_info[track]['bar_variation'] = track_info[track]['notes'] / len(track_info[track]['bar_variation'])
            track_info[track]['note_size_avg_ms'] = track_info[track]['milliseconds_total'] / track_info[track]['notes']

        x = 0

    def play(self):
        self.generate_map()
        
        for track_id in self.__map.keys():
            track = self.__map[track_id]
            print('Playing', track)
            for position in track.keys():
                msg = 'Playing: '
                for note in track[position]:
                    if not note.is_silent:
                        Beep(note.frequency, note.tempo_velocity)
                        msg += f'{note.name} ({note.tempo_velocity} millis), '
                    else:
                        time.sleep(note.tempo_velocity / 1000)
                        msg += f'SILENCE ({note.tempo_velocity} millis), '
            
                
            print(msg[:-2])
