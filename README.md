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

## 🚀 Instalación y Uso Local
1. **Clonar repositorio:** git clone https://github.com/alashk28/SYNESTHESIA-TRABAJO.git
2. **Instalar dependencias:** pip install -r requirements.txt
3. **Configurar Credenciales:** Es necesario un archivo .env con las claves de acceso de Spotify y TMDb.
4. **Ejecutar:** python app.py

   
