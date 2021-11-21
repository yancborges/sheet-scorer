import sys
sys.path.insert(0, 'C://Users//yancb//Desktop//code//repositories//sheet-scorer//code')
from unittest import TestCase, main
from app.reader import read_midi, Song
from mido import MidiFile

path = 'C://Users//yancb//Desktop//code//repositories//sheet-scorer//samples//'
file_name = 'Fur_Elise.mid'


class MidiReader(TestCase):
    
    def test_simple_read(self):
        read_midi(path + file_name)

    def test_read_response_type(self):
        file = read_midi(path + file_name)
        self.assertEqual(type(file), MidiFile)

    def test_load_song_class(self):
        song = Song(path + file_name)

    def test_song_visualization(self):
        song = Song(path + file_name)
        song.visualize()


#main()
song = Song(path + file_name)
song.score()
#song.play()

