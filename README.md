# 🐍 SamanPhotos 📸

¡Bienvenidos! SamanPhotos es un proyecto personal desarrollado para aprender y mejorar mis habilidades en Python y en el desarrollo de aplicaciones web. La aplicación permite a los usuarios subir, gestionar y visualizar fotos, además de proporcionar varias características adicionales como la geolocalización de las fotos y la descarga de imágenes. Ya iremos agregando más cosas en el futuro. La estética y apariencia es en base a [Bulma-CSS](https://bulma.io/)

## Funcionalidades ✨

- **🔐Autenticación de Usuarios**: Registro e inicio de sesión de usuarios.
- **📁Gestión de Fotos y Álbumes**: Subir, visualizar, eliminar y crear álbumes de fotos.
- **🗺️Geolocalización**: Visualización de fotos en un mapa interactivo utilizando OpenStreetMap.
- **⬇️Descarga de Fotos**: Descargar fotos individuales con su nombre original.
- **✏️Edición de Perfil**: Actualizar información del perfil como nombre, correo, contraseña, etc.
- **🔍Información de Seguridad**: Visualización de datos de inicio de sesión como la última IP, fecha de último inicio de sesión, etc.

## En desarrollo 🚧

- **🔌API**: 🚧 En desarrollo, de momento cumple con las funciones básicas CRUD, pero no se ha probado.
- **👷Face Recognition**: 🚧 En desarrollo, se están usando las librerías dlib y face-recognition, pero aún hay mucho que aprender sobre cómo usar esta biblioteca, si tienen alguna idea o alternativas, es bienvenida! (estoy desarrollando esto en un entorno Windows).
- **📅Recuerdos**: 🚧 Apenas estamos comenzando.
- **📫Confirmación de cuenta mediante token**: 🚧 Apenas comenzando.

## Problemas a corregir

El proyecto aún tiene algunos problemas, como lo que respecta al manejo de albumes, en los que aún falta mucho por desarrollar, y hay algunos bugs presente (no he logrado crear correctamente los albumes cuando se suben fotos al mismo tiempo en el formulario). 

## Instalación ⚙️

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
   flask run
   ```

## Futuras Mejoras 🚀

- **💄Mejora de la UI**: Refinar la interfaz de usuario para una mejor experiencia. El objetivo es que se asemeje un poco a Google Photos, si bien Bulma (el framework css que estoy usando) quizás no sea lo más apropiado para esto. Con el tiempo, en la medida en que se pula la parte estética y se agreguen más funciones, decidiré si mantengo la estética minimalista de Bulma o si logro implementar un diseño más semejante a Google.
- **☁️Soporte para Otros Proveedores de Almacenamiento**: Añadir soporte para almacenamiento en la nube como AWS S3.
- **🔔Notificaciones**: Implementar notificaciones por correo electrónico para eventos importantes, recuerdos, etc.
- **🔐Seguridad**: Mejorar, en la medida en que el proceso de investigación de las herramientas continúa, toda la seguridad de la gestión de las cuentas de usuario y su información, con el objetivo de hacer la app más segura y proteger información sensible (son nuestras fotografías).

## Contribuciones 🙌

Cualquier sugerencia o feedback es bienvenido para mejorar y aprender más en este camino de desarrollo. Tengo poco menos de un año dedicado (de forma más constante) al estudio de Python y el desarrollo de aplicaciones, aunque manejo el lenguaje desde hace por lo menos dos. El desarrollo de este tipo de aplicaciones es, por los momentos, una tarea que emprendo por puro deseo de aprender y resolver problemas que se me presentan a mi o a personas que conozco. Cualquier contribución, corrección, observación y/o acotación es totalmente bienvenida.

## Autor 🧑‍💻

Proyecto desarrollado por [Gabriel Baute](https://github.com/gabrielbaute). Si tienes alguna pregunta, no dudes en contactarme a través de mi [gabrielbaute@gmail.com](mailto:gabrielbaute@gmail.com).