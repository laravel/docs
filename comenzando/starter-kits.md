# Starter Kits

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [Breeze and Blade](#breeze-and-blade)
    - [Breeze and Livewire](#breeze-and-livewire)
    - [Breeze and React / Vue](#breeze-and-inertia)
    - [Breeze and Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## Introducción

Para darte una ventaja inicial en la construcción de tu nueva aplicación Laravel, estamos encantados de ofrecerte kits de inicio de autenticación y aplicación. Estos kits componen automáticamente tu aplicación con las rutas, controladores y vistas que necesitas para registrar y autenticar a los usuarios de tu aplicación.

Aunque le invitamos a utilizar estos kits de inicio, no son obligatorios. Eres libre de construir tu propia aplicación desde cero simplemente instalando una copia nueva de Laravel. De cualquier manera, ¡sabemos que construirás algo genial!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze) es una implementación mínima y sencilla de todas las funciones de Laravel de [autenticación](/docs/{{version}}/authentication), que incluyen el inicio de sesión, el registro, el restablecimiento de la contraseña, la verificación del correo electrónico y la confirmación de la contraseña. Además, Breeze incluye una sencilla página de "perfil" en la que el usuario puede actualizar su nombre, dirección de correo electrónico y contraseña.

La capa de vista por defecto de Laravel Breeze se compone de simples [templates Blade](/docs/{{version}}/blade) con [Tailwind CSS](https://tailwindcss.com). Además, Breeze ofrece opciones de andamiaje basadas en [Livewire](https://livewire.laravel.com) o [Inertia](https://inertiajs.com), con la opción de usar Vue o React para el andamiaje basado en Inertia.

<img src="https://laravel.com/img/docs/breeze-register.png">

#### Laravel Bootcamp

Si usted es nuevo en Laravel, no dude en saltar en el [Laravel Bootcamp](https://bootcamp.laravel.com). El Laravel Bootcamp le guiará a través de la construcción de su primera aplicación Laravel utilizando Breeze. Es una gran manera de conseguir un recorrido por todo lo que Laravel y Breeze tienen que ofrecer.

<a name="laravel-breeze-installation"></a>
### Instalación

En primer lugar, debes [crear una nueva aplicación Laravel](/docs/{{version}}/installation). Si crea su aplicación utilizando la función [Laravel installer](/docs/{{version}}/installation#creating-a-laravel-project), se le pedirá que instale Laravel Breeze durante el proceso de instalación. De lo contrario, tendrá que seguir las instrucciones de instalación manual a continuación.

Si ya has creado una nueva aplicación Laravel sin un kit de inicio, puedes instalar manualmente Laravel Breeze usando Composer:

```shell
composer require laravel/breeze --dev
```

Después de que Composer haya instalado el paquete Laravel Breeze, debes ejecutar el comando `breeze:install` Artisan. Este comando publica las vistas de autenticación, rutas, controladores y otros recursos en tu aplicación. Laravel Breeze publica todo su código a tu aplicación para que tengas control total y visibilidad sobre sus características e implementación.

El comando `breeze:install` te preguntará por tu frontend stack y framework de pruebas preferido:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
### Breeze y Blade

La "pila" por defecto de Breeze es la pila Blade, que utiliza simples [templates Blade](/docs/{{version}}/blade) para renderizar el frontend de su aplicación. La pila Blade puede instalarse invocando el comando `breeze:install` sin otros argumentos adicionales y seleccionando la pila de frontend Blade. Una vez instalado el andamiaje de Breeze, también debes compilar los activos del frontend de tu aplicación:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

A continuación, puede navegar a su aplicación `/login` o `/register` URLs en su navegador web. Todas las rutas de Breeze se definen en el archivo `routes/auth.php`.

> [!NOTA]  
> Para obtener más información sobre la compilación de CSS y JavaScript de su aplicación, consulte Laravel's [Vite documentation](/docs/{{version}}/vite#running-vite).

<a name="breeze-and-livewire"></a>
### Breeze and Livewire

Laravel Breeze also offers [Livewire](https://livewire.laravel.com) andamiaje. Livewire es una poderosa forma de construir interfaces de usuario dinámicas, reactivas y frontales utilizando sólo PHP.

Livewire es un gran ajuste para los equipos que utilizan principalmente plantillas Blade y están buscando una alternativa más simple a los frameworks SPA basados en JavaScript como Vue y React.

Para utilizar la pila Livewire, puede seleccionar la pila frontend Livewire al ejecutar el comando Artisan `breeze:install`. Después de instalar el andamiaje de Breeze, debes ejecutar tus migraciones de base de datos:

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
### Laravel Breeze y React / Vue

Laravel Breeze también ofrece andamiaje React y Vue a través de la implementación de [Inertia](https://inertiajs.com). Inertia le permite construir aplicaciones React y Vue modernas y de una sola página utilizando enrutamiento y controladores clásicos del lado del servidor.

Inertia le permite disfrutar de la potencia frontend de React y Vue combinada con la increíble productividad backend de Laravel y la velocidad del rayo. [Vite](https://vitejs.dev) compilación. Para utilizar una pila Inertia, puedes seleccionar las pilas frontales Vue o React al ejecutar el comando `breeze:install` Artisan.

Cuando selecciones el frontend Vue o React, el instalador de Breeze también te preguntará si deseas usar [Inertia SSR](https://inertiajs.com/server-side-rendering) o TypeScript. Una vez instalado el andamiaje de Breeze, también debes compilar los activos frontales de tu aplicación:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

A continuación, puede navegar a su aplicación `/login` o `/register` URLs en su navegador web. Todas las rutas de Breeze se definen en el archivo `routes/auth.php`.

<a name="breeze-and-next"></a>
### Laravel Breeze y Next.js / API

Laravel Breeze también puede andamiar una API de autenticación que está preparada para autenticar aplicaciones JavaScript modernas como las impulsadas por [Next](https://nextjs.org), [Nuxt](https://nuxt.com), y otros. Para empezar, seleccione la pila API como su pila deseada al ejecutar el comando `breeze:install` Artisan:

```shell
php artisan breeze:install

php artisan migrate
```

Durante la instalación, Breeze añadirá una variable de entorno `FRONTEND_URL` al archivo `.env` de tu aplicación. Esta URL debe ser la URL de su aplicación JavaScript. Normalmente será `http://localhost:3000` durante el desarrollo local. Además, debes asegurarte de que tu `APP_URL` está configurada en `http://localhost:8000`, que es la URL por defecto utilizada por el comando `serve` de Artisan.

<a name="next-reference-implementation"></a>
#### Implementación de referencia de Next.js

Finalmente, estás listo para emparejar este backend con el frontend de tu elección. Una implementación de referencia Next del frontend Breeze está [disponible en GitHub](https://github.com/laravel/breeze-next). Este frontend está mantenido por Laravel y contiene la misma interfaz de usuario que los stacks tradicionales Blade e Inertia proporcionados por Breeze.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Mientras que Laravel Breeze proporciona un punto de partida simple y mínimo para la construcción de una aplicación Laravel, Jetstream aumenta esa funcionalidad con características más robustas y pilas de tecnología frontend adicionales. **Para los recién llegados a Laravel, se recomienda aprender las cuerdas con Laravel Breeze antes de graduarse a Laravel Jetstream.

Jetstream proporciona un andamiaje de aplicaciones bellamente diseñado para Laravel e incluye inicio de sesión, registro, verificación de correo electrónico, autenticación de dos factores, gestión de sesiones, soporte de API a través de Laravel Sanctum y gestión de equipos opcional. Jetstream está diseñado utilizando [Tailwind CSS](https://tailwindcss.com) y le ofrece la posibilidad de elegir entre [Livewire](https://livewire.laravel.com) de [Inertia](https://inertiajs.com) para el frontend.

La documentación completa para la instalación de Laravel Jetstream se puede encontrar en el archivo [official de la documentación de Jetstream](https://jetstream.laravel.com).
