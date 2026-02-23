import requests
import json
from datetime import datetime
import os

# --- CONFIGURACIÓN DE IDENTIFICADORES (Fijos como pediste) ---
ID_INSTANCE = "7103524728" 
CHAT_ID = "120363406798223965@g.us" 

# --- TOKENS DE SEGURIDAD (Desde Variables de Entorno) ---
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

def generar_barra(porcentaje, longitud=15):
    """Genera una barra de progreso visual"""
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    # FILTRO TEMPORAL: Lunes(0) a Viernes(4)
    if datetime.now().weekday() > 4:
        return "SKIP: El sistema descansa los fines de semana."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. BOOT TEST: Recopilación de datos para lanzamiento
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # 2. INVESTIGACIÓN DE MERCADO: Los más vistos
        radar = sorted(
            [{"n": p.get("name"), "v": p.get("view_count", 0)} for p in productos if p.get("published")],
            key=lambda x: x['v'], reverse=True
        )
        
        # 3. PROGRESO DE ALBERTO (Check de renders)
        count_p = sum(1 for p in productos if p.get("published"))
        count_r = sum(1 for p in productos if p.get("published") and p.get("thumbnail_url") and p.get("preview_url"))
        perc_alberto = (count_r / count_p * 100) if count_p > 0 else 0

        # 4. FINANZAS: Split 65/35
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        ganancia_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(hoy_str))
        
        # --- CÁLCULOS MATEMÁTICOS ---
        # Ganancia Tomás: $$G_T = G_{total} \times 0.65$$
        # Ganancia Alberto: $$G_A = G_{total} \times 0.35$$

        # --- CONSTRUCCIÓN DEL MENSAJE ---
        msg = f"🚀 *SISTEMA CENTRAL: MISIÓN $10K*\n"
        msg += f"📅 {datetime.now().strftime('%d/%m/%Y')} | Lunes-Viernes\n"
        msg += "----------------------------------\n\n"

        # Barra Alberto
        msg += f"🎨 *PROGRESO ALBERTO (Renders):*\n"
        msg += f"{generar_barra(perc_alberto)}\n"
        msg += f"💡 {'¡Falta poco Alberto!' if perc_alberto < 100 else '¡Renders listos para el Bucket Hat!'}\n\n"

        # Investigación Gumroad
        msg += "🔍 *INVESTIGACIÓN DE TENDENCIAS:* \n"
        msg += "_Top 3 productos más vistos para hoy:_\n"
        for p in radar[:3]:
            msg += f" • {p['n']} ({p['v']} visitas)\n"

        # Reparto
        if ganancia_hoy > 0:
            msg += f"\n💰 *REPARTO:* Tomás ${ganancia_hoy*0.65:,.2f} | Alb ${ganancia_hoy*0.35:,.2f}\n"
        else:
            msg += "\n📈 *Status:* Sin ventas hoy. Monitoreando tráfico...\n"

        msg += "\n🎯 _Misión: Barras al 100% para soltar el Bucket Hat._"
        return msg

    except Exception as e:
        return f"❌ Error en el análisis: {e}"

def enviar_whatsapp(texto):
    if "SKIP" in texto: return
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    headers = {'Content-Type': 'application/json'}
    
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Estado: {r.status_code} | Respuesta: {r.text}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
