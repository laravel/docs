# Directory Structure

- [Introducción](#introduction)
- [Directorio raíz](#the-root-directory)
    - [`app`](#the-root-app-directory)
    - [`bootstrap`](#the-bootstrap-directory)
    - [`config`](#the-config-directory)
    - [`database`](#the-database-directory)
    - [`public`](#the-public-directory)
    - [`resources`](#the-resources-directory)
    - [`routes`](#the-routes-directory)
    - [`storage`](#the-storage-directory)
    - [`tests`](#the-tests-directory)
    - [`vendor`](#the-vendor-directory)
- [Directorio App](#the-app-directory)
    - [`Broadcasting`](#the-broadcasting-directory)
    - [`Console`](#the-console-directory)
    - [`Events`](#the-events-directory)
    - [`Exceptions`](#the-exceptions-directory)
    - [`Http`](#the-http-directory)
    - [`Jobs`](#the-jobs-directory)
    - [`Listeners`](#the-listeners-directory)
    - [`Mail`](#the-mail-directory)
    - [`Models`](#the-models-directory)
    - [`Notifications`](#the-notifications-directory)
    - [`Policies`](#the-policies-directory)
    - [`Providers`](#the-providers-directory)
    - [`Rules`](#the-rules-directory)

<a name="introduction"></a>
## Introducción

La estructura por defecto de la aplicación Laravel está pensada para proporcionar un gran punto de partida tanto para aplicaciones grandes como pequeñas. Pero eres libre de organizar tu aplicación como quieras. Laravel no impone casi ninguna restricción en cuanto a la ubicación de las clases, siempre y cuando Composer pueda autocargar la clase.

> NOTA  
> ¿Eres nuevo en Laravel? Echa un vistazo al [Laravel Bootcamp](https://bootcamp.laravel.com) para un tour práctico del framework mientras te guiamos en la construcción de tu primera aplicación Laravel.

<a name="the-root-directory"></a>
## El directorio raíz

<a name="the-root-app-directory"></a>
#### El directorio de aplicaciones

El directorio `app` contiene el código central de tu aplicación. Exploraremos este directorio con más detalle próximamente; sin embargo, casi todas las clases de tu aplicación estarán en este directorio.

<a name="the-bootstrap-directory"></a>
#### El directorio Bootstrap

El directorio `bootstrap` contiene el archivo `app.php` que arranca el framework. Este directorio también contiene un directorio `cache` que contiene archivos generados por el framework para optimizar el rendimiento, como archivos de caché de rutas y servicios.

<a name="the-config-directory"></a>
#### El directorio Config

El directorio `config`, como su nombre indica, contiene todos los archivos de configuración de tu aplicación. Es una gran idea leer todos estos archivos y familiarizarse con todas las opciones disponibles.

<a name="the-database-directory"></a>
#### El directorio de la base de datos

El directorio `database` contiene tus migraciones de base de datos, fábricas de modelos y semillas. Si lo desea, también puede utilizar este directorio para alojar una base de datos SQLite.

<a name="the-public-directory"></a>
#### El directorio público

El directorio `public` contiene el archivo `index.php`, que es el punto de entrada para todas las peticiones que entran en su aplicación y configura la carga automática. Este directorio también alberga sus activos como imágenes, JavaScript y CSS.

<a name="the-resources-directory"></a>
#### El directorio de recursos

El directorio `resources` contiene sus [views](/docs/{{version}}/views) así como sus activos sin compilar, como CSS o JavaScript.

<a name="the-routes-directory"></a>
#### El directorio de rutas

El directorio `routes` contiene todas las definiciones de rutas para tu aplicación. Por defecto, Laravel incluye dos archivos de rutas: `web.php` y `console.php`.

El archivo `web.php` contiene rutas que Laravel coloca en el grupo de middleware `web`, que proporciona el estado de sesión, protección CSRF, y el cifrado de cookies. Si tu aplicación no ofrece una API RESTful sin estado, lo más probable es que todas tus rutas estén definidas en el archivo `web.php`.

El archivo `console.php` es donde puede definir todos sus comandos de consola basados en cierres. Cada cierre está vinculado a una instancia de comando permitiendo un enfoque simple para interactuar con los métodos IO de cada comando. Aunque este archivo no define rutas HTTP, define puntos de entrada basados en consola (rutas) en su aplicación. También puede [programar](/docs/{{version}}/scheduling) tareas en el archivo `console.php`.

Opcionalmente, puede instalar archivos de ruta adicionales para rutas API (`api.php`) y canales de difusión (`channels.php`), a través de los comandos Artisan `install:api` y `install:broadcasting`.

El archivo `api.php` contiene rutas que están destinadas a ser sin estado, por lo que las solicitudes que entran en la aplicación a través de estas rutas están destinadas a ser autenticadas [a través de tokens](/docs/{{version}}/sanctum) y no tendrán acceso al estado de la sesión.

El archivo `channels.php` es donde puedes registrar todos los canales de [transmisión de eventos](/docs/{{version}}/broadcasting) que tu aplicación soporta.

<a name="the-storage-directory"></a>
#### El directorio de almacenamiento

El directorio `storage` contiene tus logs, plantillas Blade compiladas, sesiones basadas en ficheros, cachés de ficheros, y otros ficheros generados por el framework. Este directorio está dividido en los directorios `app`, `framework` y `logs`. El directorio `app` puede ser utilizado para almacenar cualquier archivo generado por tu aplicación. El directorio `framework` se utiliza para almacenar archivos generados por el framework y cachés. Por último, el directorio `logs` contiene los archivos de registro de tu aplicación.

El directorio `storage/app/public` puede utilizarse para almacenar archivos generados por el usuario, como avatares de perfil, que deben ser accesibles públicamente. Debes crear un enlace simbólico en `public/storage` que apunte a este directorio. Puede crear el enlace utilizando el comando `php artisan storage:link` de Artisan.

<a name="the-tests-directory"></a>
#### El directorio Tests

El directorio `tests` contiene tus pruebas automatizadas. Ejemplo [Pest](https://pestphp.com) o [PHPUnit](https://phpunit.de/) pruebas unitarias y pruebas de características se proporcionan fuera de la caja. Cada clase de prueba debe tener como sufijo la palabra `Test`. Puede ejecutar sus pruebas utilizando los comandos `/vendor/bin/pest` o `/vendor/bin/phpunit`. O, si desea una representación más detallada y hermosa de los resultados de sus pruebas, puede ejecutarlas utilizando el comando Artisan `php artisan test`.

<a name="the-vendor-directory"></a>
#### El directorio Vendor

El directorio `vendor` contiene las dependencias de [Composer](https://getcomposer.org).

<a name="the-app-directory"></a>
## El directorio de aplicaciones

La mayor parte de su aplicación se encuentra en el directorio `app`. Por defecto, este directorio tiene el nombre `App` y es autocargado por Composer usando el [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/).

Por defecto, el directorio `app` contiene los directorios `Http`, `Models` y `Providers`. Sin embargo, con el tiempo, una variedad de otros directorios serán generados dentro del directorio app a medida que utilices los comandos make Artisan para generar clases. Por ejemplo, el directorio `app/Console` no existirá hasta que ejecutes el comando Artisan `make:command` para generar una clase de comando.

Ambos directorios `Console` y `Http` son explicados en sus respectivas secciones más adelante, pero piensa en los directorios `Console` y `Http` como una API dentro del núcleo de tu aplicación. Tanto el protocolo HTTP como la CLI son mecanismos para interactuar con tu aplicación, pero en realidad no contienen lógica de aplicación. En otras palabras, son dos formas de emitir comandos a tu aplicación. El directorio `Console` contiene todos tus comandos Artisan, mientras que el directorio `Http` contiene tus controladores, middleware y peticiones.

> NOTA  
> Muchas de las clases en el directorio `app` pueden ser generadas por Artisan a través de comandos. Para revisar los comandos disponibles, ejecuta el comando `php artisan list make` en tu terminal.

<a name="the-broadcasting-directory"></a>
#### El directorio Broadcasting

El directorio `Broadcasting` contiene todas las clases de canales de difusión para tu aplicación. Estas clases se generan utilizando el comando `make:channel`. Este directorio no existe por defecto, pero se creará para ti cuando crees tu primer canal. Para saber más sobre canales, consulta la documentación sobre [difusión de eventos](/docs/{{version}}/broadcasting).

<a name="the-console-directory"></a>
#### El Directorio de la Consola

El directorio `Console` contiene todos los comandos personalizados de Artisan para su aplicación. Estos comandos pueden ser generados usando el comando `make:command`.

<a name="the-events-directory"></a>
#### El Directorio de Eventos

Este directorio no existe por defecto, pero será creado para ti por los comandos Artisan `event:generate` y `make:event`. El directorio `Events` contiene [clases de eventos](/docs/{{version}}/events). Los eventos pueden ser utilizados para alertar a otras partes de tu aplicación de que una determinada acción ha ocurrido, proporcionando una gran flexibilidad y desacoplamiento.

<a name="the-exceptions-directory"></a>
#### El directorio Exceptions

El directorio `Exceptions` contiene todas las excepciones personalizadas para tu aplicación. Estas excepciones pueden ser generadas usando el comando `make:exception`.

<a name="the-http-directory"></a>
#### El directorio Http

El directorio `Http` contiene tus controladores, middleware y peticiones de formulario. Casi toda la lógica para manejar las peticiones que entran en su aplicación se colocará en este directorio.

<a name="the-jobs-directory"></a>
#### El Directorio de Trabajos

Este directorio no existe por defecto, pero será creado para usted si ejecuta el comando `make:job` de Artisan. El directorio `Jobs` alberga los [trabajos en cola](/docs/{{version}}/queues) para su aplicación. Los trabajos pueden ser puestos en cola por su aplicación o ejecutarse sincrónicamente dentro del ciclo de vida de la solicitud actual. Los trabajos que se ejecutan de forma sincrónica durante la solicitud actual a veces se denominan "comandos", ya que son una implementación del [patrón de comandos](https://en.wikipedia.org/wiki/Command_pattern).

<a name="the-listeners-directory"></a>
#### El directorio Listeners

Este directorio no existe por defecto, pero será creado para ti si ejecutas los comandos Artisan `event:generate` o `make:listener`. El directorio `Listeners` contiene las clases que manejan tus [eventos](/docs/{{version}}/events). Los escuchadores de eventos reciben una instancia de evento y ejecutan la lógica en respuesta al evento que se dispara. Por ejemplo, un evento `UserRegistered` podría ser manejado por un oyente `SendWelcomeEmail`.

<a name="the-mail-directory"></a>
#### El Directorio de Correo

Este directorio no existe por defecto, pero será creado para usted si ejecuta el comando `make:mail` de Artisan. El directorio `Mail` contiene todas sus [clases que representan emails](/docs/{{version}}/mail) enviados por su aplicación. Los objetos Mail le permiten encapsular toda la lógica de construcción de un correo electrónico en una única y simple clase que puede ser enviada utilizando el método `Mail::send`.

<a name="the-models-directory"></a>
#### El directorio Models

El directorio `Models` contiene todas tus [clases de modelos Eloquent](/docs/{{version}}/eloquent). El ORM de Eloquent incluido con Laravel proporciona una hermosa y simple implementación de ActiveRecord para trabajar con tu base de datos. Cada tabla de la base de datos tiene su correspondiente "Modelo" que se utiliza para interactuar con esa tabla. Los modelos te permiten consultar los datos de tus tablas, así como insertar nuevos registros en la tabla.

<a name="the-notifications-directory"></a>
#### El Directorio de Notificaciones

Este directorio no existe por defecto, pero será creado para usted si ejecuta el comando `make:notification` de Artisan. El directorio `Notifications` contiene todas las [notificaciones] "transaccionales"(/docs/{{version}}/notifications) que son enviadas por tu aplicación, como simples notificaciones sobre eventos que ocurren dentro de tu aplicación. La función de notificación de Laravel abstrae el envío de notificaciones a través de una variedad de controladores, tales como correo electrónico, Slack, SMS, o almacenados en una base de datos.

<a name="the-policies-directory"></a>
#### El Directorio de Políticas

Este directorio no existe por defecto, pero será creado para usted si ejecuta el comando `make:policy` de Artisan. El directorio `Policies` contiene las [clases de políticas de autorización](/docs/{{version}}/authorization) para su aplicación. Las políticas se utilizan para determinar si un usuario puede realizar una acción determinada contra un recurso.

<a name="the-providers-directory"></a>
#### El directorio de proveedores

El directorio `Providers` contiene todos los [proveedores de servicios](/docs/{{version}}/providers) para su aplicación. Los proveedores de servicios arrancan tu aplicación vinculando servicios en el contenedor de servicios, registrando eventos, o realizando cualquier otra tarea para preparar tu aplicación para las peticiones entrantes.

En una aplicación Laravel nueva, este directorio ya contendrá el `AppServiceProvider`. Eres libre de añadir tus propios proveedores a este directorio según sea necesario.

<a name="the-rules-directory"></a>
#### El Directorio de Reglas

Este directorio no existe por defecto, pero será creado para usted si ejecuta el comando Artisan `make:rule`. El directorio `Rules` contiene los objetos de reglas de validación personalizados para su aplicación. Las reglas se utilizan para encapsular lógica de validación complicada en un objeto simple. Para obtener más información, consulte la [documentación de validación](/docs/{{version}}/validation).
