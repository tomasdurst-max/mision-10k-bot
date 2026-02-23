import os
import requests
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURACIÓN DE VARIABLES (REGLA DE ORO: NO TOCAR ACÁ, CARGAR EN RAILWAY) ---
GUMROAD_TOKEN = os.getenv('GUMROAD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GREEN_ID = os.getenv('GREEN_API_ID')
GREEN_TOKEN = os.getenv('GREEN_API_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

# Configurar el Cerebro de la IA
genai.configure(api_key=GOOGLE_API_KEY)
# Usamos flash-1.5 que es rápido y potente para análisis de ventas
model = genai.GenerativeModel('gemini-1.5-flash')

def auditar_negocio_10k():
    print(f"[{datetime.now()}] Iniciando auditoría de la Misión $10k...")
    
    try:
        # 1. Obtener productos de Gumroad
        url_gumroad = f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}"
        res = requests.get(url_gumroad)
        data = res.json()
        
        if not data.get('success', True): # Gumroad a veces no manda 'success' pero sí los datos
            productos = data.get('products', [])
        else:
            productos = data.get('products', [])

        # Filtrar los que no tienen render (thumbnail)
        faltantes = [p['name'] for p in productos if not p.get('thumbnail_url')]
        total_ventas = sum(p.get('sales_count', 0) for p in productos)
        
        # 2. El Cerebro analiza y genera la orden para Alberto
        conteo_faltantes = len(faltantes)
        lista_nombres = ", ".join(faltantes) if faltantes else "¡Ninguno! Todo tiene render."
        
        prompt = f"""
        Sos el CEO virtual de la marca de Streetwear 3D de Tomás. 
        Tu objetivo: llegar a $10,000 USD de ganancia mensual.
        
        INFORME DE HOY:
        - Ventas acumuladas: {total_ventas}
        - Productos sin render/miniatura: {conteo_faltantes}
        - Nombres de productos a corregir: {lista_nombres}
        
        TAREA:
        Escribí un mensaje corto y potente para el grupo de WhatsApp donde están Tomás y Alberto.
        1. Decile a Alberto qué renders tiene que priorizar hoy mismo.
        2. Tirá una idea de "esteroides" para vender más (ej. un pack nuevo, un curso en Gumroad, etc.).
        3. Sé directo, motivador y usá emojis de fuego y cohetes.
        """
        
        vision_ia = model.generate_content(prompt).text

        # 3. Formatear el reporte visual
        total_prods = len(productos)
        listos = total_prods - conteo_faltantes
        porcentaje = int((listos / total_prods) * 100) if total_prods > 0 else 0
        barras = "■" * (porcentaje // 10) + "□" * (10 - (porcentaje // 10))

        mensaje_final = (
            f"🚀 *SISTEMA POTENCIADO - MISIÓN $10K*\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y | %H:%M')}\n"
            f"----------------------------------\n\n"
            f"📊 *Progreso de Catálogo:* {barras} {porcentaje}%\n"
            f"📦 *Ventas totales:* {total_ventas}\n\n"
            f"🧠 *ORDEN DE LA IA:*\n{vision_ia}\n\n"
            f"🎯 _Automatización activa. Vamos por esos $10k._"
        )

        # 4. Enviar al Grupo de WhatsApp
        url_wa = f"https://api.green-api.com/waInstance{GREEN_ID}/sendMessage/{GREEN_TOKEN}"
        payload = {
            "chatId": GROUP_ID,
            "message": mensaje_final
        }
        
        response = requests.post(url_wa, json=payload)
        if response.status_code == 200:
            print("Reporte enviado al grupo con éxito.")
        else:
            print(f"Error enviando WhatsApp: {response.text}")

    except Exception as e:
        print(f"Error crítico en el sistema: {str(e)}")

if __name__ == "__main__":
    auditar_negocio_10k()
