# Starter Kits

- [Introduction](#introduction)
- [Creating an Application Using a Starter Kit](#creating-an-application)
- [Available Starter Kits](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [Starter Kit Customization](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [WorkOS AuthKit Authentication](#workos)

<a name="introduction"></a>
## Introduction

To give you a head start building your new Laravel application, we are happy to offer [application starter kits](https://laravel.com/starter-kits). These starter kits give you a head start on building your next Laravel application, and include the routes, controllers, and views you need to register and authenticate your application's users.

While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great!

<a name="creating-an-application"></a>
## Creating an Application Using a Starter Kit

To create a new Laravel application using one of our starter kits, you should first [install PHP and the Laravel CLI tool](/docs/{{version}}/installation#installing-php). If you already have PHP and Composer installed, you may install the Laravel installer CLI tool via Composer:

```shell
composer global require laravel/installer
```

Then, create a new Laravel application using the Laravel installer CLI. The Laravel installer will prompt you to select your preferred starter kit:

```shell
laravel new my-app
```

After creating your Laravel application, you only need to install its frontend dependencies via NPM and start the Laravel development server:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Once you have started the Laravel development server, your application will be accessible in your web browser at [http://localhost:8000](http://localhost:8000).

<a name="available-starter-kits"></a>
## Available Starter Kits

<a name="react"></a>
### React

Our React starter kit provides a robust, modern starting point for building Laravel applications with a React frontend using [Inertia](https://inertiajs.com).

Inertia allows you to build modern, single-page React applications using classic server-side routing and controllers. This lets you enjoy the frontend power of React combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation.

The React starter kit utilizes React 19, TypeScript, Tailwind, and the [shadcn/ui](https://ui.shadcn.com) component library.

<a name="vue"></a>
### Vue

Our Vue starter kit provides a great starting point for building Laravel applications with a Vue frontend using [Inertia](https://inertiajs.com).

Inertia allows you to build modern, single-page Vue applications using classic server-side routing and controllers. This lets you enjoy the frontend power of Vue combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation.

The Vue starter kit utilizes the Vue Composition API, TypeScript, Tailwind, and the [shadcn-vue](https://www.shadcn-vue.com/) component library.

<a name="livewire"></a>
### Livewire

Our Livewire starter kit provides the perfect starting point for building Laravel applications with a [Laravel Livewire](https://livewire.laravel.com) frontend.

Livewire is a powerful way of building dynamic, reactive, frontend UIs using just PHP. It's a great fit for teams that primarily use Blade templates and are looking for a simpler alternative to JavaScript-driven SPA frameworks like React and Vue.

The Livewire starter kit utilizes Laravel Volt, Tailwind, and the [Flux UI](https://fluxui.dev) component library.

<a name="starter-kit-customization"></a>
## Starter Kit Customization

<a name="react-customization"></a>
### React

Our React starter kit is built with Inertia 2, React 19, Tailwind 4, and [shadcn/ui](https://ui.shadcn.com). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization.

The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application:

```text
resources/js/
├── components/    # Reusable React components
├── hooks/         # React hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

<a name="react-available-layouts"></a>
#### Available Layouts

The React starter kit includes two different primary layouts for you choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is imported at the top of your application's `resources/js/layouts/app-layout.tsx` file:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### Sidebar Variants

The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/app-sidebar.tsx` component:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### Authentication Page Layout Variants

The authentication pages included with the React starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split".

To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/auth-layout.tsx` file:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Our Vue starter kit is built with Inertia 2, Vue 3 Composition API, Tailwind, and [shadcn-vue](https://www.shadcn-vue.com/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization.

The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application:

```text
resources/js/
├── components/    # Reusable Vue components
├── composables/   # Vue composables / hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

<a name="vue-available-layouts"></a>
#### Available Layouts

The Vue starter kit includes two different primary layouts for you choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is imported at the top of your application's `resources/js/layouts/AppLayout.vue` file:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### Sidebar Variants

The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/AppSidebar.vue` component:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### Authentication Page Layout Variants

The authentication pages included with the Vue starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split".

To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/AuthLayout.vue` file:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Our Livewire starter kit is built with Livewire 3, Laravel Volt, Tailwind, and [Flux UI](https://fluxui.dev/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization.

The majority of the frontend code is located in the `resources/views` directory. You are free to modify any of the code to customize the appearance and behavior of your application:

```text
resources/views
├── components            # Reusable Livewire components
├── flux                  # Customized Flux components
├── livewire              # Livewire pages
├── partials              # Reusable Blade partials
├── dashboard.blade.php   # Authenticated user dashboard
├── welcome.blade.php     # Guest user welcome page
```

<a name="livewire-available-layouts"></a>
#### Available Layouts

The Livewire starter kit includes two different primary layouts for you choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is used by your application's `resources/views/components/layouts/app.blade.php` file:

```blade
<x-layouts.app.header>
    <flux:main>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### Authentication Page Layout Variants

The authentication pages included with the Livewire starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split".

To change your authentication layout, modify the layout that is used by your application's `resources/views/components/layouts/auth.blade.php` file:

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="workos-authkit-authentication"></a>
## WorkOS AuthKit Authentication

By default, the React, Vue, and Livewire starter kits all utilize Laravel's built-in authentication system to offer login, registration, password reset, email verification, and more. In addition, we also offer a [WorkOS AuthKit](https://authkit.com) powered variant of each starter kit that offers:

<div class="content-list" markdown="1">

- Social authentication (Google, Microsoft, GitHub, and Apple)
- Passkey authentication
- Email based "Magic Auth"
- SSO

</div>

Using WorkOS as your authentication provider [requires a WorkOS account](https://workos.com). WorkOS offers free authentication for applications up to 1 million monthly active users.

To use WorkOS AuthKit as your application's authentication provider, select the WorkOS option when creating your new starter kit powered application via `laravel new`.

### Configuring Your WorkOS Starter Kit

After creating a new application using a WorkOS powered starter kit, you should set the `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, and `WORKOS_REDIRECT_URL` environment variables in your application's `.env` file. These variables should match the values provided to you in the WorkOS dashboard for your application:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

<a name="configuring-authkit-authentication-methods"></a>
#### Configuring AuthKit Authentication Methods

When using a WorkOS powered starter kit, we recommend that you disable "Email + Password" authentication within your application's WorkOS AuthKit configuration settings, allowing users to only authenticate via social authentication providers, passkeys, "Magic Auth", and SSO. This allows your application to totally avoid handling user passwords.

<a name="configuring-authkit-session-timeouts"></a>
#### Configuring AuthKit Session Timeouts

In addition, we recommend that you configure your WorkOS AuthKit session inactivity timeout to match your Laravel application's configured session timeout threshold, which is typically two hours.
