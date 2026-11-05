import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)
CORS(app)

# ⚠️ PEGA AQUÍ TU NUEVA CLAVE DE GROQ (empieza con gsk_...)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    mensaje_usuario = data.get('mensaje')
    
    if not mensaje_usuario:
        return jsonify({"error": "No se recibió ningún mensaje"}), 400

    try:
        # Usamos un modelo gratuito de Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Eres el asistente virtual de SOLDESP, empresa peruana de ingeniería y soldadura. "
                        "Nuestra ubicación exacta es: URB. JOSÉ CARLOS MARIÁTEGUI MZ 'M' LT 14, PAMPA INALÁMBRICA, ILO, MOQUEGUA - PERÚ. "
                        "Nuestros servicios son: fabricación metálica, soldaduras especiales, mantenimiento de plantas, arenado y pintura. "
                        "Responde siempre en español, de forma breve, amable y profesional. "
                        "Si el usuario pregunta por la ubicación, dale EXACTAMENTE la dirección que te di arriba. No inventes otras direcciones. "
                        "Si el usuario pide contactarte, hablar con un asesor o pide el número de teléfono, "
                        "DEBES responder incluyendo obligatoriamente este código HTML exacto al final de tu mensaje: "
                        "<br><br><a href='https://wa.me/51953660826' target='_blank' style='display:inline-block; padding:10px 20px; background-color:#ff6b00; color:white; text-decoration:none; border-radius:5px; font-weight:bold;'>Haz clic aquí para ir a WhatsApp</a>"
                    )
                },
                {"role": "user", "content": mensaje_usuario}
            ],
            model="openai/gpt-oss-120b", # Modelo gratuito y potente
        )
        return jsonify({"respuesta": chat_completion.choices[0].message.content})
        
    except Exception as e:
        print(f"ERROR DETECTADO: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)