import json
import urllib3
import sys, re
import time
import util
reload(sys)

sys.setdefaultencoding('utf8')

musicovery_api = 'musicovery_api'

musicovery_url = 'http://musicovery.com/api/V2/playlist.php?&fct=getfrommood&popularitymax=100&popularitymin=50&trackvalence={valence}&trackarousal={arousal}&resultsnumber=100&listenercountry=us&format=json&before1950=false&date50=true&date60=true&date70=false&date80=false&date90=false&date00=false&date10=false&apikey={api_key}'

musicovery_search = 'http://musicovery.com/api/V2/track.php?fct=search&title={title}&artistname={artist}&format=json'#&apikey={api_key}'

def search_track():
    lines = open('data/SongswithChords.csv').read().split('\r')
    api_key = util.get_config([musicovery_api])[musicovery_api] 
    f = open('data/songswithchords_musicoveryid.csv','w')
    http = urllib3.PoolManager()    
    for line in lines[1::
        if line.strip() == '':
            continue
        data = re.compile(',').split(line.strip())
        artist = data[1].strip().replace(' ','%20').replace('&', '%27') 
        title = data[2].strip().replace(' ', '%20').replace('&', '%27')
        url = musicovery_search.format(**{'title':title}, 'artist':artist, 'api_key':api_key})
        r = http.request('GET', url)
        jsondata = json.loads(r.data)



def get_songs():
    api_key = util.get_config([musicovery_api])[musicovery_api]
    valences = range(50000, 1000000, 100000)
    arousals = range(50000, 1000000, 100000)
    f = open('data/musicovery_60.csv','w')
    http = urllib3.PoolManager()
    for valence in valences:
        for arousal in arousals:
            print 'getting songs for valence ' + str(valence) + '  arousal: ' + str(arousal)
            url = musicovery_url.format(**{'valence':valence, 'arousal':arousal, 'api_key':api_key})
            r = http.request('GET', url)
            jsondata = json.loads(r.data)
            print url 
            if jsondata['root']['response']['code'] != '100':
                print 'ERROR out ' + jsondata['root']['response']['code']
                time.sleep(2)
                r = http.request('GET', url)
                jsondata = json.loads(r.data)
            for track in jsondata['root']['tracks']['track']:
                try:
                    title = defaultMe(track['title'])
                    id = defaultMe(track['id'])
                    artist = defaultMe(track['artist']['name'])
                    artist_mbid = defaultMe(track['artist']['mbid'])
                    music_valence = defaultMe(track['valence'])
                    music_arousal = defaultMe(track['arousal'])
                    releasedate = defaultMe(track['releasedate'])
                    genre = defaultMe(track['genre'])
                    line = str(id) + ',' + title + ',' + artist + ',' + \
                           artist_mbid + ',' + str(music_valence) + ',' + \
                           str(music_arousal)      
                    f.write(line + '\n')
                    f.flush()
                except:
                    print 'some error for one track!!'
                    continue    
    f.close()    

def get_unique():
    f = open('data/musicovery_unique.csv','w')
    lines = open('data/musicovery_all.csv').read().split('\r') 
    unique = {}
    for line in lines:
        if line.strip() == '':
            continue
        song_id, title, artist, mbid, valence, arousal = re.compile(',').split(line.strip())
        if song_id in unique:
            continue
        unique[song_id] = line
        f.write(line + '\n')
        f.flush()
    print 'Out of ' + str(len(lines)) + '   only ' + str(len(unique)) + '  are unique'    
    f.close()     


def defaultMe(p):
    if len(p) == 0:
        return 'NOTPRESENT'
    return p  
