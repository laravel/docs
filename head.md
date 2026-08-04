# Laravel Head

- [Introduction](#introduction)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Resolution Precedence](#resolution-precedence)
- [Defining Metadata](#defining-metadata)
    - [Defaults](#defaults)
    - [Route Metadata](#route-metadata)
    - [Runtime Metadata](#runtime-metadata)
    - [Error Pages](#error-pages)
- [Open Graph](#open-graph)
    - [X / Twitter Cards](#twitter-cards)
- [Theme Colors](#theme-colors)
- [Application Metadata and Icons](#app-metadata-and-icons)
- [Progressive Web Apps](#progressive-web-apps)
- [Performance and Discovery](#performance-and-discovery)
- [Custom Tags](#custom-tags)
- [Schemas](#schemas)
    - [Breadcrumbs](#breadcrumbs)
    - [FAQs](#faqs)
    - [Custom Schemas](#custom-schemas)
- [Rendering](#rendering)
    - [Blade](#blade)
    - [Livewire](#livewire)
    - [Inertia](#inertia)

<a name="introduction"></a>
## Introduction

[Laravel Head](https://github.com/laravel/head) provides a fluent API for managing your application's document `<head>` element, including title and meta tags, Open Graph metadata, canonical URLs, robots directives, performance hints, and structured data. It works with Blade, Livewire, and Inertia.

<a name="installation"></a>
## Installation

You may install Laravel Head using the Composer package manager:

```shell
composer require laravel/head
```

<a name="quickstart"></a>
## Quickstart

Register site-wide defaults in a service provider:

```php
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(fn (HeadBuilder $head) => $head
    ->title('Laravel', suffix: ' - Laravel')
    ->description('Build something great.'));
```

Set page-specific metadata at runtime:

```php
Head::title($post->title)
    ->description($post->description);
```

Render the resolved tags in your layout:

```blade
<head>
    @head
</head>
```

<a name="resolution-precedence"></a>
## Resolution Precedence

Page metadata resolves from five layers, listed from lowest to highest priority:

1. Page defaults
2. Route group metadata
3. Route metadata
4. Runtime metadata
5. Error metadata

Higher layers replace lower layers field by field. For example, a runtime title replaces the route title without replacing the route description. The sections that follow describe how to set metadata at each layer. For information about rendering the resolved metadata in Blade, Livewire, and Inertia, see [Rendering](#rendering).

<a name="defining-metadata"></a>
## Defining Metadata

Laravel Head allows you to define metadata using site-wide defaults, route metadata, runtime calls, and error page definitions.

<a name="defaults"></a>
### Defaults

Register page defaults in a service provider:

```php
use Laravel\Head\Enums\OgType;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(function (HeadBuilder $head) {
    $head
        ->title('Laravel', suffix: ' - Laravel')
        ->description('Build something great.')
        ->canonical()
        ->og(siteName: 'Laravel', type: OgType::Website)
        ->searchableByRobots()
        ->preconnect('https://fonts.example.com');
});
```

Defaults are the lowest-priority page metadata layer. If no route, runtime, or error metadata sets a title, `Laravel` renders as-is. When a higher layer sets a page title, the inherited suffix is applied, so `Head::title('About')` renders `About - Laravel`. Pass `exact: true` for titles that should ignore an inherited prefix or suffix.

Calling `Head::canonical()` renders a canonical URL using the current request URL. To set an explicit URL, pass a string such as `Head::canonical('/about')`. Canonical URLs are normalized to `https` by default; pass `forceHttps: false` to preserve the request scheme.

Robots directives may be passed as a raw string, as `RobotsRule` enum cases, or as a list mixing both forms. Lists are rendered as comma-separated directives, so `Head::robots([RobotsRule::NoIndex, RobotsRule::NoFollow])` renders `noindex, nofollow`.

For convenience, the `searchableByRobots` method renders `all`, while the `hiddenFromRobots` method renders `none`.

<a name="route-metadata"></a>
### Route Metadata

You may define metadata directly on routes, which is especially useful for semi-static pages whose metadata is known ahead of time.

<a name="routes-and-groups"></a>
#### Routes and Groups

```php
Route::view('/contact', 'contact')
    ->name('contact')
    ->withHead(
        title: 'Contact Us',
        description: 'Get in touch.',
    );
```

Shared route metadata may be applied to a group at any position in the chain:

```php
Route::withHead(robots: 'noindex, nofollow')
    ->prefix('admin')
    ->name('admin.')
    ->group(function () {
        Route::get('/dashboard', DashboardController::class)
            ->name('dashboard')
            ->withHead(title: 'Dashboard');
    });
```

You may also define metadata for resource and singleton routes:

```php
Route::resource('posts', PostController::class)->withHead(
    robots: 'index, follow',
);

Route::singleton('profile', ProfileController::class)->withHead(
    title: 'Your Profile',
);
```

The `withHead` method stores plain arrays through Laravel's native route metadata API. It is equivalent to calling the `metadata` method with the attributes nested under a `head` key, so the metadata remains compatible with cached routes.

The named arguments are intentionally limited to Laravel Head's built-in route properties so editors and static analysis can catch misspelled names. Route attributes registered by custom tag builders may be passed through `extensions`:

```php
Route::get('/article', ArticleController::class)->withHead(
    title: 'Article',
    extensions: ['readingTime' => 4],
);
```

<a name="supported-properties"></a>
#### Supported Properties

The supported route properties map to the same names as the fluent builder methods:

| Category | Properties |
| --- | --- |
| Document | `title`, `description`, `canonical`, `robots` |
| Application metadata | `themeColor`, `applicationName`, `colorScheme`, `referrer`, `viewport`, `appleWebAppTitle`, `webAppCapable`, `appleWebAppStatusBarStyle` |
| Social | `og`, `ogImage`, `ogVideo`, `ogAudio`, `twitter`, `twitterImage` |
| Performance | `preload`, `prefetch`, `preconnect`, `dnsPrefetch` |
| Discovery | `alternates`, `feed`, `icon`, `favicon`, `appleTouchIcon`, `appleTouchStartupImage`, `maskIcon`, `manifest` |
| Structured data | `schema` |
| Custom tags | `meta`, `link` |

Nested option names use the same `camelCase` naming as the fluent API, such as `forceHttps`, `siteName`, and `secureUrl`.

Repeatable properties, such as `ogImage`, `preload`, `feed`, `schema`, `icon`, and `appleTouchStartupImage`, accept either a single value or a list.

<a name="runtime-metadata"></a>
### Runtime Metadata

When a value isn't known until a request arrives, such as the title of a post being viewed, you may set it at runtime:

```php
use Laravel\Head\Facades\Head;

public function __invoke(Post $post): Response
{
    Head::title($post->title);

    // ...
}
```

Runtime calls made via the `Head` facade override route metadata for request-dependent data. Controllers and actions are the most common places to make these calls:

```php
use App\Models\Post;
use Laravel\Head\Facades\Head;

public function show(Post $post)
{
    Head::title($post->title)
        ->description($post->description);

    return view('posts.show', ['post' => $post]);
}
```

Multiple runtime calls are merged in the order they run. For single-value fields such as title, description, canonical URL, and robots directives, the later call takes precedence. Repeatable fields retain multiple entries, but adding the same key again updates the earlier entry. For the `ogImage` method, the URL is the key:

```php
Head::ogImage('/images/cover.jpg', alt: 'Draft cover')
    ->ogImage('/images/gallery.jpg', alt: 'Gallery image')
    ->ogImage('/images/cover.jpg', alt: 'Final cover', width: 1200, height: 630);
```

```html
<meta property="og:image" content="/images/cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Final cover">
<meta property="og:image" content="/images/gallery.jpg">
<meta property="og:image:alt" content="Gallery image">
```

Open Graph media inherited from your defaults acts as a fallback. When route, runtime, or error metadata defines its own media of the same type, the default media is replaced instead of merged, so a page's `og:image` takes precedence over a site-wide default image.

You may fluently define conditional metadata using the `when` and `unless` methods:

```php
Head::title($post->title)
    ->when($post->isDraft(), fn ($head) => $head->hiddenFromRobots());
```

<a name="error-pages"></a>
### Error Pages

Typically, you should register error metadata within the `boot` method of your application's `AppServiceProvider` class:

```php
use Laravel\Head\ErrorPages;
use Laravel\Head\Facades\Head;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Head::errors(function (ErrorPages $errors) {
        $errors->defaults(robots: 'noindex, follow');

        $errors->status(
            404,
            title: 'Page Not Found',
            description: 'The page you are looking for could not be found.',
        );
    });
}
```

The `defaults` and `status` methods also accept the same fluent builder callback used by `Head::defaults()`:

```php
use Laravel\Head\ErrorPages;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::errors(function (ErrorPages $errors) {
    $errors->status(404, fn (HeadBuilder $head) => $head
        ->title('Page Not Found')
        ->description('The page you are looking for could not be found.'));
});
```

When a response is rendered for a registered error status, that metadata takes precedence over every other layer.

Laravel automatically detects the response status when rendering an error view or executing a respond-phase hook such as Inertia's `handleExceptionsUsing()` method. If you render an error response inside an `$exceptions->render()` callback, call `Head::status(404)` before rendering so the error metadata is applied.

<a name="open-graph"></a>
## Open Graph

You may set Open Graph properties using the `og` method. Repeatable media may be added using the top-level methods, which accept named arguments directly:

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\OgType;

Head::og(type: OgType::Article, title: $post->title)
    ->ogImage($post->hero_image_url)
    ->ogImage(
        $post->gallery_image_url,
        alt: $post->gallery_image_alt,
        width: 1200,
        height: 630,
        type: ImageType::Jpeg,
    );
```

The `ogImage`, `ogVideo`, and `ogAudio` methods accept a URL as their first argument, along with optional named arguments such as `alt`, `width`, `height`, `type`, and `secureUrl` where supported by the Open Graph specification.

You may pass image MIME types as `ImageType` enum cases anywhere the API accepts an image `type`, such as `ImageType::Svg`, `ImageType::Png`, `ImageType::Jpeg`, and `ImageType::Webp`.

> [!NOTE]
> Document `title` and `description` automatically fill missing `og:title` and `og:description` values.

For a single Open Graph image with no other attributes, you may pass the `image` named argument to the `og` method:

```php
Head::og(
    type: OgType::Website,
    title: $page->title,
    description: $page->description,
    image: $page->og_image_url,
);
```

The `og(image: ...)` and `ogImage(...)` calls write to the same underlying image list, so you may use whichever is more expressive at the call site. You may use the [`meta`](#custom-tags) method for custom Open Graph extensions such as product or article properties.

<a name="twitter-cards"></a>
### X / Twitter Cards

To render X / Twitter cards from the same title, description, and image used by Open Graph, register `twitter()` in your defaults:

```php
use Laravel\Head\Enums\TwitterCard;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(fn (HeadBuilder $head) => $head->twitter(
    card: TwitterCard::SummaryWithLargeImage,
));
```

Then set page-level metadata:

```php
Head::title('Introducing Laravel Head')
    ->description('A fluent API for Laravel document head metadata.')
    ->ogImage('https://example.com/social.jpg', alt: 'Introducing Laravel Head');
```

This renders matching Twitter tags:

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Introducing Laravel Head">
<meta name="twitter:description" content="A fluent API for Laravel document head metadata.">
<meta name="twitter:image" content="https://example.com/social.jpg">
<meta name="twitter:image:alt" content="Introducing Laravel Head">
```

You may customize individual pages with explicit Twitter values:

```php
Head::twitter(title: $post->social_title)
    ->twitterImage($post->social_image_url, alt: $post->title);
```

Route metadata accepts `twitter` and `twitterImage`.

<a name="theme-colors"></a>
## Theme Colors

You may set theme colors globally, per route, or at runtime:

```php
Head::themeColor('#0f172a');
```

This renders a `<meta name="theme-color">` tag. For media-specific theme colors, you may use the `Media` enum:

```php
use Laravel\Head\Enums\Media;

Head::themeColor('#ffffff', media: Media::Light)
    ->themeColor('#111827', media: Media::Dark);
```

The `Media` enum also includes `Portrait` and `Landscape`. The `media` argument also accepts a custom media query string.

Route metadata supports a single theme color through the same `camelCase` key:

```php
Route::view('/dashboard', 'dashboard')->withHead(
    themeColor: '#0f172a',
);
```

<a name="app-metadata-and-icons"></a>
## Application Metadata and Icons

Laravel Head includes methods for common browser and application metadata:

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\Media;

Head::applicationName('Laravel')
    ->colorScheme('light dark')
    ->referrer('strict-origin-when-cross-origin')
    ->viewport('width=device-width, initial-scale=1')
    ->appleWebAppTitle('Laravel')
    ->webAppCapable()
    ->appleWebAppStatusBarStyle('black')
    ->favicon('/favicon.svg', type: ImageType::Svg)
    ->icon('/favicon-32x32.png', type: ImageType::Png, sizes: '32x32')
    ->appleTouchIcon('/apple-touch-icon.png', sizes: '180x180')
    ->appleTouchStartupImage('/launch.png', media: Media::Portrait)
    ->maskIcon('/safari-pinned-tab.svg', color: '#111827')
    ->manifest('/site.webmanifest');
```

The `favicon` method is an alias for the `icon` method and accepts the same `type`, `sizes`, and `media` arguments.

Route metadata uses the same names:

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\Media;

Route::view('/dashboard', 'dashboard')->withHead(
    applicationName: 'Laravel',
    colorScheme: 'light dark',
    appleWebAppTitle: 'Laravel',
    webAppCapable: true,
    appleWebAppStatusBarStyle: 'black',
    favicon: [
        ['href' => '/favicon.svg', 'type' => ImageType::Svg],
        ['href' => '/favicon-32x32.png', 'type' => ImageType::Png, 'sizes' => '32x32'],
    ],
    appleTouchIcon: ['href' => '/apple-touch-icon.png', 'sizes' => '180x180'],
    appleTouchStartupImage: ['href' => '/launch.png', 'media' => Media::Portrait],
    manifest: '/site.webmanifest',
);
```

<a name="progressive-web-apps"></a>
## Progressive Web Apps

The `pwa` method configures the common document `<head>` tags needed for an installable web app:

```php
Head::pwa(
    name: 'Laravel',
    manifest: '/site.webmanifest',
    themeColor: '#0f172a',
    appleTouchIcon: '/apple-touch-icon.png',
    appleWebAppStatusBarStyle: 'black',
);
```

This renders the application name, web application manifest link, and iOS standalone metadata. If provided, the theme color, Apple status bar style, and Apple touch icon are also rendered. Creating the web application manifest and registering a service worker remain your application's responsibility.

You may use the `pwa` method in defaults or runtime metadata. Route metadata supports the individual properties shown above.

<a name="performance-and-discovery"></a>
## Performance and Discovery

Laravel Head renders performance hints, pagination links, locale alternates, and feed discovery:

```php
Head::preload(asset('fonts/inter.woff2'), as: 'font', crossorigin: true)
    ->prefetch(asset('images/next.webp'))
    ->preconnect('https://cdn.example.com')
    ->dnsPrefetch('https://analytics.example.com')
    ->paginate($posts)
    ->alternates([
        'en' => 'https://example.com/en/about',
        'fr' => 'https://example.com/fr/about',
        'x-default' => 'https://example.com/about',
    ])
    ->feed('/feed', title: 'Laravel RSS')
    ->feed('/feed.atom', type: 'atom', title: 'Laravel Atom');
```

For local assets, `preloadAsset()` and `prefetchAsset()` resolve the URL through the `asset()` helper and detect the `as` attribute from the file extension. Font preloads automatically include `crossorigin`, which the preload specification requires even for same-origin fonts:

```php
Head::preloadAsset('fonts/inter.woff2')
    ->prefetchAsset('images/next.webp');
```

```html
<link rel="preload" href="https://example.com/fonts/inter.woff2" as="font" crossorigin>
<link rel="prefetch" href="https://example.com/images/next.webp" as="image">
```

You may pass `as` explicitly to override detection. The `preloadAsset` method will throw an exception when the `as` attribute cannot be detected from the extension because browsers ignore preloads without this attribute; the `prefetchAsset` method will simply omit it.

<a name="custom-tags"></a>
## Custom Tags

For tags without a dedicated method, use `meta()` and `link()`:

```php
Head::meta('format-detection', 'telephone=no')
    ->meta('article:author', $post->author->name)
    ->link('search', '/opensearch.xml', [
        'type' => 'application/opensearchdescription+xml',
        'title' => 'Laravel Search',
    ])
    ->link('me', 'https://social.example.com/@laravel');
```

You may include a media query on a meta tag when the browser should only apply the tag under matching conditions:

```php
use Laravel\Head\Enums\Media;

Head::meta('theme-color', '#ffffff', media: Media::Light)
    ->meta('theme-color', '#111827', media: Media::Dark);
```

The `meta` method uses the `name` attribute for regular meta tags. For keys that typically use the `property` attribute, such as Open Graph (`og:`) or article metadata (`article:`), the method switches automatically:

```php
Head::meta('description', 'About Laravel')
    ->meta('og:title', 'About Laravel');
```

```html
<meta name="description" content="About Laravel">
<meta property="og:title" content="About Laravel">
```

You may pass `property: true` or `property: false` to explicitly select either attribute.

<a name="schemas"></a>
## Schemas

Built-in schema builders cover the common JSON-LD types:

```php
use Laravel\Head\Enums\OfferAvailability;
use Laravel\Head\Facades\Schema;

Head::schema(
    Schema::product()
        ->name($product->name)
        ->offers(
            Schema::offer()
                ->price($product->price)
                ->currency('USD')
                ->availability(OfferAvailability::InStock)
        )
);
```

The built-in factory methods are `article`, `blogPosting`, `product`, `offer`, `brand`, `breadcrumbs`, `faq`, `organization`, `person`, `webPage`, and `webSite`. Unknown factory methods create a generic schema object, so you can still express custom schema.org types.

When JSON-LD schema data is invalid, Laravel Head throws an exception in non-production environments and logs a warning in production.

<a name="breadcrumbs"></a>
### Breadcrumbs

Breadcrumb items may be added one at a time or in bulk. Positions are assigned automatically in the order the items are added:

```php
Head::schema(
    Schema::breadcrumbs()->items([
        'Home' => route('home'),
        'Shop' => route('shop.index'),
        'Shoes' => route('shop.category', 'shoes'),
    ])
);
```

You may use the `item` method to append a single breadcrumb item:

```php
Schema::breadcrumbs()
    ->item('Home', route('home'))
    ->item('Shop', route('shop.index'));
```

<a name="faqs"></a>
### FAQs

FAQ entries follow the same pattern. You may add them one at a time using the `question` method or in bulk using the `questions` method:

```php
Head::schema(
    Schema::faq()->questions([
        'What is Laravel Head?' => 'A fluent API for managing the document head.',
        'Is it free?' => 'Yes, it is open source.',
    ])
);
```

<a name="custom-schemas"></a>
### Custom Schemas

You may explicitly register custom schema types:

```php
use DateTimeInterface;
use Laravel\Head\Facades\Schema;
use Laravel\Head\Schema\SchemaObject;
use Laravel\Head\SchemaType;

#[SchemaType('JobPosting')]
class JobPosting extends SchemaObject
{
    public function title(string $title): static
    {
        return $this->set('title', $title);
    }

    public function datePosted(DateTimeInterface|string $date): static
    {
        return $this->date('datePosted', $date);
    }
}

Schema::register(JobPosting::class);

Head::schema(
    Schema::jobPosting()
        ->title('Senior Laravel Developer')
        ->datePosted(now())
);
```

<a name="rendering"></a>
## Rendering

Laravel Head resolves page metadata into tags for the current response. How these tags are rendered depends on your application stack.

The HTML renderer powers the `@head` directive and the rendered elements that Laravel Head shares with Inertia via the `head` prop. The array renderer powers `Head::toArray()` for applications that need the resolved metadata as structured data.

<a name="blade"></a>
### Blade

Render the accumulated tags in your layout's `<head>` with the `@head` directive:

```blade
<head>
    <meta charset="utf-8">
    @head
</head>
```

The `@head` directive renders synchronously, so you should define page metadata before the layout is rendered.

<a name="livewire"></a>
### Livewire

Livewire applications use the same `@head` directive in their document layout:

```blade
<head>
    @head
</head>

<body>
    {{ $slot }}

    @livewireScripts
</body>
```

No Livewire-specific configuration is required. Laravel Head metadata is resolved per request, and the resolver is request-scoped. Therefore, each `wire:navigate` visit fetches a fresh document whose `@head` output reflects the destination route's metadata. Pages visited using `wire:navigate` receive the appropriate route, runtime, and error metadata without requiring component-level head code.

<a name="inertia"></a>
### Inertia

Use the same `@head` directive in your Inertia root template, alongside Inertia's own components:

```blade
<html>
<head>
    <meta charset="utf-8">
    @head

    @viteReactRefresh
    @vite(['resources/css/app.css', 'resources/js/app.tsx'])
    <x-inertia::head />
</head>
<body>
    <x-inertia::app />
</body>
</html>
```

When Inertia is installed, Laravel Head automatically shares the page-managed head as an array of rendered element strings under a `head` prop on every page object:

```json
{
    "props": {
        "head": [
            "<title data-inertia=\"title\">Dashboard - Laravel</title>",
            "<meta data-inertia=\"description\" name=\"description\" content=\"Your application overview.\">"
        ]
    }
}
```

Enable Inertia's `serverHead` option wherever your application calls `createInertiaApp()`. The option is available in Inertia 3.5 and later:

```js
createInertiaApp({
    // ...
    serverHead: true,
});
```

Each page-managed element has a stable `data-inertia` key. The `@head` directive renders the initial document, after which Inertia adopts those elements and keeps them synchronized during standard visits, [instant visits](https://inertiajs.com/docs/v3/the-basics/instant-visits), and back and forward navigation. The elements are present in the initial HTML response, so crawlers and link-preview bots can read them without executing JavaScript. No client-side `<Head>` component is required.

This works with or without [server-side rendering (SSR)](https://inertiajs.com/docs/v3/advanced/server-side-rendering). If your application has a separate SSR entry point, enable `serverHead` there too. Laravel Head automatically deduplicates page-managed elements between `@head` and `<x-inertia::head />`, regardless of their order, while preserving other head elements produced by JavaScript SSR.

> [!NOTE]
> When adding Laravel Head to an existing Inertia application, remove any title callbacks from `resources/js/app.tsx` and `resources/js/ssr.tsx` so Laravel Head can manage the final document title, and move tags managed by Inertia's [`<Head>` component](https://inertiajs.com/docs/v3/the-basics/title-and-meta) into Laravel Head so the two never define the same element.

The `head` prop is omitted from partial reload responses, so Inertia retains the last full page's head. Instant visits likewise retain the current head until the background response arrives. If your application already uses the `head` prop, change its name in a service provider:

```php
use Laravel\Head\Facades\Head;

public function boot(): void
{
    Head::inertia(prop: '_head');
}
```

Then point Inertia at the same prop with `serverHead: '_head'`.

<a name="static-inertia-tags"></a>
#### Static Inertia Tags

Most tags should live in defaults, route metadata, or runtime metadata so Laravel Head can resolve the right value for each page. Use Inertia globals only for document tags rendered in the first HTML response and left unchanged by Inertia for the rest of the session.

Register them in a service provider with `Head::inertiaGlobals()`:

```php
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::inertiaGlobals(function (HeadBuilder $head) {
    $head
        ->viewport('width=device-width, initial-scale=1')
        ->colorScheme('light dark')
        ->icon('/favicon.svg', type: 'image/svg+xml')
        ->appleTouchIcon('/apple-touch-icon.png', sizes: '180x180')
        ->manifest('/site.webmanifest');
});
```

Inertia globals are excluded from the `head` prop, rendered without `data-inertia` ownership attributes, and never updated after the first response. These globals are suitable for stable browser hints such as viewport, color scheme, favicons, touch icons, and manifests. If a tag is page-specific, SEO-relevant, or may be overridden later, put it in `defaults`, route metadata, or runtime metadata instead.

Applications that need the resolved metadata as structured data instead of rendered tags may call `Head::toArray()`. The returned data includes titles, Open Graph values, JSON-LD schemas, and other resolved metadata.
