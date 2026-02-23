import requests
import json
from datetime import datetime, timedelta
import os
import random
import traceback

# --- CONFIGURACIÓN CENTRAL ---
ID_INSTANCE = "7103524728"
CHAT_ID = "120363406798223965@g.us"
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

def generar_barra(porcentaje, longitud=15):
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    hoy = datetime.now()
    ayer = hoy - timedelta(days=1)
    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Llamadas a la API con verificación de integridad
        p_req = requests.get("https://api.gumroad.com/v2/products", headers=headers, timeout=15)
        s_req = requests.get("https://api.gumroad.com/v2/sales", headers=headers, timeout=15)
        
        # Validación de respuesta JSON
        if p_req.status_code != 200:
            return f"❌ Error Gumroad (Status {p_req.status_code}): El Token podría estar vencido o la API caída."
        
        try:
            productos_data = p_req.json()
            ventas_data_raw = s_req.json()
        except Exception:
            return "❌ Error: Gumroad no envió datos válidos. Reintenta en unos minutos."

        productos = productos_data.get("products", [])
        ventas_data = ventas_data_raw.get("sales", [])
        
        # 2. Investigación de Tendencias
        ranking = sorted([{"n": p.get("name", "S/N"), "v": p.get("view_count", 0)} for p in productos if p.get("published")], key=lambda x: x['v'], reverse=True)
        
        # 3. Auditoría Alberto (Check de al menos 5 thumbnails)
        con_renders = [p.get("name") for p in productos if p.get("published") and p.get("thumbnail_url") and p.get("preview_url")]
        tareas_alb = [p.get("name") for p in productos if p.get("published") and (not p.get("thumbnail_url") or not p.get("preview_url"))]
        
        # 4. Auditoría Tomás (SEO y Limpieza)
        tareas_tomas = [p.get("name") for p in productos if p.get("published") and not p.get("tags")]
        borradores = [p.get("name") for p in productos if not p.get("published")]

        # 5. Cálculo de Salud y Finanzas
        puntos_max = len(productos) * 3
        puntos_hoy = sum(1 for p in productos if p.get("published")) + len(con_renders) + sum(1 for p in productos if p.get("published") and p.get("tags"))
        salud = (puntos_hoy / puntos_max * 100) if puntos_max > 0 else 0

        ganancia_hoy = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(hoy.strftime("%Y-%m-%d")))
        ganancia_ayer = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(ayer.strftime("%Y-%m-%d")))

        # --- CONSTRUCCIÓN DEL MENSAJE ---
        msg = f"🚀 *SISTEMA CENTRAL: ESTRATEGIA $10K*\n"
        msg += f"📅 {hoy.strftime('%d/%m/%Y')} | Reporte de Control\n"
        msg += "----------------------------------\n\n"

        msg += f"📊 *SALUD DE LA TIENDA:* \n{generar_barra(salud)}\n\n"

        msg += f"🔄 *COMPARATIVA 24H:*\n"
        msg += f" • Hoy: ${ganancia_hoy:,.2f}\n"
        msg += f" • Ayer: ${ganancia_ayer:,.2f}\n\n"

        # SECCIÓN ALBERTO: Foco en los 5 thumbnails
        msg += f"🎨 *ALBERTO (Check de Renders):*\n"
        msg += f" ✅ Renders OK: {len(con_renders)}/5\n"
        
        if tareas_alb:
            msg += f" ⚠️ *Pendientes (Próximos 5):*\n"
            for t in tareas_alb[:5]:
                msg += f" • {t}\n"
        else:
            msg += " ⭐ ¡Todo el catálogo tiene renders pro!\n"

        # SECCIÓN TOMÁS
        msg += f"\n💡 *TOMÁS (SEO & Limpieza):*\n"
        msg += f" ⚠️ {len(tareas_tomas)} sin Tags | 🧹 {len(borradores)} borradores.\n"

        if ganancia_hoy > 0:
            msg += f"\n💰 *REPARTO:* T (65%): ${ganancia_hoy*0.65:,.2f} | A (35%): ${ganancia_hoy*0.35:,.2f}\n"

        msg += "\n🎯 _Misión: Subir los 5 thumbnails para el Bucket Hat._"
        return msg

    except Exception:
        return f"❌ Error Crítico de Conexión:\n{traceback.format_exc()[:150]}"

def enviar_whatsapp(texto):
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    try:
        requests.post(url, json={"chatId": CHAT_ID, "message": texto}, timeout=10)
    except:
        pass

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
