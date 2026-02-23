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
    if not all([GUMROAD_TOKEN, ID_INSTANCE, API_TOKEN, CHAT_ID]):
        return "❌ Error: Faltan configurar variables de entorno en Railway."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        radar_trafico = []
        for p in productos:
            if p.get("published"):
                radar_trafico.append({
                    "nombre": p.get("name"),
                    "vistas": p.get("view_count", 0),
                    "ventas": p.get("sales_count", 0)
                })
        
        tendencias = sorted(radar_trafico, key=lambda x: x['vistas'], reverse=True)
        
        count_publicados = sum(1 for p in productos if p.get("published"))
        count_con_renders = sum(1 for p in productos if p.get("thumbnail_url") and p.get("preview_url"))
        perc_renders = (count_con_renders / count_publicados * 100) if count_publicados > 0 else 0

        hoy_str = datetime.now().strftime("%Y-%m-%d")
        ganancia_bruta_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(hoy_str))
        
        msg = f"🚀 *SISTEMA CENTRAL: MISIÓN $10K*\n"
        msg += f"📅 Reporte: {datetime.now().strftime('%d/%m/%Y')}\n"
        msg += "----------------------------------\n\n"
        msg += f"🎨 *ESTADO DE RENDERS (Alberto):*\n"
        msg += f"{generar_barra(perc_renders, 15)}\n\n"
        msg += "🔍 *INVESTIGACIÓN DE TENDENCIAS:*\n"
        for t in tendencias[:3]:
            msg += f" • {t['nombre']}: {t['vistas']} views\n"
        
        if ganancia_bruta_hoy > 0:
            msg += f"\n💰 *GANANCIAS:* ${ganancia_bruta_hoy:,.2f} (T: 65% | A: 35%)\n"
        
        msg += "\n🎯 _Meta: Bucket Hat Tutorial._"
        return msg

    except Exception as e:
        return f"❌ Error de Análisis: {e}"

def enviar_whatsapp(texto):
    # Construcción de la URL
    url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"--- DIAGNÓSTICO DE ENVÍO ---")
        print(f"Estado HTTP: {response.status_code}")
        print(f"Respuesta API: {response.text}")
        print(f"---------------------------")
    except Exception as e:
        print(f"❌ Error crítico en la petición: {e}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
