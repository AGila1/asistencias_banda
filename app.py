"""
Aplicación principal de gestión de asistencias de Asociación Cultural Musical Cabra del Santo Cristo
"""
import streamlit as st
import os
from supabase_database import SupabaseDatabase
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Asistencias - Asociación Cultural Musical Cabra del Santo Cristo",
    page_icon="🎺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar base de datos usando Supabase
@st.cache_resource
def get_database():
    try:
        # Intentar obtener de secrets de Streamlit
        if "supabase" in st.secrets:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
        # Fallback a variables de entorno
        else:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            st.error("❌ Error: No se encontraron las credenciales de Supabase")
            st.info("Configura en Streamlit Cloud → Settings → Secrets:")
            st.code("""[supabase]
url = "https://YOUR_PROJECT_ID.supabase.co"
key = "YOUR_ANON_PUBLIC_KEY"
""")
            st.stop()

        return SupabaseDatabase(url=url, key=key)
    except Exception as e:
        st.error(f"❌ Error al conectar con Supabase: {str(e)}")
        st.stop()

db = get_database()

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar para navegación
st.sidebar.title("🎺 Menú Principal")
pagina = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "👥 Miembros", "📅 Eventos", "✅ Asistencias", "💰 Pagos", "📊 Estadísticas"]
)

