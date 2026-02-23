import requests
import json
from datetime import datetime
import calendar
import os

# --- CONFIGURACIÓN CENTRAL (EXTRACCIÓN DESDE RAILWAY) ---
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def generar_barra(porcentaje, longitud=10):
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    # Validación: 5 es Sábado, 6 es Domingo
    dia_semana = datetime.now().weekday()
    if dia_semana not in [5, 6]:
        return "SKIP: Hoy no es fin de semana."

    # Verificación de que las variables existen
    if not all([GUMROAD_TOKEN, ID_INSTANCE, API_TOKEN, CHAT_ID]):
        return "❌ Error: Faltan configurar variables de entorno en Railway."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # INVESTIGACIÓN DE TENDENCIAS
        radar_trafico = []
        for p in productos:
            if p.get("published"):
                radar_trafico.append({
                    "nombre": p.get("name"),
                    "vistas": p.get("view_count", 0),
                    "ventas": p.get("sales_count", 0)
                })
        
        tendencias = sorted(radar_trafico, key=lambda x: x['vistas'], reverse=True)
        
        # AUDITORÍA ALBERTO (PROGRESO RENDERS)
        count_publicados = sum(1 for p in productos if p.get("published"))
        count_con_renders = sum(1 for p in productos if p.get("thumbnail_url") and p.get("preview_url"))
        perc_lanzamiento = (count_con_renders / count_publicados * 100) if count_publicados > 0 else 0

        # REPARTO FINANCIERO
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        ganancia_bruta_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(hoy_str))
        
        # MENSAJE DE WHATSAPP
        msg = f"🚀 *OPERACIÓN FIN DE SEMANA: RUTA AL $10K*\n"
        msg += f"📅 {datetime.now().strftime('%d/%m/%Y')} | Enfoque: Tendencias\n"
        msg += "----------------------------------\n\n"

        msg += f"🎨 *PROGRESO RENDERS (Alberto):*\n"
        msg += f"{generar_barra(perc_lanzamiento, 15)}\n"
        if perc_lanzamiento < 100:
            msg += f"💡 _¡Falta poco, Alberto! Solo {count_publicados - count_con_renders} productos más._\n\n"
        else:
            msg += "✅ ¡TODO LISTO PARA EL BUCKET HAT!\n\n"

        msg += "🔍 *INVESTIGACIÓN DE MERCADO:* \n"
        msg += "_Productos con más tracción hoy:_\n"
        for t in tendencias[:3]:
            msg += f" • {t['nombre']} ({t['vistas']} views)\n"

        if ganancia_bruta_hoy > 0:
            msg += f"\n💰 *REPARTO:* Tomás ${ganancia_bruta_hoy*0.65:,.2f} | Alb ${ganancia_bruta_hoy*0.35:,.2f}\n"

        msg += "\n🎯 _Misión: Mantener el ritmo para el lanzamiento del Bucket Hat._"
        return msg

    except Exception as e:
        return f"❌ Error en el análisis: {e}"

def enviar_whatsapp(texto):
    if "SKIP" in texto:
        print(texto)
        return
        
    url = f"https://7103.api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    try:
        requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except Exception as e:
        print(f"Error enviando WhatsApp: {e}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
