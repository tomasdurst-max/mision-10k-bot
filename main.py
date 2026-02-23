import requests
import google.generativeai as genai

# --- PONÉ TUS DATOS ACÁ PARA PROBAR ---
GUMROAD_TOKEN = '-hGka4dRKCM_2MKYdlPhDKGICwC5ImU3lenNx8Fhcow'
GOOGLE_API_KEY = 'AIzaSyDl9-Z0ClK73TXRB9O2ktKaEplSq9DSfiI'
GREEN_ID = '7103524728'
GREEN_TOKEN = '525e960f7e194bd0851a01fe0162e3bc072b90b140614a3ead'

genai.configure(api_key=GOOGLE_API_KEY)
# USAMOS ESTE MODELO QUE ES EL MÁS ESTABLE
model = genai.GenerativeModel('gemini-1.5-flash') 

def probar_y_enviar():
    # 1. IA Piensa
    respuesta = model.generate_content("Saluda a Alberto y decile que el bot ya tiene cerebro nuevo.")
    
    # 2. WhatsApp Envía
    url = f"https://api.green-api.com/waInstance{GREEN_ID}/sendMessage/{GREEN_TOKEN}"
    payload = {"chatId": "5492664933617@c.us", "message": respuesta.text}
    requests.post(url, json=payload)
    print("Mensaje enviado con éxito!")

probar_y_enviar()
