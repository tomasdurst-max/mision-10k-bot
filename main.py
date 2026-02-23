import os
import requests
import google.generativeai as genai
from datetime import datetime

# --- CARGA FORZADA ---
# Usamos nombres genéricos para que no haya error de 'name not defined'
G_TOKEN = os.getenv('GUMROAD_TOKEN')
G_KEY = os.getenv('GOOGLE_API_KEY')
GR_ID = os.getenv('GREEN_API_ID')
GR_TOKEN = os.getenv('GREEN_API_TOKEN')
# TU NÚMERO (El que ya probaste que funciona en el panel)
DESTINO = "5491156063862@c.us" 

def enviar_whatsapp(txt):
    url = f"https://api.green-api.com/waInstance{GR_ID}/sendMessage/{GR_TOKEN}"
    payload = {"chatId": DESTINO, "message": txt}
    r = requests.post(url, json=payload)
    return r.status_code

def auditar():
    print("--- INICIANDO TEST ---")
    
    # Test 1: ¿Llegan las variables de Railway?
    if not all([G_TOKEN, G_KEY, GR_ID, GR_TOKEN]):
        error_msg = f"❌ Error: Faltan variables en Railway. G_KEY: {bool(G_KEY)}"
        print(error_msg)
        enviar_whatsapp(error_msg)
        return

    try:
        # Test 2: Gumroad
        res = requests.get(f"https://api.gumroad.com/v2/products?access_token={G_TOKEN}").json()
        prods = res.get('products', [])
        ventas = sum(p.get('sales_count', 0) for p in prods)

        # Test 3: IA (Si falla, mandamos el reporte igual)
        try:
            genai.configure(api_key=G_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            orden = model.generate_content("Dame una orden corta para mi socio Alberto para vender más.").text
        except:
            orden = "Alberto, el cerebro de la IA está procesando. Revisá los renders hoy."

        # ENVÍO FINAL
        mensaje = f"🚀 *REPORTE BOT RAILWAY*\n💰 Ventas: {ventas}\n🧠 *IA:* {orden}"
        status = enviar_whatsapp(mensaje)
        print(f"Resultado envío: {status}")

    except Exception as e:
        enviar_whatsapp(f"❌ Error en el código: {str(e)}")

if __name__ == "__main__":
    auditar()
