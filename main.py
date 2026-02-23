import requests
import json
from datetime import datetime
import os

# --- CONFIGURACIÓN (Podés dejar estos fijos como pediste) ---
ID_INSTANCE = "7103524728" 
CHAT_ID = "120363406798223965@g.us" 

# Estos mejor dejalos como variables de entorno por seguridad
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

def generar_barra(porcentaje, longitud=15):
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    # FILTRO: Lunes (0) a Viernes (4)
    if datetime.now().weekday() > 4:
        return "SKIP: Fin de semana."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # INVESTIGACIÓN Y PROGRESO
        radar = sorted([{"n": p.get("name"), "v": p.get("view_count", 0)} for p in productos if p.get("published")], key=lambda x: x['v'], reverse=True)
        count_p = sum(1 for p in productos if p.get("published"))
        count_r = sum(1 for p in productos if p.get("published") and p.get("thumbnail_url") and p.get("preview_url"))
        
        perc_alberto = (count_r / count_p * 100) if count_p > 0 else 0
        ganancia_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(datetime.now().strftime("%Y-%m-%d")))

        # MENSAJE
        msg = f"🚀 *SISTEMA CENTRAL: MISIÓN $10K*\n"
        msg += f"📅 Reporte: {datetime.now().strftime('%d/%m/%Y')}\n"
        msg += "----------------------------------\n\n"
        msg += f"🎨 *PROGRESS (Alberto):*\n{generar_barra(perc_alberto)}\n\n"
        msg += "🔍 *INVESTIGACIÓN (Tendencias):*\n"
        for p in radar[:3]:
            msg += f" • {p['n']}: {p['v']} visitas\n"
        
        if ganancia_hoy > 0:
            msg += f"\n💰 *REPARTO:* T: ${ganancia_hoy*0.65:,.2f} | A: ${ganancia_hoy*0.35:,.2f}\n"

        msg += "\n🎯 _Meta: Bucket Hat Tutorial._"
        return msg
    except Exception as e:
        return f"❌ Error: {e}"

def enviar_whatsapp(texto):
    if "SKIP" in texto: return
    # URL UNIVERSAL - Si esto da 403, revisá que el API_TOKEN sea correcto en Railway
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    headers = {'Content-Type': 'application/json'}
    payload = {"chatId": CHAT_ID, "message": texto}
    
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Estado: {r.status_code} | Respuesta: {r.text}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
