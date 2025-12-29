import os
import logging
import requests
import random
from flask import Flask, render_template, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from collections import Counter
from dotenv import load_dotenv

# --- 1. CONFIGURACIÓN ---
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- 2. CREDENCIALES ---
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, TMDB_API_KEY]):
    logger.error("FALTAN VARIABLES DE ENTORNO EN RENDER")

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_super_secreta_anti_logout')

# --- 3. SCOPE (PERMISOS) AMPLITADO ---
SCOPE = 'user-top-read user-read-private'

