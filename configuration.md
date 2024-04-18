# Configuración

- Introducción](#introduction)
- Configuración del entorno](#environment-configuration)
    - Tipos de variables de entorno](#environment-variable-types)
    - Recuperación de la configuración del entorno](#retrieving-environment-configuration)
    - Determinación del entorno actual](#determining-the-current-environment)
    - Cifrado de archivos de entorno](#encrypting-environment-files)
- Acceso a los valores de configuración](#accessing-configuration-values)
- Almacenamiento en caché de la configuración](#configuration-caching)
- Publicación de la configuración](#configuration-publishing)
- Modo de depuración](#debug-mode)
- Modo de mantenimiento](#maintenance-mode)

<a name="introduction"></a>
## Introducción

Todos los archivos de configuración del framework Laravel se almacenan en el directorio `config`. Cada opción está documentada, así que siéntete libre de revisar los archivos y familiarizarte con las opciones disponibles.

Estos archivos de configuración te permiten configurar cosas como la información de conexión a tu base de datos, la información de tu servidor de correo, así como otros valores de configuración básicos como la zona horaria de tu aplicación y la clave de encriptación.

<a name="the-about-command"></a>
#### El comando `about

Laravel puede mostrar una visión general de la configuración, controladores y entorno de tu aplicación a través del comando `about` Artisan.

```shell
php artisan about
```

Si sólo le interesa una sección concreta del resumen de la aplicación, puede filtrarla con la opción `--only`:

```shell
php artisan about --only=environment
```

O, para explorar en detalle los valores de un archivo de configuración específico, puede utilizar el comando `config:show` de Artisan:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## Configuración del entorno

A menudo es útil tener diferentes valores de configuración basados en el entorno donde se está ejecutando la aplicación. Por ejemplo, es posible que desee utilizar un controlador de caché diferente a nivel local que en su servidor de producción.

Para hacer esto más fácil, Laravel utiliza la librería PHP [DotEnv](https://github.com/vlucas/phpdotenv). En una nueva instalación de Laravel, el directorio raíz de tu aplicación contendrá un archivo `.env.example` que define muchas variables de entorno comunes. Durante el proceso de instalación de Laravel, este archivo se copiará automáticamente a `.env`.

El archivo `.env` por defecto de Laravel contiene algunos valores de configuración comunes que pueden diferir en función de si tu aplicación se ejecuta localmente o en un servidor web de producción. Estos valores son leídos por los archivos de configuración dentro del directorio `config` usando la función `env` de Laravel.

Si estás desarrollando con un equipo, es posible que desees seguir incluyendo y actualizando el archivo `.env.example` con tu aplicación. Al poner valores de marcador de posición en el archivo de configuración de ejemplo, otros desarrolladores de tu equipo pueden ver claramente qué variables de entorno son necesarias para ejecutar tu aplicación.

> [!NOTE]
> Cualquier variable de tu archivo `.env` puede ser anulada por variables de entorno externas, como variables de entorno a nivel de servidor o a nivel de sistema.

<a name="environment-file-security"></a>
#### Seguridad del archivo de entorno

Su archivo `.env` no debe ser enviado al control de código fuente de su aplicación, ya que cada desarrollador / servidor que utilice su aplicación podría requerir una configuración de entorno diferente. Además, esto supondría un riesgo de seguridad en el caso de que un intruso accediera a tu repositorio de control de código fuente, ya que cualquier credencial sensible quedaría expuesta.

Sin embargo, es posible cifrar tu fichero de entorno usando el [cifrado de entorno] integrado de Laravel (#encrypting-environment-files). Los archivos de entorno cifrados pueden colocarse en el control de código fuente de forma segura.

<a name="additional-environment-files"></a>
#### Ficheros de entorno adicionales

Antes de cargar las variables de entorno de tu aplicación, Laravel determina si se ha proporcionado externamente una variable de entorno `APP_ENV` o si se ha especificado el argumento CLI `--env`. Si es así, Laravel intentará cargar un archivo `.env.[APP_ENV]` si existe. Si no existe, se cargará el fichero `.env` por defecto.

<a name="environment-variable-types"></a>
### Tipos de variables de entorno

Todas las variables en sus ficheros `.env` son típicamente interpretadas como cadenas, por lo que se han creado algunos valores reservados para permitirle devolver un rango más amplio de tipos desde la función `env()`:

| `.env` Value | `env()` Value |
|--------------|---------------|
| true         | (bool) true   |
| (true)       | (bool) true   |
| false        | (bool) false  |
| (false)      | (bool) false  |
| empty        | (string) ''   |
| (empty)      | (string) ''   |
| null         | (null) null   |
| (null)       | (null) null   |

Si necesita definir una variable de entorno con un valor que contenga espacios, puede hacerlo encerrando el valor entre comillas dobles:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### Recuperando la Configuración del Entorno

Todas las variables listadas en el fichero `.env` serán cargadas en el superglobal PHP `$_ENV` cuando su aplicación reciba una petición. Sin embargo, puede usar la función `env` para recuperar valores de estas variables en sus ficheros de configuración. De hecho, si revisas los archivos de configuración de Laravel, notarás que muchas de las opciones ya utilizan esta función:

    'debug' => env('APP_DEBUG', false),

El segundo valor que se pasa a la función `env` es el "valor por defecto". Este valor se devolverá si no existe ninguna variable de entorno para la clave dada.

<a name="determining-the-current-environment"></a>
### Determinar el entorno actual

El entorno actual de la aplicación se determina a través de la variable `APP_ENV` de tu fichero `.env`. Puede acceder a este valor mediante el método `environment` de la [fachada] `App`(/docs/{{version}}/facades):

    use Illuminate\Support\Facades\App;

    $environment = App::environment();

También puede pasar argumentos al método `environment` para determinar si el entorno coincide con un valor dado. El método devolverá `true` si el entorno coincide con alguno de los valores dados:

    if (App::environment('local')) {
        // The environment is local
    }

    if (App::environment(['local', 'staging'])) {
        // The environment is either local OR staging...
    }

> [!NOTE]  
> La detección del entorno actual de la aplicación puede anularse definiendo una variable de entorno `APP_ENV` a nivel de servidor.

<a name="encrypting-environment-files"></a>
### Cifrado de archivos de entorno

Los archivos de entorno sin cifrar nunca deben ser almacenados en el control de código fuente. Sin embargo, Laravel le permite cifrar sus archivos de entorno para que puedan ser agregados de forma segura al control de código fuente con el resto de su aplicación.

<a name="encryption"></a>
#### Cifrado

Para cifrar un archivo de entorno, puede utilizar el comando `env:encrypt`:

```shell
php artisan env:encrypt
```

Ejecutar el comando `env:encrypt` encriptará tu archivo `.env` y colocará el contenido encriptado en un archivo `.env.encrypted`. La clave de descifrado se muestra en la salida del comando y debe guardarse en un gestor de contraseñas seguro. Si desea proporcionar su propia clave de cifrado puede utilizar la opción `--key` al invocar el comando:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]  
> La longitud de la clave proporcionada debe coincidir con la longitud de clave requerida por el cifrado utilizado. Por defecto, Laravel utilizará el cifrado `AES-256-CBC` que requiere una clave de 32 caracteres. Eres libre de utilizar cualquier cifrado soportado por Laravel [encrypter](/docs/{{version}}/encryption) pasando la opción `--cipher` al invocar el comando.

Si tu aplicación tiene múltiples archivos de entorno, como `.env` y `.env.staging`, puedes especificar el archivo de entorno que debe ser cifrado proporcionando el nombre del entorno a través de la opción `--env`:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### Descifrado

Para desencriptar un fichero de entorno, puedes usar el comando `env:decrypt`. Este comando requiere una clave de descifrado, que Laravel recuperará de la variable de entorno `LARAVEL_ENV_ENCRYPTION_KEY`:

```shell
php artisan env:decrypt
```

O bien, la clave puede proporcionarse directamente al comando mediante la opción `--key`:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

Cuando se invoca el comando `env:decrypt`, Laravel descifrará el contenido del fichero `.env.encrypted` y colocará el contenido descifrado en el fichero `.env`.

La opción `--cipher` puede ser proporcionada al comando `env:decrypt` para utilizar un cifrado personalizado:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

Si su aplicación tiene varios archivos de entorno, como `.env` y `.env.staging`, puede especificar el archivo de entorno que debe descifrarse proporcionando el nombre del entorno mediante la opción `--env`:

```shell
php artisan env:decrypt --env=staging
```

Para sobrescribir un archivo de entorno existente, puede proporcionar la opción `--force` al comando `env:decrypt`:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## Acceso a los valores de configuración

Puedes acceder fácilmente a tus valores de configuración usando la fachada `Config` o la función global `config` desde cualquier parte de tu aplicación. Puede acceder a los valores de configuración utilizando la sintaxis "dot", que incluye el nombre del fichero y la opción a la que desea acceder. También puede especificarse un valor por defecto, que será devuelto si la opción de configuración no existe:

    use Illuminate\Support\Facades\Config;

    $value = Config::get('app.timezone');

    $value = config('app.timezone');

    // Retrieve a default value if the configuration value does not exist...
    $value = config('app.timezone', 'Asia/Seoul');

Para establecer valores de configuración en tiempo de ejecución, puedes invocar el método `set` de la fachada `Config` o pasar un array a la función `config`:

    Config::set('app.timezone', 'America/Chicago');

    config(['app.timezone' => 'America/Chicago']);

Para ayudar al análisis estático, la fachada `Config` también proporciona métodos de recuperación de configuraciones tipadas. Si el valor de configuración recuperado no coincide con el tipo esperado, se lanzará una excepción:

    Config::string('config-key');
    Config::integer('config-key');
    Config::float('config-key');
    Config::boolean('config-key');
    Config::array('config-key');

<a name="configuration-caching"></a>
## Caché de configuración

Para aumentar la velocidad de tu aplicación, debes cachear todos tus archivos de configuración en un solo archivo usando el comando `config:cache` de Artisan. Esto combinará todas las opciones de configuración para tu aplicación en un solo archivo que puede ser cargado rápidamente por el framework.

Normalmente deberías ejecutar el comando `php artisan config:cache` como parte de tu proceso de despliegue de producción. El comando no debe ser ejecutado durante el desarrollo local ya que las opciones de configuración necesitarán ser cambiadas frecuentemente durante el curso del desarrollo de su aplicación.

Una vez que la configuración ha sido cacheada, el archivo `.env` de tu aplicación no será cargado por el framework durante las peticiones o comandos de Artisan; por lo tanto, la función `env` solo devolverá variables de entorno externas, a nivel de sistema.

Por esta razón, debes asegurarte de que sólo llamas a la función `env` desde los archivos de configuración (`config`) de tu aplicación. Puedes ver muchos ejemplos de esto examinando los archivos de configuración por defecto de Laravel. Se puede acceder a los valores de configuración desde cualquier parte de tu aplicación usando la función `config` [descrita anteriormente](#accessing-configuration-values).

El comando `config:clear` se puede utilizar para purgar la configuración almacenada en caché:

```shell
php artisan config:clear
```

> [!WARNING]  
> Si ejecutas el comando `config:cache` durante tu proceso de despliegue, debes asegurarte de que sólo estás llamando a la función `env` desde dentro de tus ficheros de configuración. Una vez que la configuración se ha almacenado en caché, el archivo `.env` no se cargará; por lo tanto, la función `env` sólo devolverá variables de entorno externas, a nivel de sistema.

<a name="configuration-publishing"></a>
## Publicación de la configuración

La mayoría de los archivos de configuración de Laravel ya están publicados en el directorio `config` de tu aplicación; sin embargo, ciertos archivos de configuración como `cors.php` y `view.php` no están publicados por defecto, ya que la mayoría de las aplicaciones nunca necesitarán modificarlos.

Sin embargo, puede utilizar el comando `config:publish` de Artisan para publicar cualquier archivo de configuración que no esté publicado por defecto:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## Modo Depuración

La opción `debug` en su fichero de configuración `config/app.php` determina cuánta información sobre un error se muestra realmente al usuario. Por defecto, esta opción está configurada para respetar el valor de la variable de entorno `APP_DEBUG`, que se almacena en su archivo `.env`.

> [!WARNING]  
> Para el desarrollo local, debe establecer la variable de entorno `APP_DEBUG` en `true`. **En su entorno de producción, este valor debe ser siempre `false`. Si la variable se establece en `true` en producción, corres el riesgo de exponer valores de configuración sensibles a los usuarios finales de tu aplicación.

<a name="maintenance-mode"></a>
## Modo Mantenimiento

Cuando su aplicación está en modo de mantenimiento, se mostrará una vista personalizada para todas las peticiones en su aplicación. Esto hace que sea fácil de "desactivar" su aplicación mientras se está actualizando o cuando se está realizando el mantenimiento. Se incluye una comprobación del modo de mantenimiento en la pila de middleware predeterminada para su aplicación. Si la aplicación está en modo mantenimiento, se lanzará una instancia `Symfony\Component\HttpKernel\Exception\HttpException` con un código de estado 503.

Para habilitar el modo de mantenimiento, ejecuta el comando `down` de Artisan:

```shell
php artisan down
```

Si desea que la cabecera HTTP `Refresh` se envíe con todas las respuestas del modo de mantenimiento, puede proporcionar la opción `refresh` al invocar el comando `down`. La cabecera `Refresh` indicará al navegador que actualice automáticamente la página tras el número de segundos especificado:

```shell
php artisan down --refresh=15
```

También puede proporcionar una opción `retry` al comando `down`, que se establecerá como valor de la cabecera HTTP `Retry-After`, aunque los navegadores suelen ignorar esta cabecera:

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### Anulación del modo de mantenimiento

Para permitir que el modo de mantenimiento sea evitado utilizando un token secreto, puede utilizar la opción `secret` para especificar un token de evasión del modo de mantenimiento:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

Después de poner la aplicación en modo de mantenimiento, puede navegar a la URL de la aplicación que coincida con este token y Laravel emitirá una cookie de bypass de modo de mantenimiento a su navegador:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Si quieres que Laravel genere el token secreto por ti, puedes usar la opción `with-secret`. El secreto se te mostrará una vez que la aplicación esté en modo mantenimiento:

```shell
php artisan down --with-secret
```

Cuando acceda a esta ruta oculta, será redirigido a la ruta `/` de la aplicación. Una vez que la cookie haya sido emitida a su navegador, podrá navegar por la aplicación normalmente como si no estuviera en modo de mantenimiento.

> [!NOTE]  
> Your maintenance mode secret should typically consist of alpha-numeric characters and, optionally, dashes. You should avoid using characters that have special meaning in URLs such as `?` or `&`.

<a name="maintenance-mode-on-multiple-servers"></a>
#### Modo de mantenimiento en múltiples servidores

Por defecto, Laravel determina si tu aplicación está en modo mantenimiento usando un sistema basado en ficheros. Esto significa que para activar el modo de mantenimiento, el comando `php artisan down` tiene que ser ejecutado en cada servidor que aloje tu aplicación.

Alternativamente, Laravel ofrece un método basado en caché para manejar el modo de mantenimiento. Este método requiere ejecutar el comando `php artisan down` en un solo servidor. Para utilizar este método, modifica el parámetro "driver" en el archivo `config/app.php` de tu aplicación a `cache`. A continuación, seleccione un `almacén` de caché que sea accesible por todos sus servidores. Esto asegura que el estado del modo de mantenimiento se mantiene de forma consistente en todos los servidores:

```php
'maintenance' => [
    'driver' => 'cache',
    'store' => 'database',
],
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### Pre-Renderización de la Vista en Modo Mantenimiento

Si utilizas el comando `php artisan down` durante el despliegue, tus usuarios pueden encontrarse ocasionalmente con errores si acceden a la aplicación mientras se están actualizando tus dependencias de Composer u otros componentes de la infraestructura. Esto ocurre porque una parte significativa del framework Laravel debe arrancar para determinar que tu aplicación está en modo mantenimiento y renderizar la vista de modo mantenimiento usando el motor de plantillas.

Por esta razón, Laravel permite pre-renderizar una vista en modo mantenimiento que será devuelta al principio del ciclo de petición. Esta vista se renderiza antes de que se haya cargado ninguna de las dependencias de tu aplicación. Puedes pre-renderizar una plantilla de tu elección usando la opción `render` del comando `down`:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### Redireccionando Peticiones en Modo Mantenimiento

Mientras está en modo mantenimiento, Laravel mostrará la vista de modo mantenimiento para todas las URLs de la aplicación a las que el usuario intente acceder. Si lo desea, puede indicar a Laravel que redirija todas las peticiones a una URL específica. Esto puede lograrse utilizando la opción `redirect`. Por ejemplo, es posible que desee redirigir todas las solicitudes a la `/` URI:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### Desactivación del modo de mantenimiento

Para desactivar el modo de mantenimiento, utilice el comando `up`:

```shell
php artisan up
```

> [!NOTE]  
> Puede personalizar la plantilla predeterminada del modo de mantenimiento definiendo su propia plantilla en `resources/views/errors/503.blade.php`.

<a name="maintenance-mode-queues"></a>
#### Modo de mantenimiento y colas

Mientras la aplicación esté en modo de mantenimiento, no se gestionarán [trabajos en cola](/docs/{{version}}/queues). Los trabajos se seguirán gestionando normalmente una vez que la aplicación salga del modo de mantenimiento.

<a name="alternatives-to-maintenance-mode"></a>
#### Alternativas al modo de mantenimiento

Dado que el modo de mantenimiento requiere que su aplicación tenga varios segundos de tiempo de inactividad, considere alternativas como [Laravel Vapor](https://vapor.laravel.com) y [Envoyer](https://envoyer.io) para lograr un despliegue sin tiempo de inactividad con Laravel.
