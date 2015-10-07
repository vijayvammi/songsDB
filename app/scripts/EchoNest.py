import os, re
import urllib3
import json
import time
import util
import math

import sys
reload(sys)
sys.setdefaultencoding('utf8')

song_profile_url = 'http://developer.echonest.com/api/v4/song/profile?api_key={key}&id={id}&bucket=audio_summary'

song_search_url = 'http://developer.echonest.com/api/v4/song/search?api_key={key}&format=json&results=1&combined={combined}'

echonest_api = 'echonest_api'

def get_echonest_id(file_name = 'data/musicovery_unique.csv'):
    api_key = util.get_config([echonest_api])[echonest_api]
    lines = open(file_name).read().split('\r') # weird mac issue
    http = urllib3.PoolManager()
    outfile = open('data/EchoMusic_musicovery.csv','w')
    for line in lines:
        sparams = {}
        song_id, title, artist, mbid, valence, arousal = re.compile(',').split(line.strip())
        print line
        generic = title + ' ' + artist
        generic = generic.replace('\'','%27')
        generic = generic.replace('&', ' ')
        splitAtSpace = re.compile('\s+').split(generic)
        generic = '%20'.join(splitAtSpace)
        sparams['key'] = api_key
        sparams['combined'] = generic
        url = song_search_url.format(**sparams) 
        try_again = True
        count = 0
        while try_again:
            count += 1
            r = http.request('GET', url)
            jsondata = json.loads(r.data)
            if jsondata['response']['status']['code'] == 3:
                time.sleep(3)
            else:
                try_again = False
            if count > 10:
                print  song_id + ' information not found' + r.data
                jsondata['response']['status']['code'] = 5   
                try_again = False
        if jsondata['response']['status']['code'] == 5:
            print song_id + ' information not found' + r.data      
        if len(jsondata['response']['songs']) != 0:
            dataline = unicode(line,errors='replace') + ',' 
            dataline = dataline + jsondata['response']['songs'][0]['artist_name'].replace(',',' ') + \
                    ',' + jsondata['response']['songs'][0]['artist_id'] + \
                    ',' + jsondata['response']['songs'][0]['title'].replace(',',' ')     + \
                    ',' + jsondata['response']['songs'][0]['id']        + \
                    ','+ song_id
        outfile.write(dataline + '\n')
        outfile.flush()
    outfile.close()    

def get_echonest_analysis(file_name = 'data/echo_music_songids.txt'):
    api_key = util.get_config([echonest_api])[echonest_api]
    with open(file_name) as f:
        for line in f:
            http = urllib3.PoolManager()
            song_id = line.strip() 
            params = {}
            params['key'] = api_key
            params['id'] = song_id
            url = song_profile_url.format(**params)
            print url
            try_again = True
            count = 0
            while try_again:
                count += 1
                print count
                r = http.request('GET', url)
                jsondata = json.loads(r.data)
                if jsondata['response']['status']['code'] == 3:
                    time.sleep(3)
                else:
                    try_again = False
                if count > 15:
                    print  song_id + ' information not found' + r.data
                    jsondata['response']['status']['code'] = 5   
                    try_again = False
            if jsondata['response']['status']['code'] == 5:
                print song_id + ' information not found' + r.data
            if len(jsondata['response']['songs']) != 0:
                amazon_url = jsondata['response']['songs'][0]['audio_summary']['analysis_url']
                r_amazon = http.request('GET', amazon_url)
                try:
                    json_amazon = json.loads(r_amazon.data)
                    json.dump(json_amazon,open('data/echo_analysis/'+song_id+'.json','w'))
                except:
                    print 'song_id: ' + song_id + ' has no analysis data'    


