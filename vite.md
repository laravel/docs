---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Складання ресурсів (Vite)

- [Вступ](#introduction)
- [Встановлення та налаштування](#installation)
  - [Встановлення Node](#installing-node)
  - [Встановлення Vite та плагіна Laravel](#installing-vite-and-laravel-plugin)
  - [Налаштування Vite](#configuring-vite)
  - [Завантаження скриптів і стилів](#loading-your-scripts-and-styles)
- [Запуск Vite](#running-vite)
- [Робота з JavaScript](#working-with-scripts)
  - [Псевдоніми](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Svelte](#svelte)
  - [Inertia](#inertia)
  - [Обробка URL](#url-processing)
- [Робота зі стилями](#working-with-stylesheets)
- [Робота зі шрифтами](#working-with-fonts)
  - [Провайдери шрифтів](#font-providers)
  - [Локальні шрифти](#local-fonts)
  - [Опції шрифтів](#font-options)
- [Робота з Blade і маршрутами](#working-with-blade-and-routes)
  - [Обробка статичних ресурсів через Vite](#blade-processing-static-assets)
  - [Оновлення під час збереження](#blade-refreshing-on-save)
  - [Псевдоніми](#blade-aliases)
- [Попереднє завантаження ресурсів](#asset-prefetching)
- [Власні базові URL](#custom-base-urls)
- [Змінні середовища](#environment-variables)
- [Вимкнення Vite у тестах](#disabling-vite-in-tests)
- [Рендеринг на боці сервера (SSR)](#ssr)
- [Атрибути тегів script і style](#script-and-style-attributes)
  - [Nonce для політики безпеки вмісту (CSP)](#content-security-policy-csp-nonce)
  - [Цілісність підресурсів (SRI)](#subresource-integrity-sri)
  - [Довільні атрибути](#arbitrary-attributes)
- [Розширене налаштування](#advanced-customization)
  - [CORS сервера розробки](#cors)
  - [Виправлення URL сервера розробки](#correcting-dev-server-urls)

<a name="introduction"></a>
## Вступ

[Vite](https://vitejs.dev) - це сучасний інструмент збірки фронтенду, що дає надзвичайно швидке середовище розробки й пакує ваш код для продакшену. Створюючи застосунки на Laravel, ви зазвичай використовуватимете Vite, щоб зібрати файли CSS і JavaScript у готові до продакшену ресурси.

Laravel бездоганно інтегрується з Vite завдяки офіційному плагіну та директиві Blade, які завантажують ваші ресурси для розробки й продакшену.

<a name="installation"></a>
## Встановлення та налаштування

> [!NOTE]
> Наведена нижче документація описує, як встановити й налаштувати плагін Laravel Vite вручну. Утім, [стартові набори](/docs/{{version}}/starter-kits) Laravel уже містять увесь цей каркас і є найшвидшим способом почати роботу з Laravel і Vite.

<a name="installing-node"></a>
### Встановлення Node

Перш ніж запускати Vite та плагін Laravel, переконайтеся, що встановлено Node.js (16+) і NPM:

```shell
node -v
npm -v
```

Ви можете легко встановити найновішу версію Node і NPM за допомогою простих графічних інсталяторів з [офіційного сайту Node](https://nodejs.org/en/download/). Або, якщо ви користуєтеся [Laravel Sail](https://laravel.com/docs/{{version}}/sail), викликайте Node і NPM через Sail:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Встановлення Vite та плагіна Laravel

У щойно встановленому Laravel ви знайдете файл `package.json` у корені каталогу застосунку. Типовий `package.json` уже містить усе потрібне, щоб почати роботу з Vite і плагіном Laravel. Встановити фронтенд-залежності застосунку можна через NPM:

```shell
npm install
```

<a name="configuring-vite"></a>
### Налаштування Vite

Vite налаштовується через файл `vite.config.js` у корені вашого проєкту. Ви вільні змінювати цей файл під свої потреби, а також встановлювати будь-які інші потрібні застосунку плагіни - як-от `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte` чи `@vitejs/plugin-vue`.

Плагін Laravel Vite вимагає вказати точки входу вашого застосунку. Це можуть бути файли JavaScript чи CSS, зокрема мови з попередньою обробкою - TypeScript, JSX, TSX і Sass.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css',
            'resources/js/app.js',
        ]),
    ],
});
```

Якщо ви створюєте SPA, зокрема застосунки на Inertia, Vite найкраще працює без CSS-точок входу:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css', // [tl! remove]
            'resources/js/app.js',
        ]),
    ],
});
```

Натомість вам слід імпортувати CSS через JavaScript. Зазвичай це роблять у файлі `resources/js/app.js` вашого застосунку:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Плагін Laravel також підтримує кілька точок входу та розширені опції конфігурації - як-от [точки входу SSR](#ssr).

<a name="working-with-a-secure-development-server"></a>
#### Робота із захищеним сервером розробки

Якщо ваш локальний веб-сервер віддає застосунок через HTTPS, ви можете натрапити на проблеми з підключенням до сервера розробки Vite.

Якщо ви користуєтеся [Laravel Herd](https://herd.laravel.com) і захистили сайт, або користуєтеся [Laravel Valet](/docs/{{version}}/valet) і виконали [команду secure](/docs/{{version}}/valet#securing-sites) для свого застосунку, плагін Laravel Vite автоматично виявить і використає згенерований TLS-сертифікат.

Якщо ви захистили сайт хостом, що не збігається з іменем каталогу застосунку, ви можете вказати хост вручну у файлі `vite.config.js`:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            detectTls: 'my-app.test', // [tl! add]
        }),
    ],
});
```

Використовуючи інший веб-сервер, вам слід згенерувати довірений сертифікат і вручну налаштувати Vite на його використання:

```js
// ...
import fs from 'fs'; // [tl! add]

const host = 'my-app.test'; // [tl! add]

export default defineConfig({
    // ...
    server: { // [tl! add]
        host, // [tl! add]
        hmr: { host }, // [tl! add]
        https: { // [tl! add]
            key: fs.readFileSync(`/path/to/${host}.key`), // [tl! add]
            cert: fs.readFileSync(`/path/to/${host}.crt`), // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

Якщо ви не можете згенерувати довірений сертифікат для своєї системи, встановіть і налаштуйте [плагін @vitejs/plugin-basic-ssl](https://github.com/vitejs/vite-plugin-basic-ssl). Використовуючи недовірені сертифікати, вам доведеться прийняти попередження про сертифікат для сервера розробки Vite у браузері, перейшовши за посиланням «Local» у консолі під час виконання команди `npm run dev`.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### Запуск сервера розробки в Sail на WSL2

Запускаючи сервер розробки Vite у [Laravel Sail](/docs/{{version}}/sail) на Windows Subsystem for Linux 2 (WSL2), додайте до файлу `vite.config.js` таку конфігурацію, щоб браузер міг спілкуватися із сервером розробки:

```js
// ...

export default defineConfig({
    // ...
    server: { // [tl! add:start]
        hmr: {
            host: 'localhost',
        },
    }, // [tl! add:end]
});
```

Якщо зміни у ваших файлах не відображаються в браузері під час роботи сервера розробки, вам також може знадобитися налаштувати [опцію server.watch.usePolling](https://vitejs.dev/config/server-options.html#server-watch) у Vite.

<a name="loading-your-scripts-and-styles"></a>
### Завантаження скриптів і стилів

Налаштувавши точки входу Vite, ви можете посилатися на них у директиві Blade `@vite()`, яку додаєте до `<head>` кореневого шаблону вашого застосунку:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

Якщо ви імпортуєте CSS через JavaScript, вам потрібно вказати лише точку входу JavaScript:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

Директива `@vite` автоматично виявить сервер розробки Vite і вставить клієнт Vite, щоб увімкнути гарячу заміну модулів. У режимі збірки директива завантажить ваші скомпільовані версіоновані ресурси, зокрема будь-який імпортований CSS.

За потреби ви також можете вказати шлях збірки ваших скомпільованих ресурсів під час виклику директиви `@vite`:

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### Вбудовані ресурси

Іноді може знадобитися включити сирий вміст ресурсів замість посилання на їхню версіоновану адресу. Наприклад, вам може знадобитися вставити вміст ресурсу просто в сторінку, передаючи HTML генератору PDF. Вивести вміст ресурсів Vite можна методом `content` фасаду `Vite`:

```blade
@use('Illuminate\Support\Facades\Vite')

<!doctype html>
<head>
    {{-- ... --}}

    <style>
        {!! Vite::content('resources/css/app.css') !!}
    </style>
    <script>
        {!! Vite::content('resources/js/app.js') !!}
    </script>
</head>
```

<a name="running-vite"></a>
## Запуск Vite

Запустити Vite можна двома способами. Ви можете запустити сервер розробки командою `dev` - це корисно під час локальної розробки. Сервер автоматично виявлятиме зміни у ваших файлах і миттєво відображатиме їх у відкритих вікнах браузера.

Або ж команда `build` версіонує й запакує ресурси вашого застосунку, підготувавши їх до розгортання в продакшені:

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

Якщо ви запускаєте сервер розробки в [Sail](/docs/{{version}}/sail) на WSL2, вам можуть знадобитися [додаткові опції конфігурації](#configuring-hmr-in-sail-on-wsl2).

<a name="working-with-scripts"></a>
## Робота з JavaScript

<a name="aliases"></a>
### Псевдоніми

За замовчуванням плагін Laravel надає загальний псевдонім, щоб ви могли одразу братися до справи й зручно імпортувати ресурси свого застосунку:

```js
{
    '@' => '/resources/js'
}
```

Ви можете перевизначити псевдонім `'@'`, додавши власний до конфігураційного файлу `vite.config.js`:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel(['resources/ts/app.tsx']),
    ],
    resolve: {
        alias: {
            '@': '/resources/ts',
        },
    },
});
```

<a name="vue"></a>
### Vue

Якщо ви хочете створювати фронтенд за допомогою фреймворку [Vue](https://vuejs.org/), вам також потрібно встановити плагін `@vitejs/plugin-vue`:

```shell
npm install --save-dev @vitejs/plugin-vue
```

Далі ви можете додати плагін до конфігураційного файлу `vite.config.js`. Використовуючи плагін Vue з Laravel, вам знадобиться кілька додаткових опцій:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.js']),
        vue({
            template: {
                transformAssetUrls: {
                    // The Vue plugin will re-write asset URLs, when referenced
                    // in Single File Components, to point to the Laravel web
                    // server. Setting this to `null` allows the Laravel plugin
                    // to instead re-write asset URLs to point to the Vite
                    // server instead.
                    base: null,

                    // The Vue plugin will parse absolute URLs and treat them
                    // as absolute paths to files on disk. Setting this to
                    // `false` will leave absolute URLs un-touched so they can
                    // reference assets in the public directory as expected.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> [Стартові набори](/docs/{{version}}/starter-kits) Laravel уже містять правильну конфігурацію Laravel, Vue і Vite. Вони є найшвидшим способом почати роботу з Laravel, Vue і Vite.

<a name="react"></a>
### React

Якщо ви хочете створювати фронтенд за допомогою фреймворку [React](https://reactjs.org/), вам також потрібно встановити плагін `@vitejs/plugin-react`:

```shell
npm install --save-dev @vitejs/plugin-react
```

Далі ви можете додати плагін до конфігураційного файлу `vite.config.js`:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.jsx']),
        react(),
    ],
});
```

Переконайтеся, що всі файли з JSX мають розширення `.jsx` чи `.tsx`, і за потреби не забудьте оновити свою точку входу, [як показано вище](#configuring-vite).

Вам також потрібно буде додати додаткову директиву Blade `@viteReactRefresh` поряд із наявною директивою `@vite`.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

Директиву `@viteReactRefresh` слід викликати перед директивою `@vite`.

> [!NOTE]
> [Стартові набори](/docs/{{version}}/starter-kits) Laravel уже містять правильну конфігурацію Laravel, React і Vite. Вони є найшвидшим способом почати роботу з Laravel, React і Vite.

<a name="svelte"></a>
### Svelte

Якщо ви хочете створювати фронтенд за допомогою фреймворку [Svelte](https://svelte.dev/), вам також потрібно встановити плагін `@sveltejs/vite-plugin-svelte`:

```shell
npm install --save-dev @sveltejs/vite-plugin-svelte
```

Далі ви можете додати плагін до конфігураційного файлу `vite.config.js`.

```js
import { svelte } from '@sveltejs/vite-plugin-svelte';
import laravel from 'laravel-vite-plugin';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    laravel({
      input: ['resources/js/app.ts'],
      ssr: 'resources/js/ssr.ts',
      refresh: true,
    }),
    svelte(),
  ],
});
```

> [!NOTE]
> [Стартові набори](/docs/{{version}}/starter-kits) Laravel уже містять правильну конфігурацію Laravel, Svelte і Vite. Вони є найшвидшим способом почати роботу з Laravel, Svelte і Vite.

<a name="inertia"></a>
### Inertia

Плагін Laravel Vite надає зручну функцію `resolvePageComponent`, яка допомагає розв'язувати компоненти сторінок Inertia. Нижче наведено приклад використання цього хелпера з Vue 3; утім, ви можете застосовувати цю функцію і в інших фреймворках - як-от React чи Svelte:

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```

Якщо ви використовуєте можливість розділення коду Vite разом з Inertia, радимо налаштувати [попереднє завантаження ресурсів](#asset-prefetching).

> [!NOTE]
> [Стартові набори](/docs/{{version}}/starter-kits) Laravel уже містять правильну конфігурацію Laravel, Inertia і Vite. Вони є найшвидшим способом почати роботу з Laravel, Inertia і Vite.

<a name="url-processing"></a>
### Обробка URL

Використовуючи Vite й посилаючись на ресурси в HTML, CSS чи JS вашого застосунку, варто врахувати кілька застережень. По-перше, якщо ви посилаєтеся на ресурс за абсолютним шляхом, Vite не включить його до збірки; тому переконайтеся, що ресурс доступний у вашому каталозі `public`. Уникайте абсолютних шляхів, коли використовуєте [окрему точку входу CSS](#configuring-vite), адже під час розробки браузери намагатимуться завантажити ці шляхи із сервера розробки Vite, де розміщено CSS, а не з вашого каталогу `public`.

Посилаючись на відносні шляхи ресурсів, пам'ятайте, що вони відносні до файлу, у якому їх зазначено. Будь-які ресурси, на які посилаються за відносним шляхом, буде переписано, версіоновано та запаковано Vite.

Розгляньмо таку структуру проєкту:

```text
public/
  taylor.png
resources/
  js/
    Pages/
      Welcome.vue
  images/
    abigail.png
```

Наступний приклад демонструє, як Vite поводитиметься з відносними та абсолютними URL:

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## Робота зі стилями

> [!NOTE]
> [Стартові набори](/docs/{{version}}/starter-kits) Laravel уже містять правильну конфігурацію Tailwind і Vite. Або, якщо ви хочете використовувати Tailwind із Laravel без наших стартових наборів, перегляньте [посібник Tailwind зі встановлення для Laravel](https://tailwindcss.com/docs/guides/laravel).

Усі застосунки Laravel уже містять Tailwind і правильно налаштований файл `vite.config.js`. Тож вам залишається лише запустити сервер розробки Vite або виконати команду Composer `dev`, яка запустить і сервер Laravel, і сервер Vite:

```shell
composer run dev
```

CSS вашого застосунку можна розмістити у файлі `resources/css/app.css`.

<a name="working-with-fonts"></a>
## Робота зі шрифтами

Плагін Laravel Vite може віддавати оптимізовані шрифти з вашого власного хостингу. Коли шрифти налаштовано, плагін розв'язує запитані файли шрифтів, віддає їх як ресурси Vite, генерує CSS шрифтів і записує маніфест, який може споживати [директива `@fonts`](/docs/{{version}}/blade#fonts) у Blade.

Щоб налаштувати шрифти, імпортуйте один чи кілька хелперів провайдерів із `laravel-vite-plugin/fonts` і додайте їх до опції `fonts` плагіна Laravel:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { google } from 'laravel-vite-plugin/fonts';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            fonts: [
                google('Inter', {
                    alias: 'sans',
                    weights: [400, 500, 600, 700],
                    styles: ['normal', 'italic'],
                    subsets: ['latin'],
                    display: 'swap',
                    preload: [
                        { weight: 400 },
                        { weight: 700 },
                    ],
                    fallbacks: ['system-ui', 'sans-serif'],
                }),
            ],
        }),
    ],
});
```

У цьому прикладі шрифт `Inter` буде доступний через псевдонім `sans`. Плагін згенерує CSS-змінну `--font-sans` і клас-утиліту `.font-sans`, що застосовує згенерований набір шрифтів.

<a name="font-providers"></a>
### Провайдери шрифтів

Плагін Laravel Vite містить хелпери провайдерів для Google Fonts, Bunny Fonts, Fontsource та локальних шрифтів:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { bunny, fontsource, google, local } from 'laravel-vite-plugin/fonts';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            fonts: [
                google('Inter', { alias: 'sans' }),
                bunny('Figtree', { alias: 'body' }),
                fontsource('JetBrains Mono', { alias: 'mono' }),
                local('Brand Sans', {
                    alias: 'brand',
                    src: 'resources/fonts/brand-sans',
                }),
            ],
        }),
    ],
});
```

Провайдер `fontsource` читає шрифти зі встановленого пакета Fontsource. За замовчуванням ім'я пакета виводиться з родини шрифтів - наприклад, `@fontsource/jetbrains-mono`. Якщо ваш застосунок використовує інше ім'я пакета, вкажіть його опцією `package`.

<a name="local-fonts"></a>
### Локальні шрифти

Використовуючи локальні шрифти, опція `src` може вказувати на один файл шрифту, каталог або шаблон glob. Плагін знайде підтримувані файли шрифтів і визначить їхню товщину та стиль з імен файлів:

```js
local('Brand Sans', {
    alias: 'brand',
    src: 'resources/fonts/brand-sans/*.woff2',
})
```

Якщо вам потрібен повний контроль над доступними варіантами, визначте їх явно опцією `variants`:

```js
local('Brand Sans', {
    alias: 'brand',
    variants: [
        { src: 'resources/fonts/BrandSans-Regular.woff2', weight: 400 },
        { src: 'resources/fonts/BrandSans-Italic.woff2', weight: 400, style: 'italic' },
        { src: ['resources/fonts/BrandSans-Bold.woff2', 'resources/fonts/BrandSans-Bold.ttf'], weight: 700 },
    ],
})
```

<a name="font-options"></a>
### Опції шрифтів

Залежно від провайдера, визначення шрифтів можуть приймати кілька опцій, що дозволяють налаштувати згенерований CSS:

<div class="content-list" markdown="1">

- `alias` визначає ім'я, яке використовує директива `@fonts` у Blade; за замовчуванням це slug родини шрифтів.
- `variable` визначає згенеровану CSS-змінну; за замовчуванням `--font-{alias}`.
- `weights` визначає віддалені товщини шрифтів чи товщини Fontsource, які слід розв'язати; за замовчуванням `[400]`.
- `styles` визначає віддалені стилі шрифтів чи стилі Fontsource, які слід розв'язати; за замовчуванням `['normal']`.
- `subsets` визначає віддалені підмножини шрифтів чи підмножини Fontsource, які слід розв'язати; за замовчуванням `['latin']`.
- `display` визначає значення `font-display`; за замовчуванням `swap`.
- `preload` керує тим, які варіанти WOFF2 слід завантажувати наперед. Ця опція може бути `true`, `false` або масивом селекторів `{ weight, style }`.
- `fallbacks` визначає додаткові резервні шрифти, які слід додати до згенерованого набору.
- `optimizedFallbacks` намагається згенерувати резервні шрифти з підлаштованими метриками за допомогою необов'язкового пакета `fontaine`; за замовчуванням `true`.

</div>

Оптимізовані резервні шрифти потребують пакета `fontaine`, який не встановлюється за замовчуванням. Якщо ви хочете, щоб Laravel генерував резервні шрифти з підлаштованими метриками, встановіть `fontaine` як залежність для розробки:

```shell
npm install --save-dev fontaine
```

Якщо `fontaine` не встановлено або він не може прочитати файл шрифту, Laravel пропустить оптимізований резервний шрифт для цього шрифту й далі використовуватиме шрифти, налаштовані опцією `fallbacks`.

Локальні шрифти розв'язуються з описаних вище опцій `src` чи `variants`, а не через `weights`, `styles` і `subsets`.

<a name="working-with-blade-and-routes"></a>
## Робота з Blade і маршрутами

<a name="blade-processing-static-assets"></a>
### Обробка статичних ресурсів через Vite

Коли ви посилаєтеся на ресурси у своєму JavaScript чи CSS, Vite автоматично обробляє й версіонує їх. Крім того, створюючи застосунки на Blade, Vite може обробляти й версіонувати статичні ресурси, на які ви посилаєтеся лише в шаблонах Blade.

Однак для цього потрібно повідомити Vite про ваші ресурси, вказавши їх в опції `assets` плагіна. Ця опція призначена для статичних файлів, на які ви хочете посилатися безпосередньо через `Vite::asset`. Якщо ви хочете, щоб Laravel генерував CSS шрифтів і посилання попереднього завантаження, скористайтеся натомість [опцією `fonts`](#working-with-fonts).

Наприклад, якщо ви хочете обробити й версіонувати всі зображення в `resources/images` та всі шрифти в `resources/fonts`, додайте до конфігурації Vite таке:

```js
laravel({
    input: 'resources/js/app.js',
    assets: ['resources/images/**', 'resources/fonts/**'],
})
```

Тепер ці ресурси оброблятиме Vite під час виконання `npm run build`. Далі ви можете посилатися на них у шаблонах Blade методом `Vite::asset`, який поверне версіоновану адресу ресурсу:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

> [!NOTE]
> До версії 3 плагіна Laravel Vite статичні ресурси доводилося імпортувати в точці входу застосунку через `import.meta.glob`. Опцію `assets` запроваджено через зміни у Vite 8.

<a name="blade-refreshing-on-save"></a>
### Оновлення під час збереження

Коли ваш застосунок побудовано на традиційному серверному рендерингу з Blade, Vite може покращити ваш робочий процес, автоматично оновлюючи браузер, коли ви змінюєте файли представлень. Щоб почати, просто вкажіть опцію `refresh` зі значенням `true`.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: true,
        }),
    ],
});
```

Коли опція `refresh` має значення `true`, збереження файлів у таких каталогах змусить браузер повністю оновити сторінку, поки виконується `npm run dev`:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

Стеження за каталогом `routes/**` корисне, якщо ви використовуєте [Ziggy](https://github.com/tighten/ziggy) для генерації посилань на маршрути у фронтенді вашого застосунку.

Якщо типові шляхи вам не підходять, ви можете вказати власний список шляхів для стеження:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: ['resources/views/**'],
        }),
    ],
});
```

Під капотом плагін Laravel Vite використовує пакет [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload), який пропонує розширені опції конфігурації для тонкого налаштування цієї можливості. Якщо вам потрібен такий рівень контролю, передайте визначення `config`:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: [{
                paths: ['path/to/watch/**'],
                config: { delay: 300 }
            }],
        }),
    ],
});
```

<a name="blade-aliases"></a>
### Псевдоніми

У JavaScript-застосунках поширено [створювати псевдоніми](#aliases) для каталогів, на які часто посилаються. Але ви також можете створювати псевдоніми для використання в Blade методом `macro` класу `Illuminate\Support\Facades\Vite`. Зазвичай «макроси» слід визначати в методі `boot` [сервіс-провайдера](/docs/{{version}}/providers):

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

Щойно макрос визначено, його можна викликати у ваших шаблонах. Наприклад, ми можемо скористатися визначеним вище макросом `image`, щоб послатися на ресурс `resources/images/logo.png`:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="asset-prefetching"></a>
## Попереднє завантаження ресурсів

Створюючи SPA з можливістю розділення коду Vite, потрібні ресурси завантажуються під час кожного переходу між сторінками. Це може призводити до затримок у рендерингу інтерфейсу. Якщо для обраного вами фронтенд-фреймворку це проблема, Laravel дозволяє завчасно завантажувати JavaScript- і CSS-ресурси застосунку під час першого завантаження сторінки.

Вказати Laravel завчасно завантажувати ресурси можна викликом методу `Vite::prefetch` у методі `boot` [сервіс-провайдера](/docs/{{version}}/providers):

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Vite::prefetch(concurrency: 3);
    }
}
```

У прикладі вище ресурси завантажуватимуться завчасно щонайбільше в `3` паралельні потоки під час кожного завантаження сторінки. Ви можете змінити паралельність під потреби свого застосунку або не вказувати обмеження взагалі, якщо застосунок має завантажувати всі ресурси одразу:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

За замовчуванням попереднє завантаження почнеться, коли спрацює [подія _load_ сторінки](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event). Якщо ви хочете налаштувати момент початку, вкажіть подію, яку слухатиме Vite:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

З наведеним вище кодом попереднє завантаження починатиметься, коли ви вручну надішлете подію `vite:prefetch` на об'єкті `window`. Наприклад, ви можете почати завантаження через три секунди після завантаження сторінки:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## Власні базові URL

Якщо ваші скомпільовані Vite ресурси розгорнуто на домені, відмінному від застосунку - наприклад, через CDN, - вам потрібно вказати змінну середовища `ASSET_URL` у файлі `.env` вашого застосунку:

```env
ASSET_URL=https://cdn.example.com
```

Після налаштування адреси ресурсів усі переписані URL до ваших ресурсів матимуть цей префікс:

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

Пам'ятайте, що [абсолютні URL не переписуються Vite](#url-processing), тож префікса вони не отримають.

<a name="environment-variables"></a>
## Змінні середовища

Ви можете впроваджувати змінні середовища у свій JavaScript, додавши до них префікс `VITE_` у файлі `.env` вашого застосунку:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

Звертатися до впроваджених змінних середовища можна через об'єкт `import.meta.env`:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## Вимкнення Vite у тестах

Інтеграція Vite в Laravel намагатиметься розв'язати ваші ресурси під час виконання тестів, а це вимагає або запущеного сервера розробки Vite, або зібраних ресурсів.

Якщо ви віддаєте перевагу мокуванню Vite під час тестування, викличте метод `withoutVite`, доступний у будь-яких тестах, що успадковують клас `TestCase` від Laravel:

```php tab=Pest
test('without vite example', function () {
    $this->withoutVite();

    // ...
});
```

```php tab=PHPUnit
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_vite_example(): void
    {
        $this->withoutVite();

        // ...
    }
}
```

Якщо ви хочете вимкнути Vite для всіх тестів, викличте метод `withoutVite` у методі `setUp` вашого базового класу `TestCase`:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    }// [tl! add:end]
}
```

<a name="ssr"></a>
## Рендеринг на боці сервера (SSR)

Плагін Laravel Vite робить налаштування серверного рендерингу з Vite безболісним. Щоб почати, створіть точку входу SSR у `resources/js/ssr.js` і вкажіть її, передавши опцію конфігурації плагіну Laravel:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            ssr: 'resources/js/ssr.js',
        }),
    ],
});
```

Щоб не забути перезібрати точку входу SSR, радимо доповнити скрипт «build» у файлі `package.json` вашого застосунку:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

Далі, щоб зібрати й запустити SSR-сервер, виконайте такі команди:

```shell
npm run build
node bootstrap/ssr/ssr.js
```

Якщо ви використовуєте [SSR з Inertia](https://inertiajs.com/server-side-rendering), ви можете натомість запустити SSR-сервер командою Artisan `inertia:start-ssr`:

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> [Стартові набори](/docs/{{version}}/starter-kits) Laravel уже містять правильну конфігурацію Laravel, Inertia SSR і Vite. Вони є найшвидшим способом почати роботу з Laravel, Inertia SSR і Vite.

<a name="script-and-style-attributes"></a>
## Атрибути тегів script і style

<a name="content-security-policy-csp-nonce"></a>
### Nonce для політики безпеки вмісту (CSP)

Якщо ви хочете додати [атрибут nonce](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) до своїх тегів script і style у межах [політики безпеки вмісту](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), ви можете згенерувати чи вказати nonce методом `useCspNonce` у власному [`middleware`](/docs/{{version}}/middleware):

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Vite;
use Symfony\Component\HttpFoundation\Response;

class AddContentSecurityPolicyHeaders
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        Vite::useCspNonce();

        return $next($request)->withHeaders([
            'Content-Security-Policy' => "script-src 'nonce-".Vite::cspNonce()."'",
        ]);
    }
}
```

Після виклику методу `useCspNonce` Laravel автоматично додаватиме атрибути `nonce` до всіх згенерованих тегів script і style.

Якщо вам потрібно вказати nonce деінде - зокрема в [директиві Ziggy `@route`](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy), що входить до [стартових наборів](/docs/{{version}}/starter-kits) Laravel, - ви можете отримати його методом `cspNonce`:

```blade
@routes(nonce: Vite::cspNonce())
```

Якщо ви вже маєте nonce, який хочете передати Laravel, передайте його методу `useCspNonce`:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### Цілісність підресурсів (SRI)

Якщо ваш маніфест Vite містить хеші `integrity` для ресурсів, Laravel автоматично додасть атрибут `integrity` до всіх згенерованих тегів script і style, щоб забезпечити [цілісність підресурсів](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity). За замовчуванням Vite не додає хеш `integrity` до свого маніфесту, але ви можете увімкнути це, встановивши NPM-плагін [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri):

```shell
npm install --save-dev vite-plugin-manifest-sri
```

Далі ви можете увімкнути цей плагін у файлі `vite.config.js`:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import manifestSRI from 'vite-plugin-manifest-sri';// [tl! add]

export default defineConfig({
    plugins: [
        laravel({
            // ...
        }),
        manifestSRI(),// [tl! add]
    ],
});
```

За потреби ви також можете налаштувати ключ маніфесту, за яким знаходиться хеш цілісності:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

Якщо ви хочете цілком вимкнути це автоматичне визначення, передайте `false` методу `useIntegrityKey`:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### Довільні атрибути

Якщо вам потрібно додати до тегів script і style додаткові атрибути - як-от [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change), - ви можете вказати їх методами `useScriptTagAttributes` і `useStyleTagAttributes`. Зазвичай ці методи слід викликати із [сервіс-провайдера](/docs/{{version}}/providers):

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // Specify a value for the attribute...
    'async' => true, // Specify an attribute without a value...
    'integrity' => false, // Exclude an attribute that would otherwise be included...
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

Якщо вам потрібно додавати атрибути умовно, передайте колбек, який отримає шлях до джерела ресурсу, його URL, його фрагмент маніфесту та весь маніфест:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $src === 'resources/js/app.js' ? 'reload' : false,
]);

Vite::useStyleTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $chunk && $chunk['isEntry'] ? 'reload' : false,
]);
```

> [!WARNING]
> Аргументи `$chunk` і `$manifest` будуть `null`, поки працює сервер розробки Vite.

<a name="advanced-customization"></a>
## Розширене налаштування

Одразу після встановлення плагін Vite від Laravel використовує розумні домовленості, які підійдуть більшості застосунків; утім, іноді вам може знадобитися налаштувати поведінку Vite. Щоб увімкнути додаткові можливості налаштування, ми пропонуємо такі методи й опції, які можна використати замість директиви Blade `@vite`:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // Customize the "hot" file...
            ->useBuildDirectory('bundle') // Customize the build directory...
            ->useManifestFilename('assets.json') // Customize the manifest filename...
            ->withEntryPoints(['resources/js/app.js']) // Specify the entry points...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // Customize the backend path generation for built assets...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

Далі у файлі `vite.config.js` вам слід указати ту саму конфігурацію:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // Customize the "hot" file...
            buildDirectory: 'bundle', // Customize the build directory...
            input: ['resources/js/app.js'], // Specify the entry points...
        }),
    ],
    build: {
      manifest: 'assets.json', // Customize the manifest filename...
    },
});
```

<a name="cors"></a>
### CORS сервера розробки

Якщо ви натрапляєте на проблеми зі спільним використанням ресурсів між джерелами (CORS) у браузері під час отримання ресурсів із сервера розробки Vite, вам може знадобитися надати вашому власному джерелу доступ до сервера розробки. Vite у поєднанні з плагіном Laravel дозволяє такі джерела без додаткової конфігурації:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- `APP_URL` у файлі `.env` проєкту

Найпростіший спосіб дозволити власне джерело для вашого проєкту - переконатися, що змінна середовища `APP_URL` збігається з джерелом, яке ви відкриваєте в браузері. Наприклад, якщо ви відвідуєте `https://my-app.laravel`, оновіть свій `.env` відповідно:

```env
APP_URL=https://my-app.laravel
```

Якщо вам потрібен тонший контроль над джерелами - наприклад, підтримка кількох джерел, - скористайтеся [вичерпною та гнучкою вбудованою конфігурацією CORS-сервера Vite](https://vite.dev/config/server-options.html#server-cors). Наприклад, ви можете вказати кілька джерел в опції `server.cors.origin` у файлі `vite.config.js` вашого проєкту:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [  // [tl! add]
                'https://backend.laravel',  // [tl! add]
                'http://admin.laravel:8566',  // [tl! add]
            ],  // [tl! add]
        },  // [tl! add]
    },  // [tl! add]
});
```

Ви також можете використовувати регулярні вирази - це стане в пригоді, якщо ви хочете дозволити всі джерела для певного домену верхнього рівня, як-от `*.laravel`:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [ // [tl! add]
                // Supports: SCHEME://DOMAIN.laravel[:PORT] [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### Виправлення URL сервера розробки

Деякі плагіни в екосистемі Vite припускають, що URL, які починаються з прямої скісної риски, завжди вказують на сервер розробки Vite. Однак через природу інтеграції з Laravel це не так.

Наприклад, плагін `vite-imagetools` виводить такі URL, поки Vite віддає ваші ресурси:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

Плагін `vite-imagetools` очікує, що вихідний URL перехопить Vite, і тоді плагін зможе обробити всі URL, що починаються з `/@imagetools`. Якщо ви використовуєте плагіни, які очікують такої поведінки, вам доведеться виправляти URL вручну. Це можна зробити у файлі `vite.config.js` за допомогою опції `transformOnServe`.

У цьому конкретному прикладі ми додамо URL сервера розробки до всіх входжень `/@imagetools` у згенерованому коді:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { imagetools } from 'vite-imagetools';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            transformOnServe: (code, devServerUrl) => code.replaceAll('/@imagetools', devServerUrl+'/@imagetools'),
        }),
        imagetools(),
    ],
});
```

Тепер, поки Vite віддає ресурси, він виводитиме URL, що вказують на сервер розробки Vite:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
