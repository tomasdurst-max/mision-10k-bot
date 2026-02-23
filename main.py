import os
import requests
from google import genai
from google.genai import types # Importante para la nueva configuración
from datetime import datetime

# --- CONFIGURACIÓN DE RAILWAY ---
GUMROAD_TOKEN = os.getenv('GUMROAD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GREEN_ID = os.getenv('GREEN_API_ID')
GREEN_TOKEN = os.getenv('GREEN_API_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

# Inicializar cliente forzando la versión estable v1
client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={'api_version': 'v1'} # ESTO arregla el error 404 de v1beta
)

def auditar_mision_10k():
    print(f"[{datetime.now()}] Iniciando auditoría profesional v2026...")
    
    try:
        # 1. Auditoría Gumroad
        url_gum = f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}"
        res = requests.get(url_gum).json()
        productos = res.get('products', [])
        
        faltantes = [p['name'] for p in productos if not p.get('thumbnail_url')]
        ventas = sum(p.get('sales_count', 0) for p in productos)

        # 2. Estrategia IA (Conexión Estabilizada)
        prompt = f"CEO Streetwear 3D. Analizá: {len(faltantes)} prods sin render. Ventas: {ventas}. Orden táctica para Alberto."
        
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        vision_ia = response.text

        # 3. Formatear Mensaje
        total = len(productos)
        porcentaje = int(((total - len(faltantes)) / total) * 100) if total > 0 else 0
        barras = "■" * (porcentaje // 10) + "□" * (10 - (porcentaje // 10))

        mensaje = (
            f"🚀 *SISTEMA 10K: CONEXIÓN ESTABLE*\n"
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
        print("¡Éxito! Reporte enviado al grupo.")

    except Exception as e:
        print(f"Error detectado: {str(e)}")

if __name__ == "__main__":
    auditar_mision_10k()
