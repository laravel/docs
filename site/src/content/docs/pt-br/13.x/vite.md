---
title: "Empacotamento de Assets (Vite)"
---

- [Introdução](#introduction)
- [Instalação e Configuração](#installation)
  - [Instalando o Node](#installing-node)
  - [Instalando o Vite e o Plugin Laravel](#installing-vite-and-laravel-plugin)
  - [Configurando o Vite](#configuring-vite)
  - [Carregando seus Scripts e Estilos](#loading-your-scripts-and-styles)
- [Executando o Vite](#running-vite)
- [Trabalhando com JavaScript](#working-with-scripts)
  - [Aliases](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Svelte](#svelte)
  - [Inertia](#inertia)
  - [Processamento de URLs](#url-processing)
- [Trabalhando com Stylesheets](#working-with-stylesheets)
- [Trabalhando com Fontes](#working-with-fonts)
  - [Provedores de Fontes](#font-providers)
  - [Fontes Locais](#local-fonts)
  - [Opções de Fontes](#font-options)
- [Trabalhando com Blade e Rotas](#working-with-blade-and-routes)
  - [Processando Assets Estáticos com Vite](#blade-processing-static-assets)
  - [Atualizando ao Salvar](#blade-refreshing-on-save)
  - [Aliases](#blade-aliases)
- [Pré-buscando Assets](#asset-prefetching)
- [URLs Base Personalizadas](#custom-base-urls)
- [Variáveis de Ambiente](#environment-variables)
- [Desabilitando o Vite em Testes](#disabling-vite-in-tests)
- [Renderização do Lado do Servidor (SSR)](#ssr)
- [Atributos de Tags Script e Style](#script-and-style-attributes)
  - [Nonce de Content Security Policy (CSP)](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [Atributos Arbitrários](#arbitrary-attributes)
- [Personalização Avançada](#advanced-customization)
  - [Cross-Origin Resource Sharing (CORS) do Dev Server](#cors)
  - [Corrigindo URLs do Dev Server](#correcting-dev-server-urls)

<a id="introduction"></a>
## Introdução

[Vite](https://vitejs.dev) é uma ferramenta moderna de build frontend que fornece um ambiente de desenvolvimento extremamente rápido e empacota seu código para produção. Ao construir aplicações com Laravel, você normalmente usará o Vite para empacotar os arquivos CSS e JavaScript da sua aplicação em assets prontos para produção.

O Laravel integra-se perfeitamente com o Vite fornecendo um plugin oficial e uma diretiva Blade para carregar seus assets para desenvolvimento e produção.

<a id="installation"></a>
## Instalação e Configuração

> **Nota:**
> A documentação a seguir discute como instalar e configurar manualmente o plugin Vite do Laravel. No entanto, os [starter kits](../starter-kits/) do Laravel já incluem toda essa estrutura e são a maneira mais rápida de começar com Laravel e Vite.

<a id="installing-node"></a>
### Instalando o Node

Você deve garantir que o Node.js (16+) e o NPM estejam instalados antes de executar o Vite e o plugin Laravel:

```shell
node -v
npm -v
```

Você pode facilmente instalar a versão mais recente do Node e NPM usando instaladores gráficos simples do [site oficial do Node](https://nodejs.org/en/download/). Ou, se você estiver usando o [Laravel Sail](../sail/), você pode invocar o Node e NPM através do Sail:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a id="installing-vite-and-laravel-plugin"></a>
### Instalando o Vite e o Plugin Laravel

Dentro de uma instalação nova do Laravel, você encontrará um arquivo `package.json` na raiz da estrutura de diretórios da sua aplicação. O arquivo `package.json` padrão já inclui tudo que você precisa para começar a usar o Vite e o plugin Laravel. Você pode instalar as dependências frontend da sua aplicação via NPM:

```shell
npm install
```

<a id="configuring-vite"></a>
### Configurando o Vite

O Vite é configurado via um arquivo `vite.config.js` na raiz do seu projeto. Você é livre para personalizar este arquivo com base em suas necessidades, e também pode instalar quaisquer outros plugins que sua aplicação requer, como `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte` ou `@vitejs/plugin-vue`.

O plugin Laravel do Vite requer que você especifique os pontos de entrada para sua aplicação. Estes podem ser arquivos JavaScript ou CSS, e incluem linguagens preprocessadas como TypeScript, JSX, TSX e Sass.

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

Se você estiver construindo uma SPA, incluindo aplicações construídas usando Inertia, o Vite funciona melhor sem pontos de entrada CSS:

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

Em vez disso, você deve importar seu CSS via JavaScript. Tipicamente, isso seria feito no arquivo `resources/js/app.js` da sua aplicação:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

O plugin Laravel também suporta múltiplos pontos de entrada e opções de configuração avançadas como [pontos de entrada SSR](#ssr).

<a id="working-with-a-secure-development-server"></a>
#### Trabalhando com um Servidor de Desenvolvimento Seguro

Se seu servidor web de desenvolvimento local estiver servindo sua aplicação via HTTPS, você pode ter problemas para conectar ao servidor de desenvolvimento Vite.

Se você estiver usando o [Laravel Herd](https://herd.laravel.com) e tiver segurado o site ou estiver usando o [Laravel Valet](../valet/) e tiver executado o [comando secure](../valet/#securing-sites) contra sua aplicação, o plugin Laravel do Vite detectará automaticamente e usará o certificado TLS gerado para você.

Se você segurou o site usando um host que não corresponde ao nome do diretório da aplicação, você pode especificar manualmente o host no arquivo `vite.config.js` da sua aplicação:

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

Ao usar outro servidor web, você deve gerar um certificado confiável e configurar manualmente o Vite para usar os certificados gerados:

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

Se você não conseguir gerar um certificado confiável para seu sistema, você pode instalar e configurar o [plugin @vitejs/plugin-basic-ssl](https://github.com/vitejs/vite-plugin-basic-ssl). Ao usar certificados não confiáveis, você precisará aceitar o aviso de certificado do servidor de desenvolvimento Vite no seu navegador seguindo o link "Local" no seu console ao executar o comando `npm run dev`.

<a id="configuring-hmr-in-sail-on-wsl2"></a>
#### Executando o Servidor de Desenvolvimento no Sail no WSL2

Ao executar o servidor de desenvolvimento Vite dentro do [Laravel Sail](../sail/) no Windows Subsystem for Linux 2 (WSL2), você deve adicionar a seguinte configuração ao seu arquivo `vite.config.js` para garantir que o navegador possa se comunicar com o servidor de desenvolvimento:

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

Se suas alterações de arquivo não estiverem sendo refletidas no navegador enquanto o servidor de desenvolvimento está em execução, você também pode precisar configurar a opção [server.watch.usePolling do Vite](https://vitejs.dev/config/server-options.html#server-watch).

<a id="loading-your-scripts-and-styles"></a>
### Carregando seus Scripts e Estilos

Com seus pontos de entrada Vite configurados, você pode agora referenciá-los em uma diretiva Blade `@vite()` que você adiciona ao `<head>` do template raiz da sua aplicação:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

Se você estiver importando seu CSS via JavaScript, você só precisa incluir o ponto de entrada JavaScript:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

A diretiva `@vite` detectará automaticamente o servidor de desenvolvimento Vite e injetará o cliente Vite para habilitar o Hot Module Replacement. Em modo de build, a diretiva carregará seus assets compilados e versionados, incluindo qualquer CSS importado.

Se necessário, você também pode especificar o caminho de build dos seus assets compilados ao invocar a diretiva `@vite`:

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a id="inline-assets"></a>
#### Assets Inline

Às vezes pode ser necessário incluir o conteúdo bruto dos assets em vez de vincular à URL versionada do asset. Por exemplo, você pode precisar incluir o conteúdo do asset diretamente na sua página ao passar conteúdo HTML para um gerador de PDF. Você pode exibir o conteúdo dos assets Vite usando o método `content` fornecido pela facade `Vite`:

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

<a id="running-vite"></a>
## Executando o Vite

Existem duas maneiras de executar o Vite. Você pode executar o servidor de desenvolvimento via o comando `dev`, que é útil ao desenvolver localmente. O servidor de desenvolvimento detectará automaticamente alterações nos seus arquivos e as refletirá instantaneamente em qualquer janela de navegador aberta.

Ou, executar o comando `build` versionará e empacotará os assets da sua aplicação e os preparará para você implantar em produção:

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

Se você estiver executando o servidor de desenvolvimento no [Sail](../sail/) no WSL2, você pode precisar de algumas opções de [configuração adicional](#configuring-hmr-in-sail-on-wsl2).

<a id="working-with-scripts"></a>
## Trabalhando com JavaScript

<a id="aliases"></a>
### Aliases

Por padrão, o plugin Laravel fornece um alias comum para ajudá-lo a começar rapidamente e importar convenientemente os assets da sua aplicação:

```js
{
    '@' => '/resources/js'
}
```

Você pode sobrescrever o alias `'@'` adicionando o seu próprio ao arquivo de configuração `vite.config.js`:

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

<a id="vue"></a>
### Vue

Se você gostaria de construir seu frontend usando o framework [Vue](https://vuejs.org/), então você também precisará instalar o plugin `@vitejs/plugin-vue`:

```shell
npm install --save-dev @vitejs/plugin-vue
```

Você pode então incluir o plugin no seu arquivo de configuração `vite.config.js`. Há algumas opções adicionais que você precisará ao usar o plugin Vue com o Laravel:

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

> **Nota:**
> Os [starter kits](../starter-kits/) do Laravel já incluem a configuração adequada do Laravel, Vue e Vite. Esses starter kits oferecem a maneira mais rápida de começar com Laravel, Vue e Vite.

<a id="react"></a>
### React

Se você gostaria de construir seu frontend usando o framework [React](https://reactjs.org/), então você também precisará instalar o plugin `@vitejs/plugin-react`:

```shell
npm install --save-dev @vitejs/plugin-react
```

Você pode então incluir o plugin no seu arquivo de configuração `vite.config.js`:

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

Você precisará garantir que quaisquer arquivos contenham JSX tenham uma extensão `.jsx` ou `.tsx`, lembrando de atualizar seu ponto de entrada, se necessário, como [mostrado acima](#configuring-vite).

Você também precisará incluir a diretiva Blade adicional `@viteReactRefresh` ao lado da sua diretiva `@vite` existente.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

A diretiva `@viteReactRefresh` deve ser chamada antes da diretiva `@vite`.

> **Nota:**
> Os [starter kits](../starter-kits/) do Laravel já incluem a configuração adequada do Laravel, React e Vite. Esses starter kits oferecem a maneira mais rápida de começar com Laravel, React e Vite.

<a id="svelte"></a>
### Svelte

Se você gostaria de construir seu frontend usando o framework [Svelte](https://svelte.dev/), então você também precisará instalar o plugin `@sveltejs/vite-plugin-svelte`:

```shell
npm install --save-dev @sveltejs/vite-plugin-svelte
```

Você pode então incluir o plugin no seu arquivo de configuração `vite.config.js`.

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

> **Nota:**
> Os [starter kits](../starter-kits/) do Laravel já incluem a configuração adequada do Laravel, Svelte e Vite. Esses starter kits oferecem a maneira mais rápida de começar com Laravel, Svelte e Vite.

<a id="inertia"></a>
### Inertia

O plugin Laravel do Vite fornece uma função conveniente `resolvePageComponent` para ajudá-lo a resolver seus componentes de página Inertia. Abaixo está um exemplo do helper em uso com Vue 3; no entanto, você também pode utilizar a função em outros frameworks como React ou Svelte:

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

Se você estiver usando o recurso de code splitting do Vite com Inertia, recomendamos configurar o [pré-buscamento de assets](#asset-prefetching).

> **Nota:**
> Os [starter kits](../starter-kits/) do Laravel já incluem a configuração adequada do Laravel, Inertia e Vite. Esses starter kits oferecem a maneira mais rápida de começar com Laravel, Inertia e Vite.

<a id="url-processing"></a>
### Processamento de URLs

Ao usar Vite e referenciar assets no HTML, CSS ou JS da sua aplicação, há algumas ressalvas a considerar. Primeiro, se você referenciar assets com um caminho absoluto, o Vite não incluirá o asset no build; portanto, você deve garantir que o asset esteja disponível no seu diretório público. Você deve evitar usar caminhos absolutos ao usar um [ponto de entrada CSS dedicado](#configuring-vite) porque, durante o desenvolvimento, os navegadores tentarão carregar esses caminhos do servidor de desenvolvimento Vite, onde o CSS é hospedado, em vez do seu diretório público.

Ao referenciar caminhos de assets relativos, você deve lembrar que os caminhos são relativos ao arquivo onde são referenciados. Quaisquer assets referenciados via um caminho relativos serão reescritos, versionados e empacotados pelo Vite.

Considere a seguinte estrutura de projeto:

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

O exemplo seguinte demonstra como o Vite tratará URLs relativas e absolutas:

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```

<a id="working-with-stylesheets"></a>
## Trabalhando com Stylesheets

> **Nota:**
> Os [starter kits](../starter-kits/) do Laravel já incluem a configuração adequada do Tailwind e Vite. Ou, se você gostaria de usar Tailwind e Laravel sem usar um dos nossos starter kits, confira o [guia de instalação do Tailwind para Laravel](https://tailwindcss.com/docs/guides/laravel).

Todas as aplicações Laravel já incluem Tailwind e um arquivo `vite.config.js` adequadamente configurado. Então, você só precisa iniciar o servidor de desenvolvimento Vite ou executar o comando Composer `dev`, que iniciará ambos os servidores de desenvolvimento Laravel e Vite:

```shell
composer run dev
```

O CSS da sua aplicação pode ser colocado dentro do arquivo `resources/css/app.css`.

<a id="working-with-fonts"></a>
## Trabalhando com Fontes

O plugin Laravel do Vite pode servir fontes otimizadas e auto-hospedadas para sua aplicação. Quando as fontes são configuradas, o plugin resolve os arquivos de fonte solicitados, emite-os como assets Vite, gera CSS de fontes e escreve um manifesto de fontes que pode ser consumido pela [diretiva `@fonts`](../blade/#fonts) do Blade.

Para configurar fontes, importe um ou mais helpers de provedor de `laravel-vite-plugin/fonts` e adicione-os à opção `fonts` do plugin Laravel:

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

Neste exemplo, a fonte `Inter` estará disponível através do alias `sans`. O plugin gerará uma variável CSS `--font-sans` e uma classe utilitária `.font-sans` que aplica a pilha de fontes gerada.

<a id="font-providers"></a>
### Provedores de Fontes

O plugin Laravel do Vite inclui helpers de provedor para Google Fonts, Bunny Fonts, Fontsource e fontes locais:

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

O provedor `fontsource` lê fontes de um pacote Fontsource instalado. Por padrão, o nome do pacote é derivado da família da fonte, como `@fontsource/jetbrains-mono`. Se sua aplicação usa um nome de pacote diferente, você pode especificá-lo usando a opção `package`.

<a id="local-fonts"></a>
### Fontes Locais

Ao usar fontes locais, a opção `src` pode apontar para um único arquivo de fonte, um diretório ou um padrão glob. O plugin descobrirá arquivos de fonte suportados e inferirá seu peso e estilo de seus nomes de arquivo:

```js
local('Brand Sans', {
    alias: 'brand',
    src: 'resources/fonts/brand-sans/*.woff2',
})
```

Se você precisar de controle total sobre as variantes disponíveis, você pode defini-las explicitamente usando a opção `variants`:

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

<a id="font-options"></a>
### Opções de Fontes

Dependendo do provedor, definições de fontes podem aceitar várias opções que permitem personalizar o CSS de fonte gerado:

<div class="content-list" markdown="1">

- `alias` define o nome usado pela diretiva `@fonts` do Blade e padrão para um slug da família da fonte.
- `variable` define a variável CSS gerada e padrão para `--font-{alias}`.
- `weights` define os pesos de fonte remotos ou Fontsource que devem ser resolvidos e padrão para `[400]`.
- `styles` define os estilos de fonte remotos ou Fontsource que devem ser resolvidos e padrão para `['normal']`.
- `subsets` define os subconjuntos de fonte remotos ou Fontsource que devem ser resolvidos e padrão para `['latin']`.
- `display` define o valor `font-display` e padrão para `swap`.
- `preload` controla quais variantes de fonte WOFF2 devem ser pré-carregadas. Esta opção pode ser `true`, `false` ou um array de seletores `{ weight, style }`.
- `fallbacks` define fontes de fallback adicionais que devem ser anexadas à pilha de fontes gerada.
- `optimizedFallbacks` tenta gerar font faces de fallback ajustadas por métrica usando o pacote opcional `fontaine` e padrão para `true`.

</div>

Fallbacks otimizados requerem o pacote `fontaine`, que não é instalado por padrão. Se você quiser que o Laravel gere font faces de fallback ajustadas por métrica, você deve instalar `fontaine` como uma dependência de desenvolvimento:

```shell
npm install --save-dev fontaine
```

Se `fontaine` não estiver instalado ou não conseguir ler um arquivo de fonte, o Laravel pulará o fallback otimizado para essa fonte e continuará usando quaisquer fontes configuradas via a opção `fallbacks`.

Fontes locais são resolvidas a partir das opções `src` ou `variants` descritas acima em vez de usar `weights`, `styles` e `subsets`.

<a id="working-with-blade-and-routes"></a>
## Trabalhando com Blade e Rotas

<a id="blade-processing-static-assets"></a>
### Processando Assets Estáticos com Vite

Ao referenciar assets no seu JavaScript ou CSS, o Vite processa e versiona automaticamente. Além disso, ao construir aplicações baseadas em Blade, o Vite também pode processar e versionar assets estáticos que você referencia apenas em templates Blade.

No entanto, para conseguir isso, você precisa tornar o Vite ciente dos seus assets especificando-os na opção `assets` do plugin. Esta opção é destinada para arquivos estáticos que você deseja referenciar diretamente com `Vite::asset`. Se você quiser que o Laravel gere CSS de fonte e links de pré-carregamento, use a opção [`fonts`](#working-with-fonts) em vez disso.

Por exemplo, se você quiser processar e versionar todas as imagens armazenadas em `resources/images` e todas as fontes armazenadas em `resources/fonts`, você deve adicionar o seguinte à sua configuração Vite:

```js
laravel({
    input: 'resources/js/app.js',
    assets: ['resources/images/**', 'resources/fonts/**'],
})
```

Esses assets agora serão processados pelo Vite ao executar `npm run build`. Você pode então referenciar esses assets em templates Blade usando o método `Vite::asset`, que retornará a URL versionada para um determinado asset:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

> **Nota:**
> Antes da versão 3 do plugin Laravel do Vite, assets estáticos tinham que ser importados no ponto de entrada da sua aplicação usando `import.meta.glob`. A opção `assets` foi introduzida devido a mudanças no Vite 8.

<a id="blade-refreshing-on-save"></a>
### Atualizando ao Salvar

Quando sua aplicação é construída usando renderização tradicional do lado do servidor com Blade, o Vite pode melhorar seu fluxo de trabalho de desenvolvimento atualizando automaticamente o navegador quando você faz alterações nos arquivos de view da sua aplicação. Para começar, você pode simplesmente especificar a opção `refresh` como `true`.

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

Quando a opção `refresh` é `true`, salvar arquivos nos seguintes diretórios acionará o navegador a realizar uma atualização completa da página enquanto você estiver executando `npm run dev`:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

Observar o diretório `routes/**` é útil se você estiver utilizando [Ziggy](https://github.com/tighten/ziggy) para gerar links de rotas dentro do frontend da sua aplicação.

Se esses caminhos padrão não atenderem suas necessidades, você pode especificar sua própria lista de caminhos para observar:

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

Por baixo dos panos, o plugin Laravel do Vite usa o pacote [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload), que oferece algumas opções de configuração avançadas para ajustar o comportamento deste recurso. Se você precisar deste nível de personalização, você pode fornecer uma definição `config`:

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

<a id="blade-aliases"></a>
### Aliases

É comum em aplicações JavaScript [criar aliases](#aliases) para diretórios regularmente referenciados. Mas, você também pode criar aliases para usar no Blade usando o método `macro` na classe `Illuminate\Support\Facades\Vite`. Tipicamente, "macros" devem ser definidas dentro do método `boot` de um [provedor de serviço](../providers/):

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

Uma vez que uma macro tenha sido definida, ela pode ser invocada dentro dos seus templates. Por exemplo, podemos usar a macro `image` definida acima para referenciar um asset localizado em `resources/images/logo.png`:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a id="asset-prefetching"></a>
## Pré-buscando Assets

Ao construir uma SPA usando o recurso de code splitting do Vite, os assets necessários são buscados em cada navegação de página. Este comportamento pode levar a renderização atrasada da UI. Se isso for um problema para o framework frontend da sua escolha, o Laravel oferece a capacidade de pré-buscar ansiosamente os assets JavaScript e CSS da sua aplicação no carregamento inicial da página.

Você pode instruir o Laravel a pré-buscar ansiosamente seus assets invocando o método `Vite::prefetch` no método `boot` de um [provedor de serviço](../providers/):

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

No exemplo acima, os assets serão pré-buscados com um máximo de `3` downloads concorrentes em cada carregamento de página. Você pode modificar a concorrência para atender às necessidades da sua aplicação ou especificar nenhum limite de concorrência se a aplicação deve baixar todos os assets de uma vez:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

Por padrão, o pré-buscamento começará quando o [evento _load_ da página](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) for disparado. Se você gostaria de personalizar quando o pré-buscamento começa, você pode especificar um evento que o Vite ouvirá:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

Dado o código acima, o pré-buscamento agora começará quando você despachar manualmente o evento `vite:prefetch` no objeto `window`. Por exemplo, você poderia ter o pré-buscamento começando três segundos após o carregamento da página:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a id="custom-base-urls"></a>
## URLs Base Personalizadas

Se seus assets compilados Vite forem implantados em um domínio separado da sua aplicação, como via CDN, você deve especificar a variável de ambiente `ASSET_URL` no arquivo `.env` da sua aplicação:

```env
ASSET_URL=https://cdn.example.com
```

Após configurar a URL do asset, todas as URLs reescritas para seus assets serão prefixadas com o valor configurado:

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

Lembre-se que [URLs absolutas não são reescritas pelo Vite](#url-processing), então não serão prefixadas.

<a id="environment-variables"></a>
## Variáveis de Ambiente

Você pode injetar variáveis de ambiente no seu JavaScript prefixando-as com `VITE_` no arquivo `.env` da sua aplicação:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

Você pode acessar variáveis de ambiente injetadas via o objeto `import.meta.env`:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a id="disabling-vite-in-tests"></a>
## Desabilitando o Vite em Testes

A integração Vite do Laravel tentará resolver seus assets enquanto executa seus testes, o que requer que você execute o servidor de desenvolvimento Vite ou construa seus assets.

Se você preferir fazer mock do Vite durante os testes, você pode chamar o método `withoutVite`, que está disponível para quaisquer testes que estendem a classe `TestCase` do Laravel:

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

Se você gostaria de desabilitar o Vite para todos os testes, você pode chamar o método `withoutVite` do método `setUp` na sua classe base `TestCase`:

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

<a id="ssr"></a>
## Renderização do Lado do Servidor (SSR)

O plugin Laravel do Vite torna fácil configurar a renderização do lado do servidor com Vite. Para começar, crie um ponto de entrada SSR em `resources/js/ssr.js` e especifique o ponto de entrada passando uma opção de configuração ao plugin Laravel:

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

Para garantir que você não esqueça de reconstruir o ponto de entrada SSR, recomendamos aumentar o script "build" no `package.json` da sua aplicação para criar seu build SSR:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

Então, para construir e iniciar o servidor SSR, você pode executar os seguintes comandos:

```shell
npm run build
node bootstrap/ssr/ssr.js
```

Se você estiver usando [SSR com Inertia](https://inertiajs.com/server-side-rendering), você pode usar o comando Artisan `inertia:start-ssr` para iniciar o servidor SSR:

```shell
php artisan inertia:start-ssr
```

> **Nota:**
> Os [starter kits](../starter-kits/) do Laravel já incluem a configuração adequada do Laravel, Inertia SSR e Vite. Esses starter kits oferecem a maneira mais rápida de começar com Laravel, Inertia SSR e Vite.

<a id="script-and-style-attributes"></a>
## Atributos de Tags Script e Style

<a id="content-security-policy-csp-nonce"></a>
### Nonce de Content Security Policy (CSP)

Se você deseja incluir um [atributo nonce](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) nas suas tags script e style como parte da sua [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), você pode gerar ou especificar um nonce usando o método `useCspNonce` dentro de um [middleware](../middleware/) personalizado:

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

Após invocar o método `useCspNonce`, o Laravel incluirá automaticamente os atributos `nonce` em todas as tags script e style geradas.

Se você precisar especificar o nonce em outro lugar, incluindo a [diretiva `@route` do Ziggy](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) incluída com os [starter kits](../starter-kits/) do Laravel, você pode recuperá-lo usando o método `cspNonce`:

```blade
@routes(nonce: Vite::cspNonce())
```

Se você já tem um nonce que gostaria de instruir o Laravel a usar, você pode passar o nonce ao método `useCspNonce`:

```php
Vite::useCspNonce($nonce);
```

<a id="subresource-integrity-sri"></a>
### Subresource Integrity (SRI)

Se o manifesto Vite incluir hashes `integrity` para seus assets, o Laravel adicionará automaticamente o atributo `integrity` em quaisquer tags script e style que gerar para impor [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity). Por padrão, o Vite não inclui o hash `integrity` em seu manifesto, mas você pode habilitá-lo instalando o plugin NPM [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri):

```shell
npm install --save-dev vite-plugin-manifest-sri
```

Você pode então habilitar este plugin no seu arquivo `vite.config.js`:

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

Se necessário, você também pode personalizar a chave do manifesto onde o hash de integridade pode ser encontrado:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

Se você gostaria de desabilitar completamente esta detecção automática, você pode passar `false` ao método `useIntegrityKey`:

```php
Vite::useIntegrityKey(false);
```

<a id="arbitrary-attributes"></a>
### Atributos Arbitrários

Se você precisar incluir atributos adicionais nas suas tags script e style, como o atributo [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change), você pode especificá-los via os métodos `useScriptTagAttributes` e `useStyleTagAttributes`. Tipicamente, esses métodos devem ser invocados de um [provedor de serviço](../providers/):

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

Se você precisar adicionar atributos condicionalmente, você pode passar um callback que receberá o caminho de origem do asset, sua URL, seu chunk de manifesto e o manifesto inteiro:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $src === 'resources/js/app.js' ? 'reload' : false,
]);

Vite::useStyleTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $chunk && $chunk['isEntry'] ? 'reload' : false,
]);
```

> **Aviso:**
> Os argumentos `$chunk` e `$manifest` serão `null` enquanto o servidor de desenvolvimento Vite estiver em execução.

<a id="advanced-customization"></a>
## Personalização Avançada

Pronto para uso, o plugin Vite do Laravel usa convenções sensatas que devem funcionar para a maioria das aplicações; no entanto, às vezes você pode precisar personalizar o comportamento do Vite. Para habilitar opções de personalização adicionais, oferecemos os seguintes métodos e opções que podem ser usados no lugar da diretiva Blade `@vite`:

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

Dentro do arquivo `vite.config.js`, você deve então especificar a mesma configuração:

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

<a id="cors"></a>
### Cross-Origin Resource Sharing (CORS) do Dev Server

Se você estiver enfrentando problemas de Cross-Origin Resource Sharing (CORS) no navegador ao buscar assets do servidor de desenvolvimento Vite, você pode precisar conceder à sua origem personalizada acesso ao servidor de desenvolvimento. Vite combinado com o plugin Laravel permite as seguintes origens sem qualquer configuração adicional:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- `APP_URL` no `.env` do projeto

A maneira mais fácil de permitir uma origem personalizada para seu projeto é garantir que a variável de ambiente `APP_URL` da sua aplicação corresponda à origem que você está visitando no seu navegador. Por exemplo, se você estiver visitando `https://my-app.laravel`, você deve atualizar seu `.env` para corresponder:

```env
APP_URL=https://my-app.laravel
```

Se você precisar de controle mais granular sobre as origens, como suportar múltiplas origens, você deve utilizar a [configuração CORS abrangente e flexível integrada do Vite](https://vite.dev/config/server-options.html#server-cors). Por exemplo, você pode especificar múltiplas origens na opção de configuração `server.cors.origin` no arquivo `vite.config.js` do projeto:

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

Você também pode incluir padrões regex, que podem ser úteis se você gostaria de permitir todas as origens para um determinado domínio de nível superior, como `*.laravel`:

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

<a id="correcting-dev-server-urls"></a>
### Corrigindo URLs do Dev Server

Alguns plugins dentro do ecossistema Vite assumem que URLs que começam com uma barra sempre apontarão para o servidor de desenvolvimento Vite. No entanto, devido à natureza da integração Laravel, este não é o caso.

Por exemplo, o plugin `vite-imagetools` produz URLs como as seguintes enquanto o Vite está servindo seus assets:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

O plugin `vite-imagetools` espera que a URL de saída seja interceptada pelo Vite e o plugin pode então tratar todas as URLs que começam com `/@imagetools`. Se você estiver usando plugins que esperam este comportamento, você precisará corrigir manualmente as URLs. Você pode fazer isso no seu arquivo `vite.config.js` usando a opção `transformOnServe`.

Neste exemplo particular, nós prefixaremos a URL do servidor de desenvolvimento em todas as ocorrências de `/@imagetools` dentro do código gerado:

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

Agora, enquanto o Vite estiver servindo Assets, ele produzirá URLs que apontam para o servidor de desenvolvimento Vite:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```