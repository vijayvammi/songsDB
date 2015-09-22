from database import db_session as session
from model.EchoNest import EchoNest
from model.Word import Word
from model.SongWords import SongWords
import re

def populate_words():
    with open('data/words.dat') as f:
        for line in f:
            words = re.compile(',').split(line.strip())
            for i, w in enumerate(words):
                word = Word()
                word.id = i + 1
                word.word = w
                session.add(word)
    session.commit()

def populate_songwords():
    with open('data/bow_songs.txt') as f:
        for line in f:
            data = re.compile(',').split(line.strip())
            track_id = data[0]
            for d in data[2:]:
                word_id, count = [int(x) for x in re.compile(':').split(d)]
                sw = SongWords()
                sw.track_id = track_id
                sw.word_id = word_id
                sw.count = count
                session.add(sw)
            session.commit()                  

def populate_echonest():
    with open('data/echo_music_ascii.csv') as f:
        for line in f:
            data = re.compile(',').split(line.strip())
            en = EchoNest()
            en.track_id = data[0]
            en.song_id = data[1]
            en.artist = (data[2][:50] + '..') if len(data[2]) > 50 else data[2]
            en.title = (data[3][:50] + '..') if len(data[3]) > 50 else data[3]
            en.energy = float(data[4])
            en.liveness = float(data[5])
            en.tempo = float(data[6])
            en.speechiness = float(data[7])
            en.acousticness = float(data[8])
            en.danceability = float(data[9])
            en.instrumentalness = float(data[10])
            en.loudness = float(data[11])
            en.valence = float(data[12])
            en.key = int(data[13])
            en.mode = int(data[14])
            en.time_signature = float(data[15])
            session.add(en)
    session.commit()                  