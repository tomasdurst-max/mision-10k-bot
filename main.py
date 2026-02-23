import os
import requests
import google.generativeai as genai
from datetime import datetime

# 1. CARGA SEGURA DE VARIABLES (Nombres exactos de tu Railway)
# Usamos .get() para que el bot no "explote" si falta una
GUMROAD_TOKEN = os.getenv('GUMROAD_TOKEN')
IA_KEY = os.getenv('GOOGLE_API_KEY') # Asegurate que en Railway se llame así
GREEN_ID = os.getenv('GREEN_API_ID')
GREEN_TOKEN = os.getenv('GREEN_API_TOKEN')
DESTINO = os.getenv('GROUP_ID')

def ejecutar_auditoria():
    print(f"[{datetime.now()}] --- INICIANDO SISTEMA 10K ---")
    
    # Verificación de seguridad en el log
    if not all([GUMROAD_TOKEN, IA_KEY, GREEN_ID, GREEN_TOKEN, DESTINO]):
        print("❌ ERROR: Faltan variables en Railway. Revisá los nombres.")
        return

    try:
        # 2. AUDITORÍA GUMROAD
        res_gum = requests.get(f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}")
        productos = res_gum.json().get('products', [])
        faltantes = [p['name'] for p in productos if not p.get('thumbnail_url')]
        ventas = sum(p.get('sales_count', 0) for p in productos)

        # 3. CEREBRO IA (Con paracaídas para que no tire error 404)
        try:
            genai.configure(api_key=IA_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"CEO 3D. Analizá: {len(faltantes)} prods sin render. Ventas: {ventas}. Orden para Alberto."
            vision_ia = model.generate_content(prompt).text
        except Exception as e:
            print(f"⚠️ IA en pausa: {e}")
            vision_ia = "Alberto, el cerebro está procesando ventas. Priorizá los renders de hoy."

        # 4. ENVÍO A WHATSAPP
        mensaje = (
            f"🚀 *REPORTE MISIÓN 10K*\n"
            f"📊 Ventas: {ventas} | 📦 Pendientes: {len(faltantes)}\n\n"
            f"🧠 *ORDEN:* {vision_ia}\n\n"
            f"🎯 _Sistema activo._"
        )

        url_wa = f"https://api.green-api.com/waInstance{GREEN_ID}/sendMessage/{GREEN_TOKEN}"
        requests.post(url_wa, json={"chatId": DESTINO, "message": mensaje})
        print("✅ ¡ÉXITO! Reporte enviado a WhatsApp.")

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    ejecutar_auditoria()
