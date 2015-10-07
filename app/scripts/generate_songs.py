from __future__ import division
from pydub import *
import re

min_to_ms = 60000
def getFilename(noteName):
    return 'sounds/' + noteName + '.mp3'

offset_volume = {'hihat': -3}

def createSequence(notes, BPM):
    maxBeat = 0
    for n in notes:
        if n['beat'] > maxBeat:    
            maxBeat = n['beat']
    totalLength = ( maxBeat * 1/BPM)*min_to_ms
    print totalLength
    sequence = AudioSegment.silent(totalLength)
    sounds = {}
    for i in range(0, len(notes)):
        n = notes[i]
        notename = n['note']
        filename = getFilename(notename)
        if filename in sounds:
            sound = sounds[filename]
        else:    
            sound = AudioSegment.from_mp3(filename)
            if notename == offset_volume:
                sound = sound - offset_volume
            sounds[filename] = sound   
        sequence = sequence.overlay(sound, position=(1/BPM * (n['beat']))*min_to_ms)
    return sequence

class Note:
    def __init__(self, name, beat):
        self.note = name
        self.beat = beat            

def generate_drums(num_bars):
    notes = []
    for i in range(num_bars):
        # include 4 hihats in this.
        for j in range(4):
            hi = Note('hihat', 4*i + j + 1)
            notes.append(hi.__dict__)
        kick = Note('kick', 4*i + 1)
        notes.append(kick.__dict__)
        snare = Note('snare', 4*i + 2 +1)
        notes.append(snare.__dict__)        
    return notes

def generate_bass(key, bar):
    base4 = Note(key+'_bass2', 4*bar + 1)
    #base8 = Note(key+'_bass2', 4*bar + 4 + 1)
    return [base4.__dict__]#, base8.__dict__]            


root_key = ['Ca','Db','Da','Eb','Ea','Fa','Gb','Ga','Ab','Aa','Bb','Ba']
def transpose(key):
    # return the key notes in scale of key
    index = root_key.index(key)
    scale = []
    scale.extend(root_key[index:])
    scale.extend(root_key[:index])
    return scale

#composition of chords
chord_composition = {
            '' : [1,5,8],   
            'maj' : [1, 5, 8],
            'min' : [1, 4, 8],
            'maj7' : [1, 5, 8, 12],
            'min7' :[1, 4, 8, 11],
            'dom7': [1, 5, 8, 11],
            'maj6' : [1, 5, 8, 10],
            'min6' : [1, 4, 8, 10],
            'sus4' : [1, 6, 8],
            'sus2' : [1, 3, 8],
            'aug' : [1, 5, 9],
            'dim' : [1, 4, 7],
            'dim7' : [1, 4, 7, 10],
            'hdim7' : [1, 4, 7, 10],
            '7/5' : [1, 5, 7, 11],
            '5' : [1, 8],
            '7': [1, 5, 8, 11],
            '9': [1,5, 8, 11],
            '11': [1,5, 8, 11]
        }
def get_chord_notes(chord_key, name):
    scale = transpose(chord_key)
    name = name.lower()
    if name in chord_composition:
        return [scale[x-1] for x in chord_composition[name]]
    else:
        if name.startswith('min'):
            return [scale[x-1] for x in chord_composition['min']]
        elif name.startswith('maj'):
            return [scale[x-1] for x in chord_composition['maj']]
        elif name.startswith('9'):
            return [scale[x-1] for x in chord_composition['9']]
        elif name.startswith('11'):
            return [scale[x-1] for x in chord_composition['11']]
        elif name.startswith('1'):
            return [scale[x-1] for x in chord_composition['maj']]            
        return None   

def generate_chords(key, name, bar):
    scale_notes = get_chord_notes(key, name)
    notes = []
    for i in range(4):
        for scale_note in scale_notes:
            note = Note(scale_note, 4*bar + i + 1)
            notes.append(note.__dict__)
    return notes        

def generate_progression(progression, tempo):
    num_bars = len(progression) + 1
    # the basic drums for the num_bars
    notes = generate_drums(num_bars)
    #append chords and bass to this !
    for bar, chord in enumerate(progression):
        key, name = chord.split(':')
        # add bass which is simple
        notes.extend(generate_bass(key, bar))
        # add the chords now
        notes.extend(generate_chords(key, name, bar))
    sequence = createSequence(notes, tempo)
    return sequence



sequence = generate_progression(['Ca:Maj','Aa:min', 'Ga:Maj'], 120)
sequence.export('sequence.mp4', format="mp4")

names = {'C': 'Ca', 'C#': 'Db', 'Db':'Db', 'D':'Da', 'D#': 'Eb', 'Eb':'Eb', 
        'E': 'Ea', 'Fb': 'Ea', 'F': 'Fa', 'F#': 'Gb', 'Gb':'Gb', 'G':'Ga', 
        'G#': 'Ab', 'Ab': 'Ab','A': 'Aa', 'A#': 'Bb', 'Bb':'Bb','B': 'Ba', 'Cb': 'Ba'}
def check_chords():
    lines = open('chords.txt').readlines()
    not_found = []
    for i, line in enumerate(lines):
        chords = re.compile('\|').split(line.strip())
        for chord in chords:
            key, name = chord.split(':')
            ikey = names[key]
            alt_name = name.split('(')[0].split('/')[0]
            notes = get_chord_notes(ikey, alt_name)            
            if not notes:
                print str(i) + '    ' + key + '    ' + name
                not_found.append(name)
    return list(set(not_found))

def generate_mysongs():
    file_name = 'songid_songs.csv'
    lines = open(file_name).read().split('\r')
    for line in lines:
        song_id, tempo, cps = line.strip().split(',')
        tempo = int(round(float(tempo)/4)*4)
        progression = []
        cp = cps.split('|')
        for chord in cp:
            key, name = chord.split(':')
            ikey = names[key]
            alt_name = name.split('(')[0].split('/')[0]
            progression.append(ikey + ':' + alt_name)
        #print progression
        try:    
            sequence = generate_progression(progression, tempo)
            sequence.export('songs/'+song_id.strip() + '.mp4', format="mp4")
        except:
            print song_id + '   failed'
            continue    
                