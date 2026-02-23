import os
import requests
import json
from datetime import datetime
import google.generativeai as genai

# --- CONFIGURACIÓN CENTRAL (Railway inyecta estas llaves) ---
GUMROAD_TOKEN = os.environ.get("GUMROAD_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# Datos de tu Green API
ID_INSTANCE = "7103524728" 
API_TOKEN = "525e960f7e194bd0851a01fe0162e3bc072b90b140614a3ead"
CHAT_ID = "120363406798223965@g.us"

# Configurar Inteligencia Artificial
genai.configure(api_key=GEMINI_KEY)

# CAMBIO CLAVE: Usamos 'gemini-pro' para máxima estabilidad y evitar el error 404
model = genai.GenerativeModel('gemini-pro')

def generar_barra(porcentaje, longitud=10):
    porcentaje = max(0, min(100, porcentaje))
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    try:
        # 1. Recopilación de datos reales de Gumroad
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        ganancia_bruta_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(hoy_str))
        count_publicados = sum(1 for p in productos if p.get("published"))
        count_con_renders = sum(1 for p in productos if p.get("published") and p.get("thumbnail_url") and p.get("preview_url"))

        # --- IA ANALIZANDO TU NEGOCIO CON ESTEROIDES ---
        prompt_ia = f"""
        Sos un estratega de moda 3D de élite enfocado en ventas masivas. 
        Datos actuales del negocio de Tomás:
        - Ventas de hoy: ${ganancia_bruta_hoy}
        - Total productos publicados: {count_publicados}
        - Estado de los renders (calidad visual): {count_con_renders}/{count_publicados} listos.

        TAREA:
        1. Dale una orden táctica agresiva a Alberto sobre qué tipo de renders (streetwear, telas técnicas, etc.) priorizar para Instagram hoy.
        2. Dale un consejo de escalabilidad a Tomás para llegar a los $10,000 USD mensuales usando IA y Facebook/Instagram.
        Hablá con autoridad, directo y enfocado en el dinero.
        """
        
        # Manejo de respuesta de IA para evitar errores de JSON (Expecting value)
        try:
            response = model.generate_content(prompt_ia)
            if response and response.text:
                vision_ia = response.text
            else:
                vision_ia = "La IA está procesando tendencias, el consejo estratégico llegará en el próximo reporte."
        except Exception as ia_err:
            vision_ia = f"Cerebro en mantenimiento: {ia_err}"

        # --- CONSTRUCCIÓN DEL REPORTE ---
        msg = f"🤖 *SISTEMA CENTRAL POTENCIADO: MISIÓN $10K*\n"
        msg += f"📅 Reporte: {datetime.now().strftime('%d/%m/%Y')} | 09:48 AM\n"
        msg += "----------------------------------\n\n"
        msg += f"💰 *GANANCIAS HOY:* ${ganancia_bruta_hoy:,.2f}\n"
        msg += f"👤 *Tomás (65%):* ${ganancia_bruta_hoy * 0.65:,.2f}\n"
        msg += f"🎨 *Alberto (35%):* ${ganancia_bruta_hoy * 0.35:,.2f}\n\n"
        
        porcentaje_renders = (count_con_renders / count_publicados * 100) if count_publicados > 0 else 0
        msg += f"🚀 *Renders Ready:* {generar_barra(porcentaje_renders)}\n\n"
        msg += f"🧠 *ESTRATEGIA IA (Esteroides):*\n{vision_ia}\n"
        msg += "\n🎯 _Meta: $10,000 USD._"
        return msg

    except Exception as e:
        return f"❌ Error de Sistema: {e}"

def enviar_whatsapp(texto):
    url = f"https://7103.api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error enviando WhatsApp: {e}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
