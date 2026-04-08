---
name: streamlit-feature
description: "WORKFLOW SKILL — Add new features to the banda asistencias Streamlit app. USE FOR: adding new pages, creating visualizations, implementing payment logic, adding statistics features, working with database queries. Follows app conventions: Streamlit components, plotly charts, Database class methods, page navigation patterns. DO NOT USE FOR: general Python questions, data analysis tasks, fixing runtime errors."
---

# Streamlit Feature Development

## Project Context

**App**: Sistema de gestión de asistencias para banda de música
**Tech Stack**: Streamlit + SQLite + Plotly + Pandas
**Database**: `Database` class in `database.py`

## Architecture Patterns

### Page Structure
```python
# Cada página sigue este patrón
st.sidebar.title("🎺 Menú Principal")
pagina = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "👥 Miembros", "📅 Eventos", "✅ Asistencias", "💰 Pagos", "📊 Estadísticas"]
)

if pagina == "🏠 Inicio":
    # Contenido de la página
    pass
```

### Database Queries
Always use the `Database` class methods:
```python
db = get_database()  # Already initialized in app.py

# Common methods:
db.agregar_miembro(nombre, apellidos, instrumento, email, telefono)
db.obtener_miembros()
db.agregar_evento(tipo, fecha, descripcion, lugar, importe)
db.obtener_eventos()
db.registrar_asistencia(evento_id, miembro_id, asistio)
db.calcular_pagos()
```

### Visualization Standards
Use Plotly for charts:
```python
import plotly.express as px
import plotly.graph_objects as go

# Bar charts
fig = px.bar(df, x='nombre', y='porcentaje', title='Asistencias')
fig.update_layout(xaxis_title='Miembro', yaxis_title='%')
st.plotly_chart(fig, use_container_width=True)

# Pie charts
fig = px.pie(df, values='total', names='miembro', title='Distribución')
st.plotly_chart(fig, use_container_width=True)
```

### Form Patterns
Standard Streamlit forms:
```python
with st.form("form_name"):
    col1, col2 = st.columns(2)
    with col1:
        campo1 = st.text_input("Label")
    with col2:
        campo2 = st.selectbox("Label", options)

    submitted = st.form_submit_button("Acción")
    if submitted:
        # Procesar
        st.success("Mensaje de éxito")
```

## Payment Logic Rules

### Calculations
- **Actuaciones**: `importe_total / num_asistentes`
- **Ensayos no asistidos**: `-0.50€` por cada uno
- **Total**: `suma_actuaciones - penalizaciones_ensayos`

### Database Relationship
```sql
-- Miembros con su instrumento
miembros (id, nombre, apellidos, instrumento, email, telefono, activo)

-- Eventos con importe (solo actuaciones)
eventos (id, tipo, fecha, descripcion, lugar, importe)

-- Asistencias (relación N:M)
asistencias (id, evento_id, miembro_id, asistio)
```

## Common Tasks

### Adding a New Page
1. Add page name to sidebar radio options
2. Create `if pagina == "🆕 Nueva Página":` block
3. Structure with headers: `st.header("📋 Título")`
4. Use tabs if needed: `tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])`

### Creating Statistics
1. Query data with `db.obtener_*()` methods
2. Convert to pandas DataFrame
3. Calculate metrics with pandas
4. Display with `st.metric()` or plotly charts

### Adding Database Methods
1. Edit `database.py`
2. Add method to `Database` class
3. Use `self.conn.execute()` for queries
4. Handle transactions: `self.conn.commit()`

## Best Practices

- ✅ Use emojis in headers (🎺 🎵 🎭 📊 💰 ✅)
- ✅ Wrap long forms in `with st.form():`
- ✅ Show feedback: `st.success()`, `st.error()`, `st.warning()`
- ✅ Use `st.columns()` for side-by-side layout
- ✅ Cache database with `@st.cache_resource`
- ❌ Don't use raw SQL strings in app.py (use Database class)
- ❌ Don't forget `use_container_width=True` in charts

## Example: Adding Export Feature

```python
# In the appropriate page section
if st.button("📥 Exportar a Excel"):
    df_pagos = db.calcular_pagos()

    # Convert to DataFrame
    df = pd.DataFrame(df_pagos)

    # Create Excel file in memory
    from io import BytesIO
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Pagos', index=False)

    st.download_button(
        label="💾 Descargar Excel",
        data=buffer.getvalue(),
        file_name=f"pagos_banda_{date.today()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.success("✅ Archivo generado")
```

## Checklist Before Completing

- [ ] Database queries use `Database` class methods
- [ ] Forms have success/error messages
- [ ] Charts use plotly with `use_container_width=True`
- [ ] Page follows sidebar navigation pattern
- [ ] Headers use appropriate emojis
- [ ] Code follows existing indentation (4 spaces)
