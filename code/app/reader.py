from mido import MidiFile
import matplotlib as plt


def read_midi(file: str) -> object:
    return MidiFile(file)


class Song:

    __midi = None

    def __init__(self, file_path):
        self.__midi = read_midi(file_path)
        self.get_messages()

    def get_messages(self):

        time_lenght = 0
        note_count = 0

        # for i, track in enumerate(self.__midi.tracks):
        #     for msg in track:
        #         print(msg)

        self.time_lenght = time_lenght
        self.note_count = note_count

    def visualize(self):

        tracks = []
        for track in self.__midi.tracks:
            notes = [note for note in track if note.name == 'Note On']
            pitch = [note.pitch for note in notes]
            tick = [note.tick for note in notes]
            tracks += [tick, pitch]
        plt.plot(*tracks)
        plt.show()
