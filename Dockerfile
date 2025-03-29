# Usar una imagen base de Python 3.13
FROM python:3.13-slim

# Evitar consultas interactivas durante la instalación de paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos e instalar las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Crear las carpetas necesarias
RUN mkdir -p instance uploads logs

# Establecer las variables de entorno predeterminadas
ENV FLASK_ENV=production
ENV PORT=5000

# Exponer el puerto en el que corre la aplicación
EXPOSE ${PORT}

# Comando para correr la aplicación usando waitress
CMD ["python", "production.py"]