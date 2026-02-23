import requests
import json
from datetime import datetime, timedelta
import os
import random
import traceback

# --- CONFIGURACIÓN DE IDENTIFICADORES ---
ID_INSTANCE = "7103524728"
CHAT_ID = "120363406798223965@g.us"

# --- SEGURIDAD (Cargados en Railway/GitHub) ---
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

# --- PARÁMETROS DE NEGOCIO ---
META_OBJETIVO = 10000.0  # El objetivo de los $10k

def generar_barra(porcentaje, longitud=15):
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def auditoria_mision_10k():
    hoy = datetime.now()
    if hoy.weekday() > 4: return "SKIP: Fin de semana."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Extracción de Datos
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # 2. Análisis de Conversión y Tendencias
        ranking = []
        referidores = {}
        total_ganancia_historica = 0
        ganancia_hoy = 0
        hoy_str = hoy.strftime("%Y-%m-%d")

        for v in ventas_data:
            monto = v.get("price", 0) / 100
            total_ganancia_historica += monto
            if v.get("created_at", "").startswith(hoy_str):
                ganancia_hoy += monto
            
            # Rastrear de dónde viene el tráfico
            ref = v.get("referrer", "Directo/Buscador")
            referidores[ref] = referidores.get(ref, 0) + 1

        for p in productos:
            if p.get("published"):
                vistas = p.get("view_count", 1)
                ventas = p.get("sales_count", 0)
                cvr = (ventas / vistas * 100) if vistas > 0 else 0
                ranking.append({
                    "n": p.get("name"),
                    "v": vistas,
                    "cvr": cvr,
                    "img": p.get("thumbnail_url") and p.get("preview_url")
                })

        # Ordenar por visitas
        ranking = sorted(ranking, key=lambda x: x['v'], reverse=True)
        fuentes_top = sorted(referidores.items(), key=lambda x: x[1], reverse=True)[:2]

        # 3. Auditoría de Tareas (Alberto y Tomás)
        tareas_alberto = [p['n'] for p in ranking if not p['img']]
        tareas_seo = [p['n'] for p in productos if p.get("published") and not p.get("tags")]
        
        # 4. Cálculo de Meta
        progreso_meta = (total_ganancia_historica / META_OBJETIVO) * 100

        # --- CONSTRUCCIÓN DEL DASHBOARD ---
        logro = "🏆 " if ganancia_hoy > 0 else "🚀 "
        msg = f"{logro}*ESTRATEGIA $10K: GROWTH ENGINE*\n"
        msg += f"📅 Reporte: {hoy.strftime('%d/%m/%Y')} | Status: Escalando\n"
        msg += "----------------------------------\n\n"

        # Sección Meta Financiera
        msg += f"🎯 *OBJETIVO FINAL ($10,000):*\n"
        msg += f"{generar_barra(progreso_meta, 20)}\n"
        msg += f"💰 Acumulado: ${total_ganancia_historica:,.2f} / $10,000\n\n"

        # Inteligencia de Mercado
        msg += "📈 *INTELIGENCIA DE VENTAS:*\n"
        for p in ranking[:3]:
            # Marcar productos con alta conversión
            status = "🔥" if p['cvr'] > 5 else "👀"
            msg += f" {status} {p['n']}: {p['v']} views ({p['cvr']:.1f}% Conv.)\n"
        
        if fuentes_top:
            msg += f"\n🌍 *TRÁFICO TOP:* {fuentes_top[0][0]}\n"

        # Plan de Acción Alberto
        msg += f"\n🎨 *ALBERTO (Faltan Renders):*\n"
        if tareas_alberto:
            for t in tareas_alberto[:3]: msg += f" • {t}\n"
        else: msg += " ✅ ¡Catálogo visual al 100%!\n"

        # Plan de Acción Tomás
        msg += f"\n💡 *TOMÁS (SEO & Growth):*\n"
        if tareas_seo:
            msg += f" ⚠️ {len(tareas_seo)} productos sin SEO.\n"
        msg += f" 🧹 {len([p for p in productos if not p.get('published')])} borradores por limpiar.\n"

        # Finanzas del día
        if ganancia_hoy > 0:
            msg += f"\n💰 *REPARTO HOY:* T: ${ganancia_hoy*0.65:,.2f} | A: ${ganancia_hoy*0.35:,.2f}\n"

        msg += "\n🎯 _Acción sugerida: Potenciar el producto con mayor CVR._"
        return msg

    except Exception:
        return f"❌ Error Crítico: {traceback.format_exc()[:150]}"

def enviar_whatsapp(texto):
    if "SKIP" in texto: return
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"Estado HTTP: {r.status_code}")
    except: print("Fallo de red")

if __name__ == "__main__":
    print(auditoria_mision_10k()) # Test local
    enviar_whatsapp(auditoria_mision_10k())
