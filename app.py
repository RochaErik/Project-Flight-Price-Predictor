import pandas as pd
from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)

