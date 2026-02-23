import requests
import json
from datetime import datetime
import os
import random

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
    """Genera un mensaje de cierre de semana no genérico."""
    mensajes = [
        "🍻 ¡Se terminó la semana, cracks! Alberto, soltá el mouse. Tomás, apagá el SEO. ¡A disfrutar!",
        "🍕 ¡Viernes! La tienda queda en piloto automático. Gran laburo, el $10K está cada vez más cerca.",
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
        return "❌ ERROR: Faltan los Tokens en la configuración de Railway/GitHub."

    headers = {"Authorization": f"Bearer {GUMROAD_TOKEN}"}
    
    try:
        # 1. Carga de datos
        res_p = requests.get("https://api.gumroad.com/v2/products", headers=headers).json()
        res_s = requests.get("https://api.gumroad.com/v2/sales", headers=headers).json()
        
        productos = res_p.get("products", [])
        ventas_data = res_s.get("sales", [])
        
        # 2. Investigación de Tendencias y Radar Viral
        ranking = sorted(
            [{"n": p.get("name"), "v": p.get
