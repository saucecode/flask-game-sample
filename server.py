from flask import *
import os, json, time, random

app = Flask(__name__)
app.secret_key = '1234567'

def save_players(players):
	with open('players.json','w') as f:
		json.dump(players,f)

if not os.path.exists('players.json'):
	save_players({})

with open('players.json','r') as f:
	players = json.load(f)



class City(object):
	def __init__(self, name, items):
		self.name = name
		self.prices = {item: 100 for item in items}
		self.last_price_update = time.time()
	
	def get_prices(self):
		if time.time() - self.last_price_update > 10:
			self.last_price_update = time.time()
			self.update_prices()
		return self.prices

cities = [
	City('New Penzance', ['Mutton', 'Leg of Lamb', 'Pork-flavored sausage', 'Vegan chicken nuggets']),
	City('District 9', ['Black goo', 'Leg of Lamb', 'Pork-flavored sausage', 'Vegan chicken nuggets']),
	City('Los Santos', ['Leg of Lamb', 'Halloween mask', 'Vegan chicken nuggets']),
	City('Medieval Europe', ['Halloween mask', 'Black goo', 'Mutton'])
]

def create_player():
	return {
		'location': random.choice(cities).name,
		'last_seen': time.time(),
		'money': 1000,
		'inventory': {}
	}



@app.route('/')
def home():
	if session.get('name', None) is None or session.get('name') not in players:
		return 'You are not logged in.<br/><form method="POST" action="/login">Player name: <input type="text" name="name" /></form>'
		
	else:
		return render_template('main_screen.html',
			players=players, cities=cities, name=session['name'],
			city=next(c for c in cities if c.name == players[session.get('name')]['location'])
		)



@app.route('/login', methods=['POST'])
def login():
	name = request.form['name']
	session['name'] = name
	
	if name not in players:
		players[name] = create_player()
		return f'Created a new account for {session["name"]}<br/><a href="/">return</a>'
		save_players(players)
		
	else:
		return f'Logged in as {session["name"]} -- welcome back!<br/><a href="/">return</a>'



if __name__ == '__main__':
	app.run(debug=True, threaded=True)