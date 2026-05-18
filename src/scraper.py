import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import unicodedata
import os
from requests.exceptions import RequestException, Timeout, HTTPError


URL = "https://web.archive.org/web/20251209132303/https://famaf.unc.edu.ar/la-facultad/institucional/areas-y-departamentos/%C3%A1rea-direcci%C3%B3n-de-ense%C3%B1anza/despacho-de-Estudiantes-informa/"

DIAS = [
    "lunes","martes","miercoles","miércoles",
    "jueves","viernes","sabado","sábado","domingo",
]


# ---------- utils ----------
def normalizar(texto):
    texto = texto.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def es_match(texto):
    return "aula" in texto and "examen" in texto


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

def consultar_fechas_disponibles():
    session = requests.Session()
    soup = get_html(session,URL)

    resultados = []
    coincidencias = 0
    guardadas = 0

    for h2 in soup.find_all("h2", class_="title"):
        texto_original = h2.get_text(strip=True)
        texto = normalizar(texto_original)

        if not es_match(texto):
            continue

        print(f"\nMatch encontrado: {texto_original}")
        coincidencias += 1

        dia = extraer_dia(texto)
        if not dia:
            print("No se encontró día, se ignora")
            continue

        img_rel = obtener_imagen(h2)
        if not img_rel:
            print("No se encontró imagen asociada")
            continue

        img_url = urljoin(URL, img_rel)
        print("Descargando:", img_url)

        data, ext = descargar(session,img_url)

        nombre = f"aula-final-{dia}{ext}"
        ruta = guardar(nombre, data)
        guardadas+=1


        resultados.append({
            "dia": dia,
            "ruta": ruta
        })

        print("Guardada como", nombre)

    if coincidencias == 0:
        print("No se encontraron aulas de examen")
    else:
        print(f"Coincidencias: {coincidencias}")
        print(f"Imágenes guardadas: {guardadas}")

    return resultados
