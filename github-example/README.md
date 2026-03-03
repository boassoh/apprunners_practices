# GitHub Integration Example

Esta carpeta contiene una versión simplificada de la aplicación diseñada específicamente para funcionar con la integración directa de App Runner con GitHub.

## Diferencias con la versión principal:

- **Sin Dockerfile**: App Runner usa su build nativo de Python
- **Flask 2.3.0**: Versión más estable y compatible
- **Estructura simple**: Solo los archivos esenciales

## Archivos:

- `app.py` - Aplicación Flask
- `requirements.txt` - Dependencias (Flask 2.3.0)
- `templates/index.html` - Template HTML

## Uso en App Runner:

1. **Source directory**: `/github-example`
2. **Runtime**: Python 3
3. **Build command**: `pip install -r requirements.txt`
4. **Start command**: `python app.py`
5. **Port**: 8080
