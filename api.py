from flask import *
from flask_sqlalchemy import *
import requests

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

# Instantiate SQLAlchemy class
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2f16279074774c350b2e6e50652b4b90'

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()
        print(r)
        weather = {
            'city': city.name,
            'temperature': float("%2f" % (r['main']['temp'] - 273.15)),
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }

        weather_data.append(weather)

    print(weather_data)

    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run()
