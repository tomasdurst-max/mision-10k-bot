import os
import requests
import json
from datetime import datetime
import google.generativeai as genai

# --- CONFIGURACIÓN CENTRAL ---
GUMROAD_TOKEN = os.environ.get("GUMROAD_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# Datos de tu Green API
ID_INSTANCE = "7103524728" 
API_TOKEN = "525e960f7e194bd0851a01fe0162e3bc072b90b140614a3ead"
CHAT_ID = "120363406798223965@g.us"

# Configurar IA con paracaídas para errores
genai.configure(api_key=GEMINI_KEY)

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
        count_con_renders = sum(1 for p in productos if p.get("published") and p.get("thumbnail_url"))

        # --- IA CON ESTEROIDES Y FILTROS DESACTIVADOS ---
        vision_ia = ""
        try:
            # Usamos gemini-1.5-flash que es gratuito y veloz en Railway
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt_ia = f"""
            Actúa como un estratega de negocios 3D de élite para la marca de Tomás en Argentina. 
            OBJETIVO: Vender masivamente texturas y assets 3D para llegar a $10,000 USD/mes.

            DATOS:
            - Ventas hoy: ${ganancia_bruta_hoy}
            - Eficiencia de catálogo: {count_con_renders}/{count_publicados} productos con render.

            TAREA:
            1. Dale una orden directa a Alberto sobre qué estética de streetwear (ej: techwear, cyberpunk, minimal) renderizar hoy para reventar Instagram.
            2. Decile a Tomás cómo usar estos datos para escalar con anuncios en Facebook.
            Sé breve, rudo y enfocado en el profit.
            """
            
            # Configuración de seguridad para que la IA no se bloquee al hablar de dinero o ser "agresiva"
            response = model.generate_content(
                prompt_ia,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )
            vision_ia = response.text if response.text else "IA analizando tendencias..."
        except Exception as ia_err:
            vision_ia = f"Cerebro recalculando: La IA detectó mucha potencia y se reinició. Intenta de nuevo."

        # --- REPORTE FINAL ---
        msg = f"🤖 *SISTEMA POTENCIADO: MISIÓN $10K*\n"
        msg += f"📅 {datetime.now().strftime('%d/%m/%Y')} | 09:48 AM\n"
        msg += "----------------------------------\n\n"
        msg += f"💰 *VENTAS HOY:* ${ganancia_bruta_hoy:,.2f}\n"
        msg += f"👤 *Tomás (65%):* ${ganancia_bruta_hoy * 0.65:,.2f}\n"
        msg += f"🎨 *Alberto (35%):* ${ganancia_bruta_hoy * 0.35:,.2f}\n\n"
        
        porcentaje_renders = (count_con_renders / count_publicados * 100) if count_publicados > 0 else 0
        msg += f"🚀 *Renders Ready:* {generar_barra(porcentaje_renders)}\n\n"
        msg += f"🧠 *ESTRATEGIA IA:*\n{vision_ia}\n"
        msg += "\n🎯 _Rumbo a los $10,000 USD._"
        return msg

    except Exception as e:
        return f"❌ Error Crítico: {e}"

def enviar_whatsapp(texto):
    url = f"https://7103.api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    requests.post(url, json=payload)

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
