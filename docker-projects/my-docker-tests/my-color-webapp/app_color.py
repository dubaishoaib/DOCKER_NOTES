import os
from flask import Flask
app = Flask(__name__)

color = os.environ.get('APP_COLOR')

@app.route("/")
def main():
    print(color)
    return "Welcome!"

@app.route('/how are you')
def hello():
    return 'I am good, how about you?'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
