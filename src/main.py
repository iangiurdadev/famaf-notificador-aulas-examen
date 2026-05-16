usuarios = leer_sheets()
fechas = fetch_fechas()

for fecha in fechas:
    for u in usuarios:
        if u["fecha"] == fecha:
            enviar_mail(u, fecha)