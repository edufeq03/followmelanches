from flask import Flask, render_template, jsonify, request, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

names = ["Big Mac", "Cheddar", "Duplo Cheddar", "Quarteirão", "Duplo Quarteirão", "Chicken", "Chicken Bacon", "Junior", "Tasty", "Tasty Queijo", "Fiesta", "CheeseBurger", "Hamburger", "Duplo Queijo", "Duplo Bacon", "Triplo Burguer", "Brabo Melt", "Brabo Bacon", "Delux", "Chicken Melt", "Legend", "Elite"]
leaderboard = []

@app.route('/')
def index():
    if 'sequence' not in session:
        session['sequence'] = []
    if 'score' not in session:
        session['score'] = 0
    return render_template('index.html', names=names)

@app.route('/next_sequence', methods=['GET'])
def next_sequence():
    next_button = random.choice(names)
    session['sequence'].append(next_button)
    session.modified = True
    return jsonify({'sequence': session['sequence']})

@app.route('/check_sequence', methods=['POST'])
def check_sequence():
    user_sequence = request.json.get('sequence')
    if user_sequence == session['sequence']:
        session['score'] += 1
        return jsonify({'status': 'correct', 'score': session['score']})
    else:
        return jsonify({'status': 'incorrect', 'score': session['score']})

@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.json
    player_info = {
        'score': session['score'],
        'name': data['name'],
        'position': data['position'],
        'store_code': data['store_code']
    }
    leaderboard.append(player_info)
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'status': 'score added', 'leaderboard': leaderboard[:5]})

@app.route('/reset_game', methods=['POST'])
def reset_game():
    session['sequence'] = []
    session['score'] = 0
    session.modified = True
    return jsonify({'status': 'reset', 'score': session['score']})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify({'leaderboard': leaderboard[:5]})

if __name__ == '__main__':
    app.run(debug=True)

