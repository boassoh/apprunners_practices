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
echo "📊 Objetivo: Escalar de 1 a 3 instancias"
echo "🎯 URL: $URL"
echo "⏱️  Duración: 5 minutos"
echo ""

# Función para enviar requests continuos
send_requests() {
    local worker_id=$1
    local count=0
    local success=0
    local errors=0
    local end_time=$((SECONDS + 300))
    
    while [ $SECONDS -lt $end_time ]; do
        response=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null)
        ((count++))
        
        if [ "$response" = "200" ]; then
            ((success++))
        else
            ((errors++))
        fi
        
        # Mostrar progreso cada 20 requests
        if [ $((count % 20)) -eq 0 ]; then
            echo "[Worker $worker_id] $count requests | ✓ $success | ✗ $errors"
        fi
        
        sleep 0.3
    done
    
    echo "[Worker $worker_id] Completado: $count total | ✓ $success | ✗ $errors"
}

echo "⏳ Iniciando 25 workers concurrentes..."
echo "📈 Abre App Runner Console AHORA para ver el escalado en tiempo real"
echo ""
echo "Esperando 3 segundos antes de iniciar..."
sleep 3
echo ""

# Iniciar 25 workers (suficiente para forzar 3 instancias con sleep(1))
for i in {1..25}; do
    send_requests $i &
done

# Esperar a que terminen
wait

echo ""
echo "✅ Prueba completada"
echo ""
echo "📊 Verifica en App Runner Console:"
echo "   - Active instances debería mostrar 3"
echo "   - CloudWatch Metrics > ActiveInstances"
echo "   - Logs para ver requests procesados"
