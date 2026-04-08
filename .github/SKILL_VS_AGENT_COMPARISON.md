# 🎯 Comparación: Skill vs Agente Personalizado

## Ejemplos Creados

### 📚 SKILL: streamlit-feature
**Ubicación**: `.github/skills/streamlit-feature/SKILL.md`

### 🤖 AGENTE: attendance-analyzer
**Ubicación**: `.github/agents/attendance-analyzer.agent.md`

---

## 🔍 Diferencias Fundamentales

| Aspecto | SKILL | AGENTE |
|---------|-------|--------|
| **Qué es** | Conocimiento especializado | Subagente autónomo |
| **Quién ejecuta** | GitHub Copilot (yo) con conocimiento adicional | Subagente independiente |
| **Cuándo se activa** | Automáticamente cuando se detecta la tarea | Manualmente con `@nombre-agente` |
| **Objetivo** | **Guiar** cómo hacer las tareas | **Ejecutar** tareas específicas |
| **Puede editar código** | ✅ Sí (yo lo hago siguiendo el skill) | ⚠️ Según configuración en `tools:` |
| **Devuelve** | Implementación directa | Reporte final único |
| **Interacción** | Conversacional (múltiples turnos) | Autónomo (ejecuta y devuelve) |

---

## 📚 SKILL: streamlit-feature

### Propósito
Cuando me pidas **añadir funcionalidades** a la app de banda, yo cargo este skill primero y sigo sus mejores prácticas.

### ¿Cuándo se usa?
```
Usuario: "Agrega una página para exportar datos a Excel"
GitHub Copilot: [Carga streamlit-feature.SKILL.md automáticamente]
                 [Implementa siguiendo los patrones del skill]
```

### ¿Qué contiene?
- **Architecture Patterns**: Estructura de páginas, queries, visualizaciones
- **Payment Logic**: Reglas de cálculo específicas del dominio
- **Best Practices**: Convenciones del proyecto (emojis, forms, charts)
- **Example Code**: Snippets reutilizables

### Ejemplo de uso:
```
Tú: "Añade un gráfico de asistencias por mes"

Yo: [Leo streamlit-feature SKILL.md]
    [Sigo los patrones: plotly + Database class + page structure]
    [Implemento el código directamente en app.py]
```

### Ventajas
✅ Garantiza consistencia con tu código existente
✅ Evita reinventar patrones que ya funcionan
✅ Yo aprendo las convenciones específicas de tu proyecto
✅ Múltiples interacciones posibles (puedes pedir ajustes)

---

## 🤖 AGENTE: attendance-analyzer

### Propósito
Cuando necesites **análisis de datos**, invocas este agente que trabaja solo y te devuelve un reporte completo.

### ¿Cuándo se usa?
```
Usuario: "@attendance-analyzer Analiza las asistencias del último mes"
Subagente: [Se ejecuta de forma autónoma]
           [Lee database.py, consulta datos]
           [Calcula métricas, identifica patrones]
           [Devuelve un reporte markdown completo]
GitHub Copilot: [Te muestra el reporte que el agente devolvió]
```

### ¿Qué contiene?
- **Mission**: Analizar patrones de asistencia y pagos
- **Analysis Framework**: Qué métricas calcular
- **Report Format**: Estructura del output esperado
- **Tools**: Herramientas limitadas (read_file, grep_search, semantic_search - solo lectura)

### Ejemplo de uso:
```
Tú: "@attendance-analyzer Identifica miembros problemáticos"

Subagente autónomo:
  1. Lee database.py y app.py
  2. Busca métodos de consulta
  3. Analiza la lógica de pagos
  4. Identifica patrones (e.g., asiste solo a actuaciones)
  5. Calcula métricas
  6. Genera reporte markdown

Yo (GitHub Copilot):
  [Recibo el reporte del subagente]
  [Te lo muestro con un resumen]
```

