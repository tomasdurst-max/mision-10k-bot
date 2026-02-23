import os
import requests
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURACIÓN (Cargar en Railway > Variables) ---
GUMROAD_TOKEN = os.getenv('GUMROAD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GREEN_ID = os.getenv('GREEN_API_ID')
GREEN_TOKEN = os.getenv('GREEN_API_TOKEN')
ALBERTO_WA = "5492664933617@c.us" 

# Configurar Cerebro IA
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def auditar_negocio():
    # 1. Obtener productos de Gumroad
    res = requests.get(f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}")
    productos = res.json().get('products', [])
    
    faltantes = [p['name'] for p in productos if not p['thumbnail_url']]
    ventas_totales = sum(p['sales_count'] for p in productos)
    
    # 2. IA genera Estrategia
    contexto = f"Productos sin render: {faltantes}. Ventas totales: {ventas_totales}."
    prompt = f"Eres un CEO de Streetwear 3D. Analiza esto: {contexto}. Dile a Alberto qué renders URGEN para llegar a $10k USD."
    
    try:
        estrategia = model.generate_content(prompt).text
    except:
        estrategia = "IA recalculando... la potencia es demasiada. Intenta de nuevo."

    # 3. Formatear y enviar reporte
    porcentaje = int(((len(productos) - len(faltantes)) / len(productos)) * 100)
    barras = "■" * (porcentaje // 10) + "□" * (10 - (porcentaje // 10))
    
    msg = (
        f"🤖 *SISTEMA POTENCIADO: MISIÓN $10K*\n"
        f"📅 {datetime.now().strftime('%d/%m/%Y | %H:%M AM')}\n"
        f"----------------------------------\n\n"
        f"🚀 *Renders Ready:* {barras} {porcentaje}%\n"
        f"🧠 *ESTRATEGIA IA:*\n{estrategia}\n\n"
        f"🎯 _Rumbo a los $10,000 USD._"
    )
    
    requests.post(f"https://api.green-api.com/waInstance{GREEN_ID}/sendMessage/{GREEN_TOKEN}", 
                  json={"chatId": ALBERTO_WA, "message": msg})

if __name__ == "__main__":
    auditar_negocio()
