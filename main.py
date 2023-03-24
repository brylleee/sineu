from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Global variable to store the data
teamA = "Team A"
teamB = "Team B"
quarter = "1st Quarter"
scores = {'teamA': 0, 'teamB': 0}
teams = {'teamA': teamA, 'teamB': teamB}

# Route for serving the HTML page with the real-time updates
@app.route('/')
def index():
    return render_template('index.html', scores=scores, teams=teams, quarter=quarter)


@app.route('/init/<teamAName>/<teamBName>')
def init(teamAName, teamBName):
    global teamA
    global teamB
    teamA = teamAName
    teamB = teamBName
    teams = {'teamA': teamA, 'teamB': teamB}

    socketio.emit('teamUpdate', teams, namespace='/')
    return render_template('index.html', scores=scores, teams=teams, quarter=quarter)


@app.route('/quarterC/<int:q>')
def quarterC(q):
    global quarter
    if q == 1:
        quarter = '1st Quarter'
        socketio.emit('quarterUpdate', {'quarter': quarter}, namespace='/')
    elif q == 2:
        quarter = '2nd Quarter'
        socketio.emit('quarterUpdate', {'quarter': quarter}, namespace='/')
    elif q == 3:
        quarter = '3rd Quarter'
        socketio.emit('quarterUpdate', {'quarter': quarter}, namespace='/')
    elif q == 4:
        quarter = '4th Quarter'
        socketio.emit('quarterUpdate', {'quarter': quarter}, namespace='/')

    return render_template('index.html', scores=scores, teams=teams, quarter=quarter)


@app.route('/styles/<element>/<property>/<value>')
def styles(element, property, value):
    socketio.emit('stylesUpdate', {'element': '#'+element, 'property': property, 'value': value}, namespace='/')
    return render_template('index.html', scores=scores, teams=teams, quarter=quarter)


@app.route('/reset')
def reset():
    scores = {'teamA': 0, 'teamB': 0}
    teams = {'teamA': 'Team A', 'teamB': 'Team B'}
    quarter = "1st Quarter"
    socketio.emit('teamUpdate', teams, namespace='/')
    socketio.emit('scoreUpdate', scores, namespace='/')
    socketio.emit('quarterUpdate', {'quarter': quarter}, namespace='/')
    return render_template('index.html', scores=scores, teams=teams, quarter=quarter)


@app.route('/add/<team>/<int:points>')
def add(team, points):
    scores[team] += points
    socketio.emit('scoreUpdate', scores, namespace='/')
    return render_template('index.html', scores=scores, teams=teams, quarter=quarter)


@app.route('/correct/<team>')
def correct(team):
    if scores[team] > 0:
        scores[team] -= 1
    socketio.emit('scoreUpdate', scores, namespace='/')
    return render_template('index.html', scores=scores, teams=teams, quarter=quarter)


'''
def generate_data():
    global data
    while True:
        data = random.randint(1, 100)
        socketio.emit('new_data', {'data': data}, namespace="/")
        socketio.sleep(1)

# Emit the data over the websocket
@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(target=generate_data)
'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)