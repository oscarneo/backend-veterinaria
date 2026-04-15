# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Cloud Run usa la variable de entorno PORT (por defecto 8080)
ENV PORT 8080

# Comando para ejecutar la app
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT