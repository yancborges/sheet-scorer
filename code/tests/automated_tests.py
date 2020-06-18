import sys
sys.path.insert(0, 'C://Users//Yan//Documents//GitHub//sheet-scorer//code//')
from unittest import TestCase, main
from app.reader import read_midi, Song
from mido import MidiFile


class MidiReader(TestCase):

    path = 'C://Users//Yan//Documents//GitHub//sheet-scorer//samples//'
    file_name = 'Chopin_-_Nocturne_Op._9_No._1.mid'
    
    def test_simple_read(self):
        read_midi(self.path + self.file_name)

    def test_read_response_type(self):
        file = read_midi(self.path + self.file_name)
        self.assertEqual(type(file), MidiFile)

    def test_load_song_class(self):
        song = Song(self.path + self.file_name)

    def test_song_visualization(self):
        song = Song(self.path + self.file_name)
        song.visualize()


main()
