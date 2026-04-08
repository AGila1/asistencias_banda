# 🎺 Sistema de Gestión de Asistencias - Asociación Cultural Musical Cabra del Santo Cristo

Sistema completo para gestionar asistencias, eventos y pagos de una banda de música.

## 📋 Características

### Gestión de Miembros
- ✅ Agregar, editar y eliminar miembros
- ✅ Información detallada: nombre, apellidos, instrumento, email, teléfono
- ✅ Activar/desactivar miembros sin perder historial

### Gestión de Eventos
- 🎵 **Ensayos**: Eventos de práctica
- 🎭 **Actuaciones**: Eventos con cobro
- ✅ Registro de fecha, lugar, descripción e importe
- ✅ Editar y eliminar eventos

### Control de Asistencias
- ✅ Registro fácil de asistencias por evento
- ✅ Vista de asistencias por evento
- ✅ Historial completo por miembro

### Sistema de Pagos
- 💰 **Actuaciones**: El importe se reparte entre los asistentes
- ❌ **Penalización**: -0.50€ por cada ensayo no asistido
- 📊 Cálculo automático del total a pagar por miembro
- 📈 Visualización con gráficos interactivos

### Estadísticas
- 📊 Porcentaje de asistencia general
- 📊 Porcentaje por tipo de evento (ensayos/actuaciones)
- 📊 Comparativas entre miembros
- 📊 Gráficos interactivos

## 🚀 Instalación

### 1. Requisitos previos
- **uv** - Gestor de paquetes ultrarrápido para Python

Si no tienes uv instalado:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Instalar dependencias

```bash
uv sync
```

## ▶️ Ejecución

Para iniciar la aplicación:

```bash
uv run streamlit run app.py
```

O usa el script de inicio rápido:
```bash
./iniciar.sh
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Uso

### 1. Agregar Miembros
1. Ir a **👥 Miembros** → **Agregar Miembro**
2. Completar el formulario (el nombre es obligatorio)
3. Click en "Agregar Miembro"

### 2. Crear Eventos
1. Ir a **📅 Eventos** → **Agregar Evento**
2. Seleccionar tipo (Ensayo o Actuación)
3. Completar fecha, descripción, lugar
4. Si es actuación, indicar el importe a repartir
5. Click en "Agregar Evento"

### 3. Registrar Asistencias
1. Ir a **✅ Asistencias** → **Registrar Asistencias**
2. Seleccionar el evento
3. Marcar/desmarcar cada miembro según asistencia
4. Click en "Guardar Asistencias"

### 4. Ver Pagos
1. Ir a **💰 Pagos**
2. Ver el resumen de pagos de todos los miembros
3. Visualizar gráficos de distribución

### 5. Consultar Estadísticas
1. Ir a **📊 Estadísticas**
2. Seleccionar un miembro
3. Ver estadísticas detalladas y comparativas

## 💡 Lógica de Pagos

### Cálculo del Total a Pagar

Para cada miembro:
1. **Suma de actuaciones**: Por cada actuación a la que asistió, recibe su parte proporcional del importe
   - Ejemplo: Actuación de 300€ con 10 asistentes = 30€ por persona
2. **Penalización por ensayos**: Se restan 0.50€ por cada ensayo NO asistido
3. **Total final** = Total de actuaciones - Penalizaciones

### Ejemplo
- Miembro asistió a 2 actuaciones: 300€ (10 asistentes) y 200€ (8 asistentes)
  - Actuación 1: 300€ / 10 = 30€
  - Actuación 2: 200€ / 8 = 25€
  - Total actuaciones: 55€
- Faltó a 3 ensayos: 3 × 0.50€ = 1.50€
- **Total a pagar: 55€ - 1.50€ = 53.50€**

## 🗄️ Base de Datos

La aplicación utiliza SQLite (archivo `asistencias.db`) para almacenar:
- Miembros
- Eventos (ensayos y actuaciones)
- Asistencias

Los datos se guardan automáticamente y persisten entre sesiones.

## 📁 Estructura del Proyecto

```
asistencias-banda/
│
├── app.py              # Aplicación principal Streamlit
├── database.py         # Gestión de base de datos
├── pyproject.toml      # Dependencias y configuración del proyecto (uv)
├── README.md          # Este archivo
└── asistencias.db     # Base de datos SQLite (se crea automáticamente)
```

## 🔧 Personalización

### Cambiar la penalización por ensayo
Editar en `database.py`, línea ~259:
```python
penalizacion = ensayos_no_asistidos * 0.50  # Cambiar 0.50 por el valor deseado
```

### Modificar colores o estilos
Editar el bloque CSS en `app.py`, líneas ~20-30

## 🎯 Funcionalidades Futuras (Opcionales)

- [ ] Exportar reportes a PDF/Excel
- [ ] Notificaciones por email
- [ ] Integración con calendario
- [ ] Sistema de roles (administrador/miembro)
- [ ] Backup automático de base de datos
- [ ] Generación de informes con IA (usando API de OpenAI)

## 🆘 Solución de Problemas

### La aplicación no inicia
```bash
# Reinstalar dependencias
uv sync --reinstall

# Verificar que uv está instalado
uv --version
```

### uv no está instalado
```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reiniciar el terminal y verificar
uv --version
```

### Error de base de datos
Eliminar el archivo `asistencias.db` y reiniciar la aplicación. Se creará una nueva base de datos vacía.

## 📝 Notas

- La base de datos se crea automáticamente la primera vez que ejecutas la aplicación
- Los miembros "eliminados" se desactivan pero mantienen su historial
- Todos los cálculos de pagos se hacen en tiempo real

## 👨‍💻 Desarrollo

Tecnologías utilizadas:
- **uv**: Gestor de paquetes ultrarrápido para Python
- **Streamlit**: Framework de aplicación web
- **SQLite**: Base de datos
- **Pandas**: Manipulación de datos
- **Plotly**: Gráficos interactivos

---

¡Disfruta gestionando tu banda de música! 🎺🎵🎭