def get_echonest_music_qualities(file_name = 'data/echo_music_songids.txt'):
    '''
    Function used to retrieve the information in EchoNest for all the songs
    in MSD subset
    '''
    api_key = util.get_config([echonest_api])[echonest_api]
    outfile = open('data/echo_musicovery_qualities.csv','w')
    track_count, echo_count = 0, 0
    with open(file_name) as f:
        http = urllib3.PoolManager()
        for line in f:
            print line
            track_count += 1 
            song_id = line.strip() 
            params = {}
            params['key'] = api_key
            params['id'] = song_id
            url = song_profile_url.format(**params)
            print url
            try_again = True
            count = 0
            while try_again:
                count += 1
                r = http.request('GET', url)
                jsondata = json.loads(r.data)
                if jsondata['response']['status']['code'] == 3:
                    time.sleep(3)
                else:
                    try_again = False
                if count > 15:
                    print  song_id + ' information not found' + r.data
                    jsondata['response']['status']['code'] = 5   
                    try_again = False
            if jsondata['response']['status']['code'] == 5:
                print song_id + ' information not found' + r.data
            if len(jsondata['response']['songs']) != 0:
                echo_count += 1
                interested_keys = ['energy', 'liveness', 'tempo', 'speechiness', 
                        'acousticness', 'danceability','instrumentalness', 
                        'loudness', 'valence','key','mode', 'time_signature']  
                outline = song_id
                for ikey in interested_keys:
                    outline = outline + ',' + \
                        str(jsondata['response']['songs'][0]['audio_summary'][ikey])        
                outfile.write(outline+ '\n')
                outfile.flush()
    outfile.close()            
    print 'Outof : ' + str(track_count) + '    EchoNest had information for:' + str(echo_count)

chords = [ {'name': "Caj", 'vector' :[1,0,0,0,1,0,0,1,0,0,0,0], 'key': 0, 'mode': 1 },
           #{'name': "C7", 'vector': [1,0,0,0,1,0,0,1,0,0,1,0], 'key': 0, 'mode': 1 },
           {'name': "Cam", 'vector':[1,0,0,1,0,0,0,1,0,0,0,0], 'key': 0, 'mode': 0 },
           {'name': "Dbj", 'vector' :[0,1,0,0,0,1,0,0,1,0,0,0], 'key': 1, 'mode': 1 },
           #{'name': "C#7", 'vector' :[0,1,0,0,0,1,0,0,1,0,0,1], 'key': 1, 'mode': 1 },
           {'name': "Dbm", 'vector':[0,1,0,0,1,0,0,0,1,0,0,0], 'key': 1, 'mode': 0 },
           {'name': "Daj", 'vector' :[0,0,1,0,0,0,1,0,0,1,0,0],  'key': 2, 'mode': 1 },
           #{'name': "D7", 'vector' :[1,0,1,0,0,0,1,0,0,1,0,0],  'key': 2, 'mode': 1 },
           {'name': "Dam", 'vector':[0,0,1,0,0,1,0,0,0,1,0,0],  'key': 2, 'mode': 0 },
           {'name': "Ebj", 'vector' :[0,0,0,1,0,0,0,1,0,0,1,0],  'key': 3, 'mode': 1 },
           #{'name': "Eb7", 'vector' :[0,1,0,1,0,0,0,1,0,0,1,0],  'key': 3, 'mode': 1 },
           {'name': "Ebm", 'vector':[0,0,0,1,0,0,1,0,0,0,1,0],  'key': 3, 'mode': 0 },
           {'name': "Eaj", 'vector' :[0,0,0,0,1,0,0,0,1,0,0,1],  'key': 4, 'mode': 1 },
           #{'name': "E7", 'vector' :[0,0,1,0,1,0,0,0,1,0,0,1],  'key': 4, 'mode': 1 },
           {'name': "Eam", 'vector':[0,0,0,0,1,0,0,1,0,0,0,1],  'key': 4, 'mode': 0 },
           {'name': "Faj", 'vector' :[1,0,0,0,0,1,0,0,0,1,0,0],  'key': 5, 'mode': 1 },
           #{'name': "F7", 'vector' :[1,0,0,1,0,1,0,0,0,1,0,0],  'key': 5, 'mode': 1 },
           {'name': "Fam", 'vector':[1,0,0,0,0,1,0,0,1,0,0,0],  'key': 5, 'mode': 0 },
           {'name': "Gbj", 'vector' :[0,1,0,0,0,0,1,0,0,0,1,0],  'key': 6, 'mode': 1 },
           #{'name': "F#7", 'vector' :[0,1,0,0,1,0,1,0,0,0,1,0],  'key': 6, 'mode': 1 },
           {'name': "Gbm", 'vector':[0,1,0,0,0,0,1,0,0,1,0,0],  'key': 6, 'mode': 0 },
           {'name': "Gaj", 'vector' :[0,0,1,0,0,0,0,1,0,0,0,1],  'key': 7, 'mode': 1 },
           #{'name': "G7", 'vector' :[0,0,1,0,0,1,0,1,0,0,0,1],  'key': 7, 'mode': 1 },
           {'name': "Gam", 'vector':[0,0,1,0,0,0,0,1,0,0,1,0],  'key': 7, 'mode': 0 },
           {'name': "Abj", 'vector' :[1,0,0,1,0,0,0,0,1,0,0,0],  'key': 8, 'mode': 1 },
           #{'name': "Ab7", 'vector' :[1,0,0,1,0,0,1,0,1,0,0,0],  'key': 8, 'mode': 1 },
           {'name': "Abm", 'vector':[0,0,0,1,0,0,0,0,1,0,0,1],  'key': 8, 'mode': 0 },
           {'name': "Aaj", 'vector' :[0,1,0,0,1,0,0,0,0,1,0,0],  'key': 9, 'mode': 1 },
           #{'name': "A7", 'vector' :[0,1,0,0,1,0,0,1,0,1,0,0],  'key': 9, 'mode': 1 },
           {'name': "Aam", 'vector':[1,0,0,0,1,0,0,0,0,1,0,0],  'key': 9, 'mode': 0 },
           {'name': "Bbj", 'vector' :[0,0,1,0,0,1,0,0,0,0,1,0],  'key': 10, 'mode': 1 },
           #{'name': "Bb7", 'vector' :[0,0,1,0,0,1,0,0,1,0,1,0],  'key': 10, 'mode': 1 },
           {'name': "Bbm", 'vector':[0,1,0,0,0,1,0,0,0,0,1,0],  'key': 10, 'mode': 0 },
           {'name': "Baj", 'vector' :[0,0,0,1,0,0,1,0,0,0,0,1],  'key': 11, 'mode': 1 },
           #{'name': "B7", 'vector' :[0,0,0,1,0,0,1,0,0,1,0,1],  'key': 11, 'mode': 1 },
           {'name': "Bam", 'vector':[0,0,1,0,0,0,1,0,0,0,0,1],  'key': 11, 'mode': 0 }
          ]

