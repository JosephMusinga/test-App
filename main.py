# import the Flask library
from flask import Flask, render_template

app = Flask(__name__)
 
 
@app.route('/')
def home():
        return render_template('index.html')

@app.route('/transcribe')
def transcribe():
        return render_template('transcribe.html')

@app.route('/customize')
def customize():
        return render_template('customize.html')
 

if(__name__ == "__main__"):
    app.run(debug=True)
