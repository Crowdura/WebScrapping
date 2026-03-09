# Proyecto IA con Ollama

Este proyecto demuestra cómo integrar modelos de lenguaje de Ollama en aplicaciones Python para análisis de texto y validación de archivos.

## Características
- Conexión directa con Ollama vía API REST.
- Ejecución dinámica de modelos (Llama, Mistral, Gemma, etc.).
- Validación de archivos de texto según criterios definidos.
- Ejemplos prácticos de uso con `requests`.
- Realización de webScrapping para automatización.
- Exportación de archivos Csv de data obtenida

## 📦 Instalación

Clona el repositorio y crea un entorno virtual:

```bash
git clone https://github.com/usuario/proyecto-ollama.git
cd proyecto-ollama
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows
pip install -r requirements.txt

Inicio de programa
py -3 index.py