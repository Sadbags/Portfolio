from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return 'Welcome to quickr'
# Runs the application
if __name__ == '__main__':
    app.run(debug=True)
