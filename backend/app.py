from flask import Flask, render_template, request, redirect, url_for, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Define a route for the login page
@app.route('/login')
def login():
    return render_template('login.html')

# Runs the application
if __name__ == '__main__':
    app.run(debug=True)
