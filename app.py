import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración del cliente Groq (RECUERDA MOVER ESTA CLAVE A TU .env PRONTO)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- RUTA 1: EL CHATBOT ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    mensaje_usuario = data.get('mensaje')
    
    if not mensaje_usuario:
        return jsonify({"error": "No se recibió ningún mensaje"}), 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Eres el asistente virtual de SOLDESP, empresa peruana de ingeniería y soldadura. "
                        "Nuestra ubicación exacta es: URB. JOSÉ CARLOS MARIÁTEGUI MZ 'M' LT 14, PAMPA INALÁMBRICA, ILO, MOQUEGUA - PERÚ. "
                        "Nuestros servicios son: fabricación metálica, soldaduras especiales, mantenimiento de plantas, arenado y pintura. "
                        "Responde siempre en español, de forma breve, amable y profesional. "
                        
                        "REGLA ESTRICTA 1 (TEMAS PROHIBIDOS): Eres un asistente EXCLUSIVO de SOLDESP. Si el usuario te pregunta sobre temas que NO tienen relación con la empresa (como películas, política, chistes, recetas, etc.), DEBES negarte a responder cortésmente diciendo: 'Lo siento, soy el asistente virtual de SOLDESP y solo puedo responder preguntas relacionadas con nuestros servicios, ubicación o procesos de reclutamiento.' No des ninguna otra información. "
                        
                        "REGLA ESTRICTA 2 (UBICACIÓN): Si el usuario pregunta por la ubicación, dale EXACTAMENTE la dirección que te di arriba. No inventes otras direcciones. "
                        
                        "REGLA ESTRICTA 3 (EMPLEO): Si el usuario pregunta por vacantes, trabajo o postular, DEBES responder: '¡Claro que sí! Actualmente contamos con vacantes disponibles. ¿Te gustaría postular ahora o más tarde?' Y a continuación, DEBES agregar obligatoriamente este código HTML exacto para el botón: "
                        "<br><br><button onclick='abrirModalPostulacion()' style='padding:12px 20px; background-color:#0a2540; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer; font-size:14px;'>Postular ahora</button> "
                        "NO pidas el CV por el chat, solo dile que use el botón. "
                        
                        "REGLA ESTRICTA 4 (WHATSAPP): Si el usuario pide contactarte o hablar con un asesor, DEBES responder incluyendo este código HTML exacto al final de tu mensaje: "
                        "<br><br><a href='https://wa.me/51953660826' target='_blank' style='display:inline-block; padding:10px 20px; background-color:#ff6b00; color:white; text-decoration:none; border-radius:5px; font-weight:bold;'>Haz clic aquí para ir a WhatsApp</a>"
                    )
                },
                {"role": "user", "content": mensaje_usuario}
            ],
            model="openai/gpt-oss-120b",
        )
        return jsonify({"respuesta": chat_completion.choices[0].message.content})
        
    except Exception as e:
        print(f"ERROR DETECTADO EN CHAT: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- RUTA 2: RECIBIR POSTULACIONES ---
@app.route('/postular', methods=['POST'])
def postular():
    # Recibir datos del formulario
    nombre = request.form.get('nombre')
    email_user = request.form.get('email')
    telefono = request.form.get('telefono')
    puesto = request.form.get('puesto')
    archivo_cv = request.files.get('cv')

    if not archivo_cv:
        return jsonify({"error": "No se adjuntó ningún archivo CV"}), 400

    # Configurar el correo
    remitente = os.getenv("MAIL_SENDER")
    password = os.getenv("MAIL_PASSWORD")
    destinatario = os.getenv("MAIL_RECEIVER")

    # Verificar que las variables de entorno existan
    if not remitente or not password or not destinatario:
        print("❌ ERROR: Faltan variables de entorno MAIL_SENDER, MAIL_PASSWORD o MAIL_RECEIVER en el archivo .env")
        return jsonify({"error": "Error de configuración en el servidor (Faltan datos de correo)"}), 500

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = f"Nueva Postulación: {puesto} - {nombre}"

    # Cuerpo del correo
    cuerpo = f"""
    Nueva postulación recibida desde el Chatbot de SOLDESP:
    
    Nombre: {nombre}
    Correo del postulante: {email_user}
    Teléfono: {telefono}
    Puesto de interés: {puesto}
    """
    msg.attach(MIMEText(cuerpo, 'plain'))

    # Adjuntar el CV
    try:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(archivo_cv.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{archivo_cv.filename}"')
        msg.attach(part)

        # Enviar por SMTP (usando Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        
        # Imprimimos en consola para confirmar que el envío fue exitoso
        print(f"✅ CORREO ENVIADO EXITOSAMENTE A: {destinatario}")
        
        # Mensaje de éxito que se muestra en la web
        return jsonify({"mensaje": f"¡Postulación enviada con éxito! Tu CV ha llegado a Recursos Humanos. Pronto te contactaremos a {email_user}."})
    
    except smtplib.SMTPAuthenticationError:
        print("❌ ERROR DE AUTENTICACIÓN: La contraseña de Gmail es incorrecta. Recuerda usar una 'Contraseña de Aplicación', NO tu contraseña normal.")
        return jsonify({"error": "Error interno: Contraseña de correo incorrecta. Contacta al administrador."}), 500
    except Exception as e:
        print(f"❌ ERROR AL ENVIAR CORREO: {e}")
        return jsonify({"error": "No se pudo enviar el correo. Intenta más tarde."}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)