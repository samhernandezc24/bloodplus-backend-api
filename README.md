# BloodPlus Backend con Python Django Rest Framework

Implementación de una API REST de prueba para consumir datos desde el [Frontend de BloodPlus](https://).

Si planean continuar con la construcción de esta API REST, toda la documentación de la que me estoy basando se encuentra disponible en la página oficial de [Django Rest Framework](https://www.django-rest-framework.org/).

Hay que considerar seguir las convenciones comúnmente aceptadas, confundimos a los responsables del mantenimiento de la API y a los clientes que las utilizan, ya que es diferente de lo que todo el mundo espera.

---

## ¿Qué es una API REST?

Una API REST es un estilo de arquitectura de interfaz de programación de aplicaciones que se ajusta a restricciones arquitectónicas específicas, como la comunicación sin estado y los datos almacenables en caché. No es un protocolo ni un estándar. Aunque se puede acceder a las API REST a través de varios protocolos de comunicación, lo más habitual es que se llamen a través de HTTPS, por lo que las siguientes directrices se aplican a los endpoints de las API REST que se llamen a través de Internet.

> Nota: para las API REST a las que se accede a través de Internet, es recomendable seguir las [prácticas recomendadas para la autenticación de API REST](https://stackoverflow.blog/2021/10/06/best-practices-for-authentication-and-authorization-for-rest-apis/).

Si son nuevos en el tema, les recomiendo mucho leer sobre el [modelo cliente-servidor](https://es.wikipedia.org/wiki/Cliente-servidor).

---

# Resumen

Django REST framework es un potente y flexible conjunto de herramientas para construir APIs Web.

Algunas razones por las que se eligió Django Rest Framework:

- [Serialización](https://www.django-rest-framework.org/api-guide/serializers/) ya que soporta tanto fuentes de datos [ORM](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) como fuentes de datos [no-ORM](https://www.django-rest-framework.org/api-guide/serializers/#serializers).
- Personalizable hasta el final - sólo tenemos que utilizar [vistas regulares basadas en funciones](https://www.django-rest-framework.org/api-guide/views/#function-based-views) si no necesitas las [más](https://www.django-rest-framework.org/api-guide/generic-views/) [potentes](https://www.django-rest-framework.org/api-guide/viewsets/) [características](https://www.django-rest-framework.org/api-guide/routers/).
- [Amplia documentación](https://www.django-rest-framework.org/), y [gran apoyo de la comunidad](https://groups.google.com/g/django-rest-framework).

<!--
Esta es la API en producción para propósitos de prueba, disponible aquí.
-->

---

# Requisitos

- Python 3.10+

Desde mi punto de vista les **recomiendo encarecidamente** que sólo apoyó oficialmente la última versión de parche de
cada serie de Python y Django.

Para más información de [instalación de Python](https://www.python.org/).

---

# Primeros pasos

Primero tendrás que clonar el repositorio, honestamente les recomiendo darle seguimiento clonando el repositorio, pero también pueden desde la GUI de Github descargar el ZIP del proyecto.

1. Crea un nuevo directorio en tu máquina local.

2. Si han manejado comandos desde la terminal procedan a abrir el directorio donde quieren poner el proyecto desde la terminal para poder clonar el proyecto con el comando `git clone -b main https://github.com/samhernandezc24/bloodplus-backend-api.git`. Si no saben usar la terminal en dado caso deberían aprender a usar la terminal ya que la mayoría del tiempo estarás ejecutando comandos desde el CLI.

3. En caso de que no obtengas los últimos cambios realizados en el repositorio, ejecuta el siguiente comando: `git pull origin main`.

# Pasos/Comandos

Lo que haremos ahorita será crear un entorno virtual en Python para aislar las librerías que usaremos específicamente en el proyecto de las librerías globales.

> Para más información sobre los virtualenv, checa la [documentación de Python](https://docs.python.org/3/tutorial/venv.html).

1. **Entorno Virtual**: Para crear el entorno virtual, ya dentro del directorio del proyecto procederemos a ejecutar el módulo [venv](https://docs.python.org/3/library/venv.html#module-venv). Esto creará el directorio venv y adicional creará directorios para el intérprete de Python.

```bash
python -m venv venv
```

Una vez creado el entorno virtual, procederemos a activarlo.

```bash
# En Windows, ejecute:
venv\Scripts\activate.bat

# En Mac/Linux, ejecute:
source venv/bin/activate
```

(Este script está escrito para el shell bash. Si usas los shells csh o fish, hay scripts alternativos activate.csh y activate.fish que deberías usar en su lugar).

Activar el entorno virtual cambiará el prompt de tu shell para mostrar qué entorno virtual estás usando, y modificará el entorno para que al ejecutar python obtengas esa versión e instalación particular de Python. Sabrás que tu entorno virtual está activo cuando tu terminal muestre lo siguiente:

```shell
(venv) ruta\a\proyecto\bloodplus-backend-api>
```

2. **Paquetes, Requerimentos**: Puedes instalar, actualizar y eliminar paquetes usando un programa llamado pip. Por defecto pip instalará paquetes del [Índice de Paquetes de Python](https://pypi.org/). pip tiene varios subcomandos: "install", "uninstall", "freeze", etc. Pero para nuestro proyecto me he tomado la molestia de instalar los paquetes necesarios para empezar construyendo la API, he creado un archivo requirements.txt que enlista los paquetes instalados.

A continuación, el archivo `requirements.txt` puede confirmarse en el control de versiones y enviarse como parte de la aplicación. Entonces para instalar todos los paquetes necesarios:

```bash
python -m pip install -r requirements.txt
```

3. **Variables de Entorno**: Es una buena práctica separar la información sensible del proyecto. Hemos instalado un paquete llamado 'python-dotenv' que nos ayuda a gestionar las variables confidenciales fácilmente. Ahora vamos a crear un archivo env para almacenar la información que es específica para nuestro entorno de trabajo. Usa el siguiente comando en tu terminal.

```bash
# En Windows, ejecute:
copy .env.example .env

# En Mac/Linux, ejecute:
cp .env.example .env
```

Puedes usar tu nuevo archivo .env para almacenar claves API, APP_KEY, app_passwords y tendrás acceso a ellas en la aplicación Django. Abrirás ese archivo y generarás una nueva APP_KEY en la [siguiente página](https://djecrety.ir/) y la pondrás ahi `APP_KEY=<clave-generada>` y luego procederás a poner las credenciales que faltan en la configuración de la base de datos.

5. **Servidor local** - Django tiene un servidor de desarrollo integrado que es un servidor web ligero escrito puramente en Python. El servidor de desarrollo de Django nos permite desarrollar cosas rápidamente, sin tener que lidiar con la configuración de un servidor de producción - como Apache - hasta que estés listo para la producción. Utiliza el siguiente comando para iniciar un servidor de desarrollo local.

```bash
python manage.py runserver
```

Deberías ver este registro.

```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 08, 2023 - 17:50:47
Django version 4.2.1, using settings 'bloodplusbackend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Ya debería estar funcionando.

> Nota: Abra un navegador de incógnito cuando pruebe su proyecto (Ctrl + Shift + N)

- Puede acceder a la interfaz API de la aplicación backend en http://localhost:8000

---

## Licencia: MIT
