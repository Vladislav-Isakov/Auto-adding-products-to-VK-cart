import logging
from logging.handlers import RotatingFileHandler
import os
from config import Config
import requests
from requests.exceptions import Timeout
import ast
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/panel.log', maxBytes=1200000,
                                    backupCount=5)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
logging.getLogger(__name__)
logging.addHandler(file_handler)
logging.setLevel(logging.INFO)