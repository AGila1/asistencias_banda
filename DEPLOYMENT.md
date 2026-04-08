# 🚀 Guía de Despliegue en Streamlit Cloud + Supabase

## Paso 1: Crear Proyecto en Supabase

### 1.1 Ir a Supabase
- Accede a [supabase.com](https://supabase.com)
- Click en **"Start your project"** (Sign up si no tienes cuenta)

### 1.2 Crear un nuevo proyecto
- Click en **"New Project"**
- Completa:
  - **Project name**: `banda-asistencias` (o el nombre que prefieras)
  - **Database password**: Crea una contraseña fuerte
  - **Region**: Selecciona la más cercana a ti (España → `eu-west-1`)
  - Click **"Create new project"**

⏳ Espera ~2 minutos a que el proyecto se deployed

### 1.3 Obtener credenciales
- Ve a **Settings** → **API** (menú izquierdo)
- Copia:
  - **Project URL** → `SUPABASE_URL`
  - **anon public** key → `SUPABASE_KEY`
- Guárdalas en un lugar seguro

## Paso 2: Crear Tablas en Supabase

### 2.1 Ir al SQL Editor
- Click en **SQL Editor** (menú izquierdo)
- Click en **"New Query"**

### 2.2 Copiar y ejecutar este SQL

```sql
-- Tabla de miembros
CREATE TABLE miembros (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre TEXT NOT NULL,
    apellidos TEXT DEFAULT '',
    instrumento TEXT DEFAULT '',
    email TEXT DEFAULT '',
    telefono TEXT DEFAULT '',
    activo BOOLEAN DEFAULT TRUE,
    fecha_alta TIMESTAMP DEFAULT NOW()
);

-- Tabla de eventos
CREATE TABLE eventos (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tipo TEXT NOT NULL CHECK(tipo IN ('ensayo', 'actuacion')),
    fecha DATE NOT NULL,
    descripcion TEXT DEFAULT '',
    lugar TEXT DEFAULT '',
    importe NUMERIC(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de asistencias
CREATE TABLE asistencias (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    miembro_id BIGINT NOT NULL REFERENCES miembros(id) ON DELETE CASCADE,
    evento_id BIGINT NOT NULL REFERENCES eventos(id) ON DELETE CASCADE,
    asistio BOOLEAN NOT NULL,
    observaciones TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(miembro_id, evento_id)
);

-- Index para mejorar consultas
CREATE INDEX idx_asistencias_miembro ON asistencias(miembro_id);
CREATE INDEX idx_asistencias_evento ON asistencias(evento_id);
CREATE INDEX idx_eventos_fecha ON eventos(fecha DESC);
```

- Click en **"Run"** o `Ctrl+Enter`
- ✅ Verás el mensaje "Success"

### 2.3 Habilitar RLS (Row Level Security) - OPCIONAL pero recomendado

Para permitir acceso público sin autenticación:

```sql
-- Deshabilitar RLS para permitir acceso sin autenticación
ALTER TABLE miembros DISABLE ROW LEVEL SECURITY;
ALTER TABLE eventos DISABLE ROW LEVEL SECURITY;
ALTER TABLE asistencias DISABLE ROW LEVEL SECURITY;
```

## Paso 3: Instalar dependencias localmente

```bash
cd /Users/cx02150/ai_test/asistencias_banda
uv sync
```

## Paso 4: Configurar secretos localmente

### 4.1 Crear archivo de secretos
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### 4.2 Editar `.streamlit/secrets.toml`
```toml
[supabase]
url = "https://YOUR_PROJECT_ID.supabase.co"
key = "YOUR_ANON_PUBLIC_KEY"
```

Reemplaza con tus valores de Supabase (Paso 1.3)

### 4.3 Guardar en .gitignore
```bash
# Ya debería estar incluido, pero verifica
echo ".streamlit/secrets.toml" >> .gitignore
```

## Paso 5: Probar localmente

```bash
uv run streamlit run app.py
```

Si ves errores, revisa:
- ✅ Las credenciales en `.streamlit/secrets.toml` son correctas
- ✅ Las tablas se crearon en Supabase
- ✅ RLS está deshabilitado (o configurado correctamente)

## Paso 6: Desplegar en Streamlit Cloud

### 6.1 Preparar el repositorio
```bash
cd /Users/cx02150/ai_test/asistencias_banda
git add -A
git commit -m "Migración a Supabase"
git push
```

### 6.2 Ir a Streamlit Cloud
- Accede a [share.streamlit.io](https://share.streamlit.io)
- Click en **"New app"**
- Selecciona:
  - **Repository**: Tu repositorio de GitHub
  - **Branch**: `main`
  - **Main file path**: `app.py`

### 6.3 Configurar secretos en Streamlit Cloud
- Click en **"Advanced settings"** en la página de deploy
- Pega en el campo de texto:
```toml
[supabase]
url = "https://YOUR_PROJECT_ID.supabase.co"
key = "YOUR_ANON_PUBLIC_KEY"
```

- Click en **"Deploy"**

⏳ Espera ~2 minutos a que compile

## Paso 7: Verificar el despliegue

- Tu app debería estar en: `https://banda-asistencias.streamlit.app`
- Verifica que:
  - ✅ Se carga sin errores
  - ✅ Puedes agregar miembros
  - ✅ Los datos persisten (actualiza la página)
  - ✅ Las actualizaciones se guardan en Supabase

## 🔧 Troubleshooting

### "Error: No se encontraron las credenciales de Supabase"
- Verifica que `.streamlit/secrets.toml` existe y tiene:
  ```toml
  [supabase]
  url = "..."
  key = "..."
  ```
- En Streamlit Cloud, ve a **Settings** → **Secrets** y verifica los valores

### "relation 'miembros' does not exist"
- Las tablas no se crearon en Supabase
- Ve a SQL Editor en Supabase y ejecuta el script del Paso 2.2

### Datos no se guardan
- Verifica RLS en Supabase (Paso 2.3)
- Comprueba que tienes permisos de escritura en la clave API

### Lento en cargar
- Probable: Streamlit está en el tier gratuito que hiberna
- Solución: Usa el app durante los primeros 7 días
- Upgrade a Streamlit Cloud Pro para mejor rendimiento

## 📊 Monitoring

### Ver estadísticas de base de datos
- En Supabase → **Database** → puedes ver uso de storage y logs

### Ver logs de la app en Streamlit Cloud
- En Streamlit Cloud → Tu app → **Settings** → **Logs**

## 💰 Costos (tier gratuito)

| Servicio | Límite Gratuito | Costo si excede |
|----------|-----------------|-----------------|
| **Supabase** | 500MB BD, 2GB storage | $10+/mes |
| **Streamlit Cloud** | 1 app ilimitado | $5+/mes |
| **Total** | **Gratis** | ~$15/mes si crece |

Para una banda pequeña, estos límites deberían ser más que suficientes.

