---
title: "Starter Kits"
---

- [Introdução](#introduction)
- [Criando uma aplicação usando um Starter Kit](#creating-an-application)
- [Starter Kits disponíveis](#available-starter-kits)
    - [React](#react)
    - [Svelte](#svelte)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [Personalização do Starter Kit](#starter-kit-customization)
    - [React](#react-customization)
    - [Svelte](#svelte-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [Autenticação](#authentication)
    - [Habilitando e desabilitando recursos](#enabling-and-disabling-features)
    - [Personalizando a criação de usuários e a redefinição de senha](#customizing-actions)
    - [Autenticação de dois fatores](#two-factor-authentication)
    - [Limitação de taxa](#rate-limiting)
- [Equipes](#teams)
- [Autenticação com WorkOS AuthKit](#workos)
    - [Configurando seu Starter Kit do WorkOS](#configuring-your-workos-starter-kit)
- [Inertia SSR](#inertia-ssr)
- [Starter Kits mantidos pela comunidade](#community-maintained-starter-kits)
- [Perguntas frequentes](#faqs)

<a id="introduction"></a>
## Introdução

Para dar a você uma vantagem inicial na construção de sua nova aplicação Laravel, temos o prazer de oferecer [starter kits de aplicação](https://laravel.com/starter-kits). Esses starter kits dão a você uma vantagem inicial na construção de sua próxima aplicação Laravel e incluem as rotas, os controladores e as views necessários para registrar e autenticar os usuários da sua aplicação. Os starter kits usam o [Laravel Fortify](../fortify/) para fornecer autenticação.

Embora você seja bem-vindo a usar esses starter kits, eles não são obrigatórios. Você é livre para construir sua própria aplicação do zero, simplesmente instalando uma nova cópia do Laravel. De qualquer forma, sabemos que você construirá algo incrível!

<a id="creating-an-application"></a>
## Criando uma aplicação usando um Starter Kit

Para criar uma nova aplicação Laravel usando um dos nossos starter kits, você deve primeiro [instalar o PHP e a ferramenta de CLI do Laravel](../installation/#installing-php). Se você já tem o PHP e o Composer instalados, pode instalar a ferramenta de CLI do instalador do Laravel via Composer:

```shell
composer global require laravel/installer
```

Em seguida, crie uma nova aplicação Laravel usando a CLI do instalador do Laravel. O instalador do Laravel solicitará que você selecione seu starter kit preferido:

```shell
laravel new my-app
```

Depois de criar sua aplicação Laravel, você só precisa instalar suas dependências de frontend via NPM e iniciar o servidor de desenvolvimento do Laravel:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Depois de iniciar o servidor de desenvolvimento do Laravel, sua aplicação estará acessível no seu navegador web em [http://localhost:8000](http://localhost:8000).

<a id="available-starter-kits"></a>
## Starter Kits disponíveis

<a id="react"></a>
### React

Nosso starter kit React fornece um ponto de partida robusto e moderno para construir aplicações Laravel com um frontend React usando [Inertia](https://inertiajs.com).

O Inertia permite que você construa aplicações React modernas de página única usando roteamento e controladores clássicos no servidor. Isso permite que você desfrute do poder de frontend do React combinado com a incrível produtividade de backend do Laravel e a compilação ultrarrápida do Vite.

O starter kit React utiliza React 19, TypeScript, Tailwind e a biblioteca de componentes [shadcn/ui](https://ui.shadcn.com).

<a id="svelte"></a>
### Svelte

Nosso starter kit Svelte fornece um ponto de partida robusto e moderno para construir aplicações Laravel com um frontend Svelte usando [Inertia](https://inertiajs.com).

O Inertia permite que você construa aplicações Svelte modernas de página única usando roteamento e controladores clássicos no servidor. Isso permite que você desfrute do poder de frontend do Svelte combinado com a incrível produtividade de backend do Laravel e a compilação ultrarrápida do Vite.

O starter kit Svelte utiliza Svelte 5, TypeScript, Tailwind e a biblioteca de componentes [shadcn-svelte](https://www.shadcn-svelte.com/).

<a id="vue"></a>
### Vue

Nosso starter kit Vue fornece um ótimo ponto de partida para construir aplicações Laravel com um frontend Vue usando [Inertia](https://inertiajs.com).

O Inertia permite que você construa aplicações Vue modernas de página única usando roteamento e controladores clássicos no servidor. Isso permite que você desfrute do poder de frontend do Vue combinado com a incrível produtividade de backend do Laravel e a compilação ultrarrápida do Vite.

O starter kit Vue utiliza a Vue Composition API, TypeScript, Tailwind e a biblioteca de componentes [shadcn-vue](https://www.shadcn-vue.com/).

<a id="livewire"></a>
### Livewire

Nosso starter kit Livewire fornece o ponto de partida perfeito para construir aplicações Laravel com um frontend [Laravel Livewire](https://livewire.laravel.com).

O Livewire é uma maneira poderosa de construir UIs de frontend dinâmicas e reativas usando apenas o PHP. É uma ótima opção para equipes que usam principalmente templates Blade e procuram uma alternativa mais simples a frameworks SPA orientados a JavaScript como React, Svelte e Vue.

O starter kit Livewire utiliza Livewire, Tailwind e a biblioteca de componentes [Flux UI](https://fluxui.dev).

<a id="starter-kit-customization"></a>
## Personalização do Starter Kit

<a id="react-customization"></a>
### React

Nosso starter kit React é construído com Inertia 3, React 19, Tailwind 4 e [shadcn/ui](https://ui.shadcn.com). Como em todos os nossos starter kits, todo o código de backend e frontend existe dentro da sua aplicação para permitir personalização completa.

A maior parte do código de frontend está localizada no diretório `resources/js`. Você é livre para modificar qualquer parte do código para personalizar a aparência e o comportamento da sua aplicação:

```text
resources/js/
├── components/    # Reusable React components
├── hooks/         # React hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

Para publicar componentes shadcn adicionais, primeiro [encontre o componente que você deseja publicar](https://ui.shadcn.com). Em seguida, publique o componente usando `npx`:

```shell
npx shadcn@latest add switch
```

Neste exemplo, o comando publicará o componente Switch em `resources/js/components/ui/switch.tsx`. Depois que o componente tiver sido publicado, você poderá usá-lo em qualquer uma das suas páginas:

```jsx
import { Switch } from "@/components/ui/switch"

const MyPage = () => {
  return (
    <div>
      <Switch />
    </div>
  );
};

export default MyPage;
```

<a id="react-available-layouts"></a>
#### Layouts disponíveis

O starter kit React inclui dois layouts principais diferentes para você escolher: um layout "sidebar" e um layout "header". O layout sidebar é o padrão, mas você pode mudar para o layout header modificando o layout que é importado no topo do arquivo `resources/js/layouts/app-layout.tsx` da sua aplicação:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a id="react-sidebar-variants"></a>
#### Variantes de sidebar

O layout sidebar inclui três variantes diferentes: a variante sidebar padrão, a variante "inset" e a variante "floating". Você pode escolher a variante que mais gosta modificando o componente `resources/js/components/app-sidebar.tsx`:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a id="react-authentication-page-layout-variants"></a>
#### Variantes de layout da página de autenticação

As páginas de autenticação incluídas no starter kit React, como a página de login e a página de registro, também oferecem três variantes de layout diferentes: "simple", "card" e "split".

Para alterar o layout de autenticação, modifique o layout que é importado no topo do arquivo `resources/js/layouts/auth-layout.tsx` da sua aplicação:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a id="svelte-customization"></a>
### Svelte

Nosso starter kit Svelte é construído com Inertia 3, Svelte 5, Tailwind e [shadcn-svelte](https://www.shadcn-svelte.com/). Como em todos os nossos starter kits, todo o código de backend e frontend existe dentro da sua aplicação para permitir personalização completa.

A maior parte do código de frontend está localizada no diretório `resources/js`. Você é livre para modificar qualquer parte do código para personalizar a aparência e o comportamento da sua aplicação:

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```

Para publicar componentes shadcn-svelte adicionais, primeiro [encontre o componente que você deseja publicar](https://www.shadcn-svelte.com). Em seguida, publique o componente usando `npx`:

```shell
npx shadcn-svelte@latest add switch
```

Neste exemplo, o comando publicará o componente Switch em `resources/js/components/ui/switch/switch.svelte`. Depois que o componente tiver sido publicado, você poderá usá-lo em qualquer uma das suas páginas:

```svelte
<script lang="ts">
    import { Switch } from '@/components/ui/switch'
</script>

<div>
    <Switch />
</div>
```

<a id="svelte-available-layouts"></a>
#### Layouts disponíveis

O starter kit Svelte inclui dois layouts principais diferentes para você escolher: um layout "sidebar" e um layout "header". O layout sidebar é o padrão, mas você pode mudar para o layout header modificando o layout que é importado no topo do arquivo `resources/js/layouts/AppLayout.svelte` da sua aplicação:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

<a id="svelte-sidebar-variants"></a>
#### Variantes de sidebar

O layout sidebar inclui três variantes diferentes: a variante sidebar padrão, a variante "inset" e a variante "floating". Você pode escolher a variante que mais gosta modificando o componente `resources/js/components/AppSidebar.svelte`:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a id="svelte-authentication-page-layout-variants"></a>
#### Variantes de layout da página de autenticação

As páginas de autenticação incluídas no starter kit Svelte, como a página de login e a página de registro, também oferecem três variantes de layout diferentes: "simple", "card" e "split".

Para alterar o layout de autenticação, modifique o layout que é importado no topo do arquivo `resources/js/layouts/AuthLayout.svelte` da sua aplicação:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a id="vue-customization"></a>
### Vue

Nosso starter kit Vue é construído com Inertia 3, Vue 3 Composition API, Tailwind e [shadcn-vue](https://www.shadcn-vue.com/). Como em todos os nossos starter kits, todo o código de backend e frontend existe dentro da sua aplicação para permitir personalização completa.

A maior parte do código de frontend está localizada no diretório `resources/js`. Você é livre para modificar qualquer parte do código para personalizar a aparência e o comportamento da sua aplicação:

```text
resources/js/
├── components/    # Reusable Vue components
├── composables/   # Vue composables / hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

Para publicar componentes shadcn-vue adicionais, primeiro [encontre o componente que você deseja publicar](https://www.shadcn-vue.com). Em seguida, publique o componente usando `npx`:

```shell
npx shadcn-vue@latest add switch
```

Neste exemplo, o comando publicará o componente Switch em `resources/js/components/ui/Switch.vue`. Depois que o componente tiver sido publicado, você poderá usá-lo em qualquer uma das suas páginas:

```vue
<script setup lang="ts">
import { Switch } from '@/components/ui/switch'
</script>

<template>
    <div>
        <Switch />
    </div>
</template>
```

<a id="vue-available-layouts"></a>
#### Layouts disponíveis

O starter kit Vue inclui dois layouts principais diferentes para você escolher: um layout "sidebar" e um layout "header". O layout sidebar é o padrão, mas você pode mudar para o layout header modificando o layout que é importado no topo do arquivo `resources/js/layouts/AppLayout.vue` da sua aplicação:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a id="vue-sidebar-variants"></a>
#### Variantes de sidebar

O layout sidebar inclui três variantes diferentes: a variante sidebar padrão, a variante "inset" e a variante "floating". Você pode escolher a variante que mais gosta modificando o componente `resources/js/components/AppSidebar.vue`:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a id="vue-authentication-page-layout-variants"></a>
#### Variantes de layout da página de autenticação

As páginas de autenticação incluídas no starter kit Vue, como a página de login e a página de registro, também oferecem três variantes de layout diferentes: "simple", "card" e "split".

Para alterar o layout de autenticação, modifique o layout que é importado no topo do arquivo `resources/js/layouts/AuthLayout.vue` da sua aplicação:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a id="livewire-customization"></a>
### Livewire

Nosso starter kit Livewire é construído com Livewire 4, Tailwind e [Flux UI](https://fluxui.dev/). Como em todos os nossos starter kits, todo o código de backend e frontend existe dentro da sua aplicação para permitir personalização completa.

A maior parte do código de frontend está localizada no diretório `resources/views`. Você é livre para modificar qualquer parte do código para personalizar a aparência e o comportamento da sua aplicação:

```text
resources/views
├── components            # Reusable components
├── flux                  # Customized Flux components
├── layouts               # Application layouts
├── pages                 # Livewire pages
├── partials              # Reusable Blade partials
├── dashboard.blade.php   # Authenticated user dashboard
├── welcome.blade.php     # Guest user welcome page
```

<a id="livewire-available-layouts"></a>
#### Layouts disponíveis

O starter kit Livewire inclui dois layouts principais diferentes para você escolher: um layout "sidebar" e um layout "header". O layout sidebar é o padrão, mas você pode mudar para o layout header modificando o layout usado pelo arquivo `resources/views/layouts/app.blade.php` da sua aplicação. Além disso, você deve adicionar o atributo `container` ao componente principal do Flux:

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a id="livewire-authentication-page-layout-variants"></a>
#### Variantes de layout da página de autenticação

As páginas de autenticação incluídas no starter kit Livewire, como a página de login e a página de registro, também oferecem três variantes de layout diferentes: "simple", "card" e "split".

Para alterar o layout de autenticação, modifique o layout usado pelo arquivo `resources/views/layouts/auth.blade.php` da sua aplicação:

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a id="authentication"></a>
## Autenticação

Todos os starter kits usam o [Laravel Fortify](../fortify/) para lidar com a autenticação. O Fortify fornece rotas, controladores e lógica para login, registro, redefinição de senha, verificação de e-mail e muito mais.

O Fortify registra automaticamente as seguintes rotas de autenticação com base nos recursos habilitados no arquivo de configuração `config/fortify.php` da sua aplicação:

<div class="overflow-auto">

| Rota                               | Método   | Descrição                              |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login`                           | `GET`    | Exibir formulário de login                    |
| `/login`                           | `POST`   | Autenticar usuário                            |
| `/logout`                          | `POST`   | Desconectar usuário                           |
| `/register`                        | `GET`    | Exibir formulário de registro                 |
| `/register`                        | `POST`   | Criar novo usuário                            |
| `/forgot-password`                 | `GET`    | Exibir formulário de solicitação de redefinição de senha |
| `/forgot-password`                 | `POST`   | Enviar link de redefinição de senha           |
| `/reset-password/{token}`          | `GET`    | Exibir formulário de redefinição de senha     |
| `/reset-password`                  | `POST`   | Atualizar senha                               |
| `/email/verify`                    | `GET`    | Exibir aviso de verificação de e-mail         |
| `/email/verify/{id}/{hash}`        | `GET`    | Verificar endereço de e-mail                  |
| `/email/verification-notification` | `POST`   | Reenviar e-mail de verificação                |
| `/user/confirm-password`           | `GET`    | Exibir formulário de confirmação de senha     |
| `/user/confirm-password`           | `POST`   | Confirmar senha                               |
| `/two-factor-challenge`            | `GET`    | Exibir formulário de desafio de 2FA           |
| `/two-factor-challenge`            | `POST`   | Verificar código de 2FA                       |

</div>

O comando Artisan `php artisan route:list` pode ser usado para exibir todas as rotas da sua aplicação.

<a id="enabling-and-disabling-features"></a>
### Habilitando e desabilitando recursos

Você pode controlar quais recursos do Fortify estão habilitados no arquivo de configuração `config/fortify.php` da sua aplicação:

```php
use Laravel\Fortify\Features;

'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
    Features::twoFactorAuthentication([
        'confirm' => true,
        'confirmPassword' => true,
    ]),
],
```

Para desabilitar um recurso, comente ou remova a entrada desse recurso do array `features`. Por exemplo, remova `Features::registration()` para desabilitar o registro público.

Ao usar os starter kits [React](#react), [Svelte](#svelte) ou [Vue](#vue), você também precisará remover quaisquer referências às rotas do recurso desabilitado no seu código de frontend. Por exemplo, se você desabilitar a verificação de e-mail, deverá remover os imports e as referências às rotas `verification` nos seus componentes React, Svelte ou Vue. Isso é necessário porque esses starter kits usam o Wayfinder para roteamento type-safe, que gera definições de rotas em tempo de build. Se você referenciar rotas que não existem mais, sua aplicação falhará no build.

<a id="customizing-actions"></a>
### Personalizando a criação de usuários e a redefinição de senha

Quando um usuário se registra ou redefine sua senha, o Fortify invoca classes de ação localizadas no diretório `app/Actions/Fortify` da sua aplicação:

<div class="overflow-auto">

| Arquivo                        | Descrição                           |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php`           | Valida e cria novos usuários          |
| `ResetUserPassword.php`       | Valida e atualiza senhas de usuários  |
| `PasswordValidationRules.php` | Define regras de validação de senha   |

</div>

Por exemplo, para personalizar a lógica de registro da sua aplicação, você deve editar a ação `CreateNewUser`:

```php
public function create(array $input): User
{
    Validator::make($input, [
        'name' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'max:255', 'unique:users'],
        'phone' => ['required', 'string', 'max:20'], // [tl! add]
        'password' => $this->passwordRules(),
    ])->validate();

    return User::create([
        'name' => $input['name'],
        'email' => $input['email'],
        'phone' => $input['phone'], // [tl! add]
        'password' => Hash::make($input['password']),
    ]);
}
```

<a id="two-factor-authentication"></a>
### Autenticação de dois fatores

Os starter kits incluem autenticação de dois fatores (2FA) integrada, permitindo que os usuários protejam suas contas usando qualquer aplicativo autenticador compatível com TOTP. A 2FA é habilitada por padrão via `Features::twoFactorAuthentication()` no arquivo de configuração `config/fortify.php` da sua aplicação.

A opção `confirm` exige que os usuários verifiquem um código antes de a 2FA ser totalmente habilitada, enquanto `confirmPassword` exige a confirmação da senha antes de habilitar ou desabilitar a 2FA. Para mais detalhes, consulte a [documentação de autenticação de dois fatores do Fortify](../fortify/#two-factor-authentication).

<a id="rate-limiting"></a>
### Limitação de taxa

A limitação de taxa evita que ataques de força bruta e tentativas de login repetidas sobrecarreguem seus endpoints de autenticação. Você pode personalizar o comportamento de limitação de taxa do Fortify no `FortifyServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a id="teams"></a>
## Equipes

Os starter kits React, Svelte, Vue e Livewire também podem ser gerados com suporte a equipes. Quando o recurso de equipes está habilitado, cada usuário pertence a uma ou mais equipes e tem uma equipe atual. Durante o registro, novos usuários recebem automaticamente uma equipe pessoal. Os starter kits também incluem telas de gerenciamento de equipes para criar equipes, alternar entre equipes, convidar membros e atualizar detalhes da equipe.

Quando uma rota está escopada à equipe atual, o slug da equipe atual é incluído na URL. Por exemplo, a rota do dashboard se torna `/{current_team}/dashboard`, enquanto as páginas de gerenciamento de equipes usam rotas como `settings/teams/{team}`. Ao usar os parâmetros de rota `{current_team}` e `{team}`, os starter kits garantem automaticamente que o usuário autenticado pertence à equipe solicitada antes de permitir o acesso à rota.

Para tornar mais conveniente a geração de URLs que consideram a equipe, os starter kits registram valores padrão de URL para a equipe atual do usuário autenticado. Isso permite que chamadas a helpers como `route('dashboard')` incluam automaticamente o slug da equipe atual. Quando um usuário faz login, se registra ou troca de equipe, os starter kits atualizam a equipe atual e atualizam esses valores padrão de URL para que os links gerados continuem usando o contexto de equipe correto.

Ao criar ou renomear uma equipe, os starter kits também impedem que os usuários escolham nomes reservados que poderiam produzir segmentos de rota inseguros ou conflitantes. Por exemplo, nomes que colidiriam com prefixos de rota como `settings`, `login` ou `dashboard` não podem ser usados.

<a id="workos"></a>
## Autenticação com WorkOS AuthKit

Por padrão, os starter kits React, Svelte, Vue e Livewire utilizam o sistema de autenticação integrado do Laravel para oferecer login, registro, redefinição de senha, verificação de e-mail e muito mais. Além disso, também oferecemos uma variante de cada starter kit com [WorkOS AuthKit](https://authkit.com) que oferece:

<div class="content-list" markdown="1">

- Autenticação social (Google, Microsoft, GitHub e Apple)
- Autenticação por passkey
- "Magic Auth" baseada em e-mail
- SSO

</div>

Usar o WorkOS como seu provedor de autenticação [requer uma conta do WorkOS](https://workos.com). O WorkOS oferece autenticação gratuita para aplicações com até 1 milhão de usuários ativos mensais.

Para usar o WorkOS AuthKit como provedor de autenticação da sua aplicação, selecione a opção WorkOS ao criar sua nova aplicação com starter kit via `laravel new`.

<a id="configuring-your-workos-starter-kit"></a>
### Configurando seu Starter Kit do WorkOS

Depois de criar uma nova aplicação usando um starter kit com WorkOS, você deve definir as variáveis de ambiente `WORKOS_CLIENT_ID`, `WORKOS_API_KEY` e `WORKOS_REDIRECT_URL` no arquivo `.env` da sua aplicação. Essas variáveis devem corresponder aos valores fornecidos a você no dashboard do WorkOS para sua aplicação:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

Além disso, você deve configurar a URL da página inicial da aplicação no seu dashboard do WorkOS. É para essa URL que os usuários serão redirecionados após sair da sua aplicação.

<a id="configuring-authkit-authentication-methods"></a>
#### Configurando os métodos de autenticação do AuthKit

Ao usar um starter kit com WorkOS, recomendamos que você desabilite a autenticação "Email + Password" nas configurações do WorkOS AuthKit da sua aplicação, permitindo que os usuários se autentiquem apenas por meio de provedores de autenticação social, passkeys, "Magic Auth" e SSO. Isso permite que sua aplicação evite totalmente lidar com senhas de usuários.

<a id="configuring-authkit-session-timeouts"></a>
#### Configurando timeouts de sessão do AuthKit

Além disso, recomendamos que você configure o timeout de inatividade de sessão do seu WorkOS AuthKit para corresponder ao limite de timeout de sessão configurado na sua aplicação Laravel, que normalmente é de duas horas.

<a id="inertia-ssr"></a>
### Inertia SSR

Os starter kits React, Svelte e Vue são compatíveis com os recursos de [renderização no servidor](https://inertiajs.com/server-side-rendering) do Inertia. Para construir um bundle compatível com Inertia SSR para sua aplicação, execute o comando `build:ssr`:

```shell
npm run build:ssr
```

Para sua conveniência, um comando `composer dev:ssr` também está disponível. Esse comando iniciará o servidor de desenvolvimento do Laravel e o servidor de Inertia SSR depois de construir um bundle compatível com SSR para sua aplicação, permitindo que você teste sua aplicação localmente usando o mecanismo de renderização no servidor do Inertia:

```shell
composer dev:ssr
```

<a id="community-maintained-starter-kits"></a>
### Starter Kits mantidos pela comunidade

Ao criar uma nova aplicação Laravel usando o instalador do Laravel, você pode passar qualquer starter kit mantido pela comunidade e disponível no Packagist para a flag `--using`:

```shell
laravel new my-app --using=example/starter-kit
```

<a id="creating-starter-kits"></a>
#### Criando Starter Kits

Para garantir que seu starter kit esteja disponível para outras pessoas, você precisará publicá-lo no [Packagist](https://packagist.org). Seu starter kit deve definir suas variáveis de ambiente exigidas no arquivo `.env.example`, e quaisquer comandos de pós-instalação necessários devem ser listados no array `post-create-project-cmd` do arquivo `composer.json` do starter kit.

<a id="faqs"></a>
### Perguntas frequentes

<a id="faq-upgrade"></a>
#### Como faço para atualizar?

Cada starter kit oferece a você um ponto de partida sólido para sua próxima aplicação. Com a propriedade total do código, você pode ajustar, personalizar e construir sua aplicação exatamente como imagina. No entanto, não há necessidade de atualizar o próprio starter kit.

<a id="faq-enable-email-verification"></a>
#### Como habilito a verificação de e-mail?

A verificação de e-mail pode ser adicionada descomentando o import `MustVerifyEmail` no seu modelo `App/Models/User.php` e garantindo que o modelo implemente a interface `MustVerifyEmail`:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
// ...

class User extends Authenticatable implements MustVerifyEmail
{
    // ...
}
```

Depois do registro, os usuários receberão um e-mail de verificação. Para restringir o acesso a determinadas rotas até que o endereço de e-mail do usuário seja verificado, adicione o middleware `verified` às rotas:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> **Nota:**
> A verificação de e-mail não é necessária ao usar a variante [WorkOS](#workos) dos starter kits.

<a id="faq-modify-email-template"></a>
#### Como modifico o template de e-mail padrão?

Você pode querer personalizar o template de e-mail padrão para se alinhar melhor à identidade visual da sua aplicação. Para modificar esse template, você deve publicar as views de e-mail na sua aplicação com o seguinte comando:

```shell
php artisan vendor:publish --tag=laravel-mail
```

Isso gerará vários arquivos em `resources/views/vendor/mail`. Você pode modificar qualquer um desses arquivos, bem como o arquivo `resources/views/vendor/mail/themes/default.css`, para alterar o visual e a aparência do template de e-mail padrão.