def cosineSimilarity(a, b):
    dotProduct = 0
    aMagnitude = 0
    bMagnitude = 0
    for i in range(len(a)):
        dotProduct += (a[i] * b[i])
        aMagnitude += math.pow(a[i], 2)
        bMagnitude += math.pow(b[i], 2)
        
    aMagnitude = math.sqrt(aMagnitude)
    bMagnitude = math.sqrt(bMagnitude)
    
    return dotProduct / (aMagnitude * bMagnitude)

def getChordProgression(fileName):
    a = json.load(open(fileName))
    segmentLength = len(a['segments'])
    
    binSize = 10
    prevChord = ""
    chordProgression = []
    
    for segmentIndex in range(segmentLength):
        
        avgChroma = []
        
        if segmentIndex % binSize == 0:
            for i in range(binSize):
                for chroma in range(12):
                    if len(avgChroma) < 12:
                        avgChroma.append(0)
                    
                    if segmentIndex + i < segmentLength: # Don't overflow
                        avgChroma[chroma] = avgChroma[chroma] + a['segments'][segmentIndex + i]['pitches'][chroma]
                        #print segmentIndex, i, a.segments[segmentIndex + i].pitches[chroma]
            
            # normalize chroma vector - divide each by binSize
            for j in range(12):
                avgChroma[j] /= binSize;
            
            #print avgChroma
            
            # compute cosine similarity between average chroma vector and each chord in dictionary
            maxChordSim = 0
            maxChordName = ""
            maxChordMode = 0
            maxChordKey = 0
            for chordIndex in range(len(chords)):
                similarity = cosineSimilarity(avgChroma, chords[chordIndex]['vector'])
                
                if similarity > maxChordSim:
                    maxChordSim = similarity
                    maxChordName = chords[chordIndex]['name']
                    maxChordMode = chords[chordIndex]['mode']
                    maxChordKey = chords[chordIndex]['key']
                
                #print chords[chordIndex]['name'], similarity
            
            #print "CHORD: ", maxChordName, maxChordSim
            
            if prevChord != maxChordName:
                prevChord = maxChordName;
                chordProgression.append({'name' : maxChordName, 'mode':maxChordMode, 'key': maxChordKey, 'sim': round(maxChordSim, 2) })
            
            #print mark(avgChroma, 3)
            #print "---------"
        else:
            continue
        
    return chordProgression                     