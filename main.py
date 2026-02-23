import requests
import json
from datetime import datetime
import time
import schedule

# --- CONFIGURACIÓN CENTRAL ---
GUMROAD_TOKEN = "PONE_ACÁ_TU_GUMROAD_TOKEN"
ID_INSTANCE = "PONE_ACÁ_TU_ID_INSTANCE"
API_TOKEN = "PONE_ACÁ_TU_API_TOKEN"
CHAT_ID = "PONE_ACÁ_TU_CHAT_ID"  # ejemplo: "120363406798223965@g.us"


def generar_barra(porcentaje, longitud=10):
    if porcentaje < 0:
        porcentaje = 0
    if porcentaje > 100:
        porcentaje = 100
    bloques = int(porcentaje / (100 / longitud)) if longitud > 0 else 0
    return "■" * bloques + "□" * (longitud - bloques) + f" {int(porcentaje)}%"


def obtener_datos_gumroad():
    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}

    res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers)
    res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers)

    res_p.raise_for_status()
    res_s.raise_for_status()

    productos = res_p.json().get("products", [])
    ventas_data = res_s.json().get("sales", [])
    return productos, ventas_data


def construir_reporte(productos, ventas_data):
    hoy_str = datetime.now().strftime("%Y-%m-%d")

    ventas_hoy = 0
    ganancia_bruta_hoy = 0
    cursos_vendidos_hoy = []

    tareas_alberto_detalle = []
    tareas_tomas_seo = []
    borradores_tomas = []
    radar_trafico = []

    count_publicados = 0
    count_con_renders = 0

    # Auditoría de productos
    for p in productos:
        nombre = p.get("name")
        publicado = p.get("published")
        vistas = p.get("view_count", 0)
        tags = p.get("tags", [])

        if publicado:
            count_publicados += 1
            radar_trafico.append({"nombre": nombre, "vistas": vistas})

            errores_render = []
            if not p.get("thumbnail_url"):
                errores_render.append("Miniatura 1:1")
            if not p.get("preview_url"):
                errores_render.append("Portada Principal")

            if errores_render:
                tareas_alberto_detalle.append(f"{nombre} (Falta: {', '.join(errores_render)})")
            else:
                count_con_renders += 1

            if not tags or len(tags) == 0:
                tareas_tomas_seo.append(f"{nombre} (Sugerencia: 3D, Streetwear, Fashion, CLO3D)")
            else:
                borradores_tomas.append(nombre)

    # Procesamiento financiero
    for v in ventas_data:
        created_at = v.get("created_at", "")
        if created_at.startswith(hoy_str):
            monto = v.get("price", 0) / 100
            ventas_hoy += 1
            ganancia_bruta_hoy += monto
            cursos_vendidos_hoy.append(v.get("product_name"))

    ganancia_tomas = ganancia_bruta_hoy * 0.65
    ganancia_alberto = ganancia_bruta_hoy * 0.35

    # Porcentaje de progreso de Alberto
    if count_publicados > 0:
        perc_alberto = (count_con_renders / count_publicados) * 100
    else:
        perc_alberto = 100

    # Porcentaje de limpieza general y renders ready
    perc_limpieza = (count_publicados / len(productos) * 100) if len(productos) > 0 else 100
    perc_lanzamiento = (count_con_renders / count_publicados * 100) if count_publicados > 0 else 100

    # Construcción del mensaje
    msg = f"🤖 *SISTEMA CENTRAL DE OPERACIONES: MISIÓN $10K*\n"
    msg += f"📅 Reporte: {datetime.now().strftime('%d/%m/%Y')} | {datetime.now().strftime('%H:%M')}\n"
    msg += "----------------------------------\n\n"

    # Ganancias
    msg += f"💰 *REPARTO DE GANANCIAS HOY:*\n"
    if ganancia_bruta_hoy > 0:
        msg += f"💵 *Bruto:* ${ganancia_bruta_hoy:,.2f}\n"
        msg += f"👤 *Tomás (65%):* ${ganancia_tomas:,.2f}\n{generar_barra(65)}\n"
        msg += f"🎨 *Alberto (35%):* ${ganancia_alberto:,.2f}\n{generar_barra(35)}\n\n"
    else:
        msg += "📈 *Estado:* Sin ventas nuevas. Monitoreando tráfico...\n\n"

    # Barras de progreso
    msg += f"🧹 *Limpieza Tienda:* {generar_barra(perc_limpieza)}\n"
    msg += f"🚀 *Renders Ready:* {generar_barra(perc_lanzamiento)}\n\n"

    # Radar de tráfico
    msg += "📊 *PRODUCTOS MÁS VISTOS (Radar):*\n"
    ranking = sorted(radar_trafico, key=lambda x: x["vistas"], reverse=True)
    for p in ranking[:5]:
        msg += f" • {p['nombre']}: {p['vistas']} visitas\n"

    # Test de productos más vistos (prioridades)
    msg += "\n🧪 *TEST DE PRIORIDAD (Top vistos con fallos):*\n"
    nombres_top = {p["nombre"] for p in ranking[:5]}
    encontrados = False
    for t in tareas_alberto_detalle + tareas_tomas_seo:
        for nombre in nombres_top:
            if nombre in t:
                msg += f" • PRIORIDAD: {t}\n"
                encontrados = True
                break
    if not encontrados:
        msg += " ✅ Los top vistos están bien configurados por ahora.\n"

    # Tareas de Alberto
    msg += "\n🎨 *ALBERTO (Faltan Renders):*\n"
    if tareas_alberto_detalle:
        msg += f"Tu barra de progreso está en {generar_barra(perc_alberto)}\n"
        msg += "Cada pack que completes con todos los renders hace subir esta barra, te queda menos 💪\n"
        for t in tareas_alberto_detalle[:5]:
            msg += f" • {t}\n"
    else:
        msg += " ✅ ¡Todos los renders están perfectos! Barra al 100%.\n"

    # Tareas de Tomás
    msg += "\n💡 *TOMÁS (SEO & Etiquetas):*\n"
    if tareas_tomas_seo:
        msg += " ⚠️ *Faltan TAGS en:*\n"
        for s in tareas_tomas_seo[:5]:
            msg += f" • {s}\n"
    if borradores_tomas:
        msg += f" 🧹 *Borradores:* Tenés {len(borradores_tomas)} items para limpiar/borrar.\n"
    if not tareas_tomas_seo and not borradores_tomas:
        msg += " ✅ SEO y tienda impecables.\n"

    msg += "\n🎯 _Meta: Barras al 100% para soltar el Bucket Hat._"
    return msg


def enviar_whatsapp(texto):
    url = f"https://7103.api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": texto}
    headers = {"Content-Type": "application/json"}
    requests.post(url, data=json.dumps(payload), headers=headers)


def tarea_diaria():
    try:
        productos, ventas_data = obtener_datos_gumroad()
        reporte = construir_reporte(productos, ventas_data)
        enviar_whatsapp(reporte)
        print("✅ Reporte diario enviado correctamente.")
    except Exception as e:
        print(f"❌ Error en tarea_diaria: {e}")


# Programar de lunes a viernes a las 09:00
schedule.every().monday.at("09:00").do(tarea_diaria)
schedule.every().tuesday.at("09:00").do(tarea_diaria)
schedule.every().wednesday.at("09:00").do(tarea_diaria)
schedule.every().thursday.at("09:00").do(tarea_diaria)
schedule.every().friday.at("09:00").do(tarea_diaria)


if __name__ == "__main__":
    print("⏱️ Bot de reportes Gumroad iniciado. Esperando horarios programados...")
    while True:
        schedule.run_pending()
        time.sleep(30)
