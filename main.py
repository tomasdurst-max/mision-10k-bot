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

def obtener_mensaje_motivador():
    mensajes = [
        "🚀 ¡Hoy es un gran día para subir otro render, Alberto!",
        "📈 Tomás, el SEO de hoy es la venta de mañana. ¡Metele!",
        "🎯 Cada día estamos más cerca de los $10K. ¡No aflojen!",
        "🔥 El mercado 3D no duerme, ¡nosotros tampoco!",
        "✨ ¡Misión Bucket Hat en marcha! Revisen los borradores hoy."
    ]
    return random.choice(mensajes)

def auditoria_mision_10k():
    hoy = datetime.now()
    ayer = hoy - timedelta(days=1)
    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Llamada a la API
        p_req = requests.get("https://api.gumroad.com/v2/products", headers=headers)
        s_req = requests.get("https://api.gumroad.com/v2/sales", headers=headers)
        
        if p_req.status_code != 200:
            return f"❌ Error API Gumroad: {p_req.status_code}"

        productos = p_req.json().get("products", [])
        ventas_data = s_req.json().get("sales", [])
        
        # 2. Investigación de Tendencias
        ranking = sorted([{"n": p.get("name", "S/N"), "v": p.get("view_count", 0)} for p in productos if p.get("published")], key=lambda x: x['v'], reverse=True)
        
        # 3. Auditoría de Tareas (Alberto/Tomás)
        tareas_alb = [p.get("name") for p in productos if p.get("published") and (not p.get("thumbnail_url") or not p.get("preview_url"))]
        tareas_tomas = [p.get("name") for p in productos if p.get("published") and not p.get("tags")]
        borradores = [p.get("name") for p in productos if not p.get("published")]

        # 4. Cálculo de Salud
        puntos_max = len(productos) * 3
        puntos_hoy = sum(1 for p in productos if p.get("published"))
        puntos_hoy += sum(1 for p in productos if p.get("published") and p.get("thumbnail_url") and p.get("preview_url"))
        puntos_hoy += sum(1 for p in productos if p.get("published") and p.get("tags"))
        salud = (puntos_hoy / puntos_max * 100) if puntos_max > 0 else 0

        # --- LÓGICA COMPARATIVA (24h vs 48h) ---
        hoy_str = hoy.strftime("%Y-%m-%d")
        ayer_str = ayer.strftime("%Y-%m-%d")
        
        ganancia_hoy = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(hoy_str))
        ganancia_ayer = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(ayer_str))
        
        # Comparación visual
        if ganancia_hoy > ganancia_ayer:
            tendencia = "📈 ¡Superamos lo de ayer!"
        elif ganancia_hoy < ganancia_ayer and ganancia_ayer > 0:
            tendencia = "📉 Un poco más tranquilos que ayer."
        else:
            tendencia = "⚖️ Manteniendo el ritmo."

        # --- CONSTRUCCIÓN DEL MENSAJE ---
        icono = "🏆 " if (ranking and ranking[0]['v'] > 1000) else "🚀 "
        msg = f"{icono}*SISTEMA CENTRAL: ESTRATEGIA $10K*\n"
        msg += f"📅 {hoy.strftime('%d/%m/%Y')} | Reporte Diario\n"
        msg += "----------------------------------\n\n"

        msg += f"📊 *SALUD DE LA TIENDA:* \n{generar_barra(salud)}\n\n"

        # SECCIÓN COMPARATIVA
        msg += f"🔄 *COMPARATIVA 24H:*\n"
        msg += f" • Hoy: ${ganancia_hoy:,.2f}\n"
        msg += f" • Ayer: ${ganancia_ayer:,.2f}\n"
        msg += f" *Result:* {tendencia}\n\n"

        msg += "🔍 *TOP 3 TENDENCIAS:* \n"
        for i, p in enumerate(ranking[:3]):
            emoji = "🔥" if i == 0 else "•"
            msg += f" {emoji} {p['n']} ({p['v']} visitas)\n"

        msg += f"\n🎨 *ALBERTO (Renders):*\n"
        msg += f" • {tareas_alb[0]}\n" if tareas_alb else " ✅ ¡Renders listos!\n"
        
        msg += f"\n💡 *TOMÁS (SEO/Limpieza):*\n"
        msg += f" ⚠️ {len(tareas_tomas)} sin Tags | 🧹 {len(borradores)} borradores.\n"

        if ganancia_hoy > 0:
            msg += f"\n💰 *REPARTO HOY:* T: ${ganancia_hoy*0.65:,.2f} | A: ${ganancia_hoy*0.35:,.2f}\n"

        msg += f"\n✨ *NOTAS:*\n{obtener_mensaje_motivador()}"
        return msg

    except Exception:
        return f"❌ Error Crítico:\n{traceback.format_exc()[:150]}"

def enviar_whatsapp(texto):
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    try:
        r = requests.post(url, json={"chatId": CHAT_ID, "message": texto}, timeout=10)
        print(f"Estado HTTP: {r.status_code}")
    except:
        print("Error de conexión.")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
