import os
import requests
import google.generativeai as genai
from datetime import datetime

# --- VARIABLES DE RAILWAY ---
GUMROAD_TOKEN = os.getenv('GUMROAD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GREEN_ID = os.getenv('GREEN_API_ID')
GREEN_TOKEN = os.getenv('GREEN_API_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

# Configuración del motor de IA
genai.configure(api_key=GOOGLE_API_KEY)

def obtener_modelo_seguro():
    # Probamos con los dos modelos más estables
    for nombre_modelo in ['gemini-1.5-pro', 'gemini-1.5-flash']:
        try:
            model = genai.GenerativeModel(nombre_modelo)
            # Prueba rápida de conexión
            model.generate_content("test")
            print(f"Cerebro activado con: {nombre_modelo}")
            return model
        except:
            continue
    return None

def auditar_mision_10k():
    print(f"[{datetime.now()}] Iniciando auditoría de alto nivel...")
    
    try:
        # 1. Auditoría Gumroad
        url_gum = f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}"
        res = requests.get(url_gum).json()
        productos = res.get('products', [])
        
        faltantes = [p['name'] for p in productos if not p.get('thumbnail_url')]
        ventas = sum(p.get('sales_count', 0) for p in productos)

        # 2. IA con Doble Chequeo de Modelo
        brain = obtener_modelo_seguro()
        if not brain:
            vision_ia = "El cerebro de la IA está en modo ahorro. Alberto, revisá los renders manualmente hoy."
        else:
            prompt = f"CEO Streetwear 3D. Analizá: {len(faltantes)} prods sin render. Ventas: {ventas}. Orden táctica para Alberto."
            vision_ia = brain.generate_content(prompt).text

        # 3. Formatear Mensaje
        total = len(productos)
        porcentaje = int(((total - len(faltantes)) / total) * 100) if total > 0 else 0
        barras = "■" * (porcentaje // 10) + "□" * (10 - (porcentaje // 10))

        mensaje = (
            f"🚀 *SISTEMA 10K: CONTROL TOTAL*\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y | %H:%M')}\n"
            f"----------------------------------\n\n"
            f"📊 *Catálogo:* {barras} {porcentaje}%\n"
            f"💰 *Ventas:* {ventas}\n\n"
            f"🧠 *IA STRATEGY:*\n{vision_ia}\n\n"
            f"🎯 _Rumbo a los $10,000 USD._"
        )

        # 4. Enviar a WhatsApp
        url_wa = f"https://api.green-api.com/waInstance{GREEN_ID}/sendMessage/{GREEN_TOKEN}"
        requests.post(url_wa, json={"chatId": GROUP_ID, "message": mensaje})
        print("¡Misión cumplida! Reporte enviado.")

    except Exception as e:
        print(f"Error detectado: {str(e)}")

if __name__ == "__main__":
    auditar_mision_10k()
