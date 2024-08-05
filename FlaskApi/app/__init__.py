from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from app.config import Config
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})

def create_app():
    load_dotenv()  # loads variables from .env file into environment
    
    here = os.path.abspath(os.path.dirname(__file__))
    # Get the parent directory
    parent_directory = os.path.dirname(here)

    # Get the current UTC time and format it
    current_utc_time = datetime.now(timezone.utc)
    formatted_time = current_utc_time.strftime('%Y%m%d')

    # Define the log file name with the current UTC time
    logfile_name = f"Vuln_app_{formatted_time}.log"
    logfile_path = os.path.join(parent_directory, 'logs' ,logfile_name)

    # Initialize logging
    logging.basicConfig(
        filename=logfile_path, level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    log = logging.getLogger(__name__)
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app)
    
    with app.app_context():
        from app.routes import register_routes
        register_routes(app, db)

    return app
