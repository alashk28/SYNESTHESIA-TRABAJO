# SYNESTHESIA: Análisis Sensorial y Recomendación Cinematográfica

Este proyecto es una plataforma web desarrollada en Python con el framework Flask. Su objetivo es transformar el perfil auditivo de un usuario en una experiencia cinematográfica personalizada, integrando de manera automatizada las APIs de Spotify y TMDb.

## Integrantes del Grupo 

| Nombre | Codigo |
|--------|--------|
| Carmen Tullume Arlette | 20231483
| Flores Villa Brayan | 20231492
| Palma Cruz Yasmin | 20231504

**Institución:** Universidad Nacional Agraria la Molina  
**Curso:** Lenguaje de Programación 2  
**Profesor:** Ana Vargas  
**Fecha de entrega:** Lunes 29 de Diciembre del 2025  

## 📝 Descripción del Proyecto 
**Synesthesia** utiliza el procesamiento de datos en tiempo real para conectar dos industrias culturales. La aplicación extrae metadatos de audio, identifica el estado emocional del usuario ("Mood") y lo traduce a géneros cinematográficos específicos, permitiendo un descubrimiento de contenido basado en la psicología del oyente.

## 🤖 Automatización de la descarga de Información 
El sistema integra dos fuentes de datos externas mediante el consumo de APIs oficiales:
1. **Spotify Web API (Metadata Musical):**
   - **Descarga Automatizada**: El sistema extrae los 20 artistas principales y géneros del usuario mediante la librería
     spotipy
   - **Análisis de Audio**: Intenta descargar métricas técnicas como danceability, energy y valence.
   - **Algoritmo de Resiliencia (Plan B)**: Si la API restringe el acceso a métricas detalladas, el código ejecuta una
     inferencia inteligente basada en palabras clave de los géneros musicales, garantizando que la descarga de información
     nunca se detenga
2. **TMDb API (Metadata Cinematográfica):**
   - **Consulta Multi-fuente:** Utiliza la base de datos de The Movie Database para buscar películas que coincidan con el
     análisis previo.
   - **Enriquecimiento de datos:** Por cada título, se descarga automáticamente el director, el reparto principal, la
     sinopsis y la calificación crítica.

## 📊 Estructura y Resumen de la Información
La información descargada se organiza bajo una estructura lógica que permite su análisis posterior:
- **Mapeo de Datos (Cross-Platform)**: Se utiliza un diccionario técnico (GENRE_MAPPING) que vincula IDs de música con IDs
  de cine (ej: Jazz -> Crimen/Noir/Historia).
- **Clasificación de perfiles:**
  Los datos se resumen en categorías emocionales como "Euforia Total", "Melancolía Profunda" o "Oyente Equilibrado".
- **Interfaz dinámica:** Los resultados se estructuran en el frontend usando Jinja2 y Tailwind CSS, presentando métricas
  visuales y tarjetas de recomendación interactivas.
  
## 📂 Estructura del Repositorio 
El proyecto sigue una arquitectura de aplicación web moderna y escalable.

| Carpeta / Archivo | Función Técnica |
|-------------------|-------------|
| **templates/index.html** | Interfaz de usuario con renderizado dinámico de datos. Contiene el archivo HTML (index.html) procesado con Jinja2. |
| **app.py** | El núcleo de la aplicación, la lógica central. Maneja rutas (OAuth), lógica de APIs y el algoritmo de mapeo. |
| **Procfile** | Configuración de procesos para el despliegue en la nube (Gunicorn). |
| **requirements.txt** | Listado de librerías necesarias para la ejecución del entorno (flask, spotipy, python-dotenv, gunicorn, requests). |
| **.gitignore** | Protección de archivos de caché y variables de entorno .env. |
| **.env** | (Ignorado por seguridad) Archivo local que almacena las credenciales privadas de las APIs. |

## 🧩 Implementación Técnica Destacada 
A continuación, mostramos los fragmentos de código clave que hacen posible el fnucionamiento del proyecto: 

