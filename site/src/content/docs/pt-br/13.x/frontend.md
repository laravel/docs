---
title: "Frontend"
---

- [Introdução](#introduction)
- [Usando PHP](#using-php)
    - [PHP e Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [Starter Kits](#php-starter-kits)
- [Usando React, Svelte ou Vue](#using-react-svelte-or-vue)
    - [Inertia](#inertia)
    - [Starter Kits](#inertia-starter-kits)
- [Bundling de assets](#bundling-assets)

<a id="introduction"></a>
## Introdução

O Laravel é um framework backend que fornece todos os recursos de que você precisa para criar aplicações web modernas, como [roteamento](../routing/), [validação](../validation/), [cache](../cache/), [filas](../queues/), [armazenamento de arquivos](../filesystem/) e muito mais. No entanto, acreditamos que é importante oferecer aos desenvolvedores uma bela experiência full-stack, incluindo abordagens poderosas para construir o frontend da sua aplicação.

Existem duas maneiras principais de abordar o desenvolvimento de frontend ao criar uma aplicação com Laravel, e a abordagem que você escolhe é determinada por se você deseja construir seu frontend aproveitando o PHP ou usando frameworks JavaScript como React, Svelte e Vue. Discutiremos ambas as opções abaixo para que você possa tomar uma decisão informada sobre a melhor abordagem de desenvolvimento de frontend para a sua aplicação.

<a id="using-php"></a>
## Usando PHP

<a id="php-and-blade"></a>
### PHP e Blade

No passado, a maioria das aplicações PHP renderizava HTML para o navegador usando simples templates HTML intercalados com declarações `echo` em PHP, que renderizam dados que foram recuperados de um banco de dados durante a requisição:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

No Laravel, essa abordagem para renderizar HTML ainda pode ser alcançada usando [views](../views/) e [Blade](../blade/). O Blade é uma linguagem de template extremamente leve que fornece uma sintaxe curta e conveniente para exibir dados, iterar sobre dados e mais:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

Ao construir aplicações dessa forma, o envio de formulários e outras interações com a página normalmente recebem um documento HTML completamente novo do servidor, e a página inteira é renderizada novamente pelo navegador. Mesmo hoje, muitas aplicações podem ser perfeitamente adequadas para ter seus frontends construídos dessa forma usando simples templates Blade.

<a id="growing-expectations"></a>
#### Expectativas crescentes

No entanto, à medida que as expectativas dos usuários em relação às aplicações web amadureceram, muitos desenvolvedores sentiram a necessidade de construir frontends mais dinâmicos, com interações que parecem mais polidas. Diante disso, alguns desenvolvedores escolhem começar a construir o frontend da sua aplicação usando frameworks JavaScript como React, Svelte e Vue.

Outros, preferindo permanecer com a linguagem de backend com a qual estão confortáveis, desenvolveram soluções que permitem a construção de UIs de aplicações web modernas enquanto ainda utilizam principalmente sua linguagem de backend de preferência. Por exemplo, no ecossistema [Rails](https://rubyonrails.org/), isso estimulou a criação de bibliotecas como [Turbo](https://turbo.hotwired.dev/) [Hotwire](https://hotwired.dev/) e [Stimulus](https://stimulus.hotwired.dev/).

Dentro do ecossistema Laravel, a necessidade de criar frontends modernos e dinâmicos usando principalmente o PHP levou à criação do [Laravel Livewire](https://livewire.laravel.com) e do [Alpine.js](https://alpinejs.dev/).

<a id="livewire"></a>
### Livewire

O [Laravel Livewire](https://livewire.laravel.com) é um framework para construir frontends movidos a Laravel que parecem dinâmicos, modernos e vivos, assim como frontends construídos com frameworks JavaScript modernos como React, Svelte e Vue.

Ao usar o Livewire, você criará "componentes" do Livewire que renderizam uma porção discreta da sua UI e expõem métodos e dados que podem ser invocados e com os quais se pode interagir a partir do frontend da sua aplicação. Por exemplo, um simples componente "Counter" poderia ter a seguinte aparência:

```php
<?php

use Livewire\Component;

new class extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }
};
?>

<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>

```

Como você pode ver, o Livewire permite que você escreva novos atributos HTML como `wire:click` que conectam o frontend e o backend da sua aplicação Laravel. Além disso, você pode renderizar o estado atual do seu componente usando simples expressões Blade.

Para muitos, o Livewire revolucionou o desenvolvimento de frontend com Laravel, permitindo que permaneçam no conforto do Laravel enquanto constroem aplicações web modernas e dinâmicas. Normalmente, os desenvolvedores que usam Livewire também utilizam o [Alpine.js](https://alpinejs.dev/) para "polvilhar" JavaScript no frontend apenas onde ele é necessário, como para renderizar uma janela de diálogo.

Se você é novo no Laravel, recomendamos que se familiarize com o uso básico de [views](../views/) e do [Blade](../blade/). Em seguida, consulte a [documentação oficial do Laravel Livewire](https://livewire.laravel.com/docs) para aprender como levar sua aplicação ao próximo nível com componentes interativos do Livewire.

<a id="php-starter-kits"></a>
### Starter Kits

Se você quiser construir seu frontend usando PHP e Livewire, pode aproveitar o nosso [Starter Kit do Livewire](../starter-kits/) para impulsionar o desenvolvimento da sua aplicação.

<a id="using-react-svelte-or-vue"></a>
## Usando React, Svelte ou Vue

Embora seja possível construir frontends modernos usando Laravel e Livewire, muitos desenvolvedores ainda preferem aproveitar o poder de um framework JavaScript como React, Svelte ou Vue. Isso permite que os desenvolvedores aproveitem o rico ecossistema de pacotes e ferramentas JavaScript disponíveis via NPM.

No entanto, sem ferramentas adicionais, combinar Laravel com React, Svelte ou Vue nos deixaria precisando resolver uma variedade de problemas complicados, como roteamento no lado do cliente, hidratação de dados e autenticação. O roteamento no lado do cliente geralmente é simplificado usando frameworks React / Svelte / Vue opinativos como [Next](https://nextjs.org/) e [Nuxt](https://nuxt.com/); no entanto, a hidratação de dados e a autenticação permanecem como problemas complicados e trabalhosos de resolver ao combinar um framework de backend como o Laravel com esses frameworks de frontend.

Além disso, os desenvolvedores ficam mantendo dois repositórios de código separados, frequentemente precisando coordenar manutenção, lançamentos e deploys em ambos os repositórios. Embora esses problemas não sejam insuperáveis, não acreditamos que seja uma forma produtiva ou agradável de desenvolver aplicações.

<a id="inertia"></a>
### Inertia

Felizmente, o Laravel oferece o melhor dos dois mundos. O [Inertia](https://inertiajs.com) fecha a lacuna entre a sua aplicação Laravel e o seu frontend moderno em React, Svelte ou Vue, permitindo que você construa frontends completos e modernos usando React, Svelte ou Vue, enquanto aproveita as rotas e controladores do Laravel para roteamento, hidratação de dados e autenticação — tudo dentro de um único repositório de código. Com essa abordagem, você pode desfrutar de todo o poder do Laravel e do React / Svelte / Vue sem prejudicar as capacidades de nenhuma das ferramentas.

Depois de instalar o Inertia na sua aplicação Laravel, você escreverá rotas e controladores normalmente. No entanto, em vez de retornar um template Blade do seu controlador, você retornará uma página do Inertia:

```php
<?php

namespace App\Http\Controllers;

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
        return Inertia::render('users/show', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Uma página do Inertia corresponde a um componente React, Svelte ou Vue, normalmente armazenado dentro do diretório `resources/js/pages` da sua aplicação. Os dados fornecidos à página através do método `Inertia::render` serão usados para hidratar os "props" do componente da página:

```jsx
import Layout from '@/layouts/authenticated';
import { Head } from '@inertiajs/react';

export default function Show({ user }) {
    return (
        <Layout>
            <Head title="Welcome" />
            <h1>Welcome</h1>
            <p>Hello {user.name}, welcome to Inertia.</p>
        </Layout>
    )
}
```

Como você pode ver, o Inertia permite que você aproveite todo o poder do React, Svelte ou Vue ao construir seu frontend, ao mesmo tempo que fornece uma ponte leve entre o seu backend movido a Laravel e o seu frontend movido a JavaScript.

#### Renderização no lado do servidor

Se você está preocupado em mergulhar no Inertia porque sua aplicação requer renderização no lado do servidor, não se preocupe. O Inertia oferece [suporte a renderização no lado do servidor](https://inertiajs.com/server-side-rendering). E, ao fazer o deploy da sua aplicação via [Laravel Cloud](https://cloud.laravel.com) ou [Laravel Forge](https://forge.laravel.com), é muito fácil garantir que o processo de renderização no lado do servidor do Inertia esteja sempre em execução.

<a id="inertia-starter-kits"></a>
### Starter Kits

Se você quiser construir seu frontend usando Inertia e React / Svelte / Vue, pode aproveitar os nossos [Starter Kits de aplicação React, Svelte ou Vue](../starter-kits/) para impulsionar o desenvolvimento da sua aplicação. Todos esses Starter Kits criam o scaffolding do fluxo de autenticação do backend e do frontend da sua aplicação usando Inertia, React / Svelte / Vue, [Tailwind](https://tailwindcss.com) e [Vite](https://vitejs.dev), para que você possa começar a construir sua próxima grande ideia.

<a id="bundling-assets"></a>
## Bundling de assets

Independentemente de você escolher desenvolver seu frontend usando Blade e Livewire ou React / Svelte / Vue e Inertia, você provavelmente precisará fazer o bundle do CSS da sua aplicação em assets prontos para produção. Claro, se você escolher construir o frontend da sua aplicação com React, Svelte ou Vue, você também precisará fazer o bundle dos seus componentes em assets JavaScript prontos para o navegador.

Por padrão, o Laravel utiliza o [Vite](https://vitejs.dev) para fazer o bundle dos seus assets. O Vite fornece tempos de build ultrarrápidos e Hot Module Replacement (HMR) quase instantâneo durante o desenvolvimento local. Em todas as novas aplicações Laravel, incluindo aquelas que usam nossos [Starter Kits](../starter-kits/), você encontrará um arquivo `vite.config.js` que carrega nosso plugin leve do Laravel para o Vite, o que torna o Vite um prazer de usar com aplicações Laravel.

A maneira mais rápida de começar com Laravel e Vite é iniciar o desenvolvimento da sua aplicação usando [nossos Starter Kits de aplicação](../starter-kits/), que impulsionam sua aplicação fornecendo scaffolding de autenticação no frontend e no backend.

> **Nota:**
> Para uma documentação mais detalhada sobre como utilizar o Vite com Laravel, consulte a nossa [documentação dedicada sobre bundling e compilação dos seus assets](../vite/).
