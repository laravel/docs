# Frontend

- [Introducción](#introduction)
- [Uso de PHP](#using-php)
    - [PHP y Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [Kits de inicio](#php-starter-kits)
- [Uso de Vue / React](#using-vue-react)
    - [Inertia](#inertia)
    - [Kits de inicio](#inertia-starter-kits)
- [Agrupación de activos](#bundling-assets)

<a name="introduction"></a>
## Introducción

Laravel es un framework backend que proporciona todas las características que necesitas para construir aplicaciones web modernas, tales como [enrutamiento](/docs/{{version}}/enrutamiento), [validación](/docs/{{version}}/validación), [almacenamiento en caché](/docs/{{version}}/cache), [colas](/docs/{{version}}/colas), [almacenamiento de archivos](/docs/{{version}}/filesystem), y mucho más. Sin embargo, creemos que es importante ofrecer a los desarrolladores una hermosa experiencia de pila completa, incluyendo enfoques de gran alcance para la construcción de la interfaz de su aplicación.

Hay dos formas principales de abordar el desarrollo frontend al construir una aplicación con Laravel, y el enfoque que elijas está determinado por si deseas construir tu frontend aprovechando PHP o utilizando frameworks de JavaScript como Vue y React. Vamos a discutir estas dos opciones a continuación para que pueda tomar una decisión informada sobre el mejor enfoque para el desarrollo frontend para su aplicación.

<a name="using-php"></a>
## Usando PHP

<a name="php-and-blade"></a>
### PHP y Blade

En el pasado, la mayoría de las aplicaciones PHP renderizaban HTML al navegador usando plantillas HTML simples intercaladas con sentencias PHP `echo` que renderizaban datos que eran recuperados de una base de datos durante la petición:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

En Laravel, este enfoque para la representación de HTML todavía se puede lograr utilizando [views](/docs/{{version}}/views) y [Blade](/docs/{{version}}/blade). Blade es un lenguaje de plantillas extremadamente ligero que proporciona una sintaxis cómoda y corta para mostrar datos, iterar sobre datos y mucho más:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

Cuando se construyen aplicaciones de esta manera, los envíos de formularios y otras interacciones de página suelen recibir un documento HTML completamente nuevo del servidor y el navegador vuelve a renderizar toda la página. Incluso hoy en día, muchas aplicaciones pueden ser perfectamente adecuadas para tener sus frontends construidos de esta manera usando simples plantillas Blade.

<a name="growing-expectations"></a>
#### Expectativas crecientes

Sin embargo, a medida que las expectativas de los usuarios con respecto a las aplicaciones web han ido madurando, muchos desarrolladores se han encontrado con la necesidad de construir frontends más dinámicos con interacciones que se sientan más pulidas. En vista de ello, algunos desarrolladores optan por empezar a construir el frontend de sus aplicaciones utilizando frameworks de JavaScript como Vue y React.

Otros, que prefieren quedarse con el lenguaje de backend con el que se sienten cómodos, han desarrollado soluciones que permiten la construcción de interfaces de usuario de aplicaciones web modernas mientras siguen utilizando principalmente el lenguaje de backend de su elección. Por ejemplo, en el ecosistema [Rails](https://rubyonrails.org/), esto ha impulsado la creación de bibliotecas como [Turbo](https://turbo.hotwired.dev/) [Hotwire](https://hotwired.dev/) y [Stimulus](https://stimulus.hotwired.dev/).

Dentro del ecosistema Laravel, la necesidad de crear frontends modernos y dinámicos utilizando principalmente PHP ha llevado a la creación de [Laravel Livewire](https://livewire.laravel.com) y [Alpine.js](https://alpinejs.dev/).

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com) es un framework para la construcción de interfaces de Laravel que se sienten dinámicas, modernas y vivas al igual que las interfaces construidas con frameworks modernos de JavaScript como Vue y React.

Al utilizar Livewire, crearás "componentes" Livewire que renderizan una porción discreta de tu interfaz de usuario y exponen métodos y datos que pueden ser invocados e interactuados desde el frontend de tu aplicación. Por ejemplo, un simple componente "Contador" podría parecerse a lo siguiente:

```php
<?php

namespace App\Http\Livewire;

use Livewire\Component;

class Counter extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
```

Y, la plantilla correspondiente para el contador se escribiría así:

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

Como puedes ver, Livewire te permite escribir nuevos atributos HTML como `wire:click` que conectan el frontend y el backend de tu aplicación Laravel. Además, puedes renderizar el estado actual de tu componente usando simples expresiones Blade.

Para muchos, Livewire ha revolucionado el desarrollo frontend con Laravel, permitiéndoles permanecer dentro de la comodidad de Laravel mientras construyen aplicaciones web modernas y dinámicas. Por lo general, los desarrolladores que utilizan Livewire también utilizarán [Alpine.js](https://alpinejs.dev/) para "rociar" JavaScript en su frontend sólo cuando sea necesario, por ejemplo, con el fin de representar una ventana de diálogo.

Si eres nuevo en Laravel, te recomendamos que te familiarices con el uso básico de [views](/docs/{{version}}/views) y [Blade](/docs/{{version}}/blade). Después, consulta la documentación oficial de [Laravel Livewire](https://livewire.laravel.com/docs) para aprender a llevar tu aplicación al siguiente nivel con componentes interactivos Livewire.

<a name="php-starter-kits"></a>
### Kits de inicio

Si desea construir su frontend utilizando PHP y Livewire, puede aprovechar nuestros [kits de inicio] Breeze o Jetstream (/docs/{{version}}/starter-kits) para poner en marcha el desarrollo de su aplicación. Ambos kits de inicio organizan el flujo de autenticación del backend y el frontend de tu aplicación utilizando [Blade](/docs/{{version}}/blade) y [Tailwind](https://tailwindcss.com) para que puedas empezar a construir tu próxima gran idea.

<a name="using-vue-react"></a>
## Usando Vue / React

Aunque es posible construir frontends modernos utilizando Laravel y Livewire, muchos desarrolladores siguen prefiriendo aprovechar la potencia de un framework JavaScript como Vue o React. Esto permite a los desarrolladores aprovechar el rico ecosistema de paquetes JavaScript y herramientas disponibles a través de NPM.

Sin embargo, sin herramientas adicionales, el emparejamiento de Laravel con Vue o React nos dejaría con la necesidad de resolver una variedad de problemas complicados como el enrutamiento del lado del cliente, la hidratación de datos y la autenticación. El enrutamiento del lado del cliente a menudo se simplifica mediante el uso de frameworks Vue / React como [Nuxt](https://nuxt.com/) y [Next](https://nextjs.org/); sin embargo, la hidratación de datos y la autenticación siguen siendo problemas complicados y engorrosos de resolver cuando se empareja un framework backend como Laravel con estos frameworks frontend.

Además, los desarrolladores se ven obligados a mantener dos repositorios de código separados, a menudo con la necesidad de coordinar el mantenimiento, las versiones y los despliegues en ambos repositorios. Aunque estos problemas no son insuperables, no creemos que sea una forma productiva o agradable de desarrollar aplicaciones.

<a name="inertia"></a>
### Inercia

Afortunadamente, Laravel ofrece lo mejor de ambos mundos. [Inertia](https://inertiajs.com) tiende un puente entre tu aplicación Laravel y tu moderno frontend Vue o React, permitiéndote construir frontends completos y modernos usando Vue o React mientras aprovechas las rutas y controladores de Laravel para enrutamiento, hidratación de datos y autenticación - todo dentro de un único repositorio de código. Con este enfoque, se puede disfrutar de toda la potencia de Laravel y Vue / React sin paralizar las capacidades de cualquiera de las herramientas.

Después de instalar Inertia en su aplicación Laravel, escribirá rutas y controladores como de costumbre. Sin embargo, en lugar de devolver una plantilla Blade desde su controlador, devolverá una página Inertia:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): Response
    {
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Una página Inertia corresponde a un componente Vue o React, normalmente almacenado dentro del directorio `resources/js/Pages` de tu aplicación. Los datos proporcionados a la página a través del método `Inertia::render` se utilizarán para hidratar las "props" del componente de la página:

```vue
<script setup>
import Layout from '@/Layouts/Authenticated.vue';
import { Head } from '@inertiajs/vue3';

const props = defineProps(['user']);
</script>

<template>
    <Head title="User Profile" />

    <Layout>
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Profile
            </h2>
        </template>

        <div class="py-12">
            Hello, {{ user.name }}
        </div>
    </Layout>
</template>
```

Como puede ver, Inertia le permite aprovechar toda la potencia de Vue o React al construir su frontend, mientras que proporciona un puente ligero entre su backend Laravel y su frontend JavaScript.

#### Server-Side Rendering

Si le preocupa sumergirse en Inertia porque su aplicación requiere renderizado del lado del servidor, no se preocupe. Inertia ofrece [server-side rendering support](https://inertiajs.com/server-side-rendering). Y, al desplegar su aplicación a través de [Laravel Forge](https://forge.laravel.com), es muy fácil asegurarse de que el proceso de renderizado del lado del servidor de Inertia esté siempre en ejecución.

<a name="inertia-starter-kits"></a>
### Kits de inicio

Si desea construir su frontend utilizando Inertia y Vue / React, puede aprovechar nuestros [kits de inicio] Breeze o Jetstream (/docs/{{version}}/starter-kits#breeze-and-inertia) para poner en marcha el desarrollo de su aplicación. Ambos kits de inicio organizan el flujo de autenticación del backend y frontend de tu aplicación utilizando Inertia, Vue / React, [Tailwind](https://tailwindcss.com), y [Vite](https://vitejs.dev) para que puedas empezar a construir tu próxima gran idea.

<a name="bundling-assets"></a>
## Agrupación de Activos

Independientemente de si eliges desarrollar tu frontend usando Blade y Livewire o Vue / React e Inertia, probablemente necesitarás empaquetar el CSS de tu aplicación en activos listos para producción. Por supuesto, si eliges construir el frontend de tu aplicación con Vue o React, también necesitarás empaquetar tus componentes en activos JavaScript listos para el navegador.

Por defecto, Laravel utiliza [Vite](https://vitejs.dev) para empaquetar tus activos. Vite proporciona tiempos de compilación rapidísimos y un Hot Module Replacement (HMR) casi instantáneo durante el desarrollo local. En todas las nuevas aplicaciones Laravel, incluyendo aquellas que utilizan nuestros [starter kits](/docs/{{version}}/starter-kits), encontrarás un archivo `vite.config.js` que carga nuestro ligero plugin Laravel Vite que hace que sea un placer utilizar Vite con las aplicaciones Laravel.

La forma más rápida de empezar con Laravel y Vite es comenzar el desarrollo de tu aplicación utilizando [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze), nuestro kit de inicio más simple que pone en marcha tu aplicación proporcionando un andamiaje de autenticación frontend y backend.

> NOTA  
> Para una documentación más detallada sobre la utilización de Vite con Laravel, por favor consulte nuestra [documentación dedicada a la agrupación y compilación de sus activos](/docs/{{version}}/vite).
