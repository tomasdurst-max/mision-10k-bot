import requests
import json
from datetime import datetime
import os
import random

# --- CONFIGURACIÓN DE IDENTIFICADORES (Fijos para tu comodidad) ---
ID_INSTANCE = "7103524728" 
CHAT_ID = "120363406798223965@g.us" 

# --- SEGURIDAD (Se cargan en Railway o GitHub Secrets) ---
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

def generar_barra(porcentaje, longitud=15):
    """Crea una barra de progreso visual con bloques."""
    porcentaje = min(max(porcentaje, 0), 100)
    bloques = int(porcentaje / (100 / longitud))
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"

def obtener_mensaje_viernes():
    """Selecciona un mensaje motivador único para cada viernes."""
    mensajes = [
        "🍻 ¡Se terminó la semana, cracks! Alberto, soltá el mouse. Tomás, apagá el SEO. ¡A disfrutar!",
        "🍕 ¡Viernes! La tienda queda en piloto automático. Gran laburo, el $10K está cerca.",
        "🎮 Misión cumplida. Desconecten para volver el lunes con ojos nuevos. ¡Felicidades!",
        "🚀 ¡Viernes de descontrol! El Bucket Hat ya es casi una realidad. ¡Disfruten el descanso!",
        "✨ ¡Semana liquidada! Que tengan un finde de película. ¡Nos vemos el lunes en la cima!"
    ]
    # Usa el número de la semana para que el mensaje cambie cada viernes
    num_semana = datetime.now().isocalendar()[1]
    return mensajes[num_semana % len(mensajes)]

def auditoria_mision_10k():
    hoy = datetime.now()
    es_viernes = hoy.weekday() == 4
    
    # Filtro: Corre de Lunes (0) a Viernes (4)
    if hoy.weekday() > 4:
        return "SKIP: El sistema descansa los fines de semana."

    if not all([GUMROAD_TOKEN, API_TOKEN]):
        return "❌ ERROR: Faltan los Tokens (GUMROAD_TOKEN o API_TOKEN) en la configuración."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Obtener Datos
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # 2. Investigación de Tendencias (Top 3)
        ranking = sorted(
            [{"n": p.get("name"), "v": p.get("view_count", 0)} for p in productos if p.get("published")],
            key=lambda x: x['v'], reverse=True
        )
        
        # 3. Auditoría de Tareas (Limpieza y Optimización)
        tareas_alberto = []
        tareas_tomas_seo = []
        borradores_tomas = []
        puntos_totales = 0
        puntos_logrados = 0

        for p in productos:
            name = p.get("name")
            puntos_totales += 3 # Publicado, Render y Tags
            
            if p.get("published"):
                puntos_logrados += 1
                # Check Renders (Alberto)
                if not p.get("thumbnail_url") or not p.get("preview_url"):
                    tareas_alberto.append(name)
                else:
                    puntos_logrados += 1
                
                # Check SEO (Tomás)
                if not p.get("tags"):
                    tareas_tomas_seo.append(name)
                else:
                    puntos_logrados += 1
            else:
                borradores_tomas.append(name)

        salud_tienda = (puntos_logrados / puntos_totales * 100) if puntos_totales > 0 else 0
        ganancia_hoy = sum(v.get("price") / 100 for v in ventas_data if v.get("created_at").startswith(hoy.strftime("%Y-%m-%d")))

        # --- CONSTRUCCIÓN DEL MENSAJE ---
        # Logro: Si el producto top tiene más de 1000 visitas, ponemos trofeo
        logro_icono = "🏆 " if (ranking and ranking[0]['v'] > 1000) else "🚀 "
        
        msg = f"{logro_icono}*SISTEMA CENTRAL: ESTRATEGIA $10K*\n"
        msg += f"📅 {hoy.strftime('%d/%m/%Y')} | {'🔥 MODO VIERNES' if es_viernes else 'Status: Activo'}\n"
        msg += "----------------------------------\n\n"

        msg += f"📊 *SALUD DE LA TIENDA:* \n"
        msg += f"{generar_barra(salud_tienda)}\n"
        msg += "_Si llegamos al 100%, lanzamos el Bucket Hat._\n\n"

        msg += "🔍 *INVESTIGACIÓN DE TENDENCIAS:* \n"
        for i, p in enumerate(ranking[:3]):
            emoji = "🔥" if i == 0 else "•"
            if i == 0 and p['v'] > 1000: emoji = "🏆"
            msg += f" {emoji} {p['n']} ({p['v']} visitas)\n"

        # TAREAS ALBERTO (Desaparecen solas al subir el render)
        msg += f"\n🎨 *ALBERTO (Renders Pendientes):*\n"
        if tareas_alberto:
            for t in tareas_alberto[:3]: msg += f" • {t}\n"
        else:
            msg += " ✅ ¡Todos los renders están listos!\n"

        # TAREAS TOMÁS (SEO y Limpieza)
        msg += f"\n💡 *TOMÁS (SEO & Limpieza):*\n"
        if tareas_tomas_seo:
            msg += f" ⚠️ {len(tareas_tomas_seo)} items sin Tags (SEO).\n"
        if borradores_tomas:
            msg += f" 🧹 {len(borradores_tomas)} borradores por limpiar.\n"
        if not tareas_tomas_seo and not borradores_tomas:
            msg += " ✅ SEO y tienda impecables.\n"

        # Reparto Financiero
        if ganancia_hoy > 0:
            msg += f"\n💰 *REPARTO:* Tomás ${ganancia_hoy*0.65:,.2f} | Alb ${ganancia_hoy*0.35:,.2f}\n"

        # Cierre dinámico (Viernes o Meta)
        if es_viernes:
            msg += f"\n✨ *MODO FINDE:*\n{obtener_mensaje_viernes()}"
        else:
            msg += "\n🎯 _Misión: Completar tareas para dominar el mercado._"

        return msg

    except Exception as e:
        return f"❌ Error de Análisis: {e}"

def enviar_whatsapp(texto):
    if "SKIP" in texto: return
    # URL Universal para evitar Error 403
    url = f"https://api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Estado HTTP: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reporte = auditoria_mision_10k()
    enviar_whatsapp(reporte)
