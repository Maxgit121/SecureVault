import logging
from app import app
from routes import *  # Import all routes

if __name__ == "__main__":
    # Set up logging for easier debugging
    logging.basicConfig(level=logging.DEBUG)
    # Run the Flask application on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
