import requests
import json
from datetime import datetime
import os

# --- CONFIGURACIÓN CENTRAL (EXTRACCIÓN DESDE RAILWAY) ---
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def generar_barra(porcentaje, longitud=15):
    """Genera una barra de progreso visual."""
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    """Analiza productos, investiga tendencias y mide el progreso de Alberto."""
    # Validación de Fin de Semana: 5 es Sábado, 6 es Domingo
    dia_semana = datetime.now().weekday()
    if dia_semana not in [5, 6]:
        return "SKIP: Hoy no es fin de semana."

    if not all([GUMROAD_TOKEN, ID_INSTANCE, API_TOKEN, CHAT_ID]):
        return "❌ Error: Faltan configurar variables de entorno en Railway."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Obtención de datos
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # 2. Investigación de lo más visto (Gumroad Deep Dive)
        radar_trafico = []
        count_publicados = 0
        count_con_renders = 0

        for p in productos:
            if p.get("published"):
                count_publicados += 1
                radar_trafico.append({
                    "nombre": p.get("name"),
                    "vistas": p.get("view_count", 0)
                })
                # Check de renders para Alberto (miniatura y preview)
                if p.get("thumbnail_url") and p.get("preview_url"):
                    count_con_renders += 1
        
        # Ordenar por visitas para detectar tendencias
        tendencias = sorted(radar_trafico, key=lambda x: x['vistas'], reverse=True)
        
        # 3. Progreso de Renders (Barra para Alberto)
        perc_renders = (count_con_renders / count_publicados * 100) if count_publicados > 0 else 0

        # 4. Cálculo de Ganancias hoy
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        ganancia_bruta_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(hoy_str))
        
        # --- CONSTRUCCIÓN DEL MENSAJE ---
        msg = f"🚀 *OPERACIÓN FIN DE SEMANA: MISIÓN $10K*\n"
        msg += f"📅 Reporte: {datetime.now().strftime('%d/%m/%Y')}\n"
        msg += "----------------------------------\n\n"

        # Sección Alberto
        msg += f"🎨 *ESTADO DE RENDERS (Alberto):*\n"
        msg += f"{generar_barra(perc_renders)}\n"
        if perc_renders < 100:
            msg += f"💡 _Faltan {count_publicados - count_con_renders} renders para el lanzamiento._\n\n"
        else:
            msg += "✅ ¡Todo listo para el Bucket Hat!\n\n"

        # Sección Investigación
        msg += "🔍 *PRODUCTOS MÁS VISTOS (Tendencias):*\n"
        for t in tendencias[:3]:
            msg += f" • {t['nombre']}: {t['vistas']} visitas\n"
        
        # Sección Financiera
        if ganancia_bruta_hoy > 0:
            msg += f"\n💰 *GANANCIAS:* ${ganancia_bruta_hoy:,.2f}\n"
            msg += f"👤 Tomás (65%): ${ganancia_bruta_hoy*0.65:,.2f}\n"
            msg += f"🎨 Alberto (35%): ${ganancia_bruta_hoy*0.35:,.2f}\n"

        msg += "\n🎯 _Meta: Dominar el mercado 3D._"
        return msg

    except Exception as e:
        return f"❌ Error de Análisis: {e}"

def enviar_whatsapp(texto):
    """Envía el mensaje usando la URL universal corregida."""
    if "SKIP" in texto:
        print(texto)
        return

    # URL optimizada para evitar bloqueos de Nginx (Error 403)
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Estado HTTP: {response.status_code}")
        print(f"Respuesta API: {response.text}")
    except Exception as e:
        print(f"❌ Error en la conexión: {e}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
