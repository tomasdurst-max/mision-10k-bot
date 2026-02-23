import os
import requests
from google import genai # Nueva librería estable
from datetime import datetime

# --- CONFIGURACIÓN DE RAILWAY ---
GUMROAD_TOKEN = os.getenv('GUMROAD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GREEN_ID = os.getenv('GREEN_API_ID')
GREEN_TOKEN = os.getenv('GREEN_API_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

# Inicializar cliente de IA (Nueva sintaxis 2026)
client = genai.Client(api_key=GOOGLE_API_KEY)

def auditar_mision_10k():
    print(f"[{datetime.now()}] Iniciando auditoría profesional...")
    
    try:
        # 1. Auditoría Gumroad
        url_gum = f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}"
        res = requests.get(url_gum).json()
        productos = res.get('products', [])
        
        faltantes = [p['name'] for p in productos if not p.get('thumbnail_url')]
        ventas = sum(p.get('sales_count', 0) for p in productos)

        # 2. Estrategia IA (Sin errores 404)
        prompt = f"""
        CEO de Streetwear 3D. Analizá: {len(faltantes)} productos sin render ({', '.join(faltantes)}). 
        Ventas totales: {ventas}. 
        Dale una orden táctica a Alberto para el grupo de WhatsApp para facturar $10k.
        """
        
        # Nueva forma de llamar a Gemini para evitar el error 404
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        vision_ia = response.text

        # 3. Reporte Visual
        total = len(productos)
        porcentaje = int(((total - len(faltantes)) / total) * 100) if total > 0 else 0
        barras = "■" * (porcentaje // 10) + "□" * (10 - (porcentaje // 10))

        mensaje = (
            f"🚀 *SISTEMA 10K: DESPLIEGUE EXITOSO*\n"
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
        print("Misión cumplida: Reporte enviado.")

    except Exception as e:
        print(f"Error crítico: {str(e)}")

if __name__ == "__main__":
    auditar_mision_10k()
