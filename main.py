import requests
import json
from datetime import datetime, timedelta
import os
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
        p_req = requests.get("https://api.gumroad.com/v2/products", headers=headers, timeout=15)
        s_req = requests.get("https://api.gumroad.com/v2/sales", headers=headers, timeout=15)
        
        if p_req.status_code != 200:
            return f"❌ Error Gumroad (Status {p_req.status_code})"
        
        productos = p_req.json().get("products", [])
        ventas_data = s_req.json().get("sales", [])
        
        ranking = sorted(
            [{"n": p.get("name", "S/N"), "v": p.get("view_count", 0)} for p in productos if p.get("published")],
            key=lambda x: x['v'], reverse=True
        )
        
        con_renders = [p.get("name") for p in productos if p.get("published") and p.get("thumbnail_url")]
        tareas_alb = [p.get("name") for p in productos if p.get("published") and not p.get("thumbnail_url")]
        tareas_tomas_nombres = [p.get("name") for p in productos if p.get("published") and not p.get("tags")]
        borradores = [p.get("name") for p in productos if not p.get("published")]

        puntos_max = len(productos) * 3 if productos else 1
        puntos_hoy = sum(1 for p in productos if p.get("published")) + len(con_renders)
        salud = (puntos_hoy / puntos_max * 100)

        ganancia_hoy = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(hoy.strftime("%Y-%m-%d")))
        ganancia_ayer = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(ayer.strftime("%Y-%m-%d")))

        # --- CONSTRUCCIÓN DEL MENSAJE (Línea 80 Reparada) ---
        msg = f"🚀 *SISTEMA CENTRAL: ESTRATEGIA $10K*\n"
        msg += f"📅 {hoy.strftime('%d/%m/%Y')} | Escaneo Completo\n"
        msg += "----------------------------------\n\n"
        msg += f"📊 *SALUD DE LA TIENDA:* \n{generar_barra(salud)}\n\n"
        msg += "🔍 *TOP TENDENCIAS:*\n"
        for p in ranking[:3]:
            msg += f" • {p['n']} ({p['v']} visitas)\n"
        
        msg += f"\n🔄 *COMPARATIVA 24H:*\n • Hoy: ${ganancia_hoy:,.2f}\n • Ayer: ${ganancia_ayer:,.2f}\n"

        msg += f"\n🎨 *ALBERTO (Renders):* {len(con_renders)}/{len(productos)}\n"
        if tareas_alb:
            msg += " ⚠️ Pendientes: " + ", ".join(tareas_alb[:2]) + "\n"

        msg += f"\n💡 *TOMÁS (SEO):*\n"
        if tareas_tomas_nombres:
            msg += " ❌ Sin Tags en: " + ", ".join
