import os, re
import urllib3
import json
import time

song_profile_url = 'http://developer.echonest.com/api/v4/song/profile?api_key={key}&id={id}&bucket=audio_summary'

def get_echonest_music_qualities(file_name = 'subsets.txt'):
    '''
    Function used to retrieve the information in EchoNest for all the songs
    in MSD subset
    '''
    api_key = get_api_key()
    outfile = open('echo_music.csv','w')
    track_count, echo_count = 0, 0
    with open(file_name) as f:
        http = urllib3.PoolManager()
        for line in f:
            track_count += 1 
            data = re.compile('<SEP>').split(line.strip())
            track_id, song_id, artist, song_title = \
                            re.compile('<SEP>').split(line) 
            params = {}
            params['key'] = api_key
            params['id'] = song_id
            url = song_profile_url.format(**params)
            r = http.request('GET', url)
            jsondata = json.loads(r.data)
            try:
                if jsondata['response']['status']['code'] == 5:
                    print d + ' information not found' + r.data
                if jsondata['response']['status']['code'] == 3:
                    time.sleep(30)
                    r = http.request('GET', url)
                    jsondata = json.loads(r.data)
                if len(jsondata['response']['songs']) != 0:
                    echo_count += 1
                    interested_keys = ['energy', 'liveness', 'tempo', 'speechiness', 
                            'acousticness', 'danceability','instrumentalness', 
                            'loudness', 'valence','key','mode', 'time_signature']  
                    outline = ','.join(data)
                    for ikey in interested_keys:
                        outline = outline + ',' + \
                            str(jsondata['response']['songs'][0]['audio_summary'][ikey])        
                    outfile.write(outline+ '\n')
                    outfile.flush()
            except:
                print 'song with ID:' + song_id + '  raised exception'
                continue       
    outfile.close()            
    print 'Outof : ' + str(track_count) + '    EchoNest had information for:' + str(echo_count)                 

def get_api_key():
    '''
    Reads the credentials file and gets the API key
    '''
    lines = open('credentials').readlines()
    api_key = ''
    for line in lines:
        if line.startswith('#'):
            continue
        data = re.compile('\s+').split(line.strip())
        if data[0] == 'echonest_api':
            api_key = data[1].strip()
    return api_key        