import requests
import json
from datetime import datetime, timedelta
import os
import random
import traceback

# --- CONFIGURACIÓN CENTRAL (Seguridad Railway) ---
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
        # 1. ESCANEO TOTAL: Llamada a la API
        p_req = requests.get("https://api.gumroad.com/v2/products", headers=headers, timeout=15)
        s_req = requests.get("https://api.gumroad.com/v2/sales", headers=headers, timeout=15)
        
        if p_req.status_code != 200:
            return f"❌ Error Gumroad (Status {p_req.status_code}): El Token podría estar vencido."
        
        productos = p_req.json().get("products", [])
        ventas_data = s_req.json().get("sales", [])
        
        if not productos:
            return "⚠️ El escaneo se completó pero no hay productos en la cuenta."

        # 2. INVESTIGACIÓN DE MERCADO (Top 3 Más Vistos)
        ranking = sorted(
            [{"n": p.get("name", "S/N"), "v": p.get("view_count", 0)} for p in productos if p.get("published")],
            key=lambda x: x['v'], reverse=True
        )
        
        # 3. AUDITORÍA ALBERTO (Check de renders)
        con_renders = [p.get("name") for p in productos if p.get("published") and p.get("thumbnail_url") and p.get("preview_url")]
        tareas_alb = [p.get("name") for p in productos if p.get("published") and (not p.get("thumbnail_url") or not p.get("preview_url"))]
        
        # 4. AUDITORÍA TOMÁS (SEO y Limpieza - ACTUALIZADA)
        # Guardamos los nombres específicos de los productos sin tags
        tareas_tomas_nombres = [p.get("name") for p in productos if p.get("published") and not p.get("tags")]
        borradores = [p.get("name") for p in productos if not p.get("published")]

        # 5. CÁLCULO DE SALUD Y FINANZAS
        puntos_max = len(productos) * 3
        puntos_hoy = sum(1 for p in productos if p.get("published")) + len(con_renders) + (len(productos) - len(tareas_tomas_nombres))
        salud = (puntos_hoy / puntos_max * 100) if puntos_max > 0 else 0

        hoy_str = hoy.strftime("%Y-%m-%d")
        ayer_str = ayer.strftime("%Y-%m-%d")
        ganancia_hoy = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(hoy_str))
        ganancia_ayer = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(ayer_str))

        # --- CONSTRUCCIÓN DEL MENSAJE ---
        icono_inicio = "🏆 " if (ranking and ranking[0]['v'] > 1000) else "🚀 "
        msg = f"{icono_inicio}*SISTEMA CENTRAL: ESTRATEGIA $10K*\n"
        msg += f"📅 {hoy.strftime('%d/%m/%Y')} | Escaneo Completo\n"
        msg += "----------------------------------\n\n"

        msg += f"📊 *SALUD DE LA TIENDA:* \n{generar_barra(salud)}\n\n"

        # SECCIÓN INVESTIGACIÓN (TOP 3)
        msg += "🔍 *INVESTIGACIÓN: TOP 3 TENDENCIAS*\n"
        for i, p in enumerate(ranking[:3]):
            emoji = "🏆" if i == 0 else "🔥"
            msg += f" {emoji} {p['n']} ({p['v']} visitas)\n"
        msg += "\n"

        # SECCIÓN COMPARATIVA
        msg += f"🔄 *COMPARATIVA 24H:*\n"
        msg += f" •
