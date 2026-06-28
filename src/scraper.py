import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import unicodedata
import os
from requests.exceptions import RequestException, Timeout, HTTPError
import re
from datetime import datetime

URL = "https://www.famaf.unc.edu.ar/la-facultad/institucional/areas-y-departamentos/%C3%A1rea-direcci%C3%B3n-de-ense%C3%B1anza/despacho-de-Estudiantes-informa/"

DIAS = [
    "lunes","martes","miercoles","miércoles",
    "jueves","viernes","sabado","sábado","domingo",
]

MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

# ---------- utils ----------

def extraer_id_examen(texto_original, anio=2026):
    texto = normalizar(texto_original)

    match = re.search(r"(\d{1,2}) de ([a-z]+)", texto)
    if not match:
        return None

    dia = int(match.group(1))
    mes_txt = match.group(2).lower()

    mes = MESES.get(mes_txt)
    if not mes:
        return None

    return f"{dia:02d}-{mes:02d}-{anio}"

def normalizar(texto):
    texto = texto.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def es_match(texto):
    return "examen" in texto


def extraer_dia(texto):
    for dia in DIAS:
        if normalizar(dia) in texto:
            return normalizar(dia)
    return None


def obtener_imagen(h2):
    bloque = h2.find_parent().find_next("div", class_="block-image")
    if not bloque:
        return None

    img = bloque.find("img")
    if not img or not img.get("src"):
        return None

    return img["src"]


def descargar(session,url_img):
    response = session.get(url_img, timeout=10)
    response.raise_for_status()

    data = response.content
    ext = os.path.splitext(url_img)[1] or ".jpg"
    return data, ext



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(BASE_DIR, "data", "imagenes")

def guardar(nombre, data):
    os.makedirs(CARPETA, exist_ok=True)
    ruta = os.path.join(CARPETA, nombre)
    print(f"Guardando en {ruta}")

    with open(ruta, "wb") as f:
        f.write(data)

    return ruta


def get_html(session,url, timeout=10):
    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    except Timeout:
        raise Exception(f"Timeout al pedir: {url}")

    except HTTPError as e:
        raise Exception(f"Error HTTP {e.response.status_code} en {url}")

    except RequestException as e:
        raise Exception(f"Error de red en {url}: {str(e)}")


# ---------- main ----------

def procesar_examen(session, texto_original, img_rel, resultados):
    texto = normalizar(texto_original)

    if not es_match(texto):
        return False

    print(f"\nMatch encontrado: {texto_original}")

    dia = extraer_dia(texto)
    if not dia:
        print("No se encontró día, se ignora")
        return False

    id_examen = extraer_id_examen(texto_original)
    if not id_examen:
        print("No se pudo extraer id, se ignora")
        return False

    img_url = urljoin(URL, img_rel)
    print("Descargando:", img_url)

    data, ext = descargar(session, img_url)

    nombre = f"aula-final-{dia}{ext}"
    ruta = guardar(nombre, data)

    resultados.append({
        "id": id_examen,
        "dia": dia,
        "ruta": ruta
    })

    print("Guardada como", nombre)
    return True

def consultar_fechas_disponibles():
    session = requests.Session()
    soup = get_html(session, URL)

    resultados = []

    # Estrategia 1: información en el título
    for encabezado in soup.find_all(["h2", "h3", "h4"]):
        texto = encabezado.get_text(strip=True)
        img = obtener_imagen(encabezado)

        if img:
            procesar_examen(session, texto, img, resultados)

    # Si no se encontró nada, probar la otra representación
    if resultados:
        return resultados

    # Estrategia 2: información en el alt de la imagen
    for img in soup.find_all("img"):
        texto = img.get("alt", "").strip()
        src = img.get("src")

        if src:
            procesar_examen(session, texto, src, resultados)

    return resultados
