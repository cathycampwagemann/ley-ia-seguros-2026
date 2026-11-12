# Congreso Extraordinario · Ley IA y Seguros

## 1. Supabase
1. Crear proyecto en https://supabase.com.
2. Abrir SQL Editor y ejecutar `supabase.sql`.
3. En Project Settings / API (o API Keys, según interfaz) copiar Project URL y la clave **service_role** (secret). **Nunca subir la clave a GitHub ni compartirla**.

## 2. GitHub
Subir a un repositorio privado o público `app.py`, `articulos.json`, `requirements.txt`, `supabase.sql`, `.gitignore` y opcionalmente este README. No subir un archivo real `secrets.toml`.

## 3. Streamlit Community Cloud
1. Crear app desde el repositorio y elegir `app.py` como Main file.
2. En Advanced settings / Secrets, pegar las tres variables del archivo `.streamlit/secrets.toml.example`, reemplazando sus valores reales. No subir el ejemplo con claves reales.
3. Desplegar la app.

## 4. Uso el día del evento
- Computador/proyector: `https://TU-APP.streamlit.app/?vista=proyeccion` (F11 para pantalla completa).
- Celular: `https://TU-APP.streamlit.app/?vista=admin`, ingresar contraseña.
- Seleccionar las 7 letras, pulsar **Guardar las siete selecciones** y después **PROMULGAR LEY**.
- El proyector consulta Supabase cada 2 segundos y revela los siete artículos a la vez.
- Si se cambia una selección después de promulgar, hay que guardar el nuevo borrador y pulsar **PROMULGAR LEY** de nuevo.
- **Retirar ley de la proyección** vuelve a la pantalla de espera sin borrar los textos guardados.

## Seguridad y operación
La clave service_role queda exclusivamente en los secretos del servidor Streamlit. La tabla tiene RLS habilitado sin políticas públicas. El parámetro `vista=admin` no concede acceso sin contraseña. La contraseña es compartida entre administradores, y no hay registro de auditoría individual. Usa una contraseña robusta y no difundas el enlace administrativo. Streamlit Community Cloud puede suspender apps inactivas; abre ambas pantallas y prueba antes del evento. Se requiere conexión a Internet en ambos dispositivos.
