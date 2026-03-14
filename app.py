from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
conversaciones = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    numero = request.form.get('From', '')
    mensaje = request.form.get('Body', '').strip()
    if numero not in conversaciones:
        conversaciones[numero] = []
    historial = conversaciones[numero]
    historial.append({'role': 'user', 'parts': [mensaje]})
    if len(historial) > 10:
        historial = historial[-10:]
    chat = model.start_chat(history=historial[:-1])
    respuesta = chat.send_message(mensaje)
    texto = respuesta.text
    historial.append({'role': 'model', 'parts': [texto]})
    conversaciones[numero] = historial
    resp = MessagingResponse()
    resp.message(texto)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  