### 1. Algoritmo de resiliencia ("Plan B")
Para cumplir con el criterio de **Automatización**, desarrollamos un sistema de inferencia. Si la API de Spotify falla al entregar las métricas de audio (error 403 o datos vacíos), el sistema **calcula** el mood basándose en las palabras clave de los géneros musicales:

```python
 # --- PLAN B: ESTIMACIÓN INTELIGENTE BASADA EN GÉNEROS ---
        # 1. Obtenemos los géneros que calculados previamente
        user_genres = get_top_genres(sp)
        # 2. Valores base (un punto medio estándar)
        est = {'danceability': 0.5, 'energy': 0.6, 'valence': 0.6, 'acousticness': 0.3}
        # 3. Ajustamos según lo que escucha el usuario
        genres_text = " ".join(user_genres).lower()
        # Reglas de inferencia si falla la descarga directa de audio features
        if any(x in genres_text for x in ['metal', 'rock', 'punk', 'hard']):
            est['energy'] = min(0.95, est['energy'] + 0.3)
            est['acousticness'] = max(0.05, est['acousticness'] - 0.2)
            
        if any(x in genres_text for x in ['pop', 'dance', 'reggaeton', 'hip hop', 'urbano', 'latino']):
            est['danceability'] = min(0.95, est['danceability'] + 0.3)
            est['energy'] = min(0.95, est['energy'] + 0.2)
            est['valence'] = min(0.95, est['valence'] + 0.2)
        # ... (más reglas de inferencia)            
```

### 2. Mapeo cross-Platform (Diccionario)
Para traducir música a cine, creamos un diccionario que actúa como "traductor emocional". Definimos el GENRE_MAPPING para vincular géneros de Spotify con IDs específicos de TMDb:
```python
# Mapeo: Si escuchas Jazz, te recomendamos Cine de Crimen (Noir) e Historia
GENRE_MAPPING = {
    # --- POP & MAIN (Diversión, Amor, Drama) ---
    "Pop": "10402,35,10749",       # Música, Comedia, Romance
    "Dance Pop": "10402,35,18",    # Música, Comedia, Drama
    "K-Pop": "10402,10749,16",     # Música, Romance, Animación
    "Soft Pop": "10749,18,10751",  # Romance, Drama, Familia
    "Teen Pop": "35,10749,10402",  # Comedia, Romance, Música
    "Boy Band": "10402,10749,35",  # Música, Romance, Comedia
    # ... (más géneros)
}
```

### 3. Consulta dinámica a TMDb API 
Construimos la URL de consulta en tiempo real, inyectando los IDs de los géneros (genre_id_query) y aplicando filtros de calidad (vote_count.gte=300) para recomendar solo películas relevantes:

```python
# Usamos genre_id_query en la URL en vez de raw_genre_id
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key_to_use}&with_genres={genre_id_query}&language=es-ES&sort_by=popularity.desc&include_adult=false&page=1&vote_count.gte=300"
        
        try:
            response = requests.get(url)
            data = response.json()
            # Procesamiento posterior de resultados...
            # 1. Obtenemos las 20 películas
            # 2. Las barajamos
            # 3. Tomamos 5
```

### 4. Autenticación segura (OAuth) 
La conexión con Spotify se realiza utilizando variables de entorno para proteger las credenciales (SPOTIPY_CLIENT_ID), solicitando permisos específicos de lectura (user-top-read):

```python
@app.route('/login')
def login():
    handler = FlaskSessionCacheHandler(session)
    # USAMOS LA VARIABLE SCOPE GLOBAL QUE DEFINIMOS ARRIBA
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_handler=handler, show_dialog=True)
    return redirect(sp_oauth.get_authorize_url())
```

## 🚀 Instalación y Uso Local
1. **Clonar repositorio:** git clone https://github.com/alashk28/SYNESTHESIA-TRABAJO.git
2. **Instalar dependencias:** pip install -r requirements.txt
3. **Configurar Credenciales:** Es necesario un archivo .env con las claves de acceso de Spotify y TMDb.
4. **Ejecutar:** python app.py

   
