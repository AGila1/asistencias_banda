"""
Script para cargar datos de ejemplo en la base de datos
Útil para probar la aplicación
"""
from database import Database
from datetime import datetime, timedelta
import random

def cargar_datos_ejemplo():
    """Carga datos de ejemplo en la base de datos"""
    db = Database()

    print("🎺 Cargando datos de ejemplo...")

    # 1. Agregar miembros de ejemplo
    print("\n👥 Agregando miembros...")
    miembros = [
        ("Juan", "García López", "Trompeta", "juan.garcia@email.com", "600111222"),
        ("María", "Fernández Ruiz", "Saxofón", "maria.fernandez@email.com", "600222333"),
        ("Pedro", "Martínez Silva", "Trombón", "pedro.martinez@email.com", "600333444"),
        ("Ana", "López Torres", "Clarinete", "ana.lopez@email.com", "600444555"),
        ("Carlos", "Sánchez Díaz", "Flauta", "carlos.sanchez@email.com", "600555666"),
        ("Laura", "Rodríguez Moreno", "Tuba", "laura.rodriguez@email.com", "600666777"),
        ("Miguel", "González Vega", "Percusión", "miguel.gonzalez@email.com", "600777888"),
        ("Elena", "Jiménez Castro", "Saxofón Alto", "elena.jimenez@email.com", "600888999"),
        ("David", "Hernández Ramos", "Trompeta", "david.hernandez@email.com", "600999000"),
        ("Isabel", "Morales Ortiz", "Clarinete", "isabel.morales@email.com", "600000111"),
    ]

    miembros_ids = []
    for nombre, apellidos, instrumento, email, telefono in miembros:
        miembro_id = db.agregar_miembro(nombre, apellidos, instrumento, email, telefono)
        miembros_ids.append(miembro_id)
        print(f"  ✅ {nombre} {apellidos} - {instrumento}")

    # 2. Agregar eventos (ensayos y actuaciones)
    print("\n📅 Agregando eventos...")

    # Eventos de los últimos 2 meses
    fecha_base = datetime.now()
    eventos_ids = []

    # Ensayos (todos los martes y jueves de los últimos 2 meses)
    print("  🎵 Ensayos...")
    for i in range(16):  # 8 semanas = 16 ensayos
        dias_atras = i * 3.5  # Aproximadamente 2 ensayos por semana
        fecha = (fecha_base - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        evento_id = db.agregar_evento(
            tipo='ensayo',
            fecha=fecha,
            descripcion=f"Ensayo semanal",
            lugar="Sala de ensayo municipal"
        )
        eventos_ids.append(evento_id)
        print(f"    ✅ Ensayo - {fecha}")

    # Actuaciones (4 actuaciones en los últimos 2 meses)
    print("  🎭 Actuaciones...")
    actuaciones = [
        (7, "Concierto de verano", "Plaza Mayor", 500),
        (14, "Fiesta patronal", "Iglesia de San José", 400),
        (28, "Concierto benéfico", "Teatro Municipal", 350),
        (42, "Actuación privada", "Salón de eventos", 600),
    ]

    for dias_atras, descripcion, lugar, importe in actuaciones:
        fecha = (fecha_base - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        evento_id = db.agregar_evento(
            tipo='actuacion',
            fecha=fecha,
            descripcion=descripcion,
            lugar=lugar,
            importe=importe
        )
        eventos_ids.append(evento_id)
        print(f"    ✅ {descripcion} - {fecha} - {importe}€")

    # 3. Registrar asistencias aleatorias (pero realistas)
    print("\n✅ Registrando asistencias...")

    for evento_id in eventos_ids:
        evento = db.obtener_evento(evento_id)

        # Para ensayos: 70-90% de asistencia
        # Para actuaciones: 85-100% de asistencia
        if evento['tipo'] == 'ensayo':
            probabilidad_asistencia = 0.80
        else:
            probabilidad_asistencia = 0.95

        for miembro_id in miembros_ids:
            # Algunos miembros son más constantes que otros
            factor_constancia = random.uniform(0.8, 1.2)
            prob_final = probabilidad_asistencia * factor_constancia

            asistio = random.random() < prob_final
            db.registrar_asistencia(miembro_id, evento_id, asistio)

    print("    ✅ Asistencias registradas")

    # 4. Mostrar resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DE DATOS CARGADOS")
    print("="*50)

    miembros_total = db.obtener_miembros()
    eventos_total = db.obtener_eventos()
    ensayos = [e for e in eventos_total if e['tipo'] == 'ensayo']
    actuaciones = [e for e in eventos_total if e['tipo'] == 'actuacion']

    print(f"👥 Miembros: {len(miembros_total)}")
    print(f"📅 Eventos totales: {len(eventos_total)}")
    print(f"   🎵 Ensayos: {len(ensayos)}")
    print(f"   🎭 Actuaciones: {len(actuaciones)}")

    print("\n💰 RESUMEN DE PAGOS:")
    print("-" * 50)
    resumen_pagos = db.obtener_resumen_pagos()
    for pago in resumen_pagos[:5]:  # Top 5
        print(f"{pago['nombre']} {pago['apellidos']:15} | {pago['total_final']:7.2f}€")

    print("\n" + "="*50)
    print("✅ ¡Datos de ejemplo cargados correctamente!")
    print("="*50)
    print("\nPuedes iniciar la aplicación con:")
    print("  streamlit run app.py")
    print()

if __name__ == "__main__":
    # Preguntar confirmación
    respuesta = input("⚠️  ¿Estás seguro de que quieres cargar datos de ejemplo? Esto agregará datos a la base de datos. (s/n): ")

    if respuesta.lower() in ['s', 'si', 'sí', 'yes', 'y']:
        cargar_datos_ejemplo()
    else:
        print("❌ Operación cancelada")
