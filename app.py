from flask import Flask,request,render_template
import requests
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db' 

db = SQLAlchemy(app) 

class City(db.Model): 
	id = db.Column(db.Integer, primary_key = True) 
	name = db.Column(db.String(30), nullable=False) 

@app.route("/",methods=['GET','POST']) 
def index():
	if request.method == 'POST' :
		if request.form.get('city') : 
			new_city = City(name=request.form.get('city')) 
			db.session.add(new_city) 
			db.session.commit() 

		 
	cities = City.query.all()
	
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=8a224c7c8cc06bfb51401960d7fe6fc6'

	weather_data = []
	for city in cities :  
		response = requests.get(url.format(city.name)).json()

		weather = {'city' : city.name, 
					'temperature' : round(response['main']['temp']-273), 
					'description' : response['weather'][0]['description'],
					'icon' : response['weather'][0]['icon']}

		weather_data.append(weather)

	return render_template('weather.html',weather_data=weather_data)
 

if __name__ == "__main__" : 
	app.run(debug=True) 
