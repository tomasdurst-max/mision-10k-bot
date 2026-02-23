import os
import requests
import google.generativeai as genai
from datetime import datetime

# --- CARGA DE VARIABLES ---
GUMROAD_TOKEN = os.getenv('GUMROAD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GREEN_ID = os.getenv('GREEN_API_ID')
GREEN_TOKEN = os.getenv('GREEN_API_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

# Configurar IA
genai.configure(api_key=GOOGLE_API_KEY)

def ejecutar_auditoria():
    print(f"[{datetime.now()}] Iniciando...")
    try:
        # 1. Obtener datos de Gumroad
        res_gum = requests.get(f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}")
        productos = res_gum.json().get('products', [])
        
        faltantes = [p['name'] for p in productos if not p.get('thumbnail_url')]
        ventas = sum(p.get('sales_count', 0) for p in productos)

        # 2. Intentar usar la IA (con paracaídas)
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"CEO 3D. Analizá: {len(faltantes)} productos sin render. Ventas: {ventas}. Dale una orden rápida a Alberto."
            vision_ia = model.generate_content(prompt).text
        except Exception as e:
            print(f"Error en IA: {e}")
            vision_ia = "IA en mantenimiento. Alberto, priorizá los renders faltantes hoy."

        # 3. Formatear Mensaje
        msg = (
            f"🚀 *REPORTE MISIÓN 10K*\n"
            f"📊 Ventas: {ventas} | 📦 Pendientes: {len(faltantes)}\n\n"
            f"🧠 *ORDEN:* {vision_ia}\n\n"
            f"🎯 _Sistema activo._"
        )

        # 4. Enviar a WhatsApp
        url_wa = f"https://api.green-api.com/waInstance{GREEN_ID}/sendMessage/{GREEN_TOKEN}"
        requests.post(url_wa, json={"chatId": GROUP_ID, "message": msg})
        print("¡Reporte enviado!")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    ejecutar_auditoria()
