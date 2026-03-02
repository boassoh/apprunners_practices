#!/bin/bash

# Script para generar carga y observar el escalado de App Runner
# Configuración: Max concurrency = 5, Max instances = 3

URL="$1"

if [ -z "$URL" ]; then
    echo "Uso: ./load_test.sh <app-runner-url>"
    echo "Ejemplo: ./load_test.sh https://nw9i2pv6pj.eu-central-1.awsapprunner.com"
    exit 1
fi

echo "🚀 Iniciando prueba de carga..."
echo "📊 Configuración: 5 requests concurrentes por instancia, máximo 3 instancias"
echo "🎯 URL: $URL"
echo "⏱️  Duración: 5 minutos"
echo ""

# Función para enviar requests continuos
send_requests() {
    local end_time=$((SECONDS + 300))
    while [ $SECONDS -lt $end_time ]; do
        curl -s "$URL" > /dev/null &
        sleep 0.1
    done
}

echo "⏳ Enviando requests concurrentes durante 5 minutos..."
echo "📈 Abre la consola de App Runner ahora para observar el escalado"
echo ""

# Iniciar 15 procesos concurrentes enviando requests
for i in {1..15}; do
    send_requests &
done

# Esperar a que terminen todos los procesos
wait

echo ""
echo "✅ Prueba completada"
echo ""
echo "📊 Verifica en la consola de App Runner:"
echo "   - Número de instancias activas (debería haber escalado a 3)"
echo "   - Métricas de 'Active instances' en CloudWatch"
echo "   - Logs de la aplicación"
