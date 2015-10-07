from flask import render_template, request
from app import app
import app.database as database
from app.model.Songs import Song
import json 

@app.route('/')
@app.route('/input')
def input():
    return render_template("input.html")


@app.route('/output')
def output():
  #print request.form['happy']
  tempo = None
  happy = int(request.values.get('happy'))
  excite = int(request.values.get('arousal'))
  if request.values.get('tempo') != '':
    tempo  = float(request.values.get('tempo'))
  mode = int(request.values.get('mode'))
  songs = database.get_songs(happy, excite, tempo, mode)
  out = [song.as_dict() for song in songs]
  return render_template("output.html", results = out)


    


