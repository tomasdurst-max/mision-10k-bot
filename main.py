import requests
import google.generativeai as genai
import os
from datetime import datetime

# --- CONFIGURACIÓN (Usa Variables de Entorno en Railway) ---
GUMROAD_TOKEN = os.getenv('GUMROAD_TOKEN')
GREEN_API_ID = os.getenv('GREEN_API_ID')
GREEN_API_TOKEN = os.getenv('GREEN_API_TOKEN')
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER') # 5492664933617
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configurar IA
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def obtener_auditoria_gumroad():
    url = "https://api.gumroad.com/v2/products"
    params = {"access_token": GUMROAD_TOKEN}
    try:
        res = requests.get(url, params=params)
        productos = res.json().get('products', [])
        
        faltantes = []
        info_ia = []
        for p in productos:
            status_foto = "✅ OK" if p['thumbnail_url'] else "❌ FALTA RENDER"
            if not p['thumbnail_url']:
                faltantes.append(p['name'])
            info_ia.append(f"- {p['name']}: {p['sales_count']} ventas, Foto: {status_foto}")
            
        return faltantes, "\n".join(info_ia), len(productos)
    except:
        return [], "Error al conectar con Gumroad", 0

def generar_estrategia_ia(auditoria_texto):
    prompt = f"""
    Actúa como un estratega de negocios para Tomás (dueño) y Alberto (creativo).
    Objetivo: Llegar a $10,000 USD en ventas de Streetwear 3D y Cursos.
    
    Analiza esta auditoría de Gumroad:
    {auditoria_texto}
    
    INSTRUCCIONES:
    1. Si faltan renders, da una orden directa a Alberto de cuáles hacer primero.
    2. Sugiere una acción de marketing basada en los productos con más ventas.
    3. Mantén el tono de "SISTEMA POTENCIADO". Sé breve y agresivo para vender más.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Cerebro recalculando: La IA detectó mucha potencia y se reinició. Error: {str(e)}"

def enviar_reporte():
    faltantes, info_completa, total = obtener_auditoria_gumroad()
    estrategia = generar_estrategia_ia(info_completa)
    
    # Cálculos visuales para el reporte
    porcentaje = int(((total - len(faltantes)) / total) * 100) if total > 0 else 0
    barras = "■" * (porcentaje // 10) + "□" * (10 - (porcentaje // 10))
    
    mensaje = (
        f"🤖 *SISTEMA POTENCIADO: MISIÓN $10K*\n"
        f"📅 Reporte: {datetime.now().strftime('%d/%m/%Y | %H:%M AM')}\n"
        f"----------------------------------\n\n"
        f"🚀 *Renders Ready:* {barras} {porcentaje}%\n\n"
        f"🧠 *ESTRATEGIA IA (Esteroides):*\n{estrategia}\n\n"
        f"🎯 _Rumbo a los $10,000 USD._"
    )
    
    url = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
    payload = {"chatId": f"{WHATSAPP_NUMBER}@c.us", "message": mensaje}
    requests.post(url, json=payload)

if __name__ == "__main__":
    enviar_reporte()