# ===== PÁGINA DE INICIO =====
if pagina == "🏠 Inicio":
    st.markdown('<h1 class="main-header">🎺 Gestión de Asistencias - Asociación Cultural Musical Cabra del Santo Cristo</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    miembros = db.obtener_miembros(solo_activos=True)
    eventos = db.obtener_eventos()
    eventos_ensayos = [e for e in eventos if e['tipo'] == 'ensayo']
    eventos_actuaciones = [e for e in eventos if e['tipo'] == 'actuacion']

    with col1:
        st.metric("👥 Miembros Activos", len(miembros))
    with col2:
        st.metric("🎵 Ensayos", len(eventos_ensayos))
    with col3:
        st.metric("🎭 Actuaciones", len(eventos_actuaciones))

    st.divider()

    st.subheader("📋 Últimos Eventos")
    if eventos:
        eventos_recientes = eventos[:5]
        for evento in eventos_recientes:
            tipo_emoji = "🎵" if evento['tipo'] == 'ensayo' else "🎭"
            st.write(f"{tipo_emoji} **{evento['fecha']}** - {evento['descripcion'] or evento['tipo'].capitalize()}")
    else:
        st.info("No hay eventos registrados aún.")

    st.divider()

    st.subheader("💰 Resumen de Pagos")
    resumen_pagos = db.obtener_resumen_pagos()
    if resumen_pagos:
        df_pagos = pd.DataFrame(resumen_pagos)
        df_display = df_pagos[['nombre', 'apellidos', 'total_actuaciones', 'penalizacion', 'total_final']].copy()
        df_display.columns = ['Nombre', 'Apellidos', 'Actuaciones (€)', 'Penalización (€)', 'Total (€)']
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No hay datos de pagos disponibles.")

# ===== PÁGINA DE MIEMBROS =====
elif pagina == "👥 Miembros":
    st.title("👥 Gestión de Miembros")

    tab1, tab2, tab3 = st.tabs(["Ver Miembros", "Agregar Miembro", "Editar/Eliminar"])

    with tab1:
        st.subheader("Lista de Miembros")
        mostrar_inactivos = st.checkbox("Mostrar miembros inactivos")
        miembros = db.obtener_miembros(solo_activos=not mostrar_inactivos)

        if miembros:
            df_miembros = pd.DataFrame(miembros)
            df_display = df_miembros[['nombre', 'apellidos', 'instrumento', 'email', 'telefono', 'activo']].copy()
            df_display.columns = ['Nombre', 'Apellidos', 'Instrumento', 'Email', 'Teléfono', 'Activo']
            df_display['Activo'] = df_display['Activo'].map({1: '✅', 0: '❌'})
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("No hay miembros registrados.")

    with tab2:
        st.subheader("Agregar Nuevo Miembro")
        with st.form("form_agregar_miembro"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre *")
                apellidos = st.text_input("Apellidos")
                instrumento = st.text_input("Instrumento")
            with col2:
                email = st.text_input("Email")
                telefono = st.text_input("Teléfono")

            submitted = st.form_submit_button("Agregar Miembro")

            if submitted:
                if nombre:
                    miembro_id = db.agregar_miembro(nombre, apellidos, instrumento, email, telefono)
                    st.success(f"✅ Miembro '{nombre} {apellidos}' agregado correctamente (ID: {miembro_id})")
                    st.rerun()
                else:
                    st.error("El nombre es obligatorio")

    with tab3:
        st.subheader("Editar o Eliminar Miembro")
        miembros = db.obtener_miembros(solo_activos=False)

        if miembros:
            opciones_miembros = {f"{m['nombre']} {m['apellidos']} - {m['instrumento']} (ID: {m['id']})": m['id']
                                for m in miembros}

            miembro_seleccionado = st.selectbox("Seleccionar miembro", list(opciones_miembros.keys()))

            if miembro_seleccionado:
                miembro_id = opciones_miembros[miembro_seleccionado]
                miembro = db.obtener_miembro(miembro_id)

                col1, col2 = st.columns([3, 1])

                with col1:
                    with st.form("form_editar_miembro"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            nombre = st.text_input("Nombre", value=miembro['nombre'])
                            apellidos = st.text_input("Apellidos", value=miembro['apellidos'] or "")
                            instrumento = st.text_input("Instrumento", value=miembro['instrumento'] or "")
                        with col_b:
                            email = st.text_input("Email", value=miembro['email'] or "")
                            telefono = st.text_input("Teléfono", value=miembro['telefono'] or "")

                        submitted = st.form_submit_button("Actualizar Miembro")

                        if submitted:
                            if nombre:
                                db.actualizar_miembro(miembro_id, nombre, apellidos, instrumento, email, telefono)
                                st.success("✅ Miembro actualizado correctamente")
                                st.rerun()
                            else:
                                st.error("El nombre es obligatorio")

                with col2:
                    st.write("**Acciones:**")
                    if miembro['activo']:
                        if st.button("🗑️ Desactivar", use_container_width=True):
                            db.eliminar_miembro(miembro_id)
                            st.success("Miembro desactivado")
                            st.rerun()
                    else:
                        if st.button("♻️ Reactivar", use_container_width=True):
                            db.reactivar_miembro(miembro_id)
                            st.success("Miembro reactivado")
                            st.rerun()
        else:
            st.info("No hay miembros para editar")

# ===== PÁGINA DE EVENTOS =====
elif pagina == "📅 Eventos":
    st.title("📅 Gestión de Eventos")

    tab1, tab2, tab3 = st.tabs(["Ver Eventos", "Agregar Evento", "Editar/Eliminar"])

    with tab1:
        st.subheader("Lista de Eventos")
        filtro_tipo = st.radio("Filtrar por tipo", ["Todos", "Ensayos", "Actuaciones"], horizontal=True)

        if filtro_tipo == "Ensayos":
            eventos = db.obtener_eventos(tipo='ensayo')
        elif filtro_tipo == "Actuaciones":
            eventos = db.obtener_eventos(tipo='actuacion')
        else:
            eventos = db.obtener_eventos()

        if eventos:
            df_eventos = pd.DataFrame(eventos)
            df_display = df_eventos[['fecha', 'tipo', 'descripcion', 'lugar', 'importe']].copy()
            df_display.columns = ['Fecha', 'Tipo', 'Descripción', 'Lugar', 'Importe (€)']
            df_display['Tipo'] = df_display['Tipo'].map({'ensayo': '🎵 Ensayo', 'actuacion': '🎭 Actuación'})
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("No hay eventos registrados.")

    with tab2:
        st.subheader("Agregar Nuevo Evento")
        with st.form("form_agregar_evento"):
            tipo = st.selectbox("Tipo de evento *", ["ensayo", "actuacion"],
                              format_func=lambda x: "🎵 Ensayo" if x == "ensayo" else "🎭 Actuación")

            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("Fecha *", value=date.today())
                descripcion = st.text_input("Descripción")
            with col2:
                lugar = st.text_input("Lugar")
                importe = st.number_input("Importe (€)", min_value=0.0, value=0.0, step=10.0)

            submitted = st.form_submit_button("Agregar Evento")

            if submitted:
                evento_id = db.agregar_evento(tipo, str(fecha), descripcion, lugar, importe)
                st.success(f"✅ Evento agregado correctamente (ID: {evento_id})")
                st.rerun()

    with tab3:
        st.subheader("Editar o Eliminar Evento")
        eventos = db.obtener_eventos()

        if eventos:
            opciones_eventos = {f"{e['fecha']} - {e['tipo'].capitalize()} - {e['descripcion']} (ID: {e['id']})": e['id']
                               for e in eventos}

            evento_seleccionado = st.selectbox("Seleccionar evento", list(opciones_eventos.keys()))

            if evento_seleccionado:
                evento_id = opciones_eventos[evento_seleccionado]
                evento = db.obtener_evento(evento_id)

                col1, col2 = st.columns([3, 1])

                with col1:
                    with st.form("form_editar_evento"):
                        tipo = st.selectbox("Tipo de evento", ["ensayo", "actuacion"],
                                          index=0 if evento['tipo'] == 'ensayo' else 1,
                                          format_func=lambda x: "🎵 Ensayo" if x == "ensayo" else "🎭 Actuación")

                        col_a, col_b = st.columns(2)
                        with col_a:
                            fecha = st.date_input("Fecha", value=datetime.strptime(evento['fecha'], "%Y-%m-%d").date())
                            descripcion = st.text_input("Descripción", value=evento['descripcion'] or "")
                        with col_b:
                            lugar = st.text_input("Lugar", value=evento['lugar'] or "")
                            importe = st.number_input("Importe (€)", value=float(evento['importe'] or 0), step=10.0)

                        submitted = st.form_submit_button("Actualizar Evento")

                        if submitted:
                            db.actualizar_evento(evento_id, tipo, str(fecha), descripcion, lugar, importe)
                            st.success("✅ Evento actualizado correctamente")
                            st.rerun()

                with col2:
                    st.write("**Acciones:**")
                    if st.button("🗑️ Eliminar", use_container_width=True):
                        db.eliminar_evento(evento_id)
                        st.success("Evento eliminado")
                        st.rerun()
        else:
            st.info("No hay eventos para editar")

# ===== PÁGINA DE ASISTENCIAS =====
elif pagina == "✅ Asistencias":
    st.title("✅ Registro de Asistencias")

    tab1, tab2 = st.tabs(["Registrar Asistencias", "Ver Asistencias por Evento"])

    with tab1:
        st.subheader("Registrar Asistencias a un Evento")

        eventos = db.obtener_eventos()
        if eventos and db.obtener_miembros():
            opciones_eventos = {f"{e['fecha']} - {e['tipo'].capitalize()} - {e['descripcion']} (ID: {e['id']})": e['id']
                               for e in eventos}

            evento_seleccionado = st.selectbox("Seleccionar evento", list(opciones_eventos.keys()))

            if evento_seleccionado:
                evento_id = opciones_eventos[evento_seleccionado]
                evento = db.obtener_evento(evento_id)

                st.info(f"📅 {evento['fecha']} | {'🎵 Ensayo' if evento['tipo'] == 'ensayo' else '🎭 Actuación'} | {evento['descripcion']}")

                # Obtener asistencias ya registradas
                asistencias_registradas = db.obtener_asistencias_evento(evento_id)
                asistencias_dict = {a['miembro_id']: a for a in asistencias_registradas}

                miembros = db.obtener_miembros()

                st.write("### Marcar asistencias:")

                # Crear formulario para registrar asistencias
                with st.form("form_asistencias"):
                    asistencias_form = {}

                    cols = st.columns(2)
                    for idx, miembro in enumerate(miembros):
                        col = cols[idx % 2]

                        # Verificar si ya hay asistencia registrada
                        asistio_previo = asistencias_dict.get(miembro['id'], {}).get('asistio', True)

                        with col:
                            asistencias_form[miembro['id']] = st.checkbox(
                                f"{miembro['nombre']} {miembro['apellidos']} - {miembro['instrumento']}",
                                value=bool(asistio_previo),
                                key=f"asist_{miembro['id']}"
                            )

                    submitted = st.form_submit_button("Guardar Asistencias", use_container_width=True)

                    if submitted:
                        for miembro_id, asistio in asistencias_form.items():
                            db.registrar_asistencia(miembro_id, evento_id, asistio)
                        st.success("✅ Asistencias registradas correctamente")
                        st.rerun()
        else:
            st.warning("⚠️ Necesitas tener eventos y miembros registrados para registrar asistencias")

    with tab2:
        st.subheader("Ver Asistencias por Evento")

        eventos = db.obtener_eventos()
        if eventos:
            opciones_eventos = {f"{e['fecha']} - {e['tipo'].capitalize()} - {e['descripcion']} (ID: {e['id']})": e['id']
                               for e in eventos}

            evento_ver = st.selectbox("Seleccionar evento para ver", list(opciones_eventos.keys()), key="ver_evento")

            if evento_ver:
                evento_id = opciones_eventos[evento_ver]
                asistencias = db.obtener_asistencias_evento(evento_id)

                if asistencias:
                    df_asist = pd.DataFrame(asistencias)
                    df_display = df_asist[['nombre', 'apellidos', 'instrumento', 'asistio']].copy()
                    df_display.columns = ['Nombre', 'Apellidos', 'Instrumento', 'Asistió']
                    df_display['Asistió'] = df_display['Asistió'].map({1: '✅', 0: '❌'})

                    st.dataframe(df_display, use_container_width=True)

                    # Mostrar resumen
                    total = len(asistencias)
                    asistieron = len([a for a in asistencias if a['asistio']])

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total registrados", total)
                    col2.metric("Asistieron", asistieron)
                    col3.metric("No asistieron", total - asistieron)
                else:
                    st.info("No hay asistencias registradas para este evento")
        else:
            st.info("No hay eventos registrados")

# ===== PÁGINA DE PAGOS =====
elif pagina == "💰 Pagos":
    st.title("💰 Gestión de Pagos")

    resumen_pagos = db.obtener_resumen_pagos()

    if resumen_pagos:
        st.subheader("Resumen de Pagos por Miembro")

        # Crear DataFrame
        df_pagos = pd.DataFrame(resumen_pagos)

        # Tabla detallada
        df_display = df_pagos[['nombre', 'apellidos', 'instrumento', 'total_actuaciones',
                               'ensayos_no_asistidos', 'penalizacion', 'total_final']].copy()
        df_display.columns = ['Nombre', 'Apellidos', 'Instrumento', 'Actuaciones (€)',
                             'Ensayos Faltados', 'Penalización (€)', 'Total a Pagar (€)']

        st.dataframe(df_display, use_container_width=True)

        # Gráficos
        st.divider()
        st.subheader("📊 Visualización de Pagos")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de barras de totales
            df_pagos['nombre_completo'] = df_pagos['nombre'] + ' ' + df_pagos['apellidos']
            fig_barras = px.bar(
                df_pagos.head(10),
                x='nombre_completo',
                y='total_final',
                title='Top 10 - Total a Pagar por Miembro',
                labels={'nombre_completo': 'Miembro', 'total_final': 'Total (€)'},
                color='total_final',
                color_continuous_scale='Blues'
            )
            fig_barras.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_barras, use_container_width=True)

        with col2:
            # Gráfico circular de distribución
            total_general = df_pagos['total_final'].sum()
            fig_pie = px.pie(
                df_pagos.head(10),
                values='total_final',
                names='nombre_completo',
                title=f'Distribución de Pagos (Total: {total_general:.2f}€)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Comparación actuaciones vs penalizaciones
        st.divider()
        col3, col4 = st.columns(2)

        with col3:
            # Total ganado vs penalización
            totales = {
                'Concepto': ['Actuaciones', 'Penalizaciones'],
                'Importe': [df_pagos['total_actuaciones'].sum(), df_pagos['penalizacion'].sum()]
            }
            fig_comparacion = px.bar(
                totales,
                x='Concepto',
                y='Importe',
                title='Comparación: Ingresos vs Penalizaciones',
                color='Concepto',
                color_discrete_map={'Actuaciones': 'green', 'Penalizaciones': 'red'}
            )
            st.plotly_chart(fig_comparacion, use_container_width=True)

        with col4:
            # Estadísticas generales
            st.metric("💵 Total a Distribuir", f"{total_general:.2f}€")
            st.metric("🎭 Total de Actuaciones", f"{df_pagos['total_actuaciones'].sum():.2f}€")
            st.metric("❌ Total Penalizaciones", f"{df_pagos['penalizacion'].sum():.2f}€")
            st.metric("📉 Ensayos Faltados", int(df_pagos['ensayos_no_asistidos'].sum()))
    else:
        st.info("No hay datos de pagos disponibles. Registra eventos y asistencias para calcular los pagos.")

# ===== PÁGINA DE ESTADÍSTICAS =====
elif pagina == "📊 Estadísticas":
    st.title("📊 Estadísticas de Asistencia")

    miembros = db.obtener_miembros()

    if miembros:
        # Selector de miembro
        opciones_miembros = {f"{m['nombre']} {m['apellidos']} - {m['instrumento']}": m['id']
                            for m in miembros}

        miembro_seleccionado = st.selectbox("Seleccionar miembro", list(opciones_miembros.keys()))

        if miembro_seleccionado:
            miembro_id = opciones_miembros[miembro_seleccionado]
            miembro = db.obtener_miembro(miembro_id)
            stats = db.obtener_estadisticas_miembro(miembro_id)

            # Encabezado del miembro
            st.subheader(f"📋 {miembro['nombre']} {miembro['apellidos']}")
            st.write(f"**Instrumento:** {miembro['instrumento'] or 'No especificado'}")

            st.divider()

            # Métricas generales
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("📅 Total Eventos", stats['total_eventos'])
            col2.metric("✅ Asistencias", stats['total_asistencias'])
            col3.metric("📈 % Asistencia", f"{stats['porcentaje_general']:.1f}%")
            col4.metric("❌ Faltas", stats['total_eventos'] - stats['total_asistencias'])

            st.divider()

            # Estadísticas detalladas
            col5, col6 = st.columns(2)

            with col5:
                st.subheader("🎵 Ensayos")
                st.metric("Total Ensayos", stats['total_ensayos'])
                st.metric("Asistidos", stats['ensayos_asistidos'])
                st.metric("% Asistencia Ensayos", f"{stats['porcentaje_ensayos']:.1f}%")

                # Gráfico de ensayos
                if stats['total_ensayos'] > 0:
                    fig_ensayos = go.Figure(data=[go.Pie(
                        labels=['Asistidos', 'No Asistidos'],
                        values=[stats['ensayos_asistidos'],
                               stats['total_ensayos'] - stats['ensayos_asistidos']],
                        marker_colors=['#2ca02c', '#d62728']
                    )])
                    fig_ensayos.update_layout(title="Distribución Ensayos")
                    st.plotly_chart(fig_ensayos, use_container_width=True)

            with col6:
                st.subheader("🎭 Actuaciones")
                st.metric("Total Actuaciones", stats['total_actuaciones'])
                st.metric("Asistidas", stats['actuaciones_asistidas'])
                st.metric("% Asistencia Actuaciones", f"{stats['porcentaje_actuaciones']:.1f}%")

                # Gráfico de actuaciones
                if stats['total_actuaciones'] > 0:
                    fig_actuaciones = go.Figure(data=[go.Pie(
                        labels=['Asistidas', 'No Asistidas'],
                        values=[stats['actuaciones_asistidas'],
                               stats['total_actuaciones'] - stats['actuaciones_asistidas']],
                        marker_colors=['#1f77b4', '#ff7f0e']
                    )])
                    fig_actuaciones.update_layout(title="Distribución Actuaciones")
                    st.plotly_chart(fig_actuaciones, use_container_width=True)

            st.divider()

            # Información de pagos
            st.subheader("💰 Información de Pagos")
            pago = db.calcular_pago_miembro(miembro_id)

            col7, col8, col9, col10 = st.columns(4)
            col7.metric("🎭 Total Actuaciones", f"{pago['total_actuaciones']:.2f}€")
            col8.metric("❌ Ensayos Faltados", pago['ensayos_no_asistidos'])
            col9.metric("📉 Penalización", f"{pago['penalizacion']:.2f}€")
            col10.metric("💵 Total a Pagar", f"{pago['total_final']:.2f}€",
                        delta=f"{pago['total_actuaciones'] - pago['penalizacion']:.2f}€")

            # Historial de asistencias
            st.divider()
            st.subheader("📅 Historial de Asistencias")

            asistencias = db.obtener_asistencias_miembro(miembro_id)
            if asistencias:
                df_hist = pd.DataFrame(asistencias)
                df_display = df_hist[['fecha', 'tipo', 'descripcion', 'asistio']].copy()
                df_display.columns = ['Fecha', 'Tipo', 'Descripción', 'Asistió']
                df_display['Tipo'] = df_display['Tipo'].map({'ensayo': '🎵 Ensayo', 'actuacion': '🎭 Actuación'})
                df_display['Asistió'] = df_display['Asistió'].map({1: '✅', 0: '❌'})

                st.dataframe(df_display, use_container_width=True, height=400)
            else:
                st.info("No hay asistencias registradas para este miembro")

        st.divider()

        # Comparativa entre todos los miembros
        st.subheader("📊 Comparativa General de Asistencias")

        datos_comparativa = []
        for miembro in miembros:
            stats = db.obtener_estadisticas_miembro(miembro['id'])
            datos_comparativa.append({
                'nombre': f"{miembro['nombre']} {miembro['apellidos']}",
                'instrumento': miembro['instrumento'] or 'N/A',
                'porcentaje_general': stats['porcentaje_general'],
                'porcentaje_ensayos': stats['porcentaje_ensayos'],
                'porcentaje_actuaciones': stats['porcentaje_actuaciones'],
                'total_eventos': stats['total_eventos']
            })

        if datos_comparativa:
            df_comp = pd.DataFrame(datos_comparativa)
            df_comp = df_comp.sort_values('porcentaje_general', ascending=False)

            # Gráfico de barras comparativo
            fig_comp = px.bar(
                df_comp,
                x='nombre',
                y=['porcentaje_ensayos', 'porcentaje_actuaciones'],
                title='Comparativa de Asistencia por Miembro',
                labels={'value': '% Asistencia', 'nombre': 'Miembro'},
                barmode='group'
            )
            fig_comp.update_layout(xaxis_tickangle=-45, height=500)
            st.plotly_chart(fig_comp, use_container_width=True)

            # Tabla resumen
            df_display_comp = df_comp.copy()
            df_display_comp.columns = ['Nombre', 'Instrumento', '% General', '% Ensayos',
                                       '% Actuaciones', 'Total Eventos']
            st.dataframe(df_display_comp, use_container_width=True)
    else:
        st.info("No hay miembros registrados para mostrar estadísticas")

# Footer
st.sidebar.divider()
st.sidebar.caption("🎺 Sistema de Gestión de Asistencias")
st.sidebar.caption("Asociación Cultural Musical Cabra del Santo Cristo © 2026")
