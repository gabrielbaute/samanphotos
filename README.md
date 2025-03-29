# 🐍 **SamanPhotos** 📸

¡Bienvenidos! SamanPhotos es un proyecto personal desarrollado para aprender y mejorar mis habilidades en Python y en el desarrollo de aplicaciones web. La aplicación permite a los usuarios subir, gestionar y visualizar fotos, además de proporcionar varias características adicionales como la geolocalización de las fotos y la descarga de imágenes. Ya iremos agregando más cosas en el futuro. La estética y apariencia es en base a [Bulma-CSS](https://bulma.io/)

## **Funcionalidades** ✨

- **🔐Autenticación de Usuarios**: Registro e inicio de sesión de usuarios. También se incluye información de seguridad como historial de sesiones y registro de auditoría como cambios de contraseñas.
- **📁Gestión de Fotos y Álbumes**: Subir, visualizar, eliminar y crear álbumes de fotos.
- **🗺️Geolocalización**: Visualización de fotos en un mapa interactivo utilizando OpenStreetMap.
- **⬇️Descarga de Fotos**: Descargar fotos individuales con su nombre original.
- **🔍Información de Seguridad**: Visualización de datos de inicio de sesión como la última IP, fecha de último inicio de sesión, etc.

Otras funcionalidades de backend ya han sido agregadas, como un log del sistema, un panel de administrador para consultar el log sin tener que acceder al directorio raíz, estadísticas de los usuarios y la implementación de un servidor para producción (waitress, pronto soporte para gunicorn).

## **En desarrollo** 🚧

- **🔌API**: ⚠️ En desarrollo, de momento cumple con las funciones básicas CRUD, pero no se ha probado.
- **👷Face Recognition**: ⚠️ En desarrollo, se están usando las librerías dlib y face-recognition, pero aún hay mucho que aprender sobre cómo usar esta biblioteca, si tienen alguna idea o alternativas, es bienvenida! (estoy desarrollando esto en un entorno Windows).
- **📅Recuerdos**: 🚧 Apenas estamos comenzando.
- **✏️Edición de Perfil**: 🚧 Detenido, pronto retomaremos esta parte.
- **📫Confirmación de cuenta mediante token**: ✅ Completado.

## **Problemas a corregir**

El proyecto aún tiene algunos problemas, como lo que respecta al manejo de albumes, en los que aún falta mucho por desarrollar, y hay algunos bugs presente (no he logrado crear correctamente los albumes cuando se suben fotos al mismo tiempo en el formulario). 

## **Instalación** ⚙️

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/gabrielbaute/samanphotos
   cd SamanPhotos
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno:
   Crea un archivo `.env` en el directorio raíz del proyecto y añade las siguientes variables:
   
   | Variable | Descripción |
   |----------|-------------|
   | `SECRET_KEY` | Clave secreta para la seguridad de la aplicación |
   | `SQLALCHEMY_DATABASE_URI` | URI de la base de datos SQLite |
   | `MAIL_SERVER` | Servidor SMTP para el envío de correos |
   | `MAIL_PORT` | Puerto del servidor SMTP |
   | `MAIL_USERNAME` | Nombre de usuario del correo |
   | `MAIL_PASSWORD` | Contraseña del correo |
   | `MAIL_USE_TLS` | Usar TLS (True/False) |
   | `MAIL_USE_SSL` | Usar SSL (True/False) |
   | `MAIL_DEFAULT_SENDER` | Remitente predeterminado del correo |
   | `SECURITY_PASSWORD_SALT` | Sal para la seguridad de las contraseñas |
   | `JWT_SECRET_KEY` | Clave secreta para JWT |
   | `ADMIN_EMAIL` | Correo electrónico del administrador |
   | `ADMIN_PASSWORD` | Contraseña del administrador |
   | `UPLOAD_FOLDER` | Carpeta para las subidas de fotos |

5. Generar claves secretas:
   Utiliza el script `generate_keys.py` para generar los valores de `SECRET_KEY`, `JWT_SECRET_KEY` y `SECURITY_PASSWORD_SALT`.
   ```bash
   python generate_keys.py
   ```

6. Ejecutar la aplicación:
   ```bash
   py production.py
   ```

   Si requieres realizar pruebas o probar un entorno de desarrollo, ejecuta:
   ```bash
   py run.py
   ```

## **Futuras Mejoras** 🚀

- **💄Mejora de la UI**: Refinar la interfaz de usuario para una mejor experiencia. El objetivo es que se asemeje un poco a Google Photos, si bien Bulma (el framework css que estoy usando) quizás no sea lo más apropiado para esto. Con el tiempo, en la medida en que se pula la parte estética y se agreguen más funciones, decidiré si mantengo la estética minimalista de Bulma o si logro implementar un diseño más semejante a Google.
- **☁️Soporte para Otros Proveedores de Almacenamiento**: Añadir soporte para almacenamiento en la nube como AWS S3.
- **🔔Notificaciones**: Implementar notificaciones por correo electrónico para eventos importantes, recuerdos, etc.
- **🔐Seguridad**: Hay muchas mejoras que se pueden realizar en el plan ode la seguridad. Sin embargo, aún estamos discutiendo cuántos de estos elementos pueden ser necesarios, como un 2FA o iniciar sesión mediante aplicaciones de terceros (Google, Microsoft, Github, etc). Parte de las funciones necesarias para el 2FA (usando autenticador de google, por ejemplo) ya están dentro del código, pero no se han implementado aún.

## **Deploy en Docker**

Esta primera versión del servidor está pensada para desplegarse en docker y operar como web primeramente. Estamos en fase de evaluación, así que si prueban el servicio e implementan cambios que ven funcionales o soluciones prácticas, agradecemos cualquier contribución o comentario.

## Cómo Desplegar la Aplicación en Docker

### Prerrequisitos
Asegúrate de tener instalado lo siguiente:
- [Docker](https://www.docker.com/) (versión 20+ recomendada).
- [Docker Compose](https://docs.docker.com/compose/) (versión 3.8+ recomendada).

### Instrucciones para Despliegue

#### 1. Clona el repositorio
Primero, descarga el código fuente desde el repositorio:

```bash
git clone https://github.com/usuario/samanphotos.git
cd samanphotos
```

#### 2. Configura las variables de entorno
Edita el archivo `.env` en el directorio raíz del proyecto con las siguientes variables:

```env
FLASK_ENV=production
PORT=5000
DEBUG=False
SQLALCHEMY_DATABASE_URI=sqlite:////app/instance/octopus.db
SECRET_KEY=tu_clave_secreta_segura
```

#### 3. Construye y ejecuta los contenedores
Usa Docker Compose para construir las imágenes y levantar los servicios:

```bash
docker-compose up --build
```

Esto realizará las siguientes acciones:
- Construirá la imagen de la aplicación Flask desde el Dockerfile.
- Montará los volúmenes locales necesarios (`instance`, `logs`, `uploads`).
- Expondrá la aplicación en el puerto definido (por defecto, `5000`).

#### 4. Accede a la aplicación
Una vez que los contenedores estén en funcionamiento, accede a la aplicación desde tu navegador en la dirección:

```
http://localhost:5000
```

> Nota: Si cambias el puerto en el archivo `.env`, actualiza también el URL.

#### 5. Verifica el estado de los contenedores
Usa el siguiente comando para verificar los contenedores en ejecución:

```bash
docker ps
```

Esto mostrará información como el nombre del contenedor y el puerto en el que está escuchando.

#### 6. Detén los servicios
Cuando quieras detener la aplicación, usa:

```bash
docker-compose down
```

Esto eliminará los contenedores activos, pero conservará los datos en los volúmenes (`instance`, `logs`, `uploads`).

---

### Solución de Problemas

#### El contenedor no inicia
Verifica los logs del contenedor para diagnosticar problemas:

```bash
docker logs samanphotos
```

#### El servicio no responde en el navegador
Asegúrate de que el puerto definido en `.env` esté correctamente expuesto y no esté bloqueado por tu firewall.

#### Necesito reconstruir la imagen
Si realizas cambios en el código fuente y necesitas reconstruir la imagen, ejecuta:

```bash
docker-compose up --build
```

---

### Notas Adicionales
- **Entorno de Producción:** Este despliegue está configurado para producción usando `waitress` como servidor. Puedes ajustar el archivo `production.py` para otras configuraciones específicas.
- **Persistencia de Datos:** Los volúmenes montados aseguran que la base de datos SQLite, los logs y las fotos subidas permanezcan incluso después de detener los contenedores.
- **Extensiones:** Si decides usar una base de datos diferente (como PostgreSQL), puedes extender el archivo `docker-compose.yml` para incluir un servicio adicional.

---

## **Contribuciones** 🙌

Cualquier sugerencia o feedback es bienvenido para mejorar y aprender más en este camino de desarrollo. Tengo poco menos de un año dedicado (de forma más constante) al estudio de Python y el desarrollo de aplicaciones, aunque manejo el lenguaje desde hace por lo menos dos. El desarrollo de este tipo de aplicaciones es, por los momentos, una tarea que emprendo por puro deseo de aprender y resolver problemas que se me presentan a mi o a personas que conozco. Cualquier contribución, corrección, observación y/o acotación es totalmente bienvenida.

## **Autor** 🧑‍💻

Proyecto desarrollado por [Gabriel Baute](https://github.com/gabrielbaute). Si tienes alguna pregunta, no dudes en contactarme a través de mi [gabrielbaute@gmail.com](mailto:gabrielbaute@gmail.com).