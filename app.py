from flask import Flask
import scraper
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/')
def getNews():
    return scraper.getAllChannelsNews()



if __name__ == "__main__":
    app.run(debug=True)