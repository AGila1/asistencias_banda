#!/bin/bash

echo "🎺 Sistema de Gestión de Asistencias - Asociación Cultural Musical Cabra del Santo Cristo"
echo "======================================================"
echo ""

# Verificar si uv está instalado
if ! command -v uv &> /dev/null; then
    echo "❌ uv no está instalado."
    echo "📥 Instalando uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"

    if ! command -v uv &> /dev/null; then
        echo "❌ Error al instalar uv. Por favor, instálalo manualmente:"
        echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi

echo "✅ uv encontrado"
echo ""

# Sincronizar dependencias
echo "📦 Sincronizando dependencias con uv..."
uv sync
echo "✅ Dependencias sincronizadas"

echo ""
echo "¿Deseas cargar datos de ejemplo? (útil para probar la aplicación)"
echo "1) Sí, cargar datos de ejemplo"
echo "2) No, iniciar con base de datos vacía"
read -p "Selecciona una opción (1/2): " opcion

if [ "$opcion" = "1" ]; then
    echo ""
    echo "📊 Cargando datos de ejemplo..."
    uv run cargar_datos_ejemplo.py
fi

echo ""
echo "🚀 Iniciando aplicación..."
echo ""
echo "La aplicación se abrirá en tu navegador en http://localhost:8501"
echo "Presiona Ctrl+C para detener el servidor"
echo ""

uv run streamlit run app.py
