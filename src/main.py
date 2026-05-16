from scraper import consultar_fechas_disponibles
from storage import cargar_estado, guardar_estado
from notifier import notificar

def main():
    fechas = consultar_fechas_disponibles()
    notificadas = cargar_estado()

    for fecha in fechas:
        if fecha in notificadas:
            continue

        notificar(fecha)
        notificadas.add(fecha)

    guardar_estado(notificadas)