import requests
import json
from datetime import datetime
import os

# --- CONFIGURACIÓN DESDE RAILWAY ---
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def generar_barra(porcentaje, longitud=15):
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    # FILTRO: Solo corre de Lunes (0) a Viernes (4)
    dia_semana = datetime.now().weekday()
    if dia_semana > 4: 
        return "SKIP: Es fin de semana, el sistema descansa."

    if not all([GUMROAD_TOKEN, ID_INSTANCE, API_TOKEN, CHAT_ID]):
        return "❌ ERROR: Faltan variables de entorno en Railway."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Boot Test: Auditoría de Lanzamiento y Productos
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # 2. Investigación de Tendencias (Lo más visto)
        radar_trafico = []
        count_publicados = 0
        count_con_renders = 0

        for p in productos:
            if p.get("published"):
                count_publicados += 1
                radar_trafico.append({"nombre": p.get("name"), "vistas": p.get("view_count", 0)})
                # Progreso Alberto (Check de Miniatura y Preview)
                if p.get("thumbnail_url") and p.get("preview_url"):
                    count_con_renders += 1
        
        tendencias = sorted(radar_trafico, key=lambda x: x['vistas'], reverse=True)
        
        # 3. Barra de Progreso Alberto
        perc_alberto = (count_con_renders / count_publicados * 100) if count_publicados > 0 else 0

        # 4. Finanzas (Reparto 65/35)
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        ganancia_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(hoy_str))
        
        # --- CONSTRUCCIÓN DEL MENSAJE ---
        msg = f"🚀 *SISTEMA CENTRAL: MISIÓN $10K*\n"
        msg += f"📅 Reporte: {datetime.now().strftime('%d/%m/%Y')}\n"
        msg += "----------------------------------\n\n"

        # Barra Alberto
        msg += f"🎨 *ESTADO DE RENDERS (Alberto):*\n"
        msg += f"{generar_barra(perc_alberto)}\n"
        msg += f"💡 {'Faltan renders para el lanzamiento.' if perc_alberto < 100 else '¡Renders listos!'}\n\n"

        # Investigación Gumroad
        msg += "🔍 *INVESTIGACIÓN DE TENDENCIAS:* \n"
        msg += "_Tus 3 productos más vistos para hoy:_\n"
        for p in tendencias[:3]:
            msg += f" • {p['nombre']} ({p['vistas']} visitas)\n"

        if ganancia_hoy > 0:
            msg += f"\n💰 *REPARTO:* Tomás ${ganancia_hoy*0.65:,.2f} | Alberto ${ganancia_hoy*0.35:,.2f}\n"

        msg += "\n🎯 _Misión: Preparar el Bucket Hat Tutorial._"
        return msg

    except Exception as e:
        return f"❌ Error en el análisis de Gumroad: {e}"

def enviar_whatsapp(texto):
    if "SKIP" in texto:
        print(texto)
        return

    # URL Universal para evitar el error 403
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Estado HTTP: {response.status_code} | {response.text}")
    except Exception as e:
        print(f"Error enviando WhatsApp: {e}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
