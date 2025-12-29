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

# --- 4. MAPA DE GÉNEROS ULTIMATE ---
GENRE_MAPPING = {
    # --- POP & MAIN (Diversión, Amor, Drama) ---
    "Pop": "10402,35,10749",       # Música, Comedia, Romance
    "Dance Pop": "10402,35,18",    # Música, Comedia, Drama
    "K-Pop": "10402,10749,16",     # Música, Romance, Animación
    "Soft Pop": "10749,18,10751",  # Romance, Drama, Familia
    "Teen Pop": "35,10749,10402",  # Comedia, Romance, Música
    "Boy Band": "10402,10749,35",  # Música, Romance, Comedia
    
    # --- ROCK, METAL & PUNK (Intensidad, Acción, Rebeldía) ---
    "Rock": "10402,12,28",         # Música, Aventura, Acción
    "Alternative Rock": "18,878,9648", # Drama, Sci-Fi, Misterio
    "Indie Rock": "18,35,99",      # Drama, Comedia (Indie), Documental
    "Hard Rock": "28,12,53",       # Acción, Aventura, Thriller
    "Metal": "27,878,28",          # Terror, Sci-Fi, Acción
    "Heavy Metal": "27,28,14",     # Terror, Acción, Fantasía (épica)
    "Punk": "80,28,53",            # Crimen, Acción, Thriller
    "Grunge": "18,80,9648",        # Drama, Crimen, Misterio (tono oscuro)
    "Psychedelic": "878,14,9648",  # Sci-Fi, Fantasía, Misterio
    "Ska": "35,28,10402",          # Comedia, Acción, Música (energía divertida)
    
    # --- URBANO, HIP HOP & RITMO (Calle, Historias, Baile) ---
    "Hip Hop": "80,18,28",         # Crimen, Drama, Acción
    "Rap": "80,18,99",             # Crimen, Drama, Documental
    "Trap": "80,53,28",            # Crimen, Thriller, Acción
    "Reggaeton": "10402,35,10749", # Música, Comedia, Romance
    "Latin": "10402,35,10751",     # Música, Comedia, Familia
    "R&B": "10749,18,10402",       # Romance, Drama, Música
    "Soul": "10749,18,36",         # Romance, Drama, Historia
    "Funk": "80,35,10402",         # Crimen (estilo 70s), Comedia, Música
    "Disco": "10402,35,18",        # Música, Comedia, Drama (Saturday Night Fever vibes)
    
    # --- ELECTRÓNICA & FUTURO (Atmósfera, Tecnología, Club) ---
    "Electronic": "878,53,16",     # Sci-Fi, Thriller, Animación
    "Techno": "878,27,53",         # Sci-Fi, Terror, Thriller
    "House": "10402,35,18",        # Música, Comedia, Drama
    "Trance": "878,14,12",         # Sci-Fi, Fantasía, Aventura
    "Ambient": "99,878,9648",      # Documental, Sci-Fi, Misterio
    "Dubstep": "28,878,53",        # Acción, Sci-Fi, Thriller (caos y energía)
    
    # --- VIBES RELAX, CLÁSICOS & RAÍCES ---
    "Jazz": "10402,80,36",         # Música, Crimen (Noir), Historia
    "Classical": "36,18,10751",    # Historia, Drama, Familia
    "Opera": "10402,18,10749",     # Música, Drama, Romance (teatralidad)
    "Folk": "12,18,99",            # Aventura, Drama, Documental
    "Country": "37,18,10402",      # Western, Drama, Música
    "Bluegrass": "37,12,35",       # Western, Aventura, Comedia
    "Blues": "18,80,36",           # Drama, Crimen, Historia
    "Reggae": "99,35,10402",       # Documental, Comedia, Música (chill vibes)
    
    # --- OTROS ESTILOS ---
    "Soundtrack": "14,12,16",      # Fantasía, Aventura, Animación
    "Anime": "16,14,878",          # Animación, Fantasía, Sci-Fi
    "Goth": "27,14,9648",          # Terror, Fantasía, Misterio
    "Indie Pop": "35,18,10749",    # Comedia, Drama, Romance
    "Lo-Fi": "16,99,18"            # Animación, Documental, Drama (study vibes)
}



