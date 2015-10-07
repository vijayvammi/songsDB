from app.database import db_session as session
from app.model.EchoNest import EchoNest
from app.model.Word import Word
from app.model.SongWords import SongWords
from app.model.Songs import Song
import pandas as pd
import re

root_key = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']

def populate_songs():
    df = pd.read_csv('app/data/labeled_chords.csv', header = 0)
    song_ids = {}
    for index, row in df.iterrows():
        song = Song()
        if row['Echo_song_id'] in song_ids:
            continue
        else:
            song_ids[row['Echo_song_id']] = 0    
        song.song_id = row['Echo_song_id']
        song.artist = row['Local Artist']
        song.title = row['Local title']
        song.energy = row['energy']
        song.liveness = row['liveness']
        song.tempo = row['tempo']
        song.speechiness = row['speechiness']
        song.acousticness = row['acousticness']
        song.danceability = row['danceability']
        song.instrumentalness = row['instrumentalness']
        song.loudness = row['loudness']
        song.key = root_key[row['key']]
        song.mode = row['mode']
        song.valence_label = row['labeled_valence']
        song.arousal_label = row['labeled_arousal']
        session.add(song)
    session.commit()    

def populate_words():
    with open('app/data/words.dat') as f:
        for line in f:
            words = re.compile(',').split(line.strip())
            for i, w in enumerate(words):
                word = Word()
                word.id = i + 1
                word.word = w
                session.add(word)
    session.commit()

def populate_songwords():
    with open('app/data/bow_songs.txt') as f:
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
    with open('app/data/echo_music_ascii.csv') as f:
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