### Ventajas
✅ Ejecución autónoma sin supervisión
✅ Especializado en UNA tarea específica
✅ Restricción de herramientas (read-only para análisis)
✅ Output predecible y estructurado

---

## 🎭 Casos de Uso Comparados

### Escenario 1: Añadir feature de exportación a Excel

**Con SKILL (streamlit-feature)**:
```
Tú: "Agrega un botón para exportar pagos a Excel"
Copilot: [Cargo streamlit-feature SKILL]
         [Sigo patrones: st.button, pd.ExcelWriter, st.download_button]
         [Escribo el código en app.py]
         [Confirmo: "Listo, botón agregado en página Pagos"]
```

**Con AGENTE (attendance-analyzer)**:
```
❌ No es apropiado - El agente es solo para ANÁLISIS, no para añadir features
```

---

### Escenario 2: Generar reporte mensual de asistencias

**Con SKILL (streamlit-feature)**:
```
Tú: "Genera un reporte de asistencias del último mes"
Copilot: [Cargo streamlit-feature SKILL]
         [Añado una página "Reportes" siguiendo los patrones]
         [Implemento queries y visualizaciones]

❌ Problema: Estoy ADD code, pero no analizo datos existentes
```

**Con AGENTE (attendance-analyzer)**:
```
Tú: "@attendance-analyzer Analiza asistencias del último mes"
Agente: [Se ejecuta autónomamente]
        [Lee la base de datos]
        [Calcula métricas]
        [Devuelve reporte completo con insights]

✅ Perfecto: El agente analiza y reporta sin modificar nada
```

---

## 🧠 ¿Cuándo usar cada uno?

### Usa SKILL cuando:
- ✅ Necesitas **implementar código** siguiendo convenciones
- ✅ Quieres **garantizar consistencia** en el proyecto
- ✅ Vas a hacer **múltiples cambios** relacionados
- ✅ Puede haber **ida y vuelta** (ajustes, refinamiento)

**Ejemplos para tu proyecto**:
- Añadir página de estadísticas avanzadas
- Implementar sistema de notificaciones por email
- Crear feature de gestión de multas personalizadas
- Refactorizar visualizaciones

### Usa AGENTE cuando:
- ✅ Necesitas **análisis autónomo** de datos/código
- ✅ Quieres **aislar contexto** (el agente no ve toda la conversación)
- ✅ La tarea tiene **output predecible** (reporte, análisis)
- ✅ Quieres **restricción de herramientas** (e.g., solo lectura)

**Ejemplos para tu proyecto**:
- Análisis mensual de participación
- Identificar patrones de asistencia problemáticos
- Generar insights financieros
- Auditoría de datos de la base de datos

---

## 📁 Estructura de Archivos

```
asistencias banda/
├── .github/
│   ├── skills/
│   │   └── streamlit-feature/
│   │       └── SKILL.md              ← Conocimiento (yo lo cargo)
│   │
│   └── agents/
│       └── attendance-analyzer.agent.md  ← Subagente (invocación manual)
│
├── app.py
├── database.py
└── README.md
```

---

## 🎬 Probémoslo

### 1️⃣ Prueba el SKILL

Pídeme:
```
"Agrega un gráfico circular que muestre la distribución de instrumentos en la banda"
```

Yo automáticamente cargaré `streamlit-feature` SKILL y seguiré sus patrones.

### 2️⃣ Prueba el AGENTE

Pídeme:
```
"@attendance-analyzer Analiza los datos actuales y dame insights"
```

El agente se ejecutará, leerá tu database.py/app.py, y devolverá un reporte.

---

## ✨ Resumen

- **SKILL** = Yo (GitHub Copilot) + **conocimiento especializado** → Implemento código
- **AGENTE** = **Subagente autónomo** → Ejecuta tarea y devuelve resultado

Ambos son complementarios y se pueden usar en el mismo proyecto! 🚀
