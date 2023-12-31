from flask import Flask
from app import app

if Flask(__name__) == "__main__":
    app.run(debug=True)