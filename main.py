import requests
import json
from datetime import datetime
import os

# --- CONFIGURACIÓN CENTRAL (VÍA RAILWAY) ---
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def generar_barra(porcentaje, longitud=10):
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    # Eliminamos la restricción de fin de semana para que funcione SIEMPRE
    if not all([GUMROAD_TOKEN, ID_INSTANCE, API_TOKEN, CHAT_ID]):
        return "❌ Error: Faltan configurar variables de entorno en Railway."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Recopilación de datos
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # 2. Investigación de Tendencias (Lo más visto)
        radar_trafico = []
        for p in productos:
            if p.get("published"):
                radar_trafico.append({
                    "nombre": p.get("name"),
                    "vistas": p.get("view_count", 0),
                    "ventas": p.get("sales_count", 0)
                })
        
        tendencias = sorted(radar_trafico, key=lambda x: x['vistas'], reverse=True)
        
        # 3. Auditoría de Renders (Alberto)
        count_publicados = sum(1 for p in productos if p.get("published"))
        count_con_renders = sum(1 for p in productos if p.get("thumbnail_url") and p.get("preview_url"))
        perc_renders = (count_con_renders / count_publicados * 100) if count_publicados > 0 else 0

        # 4. Cálculo de Ventas hoy
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        ganancia_bruta_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(hoy_str))
        
        # --- CONSTRUCCIÓN DEL MENSAJE ---
        msg = f"🚀 *SISTEMA CENTRAL: MISIÓN $10K*\n"
        msg += f"📅 Reporte Diario: {datetime.now().strftime('%d/%m/%Y')}\n"
        msg += "----------------------------------\n\n"

        # Barra de Alberto
        msg += f"🎨 *ESTADO DE RENDERS (Alberto):*\n"
        msg += f"{generar_barra(perc_renders, 15)}\n"
        if perc_renders < 100:
            msg += f"💡 _Faltan {count_publicados - count_con_renders} productos para el 100%._\n\n"
        else:
            msg += "✅ ¡Renders completados al 100%!\n\n"

        # Radar de Tráfico
        msg += "🔍 *PRODUCTOS MÁS VISTOS (Investigación):*\n"
        for t in tendencias[:3]:
            msg += f" • {t['nombre']}: {t['vistas']} views\n"
        
        msg += "\n📈 *Estrategia:* Enfocar marketing en estos 3.\n\n"

        # Finanzas
        if ganancia_bruta_hoy > 0:
            msg += f"💰 *GANANCIAS HOY:* ${ganancia_bruta_hoy:,.2f}\n"
            msg += f"👤 Tomás (65%): ${ganancia_bruta_hoy*0.65:,.2f}\n"
            msg += f"🎨 Alberto (35%): ${ganancia_bruta_hoy*0.35:,.2f}\n"
        else:
            msg += "😴 *Ventas:* Sin novedades hoy. ¡A seguir moviendo tráfico!\n"

        msg += "\n🎯 _Meta: Bucket Hat Tutorial._"
        return msg

    except Exception as e:
        return f"❌ Error de Análisis: {e}"

def enviar_whatsapp(texto):
    url = f"https://7103.api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Estado del envío: {response.status_code}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
