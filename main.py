import requests
import json
from datetime import datetime
import os
import random
import traceback

# --- CONFIGURACIÓN DE IDENTIFICADORES (Fijos) ---
ID_INSTANCE = "7103524728"
CHAT_ID = "120363406798223965@g.us"

# --- SEGURIDAD (Desde Variables de Entorno) ---
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

def generar_barra(porcentaje, longitud=15):
    """Genera la barra visual de progreso."""
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def obtener_mensaje_viernes():
    """Mensaje de cierre único para cada viernes."""
    mensajes = [
        "🍻 ¡Se terminó la semana, cracks! Alberto, soltá el mouse. Tomás, apagá el SEO. ¡A disfrutar!",
        "🍕 ¡Viernes! La tienda queda en piloto automático. Gran laburo, el $10K está cerca.",
        "🎮 Misión cumplida. Desconecten para volver el lunes con ojos nuevos. ¡Felicidades!",
        "🚀 ¡Viernes de descontrol! El Bucket Hat ya casi es una realidad. ¡Disfruten el descanso!",
        "✨ ¡Semana liquidada con éxito! Que tengan un finde de película. ¡Nos vemos el lunes!"
    ]
    semana_actual = datetime.now().isocalendar()[1]
    return mensajes[semana_actual % len(mensajes)]

def auditoria_mision_10k():
    hoy = datetime.now()
    es_viernes = hoy.weekday() == 4
    
    # Filtro: Solo de Lunes (0) a Viernes (4)
    if hoy.weekday() > 4:
        return "SKIP: El sistema descansa el fin de semana."

    if not all([GUMROAD_TOKEN, API_TOKEN]):
        return "❌ ERROR: Faltan los Tokens en Railway (GUMROAD_TOKEN o API_TOKEN)."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Llamada a la API
        p_req = requests.get("https://api.gumroad.com/v2/products", headers=headers)
        s_req = requests.get("https://api.gumroad.com/v2/sales", headers=headers)
        
        if p_req.status_code != 200:
            return f"❌ Error API Gumroad: {p_req.status_code}. Revisá el GUMROAD_TOKEN."

        productos = p_req.json().get("products", [])
        ventas_data = s_req.json().get("sales", [])
        
        # 2. Investigación de Tendencias
        ranking = sorted(
            [{"nombre": p.get("name", "S/N"), "vistas": p.get("view_count", 0)} for p in productos if p.get("published")],
            key=lambda x: x['vistas'], reverse=True
        )
        
        # 3. Auditoría de Tareas (Limpieza Automática)
        tareas_alberto = []
        tareas_tomas_seo = []
        borradores_tomas = []
        puntos_totales = 0
        puntos_logrados = 0

        for p in productos:
            name = p.get("name", "Producto sin nombre")
            puntos_totales += 3 
            
            if p.get("published"):
                puntos_logrados += 1
                # Check Renders (Alberto)
                if not p.get("thumbnail_url") or not p.get("preview_url"):
                    tareas_alberto.append(name)
                else:
                    puntos_logrados += 1
                
                # Check Tags (Tomás)
                if not p.get("tags"):
                    tareas_tomas_seo.append(name)
                else:
                    puntos_logrados += 1
            else:
                borradores_tomas.append(name)

        salud_tienda = (puntos_logrados / puntos_totales * 100) if puntos_totales > 0 else 0
        ganancia_hoy = sum(v.get("price", 0) / 100 for v in ventas_data if v.get("created_at", "").startswith(hoy.strftime("%Y-%m-%d")))

        # --- RADAR VIRAL ---
        vistas_lista = [p['vistas'] for p in ranking]
        promedio = sum(vistas_lista) / len(vistas_lista) if vistas_lista else 0
        viral = ranking[0] if ranking and ranking[0]['vistas'] > (promedio * 2) and ranking[0]['vistas'] > 50 else None

        # --- CONSTRUCCIÓN DEL MENSAJE ---
        icono_inicio = "🏆 " if (ranking and ranking[0]['vistas'] > 1000) else "🚀 "
        msg = f"{icono_inicio}*SISTEMA CENTRAL: ESTRATEGIA $10K*\n"
        msg += f"📅 {hoy.strftime('%d/%m/%Y')} | {'🔥 MODO VIERNES' if es_viernes else 'Status: Activo'}\n"
        msg += "----------------------------------\n\n"

        msg += f"📊 *SALUD DE LA TIENDA:* \n{generar_barra(salud_tienda)}\n"
        msg += "_Al llegar al 100%, soltamos el Bucket Hat._\n\n"

        if viral:
            msg += f"⚡ *RADAR VIRAL:* ¡{viral['nombre']}! tiene {viral['vistas']} visitas. ¡Aprovechen el hype hoy!\n\n"

        msg += "🔍 *TOP 3 TENDENCIAS:* \n"
        for i, p in enumerate(ranking[:3]):
            emoji = "🏆" if i == 0 and p['vistas'] > 1000 else "🔥" if i == 0 else "•"
            msg += f" {emoji} {p['nombre']} ({p['vistas']} visitas)\n"

        msg += f"\n🎨 *ALBERTO (Renders Pendientes):*\n"
        if tareas_alberto:
            for t in tareas_alberto[:3]: msg += f" • {t}\n"
        else:
            msg += " ✅ ¡Todos los renders terminados!\n"

        msg += f"\n💡 *TOMÁS (SEO & Limpieza):*\n"
        if tareas_tomas_seo: msg += f" ⚠️ {len(tareas_tomas_seo)} items sin Tags.\n"
        if borradores_tomas: msg += f" 🧹 {len(borradores_tomas)} borradores por limpiar.\n"
        if not tareas_tomas_seo and not borradores_tomas: msg += " ✅ Tienda limpia y posicionada.\n"

        if ganancia_hoy > 0:
            # Fórmula de reparto
            msg += f"\n💰 *REPARTO:* T (65%): ${ganancia_hoy*0.65:,.2f} | A (35%): ${ganancia_hoy*0.35:,.2f}\n"

        if es_viernes:
            msg += f"\n✨ *MODO FINDE:*\n{obtener_mensaje_viernes()}"
        else:
            msg += "\n🎯 _Misión: Completar tareas para dominar el mercado._"

        return msg

    except Exception:
        return f"❌ Error Crítico:\n{traceback.format_exc()[:150]}"

def enviar_whatsapp(texto):
    if "SKIP" in texto: return
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"Estado HTTP: {r.status_code}")
    except:
        print("Error de conexión.")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
