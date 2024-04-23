# Deployment

- [Introduction](#introduction)
- [Server Requirements](#server-requirements)
- [Server Configuration](#server-configuration)
    - [Nginx](#nginx)
- [Optimization](#optimization)
    - [Caching Configuration](#optimizing-configuration-loading)
    - [Caching Events](#caching-events)
    - [Caching Routes](#optimizing-route-loading)
    - [Caching Views](#optimizing-view-loading)
- [Debug Mode](#debug-mode)
- [The Health Route](#the-health-route)
- [Easy Deployment With Forge / Vapor](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## Introducción

Cuando estés listo para desplegar tu aplicación Laravel en producción, hay algunas cosas importantes que puedes hacer para asegurarte de que tu aplicación se ejecuta de la manera más eficiente posible. En este documento, vamos a cubrir algunos grandes puntos de partida para asegurarse de que su aplicación Laravel se despliega correctamente.

<a name="server-requirements"></a>
## Requisitos del servidor

El framework Laravel tiene algunos requisitos de sistema. Usted debe asegurarse de que su servidor web tiene la siguiente versión mínima de PHP y extensiones:

<div class="content-list" markdown="1">

- PHP >= 8.2
- Ctype PHP Extension
- cURL PHP Extension
- DOM PHP Extension
- Fileinfo PHP Extension
- Filter PHP Extension
- Hash PHP Extension
- Mbstring PHP Extension
- OpenSSL PHP Extension
- PCRE PHP Extension
- PDO PHP Extension
- Session PHP Extension
- Tokenizer PHP Extension
- XML PHP Extension

</div>

<a name="server-configuration"></a>
## Configuración del servidor

<a name="nginx"></a>
### Nginx

Si está desplegando su aplicación en un servidor que ejecuta Nginx, puede utilizar el siguiente archivo de configuración como punto de partida para configurar su servidor web. Lo más probable es que este archivo tenga que ser personalizado dependiendo de la configuración de su servidor. **Si desea asistencia en la gestión de su servidor, considere el uso de un servicio de gestión y despliegue de servidores Laravel como [Laravel Forge](https://forge.laravel.com).**

Por favor, asegúrate de que, como en la configuración de abajo, tu servidor web dirige todas las peticiones al archivo `public/index.php` de tu aplicación. Nunca debe intentar mover el archivo `index.php` a la raíz de su proyecto, ya que servir la aplicación desde la raíz del proyecto expondrá muchos archivos de configuración sensibles a la Internet pública:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    root /srv/example.com/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a name="optimization"></a>
## Optimización

Cuando despliegas tu aplicación a producción, hay una variedad de archivos que deben ser cacheados, incluyendo tu configuración, eventos, rutas y vistas. Laravel proporciona un único y conveniente comando Artisan `optimize` que almacenará en caché todos estos archivos. Este comando debe ser invocado típicamente como parte del proceso de despliegue de tu aplicación:

```shell
php artisan optimize
```

El método `optimize:clear` puede utilizarse para eliminar todos los archivos de caché generados por el comando `optimize`:

```shell
php artisan optimize:clear
```

En la siguiente documentación, discutiremos cada uno de los comandos de optimización granular que son ejecutados por el comando `optimize`.

<a name="optimizing-configuration-loading"></a>
### Configuración de Caché

Cuando despliegues tu aplicación a producción, debes asegurarte de ejecutar el comando Artisan `config:cache` durante tu proceso de despliegue:

```shell
php artisan config:cache
```

Este comando combinará todos los archivos de configuración de Laravel en un único archivo en caché, lo que reduce en gran medida el número de viajes que el framework debe hacer al sistema de archivos al cargar los valores de configuración.

> [!ADVERTENCIA]  
> Si ejecutas el comando `config:cache` durante tu proceso de despliegue, debes asegurarte de que sólo estás llamando a la función `env` desde dentro de tus ficheros de configuración. Una vez que la configuración se ha almacenado en caché, el archivo `.env` no se cargará y todas las llamadas a la función `env` para variables `.env` devolverán `null`.

<a name="caching-events"></a>
### Almacenamiento en caché de eventos

Debes almacenar en caché los eventos auto-descubiertos de tu aplicación durante el proceso de despliegue. Esto puede lograrse invocando el comando `event:cache` de Artisan durante el despliegue:

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### Almacenamiento en caché de rutas

Si estás construyendo una aplicación grande con muchas rutas, debes asegurarte de que estás ejecutando el comando Artisan `route:cache` durante tu proceso de despliegue:

```shell
php artisan route:cache
```

Este comando reduce todos los registros de rutas en una única llamada a un método dentro de un archivo en caché, lo que mejora el rendimiento del registro de rutas cuando se registran cientos de rutas.

<a name="optimizing-view-loading"></a>
### Caching Views

Cuando despliegues tu aplicación a producción, debes asegurarte de ejecutar el comando Artisan `view:cache` durante tu proceso de despliegue:

```shell
php artisan view:cache
```

Este comando precompila todas tus vistas Blade para que no se compilen bajo demanda, mejorando el rendimiento de cada petición que devuelve una vista.

<a name="debug-mode"></a>
## Modo Depuración

La opción debug en su fichero de configuración `config/app.php` determina cuánta información sobre un error se muestra realmente al usuario. Por defecto, esta opción está configurada para respetar el valor de la variable de entorno `APP_DEBUG`, que se almacena en el archivo `.env` de su aplicación.

> [!ADVERTENCIA]  
> **En su entorno de producción, este valor debe ser siempre `false`. Si la variable `APP_DEBUG` se establece en `true` en producción, corres el riesgo de exponer valores de configuración sensibles a los usuarios finales de tu aplicación.**

<a name="the-health-route"></a>
## La ruta de salud

Laravel incluye una ruta de chequeo de salud que puede ser utilizada para monitorizar el estado de tu aplicación. En producción, esta ruta puede ser utilizada para informar del estado de tu aplicación a un monitor de tiempo de actividad, balanceador de carga, o sistema de orquestación como Kubernetes.

Por defecto, la ruta de comprobación de estado se sirve en `/up` y devolverá una respuesta HTTP 200 si la aplicación ha arrancado sin excepciones. En caso contrario, se devolverá una respuesta HTTP 500. Puedes configurar el URI para esta ruta en el archivo `bootstrap/app` de tu aplicación:

    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up', // [tl! remove]
        health: '/status', // [tl! add]
    )

Cuando se realizan peticiones HTTP a esta ruta, Laravel también enviará un evento `Illuminate\Foundation\Events\DiagnosingHealth`, permitiéndole realizar comprobaciones de salud adicionales relevantes para su aplicación. Dentro de un evento [listener](/docs/{{version}}/events) para este evento, puede comprobar el estado de la base de datos o de la caché de su aplicación. Si detectas un problema con tu aplicación, puedes simplemente lanzar una excepción desde el listener.

<a name="deploying-with-forge-or-vapor"></a>
## Fácil implantación con Forge / Vapor

<a name="laravel-forge"></a>
#### Laravel Forge

Si no está preparado para gestionar la configuración de su propio servidor o no se siente cómodo configurando todos los servicios necesarios para ejecutar una aplicación Laravel robusta, [Laravel Forge](https://forge.laravel.com) es una gran alternativa.

Laravel Forge puede crear servidores en varios proveedores de infraestructura como DigitalOcean, Linode, AWS, y más. Además, Forge instala y gestiona todas las herramientas necesarias para construir aplicaciones Laravel robustas, como Nginx, MySQL, Redis, Memcached, Beanstalk y más.

> [!NOTA]  
> ¿Quieres una guía completa para desplegar con Laravel Forge? Echa un vistazo al [Laravel Bootcamp](https://bootcamp.laravel.com/deploying) y la [serie de video de Forge disponible en Laracasts](https://laracasts.com/series/learn-laravel-forge-2022-edition).

<a name="laravel-vapor"></a>
#### Laravel Vapor

Si desea una plataforma de despliegue totalmente sin servidor y autoescalable adaptada a Laravel, eche un vistazo a [Laravel Vapor](https://vapor.laravel.com). Laravel Vapor es una plataforma de despliegue sin servidor para Laravel, impulsada por AWS. Lanza tu infraestructura Laravel en Vapor y enamórate de la simplicidad escalable de serverless. Laravel Vapor está ajustado por los creadores de Laravel para trabajar sin problemas con el framework para que puedas seguir escribiendo tus aplicaciones Laravel exactamente como estás acostumbrado.
