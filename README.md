# songsDB

The BIG goal of the project is to synthesize backing tracks in different genres to evoke a specified emotion. Backing tracks enable musicians to practice solos. Most of the backing tracks are either classified according to genre and creating a backing track for a paricular emotional response is done by experts (eg. Happy blues scale, uplifting rock ballad).

The emotional space this project visualizes is the commonly used VA space (Valence-Arousal). Typically different emotions in VA space could be summarized as :
      i). + Valence, + Arousal : Happy, energetic, exciting, inspirational, motivational.
      ii). + Valence, - Arousal : Serene, relaxing, tranquil, calm, peaceful.
      iii). -Valence, + Arousal : Anxious, anger, terrified, disgusted.
      iv). -Valance - Arousal : sad, depresssing, bored, despair. 
      
To be specific about the project goal, upon chosing the quadrant in the VA space, tempo, time signature and key, this project aims to suggest a chord progression that is frequently used in songs that typically evoke such response. 

Datasets used: 
i). Subset of million songs database (MSD): 10,000 songs from the MSD are used in the analysis to squeeze out the important features that render the emotional features of a song.
ii). Lyrics of the songs in MSD. Often times, lyrics are written to complement the emotional content in a song. This lyrics are used in a Bag-of-Words format provided by MSD database.
iii). EchoNest API : EchoNest is a comprehensive platform to analyze the audio features of a song. To use the latest analysis of the EchoNest (V4 at the time of project), audio summary features such as tmepo, valence, loudness, danceability etc. have been retrieved from their dataabase. 
iv). Last.Fm tag library: Social tags attached to each song by listeners are collected my MSD and these have been used to classify the song into one of the VA quadrants using Echonest features and lyrics.  
