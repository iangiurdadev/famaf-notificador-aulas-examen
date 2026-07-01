import gspread
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS = BASE_DIR / "credentials" / "service_account.json"


COLUMNA_FECHA = "¿En qué fecha rendís?"
COLUMNA_CORREO = "Correo electronico"

MAX_REGISTROS = 100


class GoogleSheets:
    def __init__(self, credentials_file, spreadsheet_name, worksheet_name):
        self.gc = gspread.service_account(filename=credentials_file)
        self.sh = self.gc.open(spreadsheet_name)
        self.sheet = self.sh.worksheet(worksheet_name)

    def imprimir_tabla(self):
        datos = self.sheet.get_all_records()
        df = pd.DataFrame(datos)
        print(df)

    def obtener_registros(self):
        registros = self.sheet.get_all_records()


        if len(registros) > MAX_REGISTROS:
            raise RuntimeError(
                f"Se excedió el límite de {MAX_REGISTROS} respuestas "
                f"({len(registros)} encontradas)."
            )

        return registros

    def obtener_interesados(self):
        registros = self.obtener_registros()

        interesados = {}

        for registro in registros:
            fecha = registro[COLUMNA_FECHA].replace("/", "-")
            correo = registro[COLUMNA_CORREO]

            if fecha not in interesados:
                interesados[fecha] = []

            interesados[fecha].append(correo)

        return interesados




if __name__ == "__main__":
    gs = GoogleSheets(
        str(CREDENTIALS),
        "Formulario Prueba (Respuestas)",
        "Hoja 1"
    )

    print("TEST")
    interesados = gs.obtener_interesados()
    print(interesados)