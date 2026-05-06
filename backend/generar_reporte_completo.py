import os
import sys
import subprocess

def run_tests():
    print("Ejecutando pruebas...")
    # Ejecutar pytest con cobertura y reportes individuales
    subprocess.run([
        sys.executable, "-m", "pytest",
        "--cov=app",
        "--cov-report=html",
        "--html=report.html",
        "--self-contained-html"
    ], check=False)

def combine_reports():
    # Verificar que existan los archivos necesarios
    if not os.path.exists("report.html") or not os.path.exists("htmlcov/index.html"):
        print("Faltan archivos de reporte. Asegúrate de haber ejecutado las pruebas.")
        return

    # Leer el contenido de ambos reportes
    with open("report.html", "r", encoding="utf-8") as f:
        pytest_content = f.read()

    # Extraer la tabla de resumen de cobertura desde htmlcov/index.html
    with open("htmlcov/index.html", "r", encoding="utf-8") as f:
        coverage_html = f.read()
        # Tomar solo la tabla de resumen (extraemos la parte útil)
        start_marker = '<table class="index">'
        end_marker = '</table>'
        if start_marker in coverage_html and end_marker in coverage_html:
            start_idx = coverage_html.find(start_marker)
            end_idx = coverage_html.find(end_marker, start_idx) + len(end_marker)
            coverage_summary = coverage_html[start_idx:end_idx]
        else:
            coverage_summary = "<p>No se pudo extraer el resumen de cobertura.</p>"

    # Construir el reporte combinado
    combined = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reciclap - Reporte de Pruebas y Cobertura</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 2em; background: #f5f0e8; }}
        h1, h2 {{ color: #2e7d32; }}
        .report-container {{ background: white; padding: 1.5em; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 2em; }}
    </style>
</head>
<body>
    <h1>♻️ Reciclap - Reporte de Pruebas y Cobertura</h1>
    <div class="report-container">
        <h2>📋 Resultados de Pruebas</h2>
        {pytest_content}
    </div>
    <div class="report-container">
        <h2>📊 Resumen de Cobertura</h2>
        {coverage_summary}
        <p><a href="htmlcov/index.html" target="_blank">Ver cobertura detallada</a></p>
    </div>
</body>
</html>"""

    # Guardar el reporte combinado
    with open("reporte_completo.html", "w", encoding="utf-8") as f:
        f.write(combined)

    print("Reporte combinado generado: reporte_completo.html")

if __name__ == "__main__":
    run_tests()
    combine_reports()