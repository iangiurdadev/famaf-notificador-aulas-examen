# Automatización Aulas de Exámenes

Script en Python que monitorea la publicación de aulas de exámenes y envía notificaciones por email a los estudiantes según la fecha en la que rinden.

---

## Cómo funciona

1. Se ejecuta un scraper que obtiene las fechas de exámenes disponibles en la página.

2. Los usuarios se obtienen desde una fuente externa, donde cada usuario registra:
   - email
   - fecha en la que rinde

3. Para cada fecha detectada:
   - Se buscan los usuarios que coinciden con esa fecha
   - Se envía una notificación por email a cada uno

4. Se guarda un registro de las fechas ya notificadas para evitar envíos duplicados.
