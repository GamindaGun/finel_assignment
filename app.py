# Import necessary libraries
from flask import Flask, render_template, request
from weather import main as get_weather     # Import the main function from the weather module
import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import yaml


app = Flask(__name__)

# yaml.load("C:\\Unit4\\finel_assignment\\weatherbotdata.yml")
chatbot = ChatBot('ChatBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("C:\\Unit4\\finel_assignment\\weatherbotdata.yml")


app.config['SECRET_KEY'] = "MY KEY"  # Set a secret key for Flask session management


# Define a form class for city selection
class CityDataInputForm(FlaskForm):
    city_name = SelectField('cityNam', validators=[DataRequired()],
                            choices=['Lake District National Park UK',
                                     'Corfe Castle UK', 'The Cotswolds UK', 'Cambridge UK',
                                     'Bristol UK', 'Oxford UK', 'Norwich UK', 'Stonehenge UK',
                                     'Watergate UK', 'Birmingham UK'])
    submit = SubmitField("Submit")


# Define the main route for the web application
@app.route("/", methods=['GET', 'POST'])

def index():
    city_name = None
    form = CityDataInputForm(request.form)

    # Handle form submission
    if form.validate_on_submit():
        city_name = form.city_name.data
        form.city_name.data = ''

    current_year = datetime.datetime.now().year

    current_weather_data = None
    forecast_weather_data = None

    if request.method == 'POST':
        city = request.form.get('city_name')

        # Retrieve current and forcast weather data
        current_weather_data, forecast_weather_data = get_weather(city)
        # You should have separate functions to fetch current weather and forecast data



    # Render the HTML template with form, current and forcast weather data, and current year
    return render_template('index.html', form=form, city_name=city_name,
                           current_weather_data=current_weather_data,
                           forecast_weather_data=forecast_weather_data,
                           year=current_year)

@app.route("/home")
def home():
    return render_template("index.html")

# Define a route for handling bot responses
@app.route("/getBotResponse")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

# Run the Flask application if executed as the main script
if __name__ == "__main__":
    app.run(debug=True)
