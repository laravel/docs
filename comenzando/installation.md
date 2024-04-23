# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Creating a Laravel Project](#creating-a-laravel-project)
- [Initial Configuration](#initial-configuration)
    - [Environment Based Configuration](#environment-based-configuration)
    - [Databases and Migrations](#databases-and-migrations)
    - [Directory Configuration](#directory-configuration)
- [Docker Installation Using Sail](#docker-installation-using-sail)
    - [Sail on macOS](#sail-on-macos)
    - [Sail on Windows](#sail-on-windows)
    - [Sail on Linux](#sail-on-linux)
    - [Choosing Your Sail Services](#choosing-your-sail-services)
- [IDE Support](#ide-support)
- [Next Steps](#next-steps)
    - [Laravel the Full Stack Framework](#laravel-the-fullstack-framework)
    - [Laravel the API Backend](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Conoce Laravel

Laravel es un framework de aplicaciones web con una sintaxis expresiva y elegante. Un framework web proporciona una estructura y un punto de partida para la creación de su aplicación, lo que le permite centrarse en la creación de algo increíble mientras nosotros nos ocupamos de los detalles.

Laravel se esfuerza por proporcionar una experiencia de desarrollador increíble al tiempo que proporciona características de gran alcance, tales como la inyección de dependencia a fondo, una capa de abstracción de base de datos expresiva, colas y trabajos programados, pruebas unitarias y de integración, y mucho más.

Tanto si eres nuevo en los frameworks web PHP como si tienes años de experiencia, Laravel es un framework que puede crecer contigo. Te ayudaremos a dar tus primeros pasos como desarrollador web o te daremos un empujón mientras llevas tu experiencia al siguiente nivel. No podemos esperar a ver lo que construyes.

> [!NOTA]  
> ¿Nuevo en Laravel? Echa un vistazo a la [Laravel Bootcamp](https://bootcamp.laravel.com) para un recorrido práctico del marco mientras te guiamos a través de la construcción de su primera aplicación Laravel.

<a name="why-laravel"></a>
### ¿Por qué Laravel?

Hay una gran variedad de herramientas y frameworks disponibles para construir una aplicación web. Sin embargo, creemos que Laravel es la mejor opción para construir aplicaciones web modernas y full-stack.

#### Un Framework Progresivo

Nos gusta llamar a Laravel un framework "progresivo". Con esto queremos decir que Laravel crece contigo. Si estás dando tus primeros pasos en el desarrollo web, la amplia biblioteca de documentación, guías y [tutoriales en vídeo](https://laracasts.com) te ayudarán a aprender sin sentirte abrumado.

Si eres un desarrollador senior, Laravel te da herramientas robustas para [inyección de dependencia](/docs/{{version}}/container), [pruebas unitarias](/docs/{{version}}/testing), [colas](/docs/{{version}}/queues), [eventos en tiempo real](/docs/{{version}}/broadcasting), y mucho más. Laravel está afinado para la construcción de aplicaciones web profesionales y listo para manejar las cargas de trabajo de la empresa.

#### Un marco escalable

Laravel es increíblemente escalable. Gracias a la naturaleza escalable de PHP y al soporte integrado de Laravel para sistemas de caché rápidos y distribuidos como Redis, el escalado horizontal con Laravel es pan comido. De hecho, las aplicaciones Laravel se han escalado fácilmente para manejar cientos de millones de peticiones al mes.

¿Necesitas escalado extremo? Plataformas como [Laravel Vapor](https://vapor.laravel.com) le permiten ejecutar su aplicación Laravel a escala casi ilimitada en la última tecnología sin servidor de AWS.

#### Un framework comunitario

Laravel combina los mejores paquetes del ecosistema PHP para ofrecer el framework más robusto y amigable para desarrolladores disponible. Además, miles de desarrolladores con talento de todo el mundo han [contribuido al framework](https://github.com/laravel/framework). Quién sabe, quizás incluso te conviertas en un contribuidor de Laravel.

<a name="creating-a-laravel-project"></a>
## Creando un Proyecto Laravel

Antes de crear tu primer proyecto Laravel, asegúrate de que tu máquina local tiene PHP y [Composer](https://getcomposer.org) instalados. Si estás desarrollando en macOS o Windows, PHP y Composer se pueden instalar en minutos a través de [Laravel Herd](https://herd.laravel.com). Además, recomendamos [installing Node and NPM](https://nodejs.org).

Después de haber instalado PHP y Composer, puedes crear un nuevo proyecto Laravel a través del comando `create-project` de Composer:

```nothing
composer create-project laravel/laravel example-app
```

O puedes crear nuevos proyectos Laravel instalando globalmente [el instalador de Laravel](https://github.com/laravel/installer) a través de Composer:

```nothing
composer global require laravel/installer

laravel new example-app
```

Una vez creado el proyecto, inicia el servidor de desarrollo local de Laravel utilizando el comando `serve` de Laravel Artisan:

```nothing
cd example-app

php artisan serve
```

Una vez que hayas iniciado el servidor de desarrollo Artisan, tu aplicación será accesible en tu navegador web en [http://localhost:8000](http://localhost:8000). A continuación, estás listo para [comenzar a dar tus siguientes pasos en el ecosistema Laravel](#next-steps). Por supuesto, también puedes querer [configurar una base de datos](#databases-and-migrations).

> [!NOTA]
> Si desea una ventaja al desarrollar su aplicación Laravel, considere el uso de uno de nuestros [starter kits](/docs/{{version}}/starter-kits). Los kits de inicio de Laravel proporcionan un andamiaje de autenticación backend y frontend para tu nueva aplicación Laravel.

<a name="initial-configuration"></a>
## Configuración Inicial

Todos los archivos de configuración para el framework Laravel se almacenan en el directorio `config`. Cada opción está documentada, así que siéntete libre de revisar los archivos y familiarizarte con las opciones disponibles.

Laravel casi no necesita configuración adicional. ¡Eres libre de empezar a desarrollar! Sin embargo, es posible que desee revisar el archivo `config/app.php` y su documentación. Contiene varias opciones como `timezone` y `locale` que puedes querer cambiar de acuerdo a tu aplicación.

<a name="environment-based-configuration"></a>
### Configuración basada en el entorno

Dado que muchos de los valores de las opciones de configuración de Laravel pueden variar dependiendo de si tu aplicación se está ejecutando en tu máquina local o en un servidor web de producción, muchos valores de configuración importantes se definen utilizando el archivo `.env` que existe en la raíz de tu aplicación.

Su archivo `.env` no debe ser enviado al control de código fuente de su aplicación, ya que cada desarrollador / servidor que utilice su aplicación podría requerir una configuración de entorno diferente. Además, esto supondría un riesgo de seguridad en el caso de que un intruso accediera a tu repositorio de control de código fuente, ya que cualquier credencial sensible quedaría expuesta.

> [!NOTA]
> Para obtener más información sobre el archivo `.env` y la configuración basada en el entorno, consulte el documento completo [configuration documentation](/docs/{{version}}/configuration#environment-configuration).

<a name="databases-and-migrations"></a>
### Bases de datos y migraciones

Ahora que has creado tu aplicación Laravel, probablemente quieras almacenar algunos datos en una base de datos. Por defecto, el fichero de configuración `.env` de tu aplicación especifica que Laravel interactuará con una base de datos SQLite.

Durante la creación del proyecto, Laravel creó un archivo `database/database.sqlite` para ti, y ejecutó las migraciones necesarias para crear las tablas de la base de datos de la aplicación.

Si prefieres utilizar otro controlador de base de datos como MySQL o PostgreSQL, puedes actualizar tu fichero de configuración `.env` para utilizar la base de datos apropiada. Por ejemplo, si desea utilizar MySQL, actualice las variables `DB_*` de su archivo de configuración `.env` de la siguiente manera:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

Si decide utilizar una base de datos que no sea SQLite, tendrá que crear la base de datos y ejecutar la aplicación [database migrations](/docs/{{version}}/migrations):

```shell
php artisan migrate
```

> [!NOTA]
> Si está desarrollando en macOS y necesita instalar MySQL, PostgreSQL o Redis localmente, considere usar [DBngin](https://dbngin.com/).

<a name="directory-configuration"></a>
### Configuración del directorio

Laravel siempre debe ser servido desde la raíz del "directorio web" configurado para su servidor web. No debe intentar servir una aplicación Laravel desde un subdirectorio del "directorio web". Intentarlo podría exponer archivos sensibles presentes en su aplicación.

<a name="docker-installation-using-sail"></a>
## Instalación en Docker usando Sail

Queremos que sea lo más fácil posible empezar con Laravel independientemente de tu sistema operativo preferido. Por lo tanto, hay una variedad de opciones para desarrollar y ejecutar un proyecto Laravel en su máquina local. Si bien es posible que desee explorar estas opciones en un momento posterior, Laravel proporciona [Sail](/docs/{{version}}/sail), una solución integrada para ejecutar su proyecto Laravel utilizando [Docker](https://www.docker.com).

Docker es una herramienta para ejecutar aplicaciones y servicios en "contenedores" pequeños y ligeros que no interfieren con el software instalado o la configuración de tu máquina local. Esto significa que no tienes que preocuparte de configurar o instalar complicadas herramientas de desarrollo como servidores web y bases de datos en tu máquina local. Para empezar, sólo tienes que instalar [Docker Desktop](https://www.docker.com/products/docker-desktop).

Laravel Sail es una interfaz de línea de comandos ligera para interactuar con la configuración Docker por defecto de Laravel. Sail proporciona un gran punto de partida para la construcción de una aplicación Laravel usando PHP, MySQL y Redis sin necesidad de experiencia previa en Docker.

> [!NOTA]  
> ¿Ya es un experto en Docker? No te preocupes. Todo sobre Sail se puede personalizar utilizando el archivo `docker-compose.yml` incluido con Laravel.

<a name="sail-on-macos"></a>
### Navegar en macOS

Si está desarrollando en un Mac y [Docker Desktop](https://www.docker.com/products/docker-desktop) ya está instalado, puede utilizar un simple comando de terminal para crear un nuevo proyecto Laravel. Por ejemplo, para crear una nueva aplicación Laravel en un directorio llamado "example-app", puedes ejecutar el siguiente comando en tu terminal:

```shell
curl -s "https://laravel.build/example-app" | bash
```

Por supuesto, puedes cambiar "example-app" en esta URL por lo que quieras - sólo asegúrate de que el nombre de la aplicación sólo contiene caracteres alfanuméricos, guiones y guiones bajos. El directorio de la aplicación Laravel se creará dentro del directorio desde el que ejecutes el comando.

La instalación de Sail puede tardar varios minutos mientras se crean los contenedores de la aplicación de Sail en tu máquina local.

Una vez creado el proyecto, puedes navegar hasta el directorio de la aplicación e iniciar Laravel Sail. Laravel Sail proporciona una sencilla interfaz de línea de comandos para interactuar con la configuración Docker por defecto de Laravel:

```shell
cd example-app

./vendor/bin/sail up
```

Una vez que se hayan iniciado los contenedores Docker de la aplicación, debe ejecutar la aplicación [database migrations](/docs/{{version}}/migrations):

```shell
./vendor/bin/sail artisan migrate
```

Por último, puede acceder a la aplicación en su navegador web en: http://localhost.

> [!NOTA]  
> Para seguir aprendiendo más sobre Laravel Sail, revisa su [documentación completa](/docs/{{version}}/sail).

<a name="sail-on-windows"></a>
### Laravel en Windows

Antes de crear una nueva aplicación Laravel en su máquina Windows, asegúrese de instalar [Docker Desktop](https://www.docker.com/products/docker-desktop). A continuación, debe asegurarse de que Windows Subsystem for Linux 2 (WSL2) está instalado y habilitado. WSL permite ejecutar ejecutables binarios de Linux de forma nativa en Windows 10. Encontrará información sobre cómo instalar y habilitar WSL2 en la página web de Microsoft [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

> [!NOTA]  
> Después de instalar y habilitar WSL2, debe asegurarse de que Docker Desktop es [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/).

A continuación, está listo para crear su primer proyecto Laravel. Inicie [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) e inicie una nueva sesión de terminal para su sistema operativo Linux WSL2. A continuación, puede utilizar un simple comando de terminal para crear un nuevo proyecto Laravel. Por ejemplo, para crear una nueva aplicación Laravel en un directorio llamado "example-app", puedes ejecutar el siguiente comando en tu terminal:

```shell
curl -s https://laravel.build/example-app | bash
```

Por supuesto, puedes cambiar "example-app" en esta URL por lo que quieras - sólo asegúrate de que el nombre de la aplicación sólo contiene caracteres alfanuméricos, guiones y guiones bajos. El directorio de la aplicación Laravel se creará dentro del directorio desde el que ejecutes el comando.

La instalación de Sail puede tardar varios minutos mientras se crean los contenedores de la aplicación de Sail en tu máquina local.

Una vez creado el proyecto, puedes navegar hasta el directorio de la aplicación e iniciar Laravel Sail. Laravel Sail proporciona una sencilla interfaz de línea de comandos para interactuar con la configuración Docker por defecto de Laravel:

```shell
cd example-app

./vendor/bin/sail up
```

Una vez que se hayan iniciado los contenedores Docker de la aplicación, debe ejecutar la aplicación [migración de base de datos](/docs/{{version}}/migrations):

```shell
./vendor/bin/sail artisan migrate
```

Por último, puede acceder a la aplicación en su navegador web en: http://localhost.

> [!NOTA]  
> Para seguir aprendiendo más sobre Laravel Sail, revisa su [complete documentation](/docs/{{version}}/sail).

#### Desarrollando dentro de WSL2

Por supuesto, usted tendrá que ser capaz de modificar los archivos de aplicación Laravel que se crearon dentro de su instalación WSL2. Para ello, le recomendamos que utilice la herramienta de Microsoft [Visual Studio Code](https://code.visualstudio.com) y su extensión para [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).

Una vez instaladas estas herramientas, puede abrir cualquier proyecto Laravel ejecutando el comando `code .` desde el directorio raíz de su aplicación utilizando el Terminal de Windows.

<a name="sail-on-linux"></a>
### Navegar en Linux

Si estás desarrollando en Linux y [Docker Compose](https://docs.docker.com/compose/install/) ya está instalado, puedes usar un simple comando de terminal para crear un nuevo proyecto Laravel.

En primer lugar, si está utilizando Docker Desktop para Linux, debe ejecutar el siguiente comando. Si no está utilizando Docker Desktop para Linux, puede omitir este paso:

```shell
docker context use default
```

A continuación, para crear una nueva aplicación Laravel en un directorio llamado "example-app", puede ejecutar el siguiente comando en su terminal:

```shell
curl -s https://laravel.build/example-app | bash
```

Por supuesto, puedes cambiar "example-app" en esta URL por lo que quieras - sólo asegúrate de que el nombre de la aplicación sólo contiene caracteres alfanuméricos, guiones y guiones bajos. El directorio de la aplicación Laravel se creará dentro del directorio desde el que ejecutes el comando.

La instalación de Sail puede tardar varios minutos mientras se crean los contenedores de la aplicación de Sail en tu máquina local.

Una vez creado el proyecto, puedes navegar hasta el directorio de la aplicación e iniciar Laravel Sail. Laravel Sail proporciona una sencilla interfaz de línea de comandos para interactuar con la configuración Docker por defecto de Laravel:

```shell
cd example-app

./vendor/bin/sail up
```

Una vez que se hayan iniciado los contenedores Docker de la aplicación, debe ejecutar la aplicación [database migrations](/docs/{{version}}/migrations):

```shell
./vendor/bin/sail artisan migrate
```

Por último, puede acceder a la aplicación en su navegador web en: http://localhost.

> [!NOTA]  
> Para seguir aprendiendo más sobre Laravel Sail, revisa la [documentación completa](/docs/{{version}}/sail).

<a name="choosing-your-sail-services"></a>
### Elección de los servicios Sail

Al crear una nueva aplicación Laravel a través de Sail, puedes utilizar la variable `with` query string para elegir qué servicios deben configurarse en el fichero `docker-compose.yml` de tu nueva aplicación. Los servicios disponibles incluyen `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, y `mailpit`:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

Si no especifica qué servicios desea configurar, se configurará una pila por defecto de `mysql`, `redis`, `meilisearch`, `mailpit` y `selenium`.

Puede indicar a Sail que instale un [Devcontainer](/docs/{{version}}/sail#using-devcontainers) añadiendo el parámetro `devcontainer` a la URL:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## Soporte IDE

Usted es libre de utilizar cualquier editor de código que desee en el desarrollo de aplicaciones Laravel, sin embargo, [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/) ofrece un amplio soporte para Laravel y su ecosistema, incluyendo [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html).

Además, la comunidad mantuvo [Laravel Idea](https://laravel-idea.com/) PhpStorm plugin ofrece una variedad de útiles aumentos IDE, incluyendo la generación de código, Eloquent terminación de sintaxis, terminación de reglas de validación, y más.

<a name="next-steps"></a>
## Próximos pasos

Ahora que has creado tu proyecto Laravel, puede que te estés preguntando qué aprender a continuación. En primer lugar, le recomendamos que se familiarice con el funcionamiento de Laravel leyendo la siguiente documentación:

<div class="content-list" markdown="1">

- [Request Lifecycle](/docs/{{version}}/lifecycle)
- [Configuration](/docs/{{version}}/configuration)
- [Directory Structure](/docs/{{version}}/structure)
- [Frontend](/docs/{{version}}/frontend)
- [Service Container](/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)

</div>

Cómo desea utilizar Laravel también dictará los próximos pasos en su viaje. Hay una variedad de maneras de utilizar Laravel, y vamos a explorar dos casos de uso principales para el marco de abajo.

> [!NOTA]  
> ¿Eres nuevo en Laravel? Echa un vistazo a la [Laravel Bootcamp](https://bootcamp.laravel.com) para un tour práctico del framework mientras te guiamos en la construcción de tu primera aplicación Laravel.

<a name="laravel-the-fullstack-framework"></a>
### Laravel el framework de pila completa

Laravel puede servir como un marco de pila completa. Por framework "full stack" nos referimos a que vas a utilizar Laravel para enrutar peticiones a tu aplicación y renderizar tu frontend vía [Blade templates](/docs/{{version}}/blade) o una tecnología híbrida de aplicación de una sola página como [Inertia](https://inertiajs.com). Esta es la forma más común de utilizar el framework Laravel, y, en nuestra opinión, la forma más productiva de utilizar Laravel.

Si piensa utilizar Laravel de este modo, le recomendamos que consulte nuestra documentación sobre [frontend development](/docs/{{version}}/frontend), [routing](/docs/{{version}}/routing), [views](/docs/{{version}}/views), or the [Eloquent ORM](/docs/{{version}}/eloquent). Además, puede que le interese conocer paquetes comunitarios como [Livewire](https://livewire.laravel.com) and [Inertia](https://inertiajs.com). Estos paquetes le permiten utilizar Laravel como un framework de pila completa mientras disfruta de muchas de las ventajas de interfaz de usuario proporcionadas por las aplicaciones JavaScript de una sola página.

Si está utilizando Laravel como un framework completo, también le recomendamos encarecidamente que aprenda a compilar el CSS y JavaScript de su aplicación utilizando [Vite](/docs/{{version}}/vite).

> [!NOTA]  
> Si quieres empezar a crear tu aplicación, consulta una de nuestras guías oficiales. [application starter kits](/docs/{{version}}/starter-kits).

<a name="laravel-the-api-backend"></a>
### Laravel el API Backend

Laravel también puede servir como API backend para una aplicación JavaScript de una sola página o una aplicación móvil. Por ejemplo, puede utilizar Laravel como API backend para su [Next.js](https://nextjs.org) aplicación. En este contexto, puede utilizar Laravel para proporcionar [authentication](/docs/{{version}}/sanctum) y almacenamiento/recuperación de datos para tu aplicación, a la vez que aprovechas los potentes servicios de Laravel como colas, correos electrónicos, notificaciones y mucho más.

Si esta es la forma en que planea utilizar Laravel, es posible que desee consultar nuestra documentación sobre [routing](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), y [Eloquent ORM](/docs/{{version}}/eloquent).

> [!NOTA]  
> ¿Necesita un andamiaje inicial para su backend Laravel y su frontend Next.js? Laravel Breeze ofrece un [API stack](/docs/{{version}}/starter-kits#breeze-and-next) así como un [Next.js frontend implementation](https://github.com/laravel/breeze-next) para que puedas empezar en cuestión de minutos.
