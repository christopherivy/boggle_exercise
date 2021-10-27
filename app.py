from flask import Flask, request, render_template, redirect, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"

boggle_game = Boggle()


@app.route('/')
def homepage():
   """ Show the board. """

   board = boggle_game.make_board()
   session['board'] = board
   highscore = session.get('highscore', 0)
   number_of_plays = session.get('number_of_plays', 0)

   return render_template('index.html', board=board, highscore=highscore, number_of_plays=number_of_plays)


@app.route('/check-word')
def check_word():
   """ Check if the word is in the dictionary (words.txt) """

   word = request.arg['word']
   board = session['board']
   response = boggle_game.check_valid_word(board, word)

   return jsonify({'result': response})


@app.route('/post-score', methods=['POST'])
def post_score():
   """ Get score, update number_of_plays, update highest score """

   score = request.json['score']
   highscore = session.get('highscore', 0)
   number_of_plays = session.get('number_of_plays', 0)

   session['number_of_plays'] = number_of_plays + 1
   session['highscore'] = max(score, highscore)

   return jsonify(brokeRecord=score > highscore)
